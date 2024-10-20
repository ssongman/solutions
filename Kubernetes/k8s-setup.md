# k8s-setup



# 1. 개요

바닐라 쿠버네티스(Vanilla Kubernetes)를 3대의 Ubuntu VM에 설치한다. 마스터 노드 1대와 워커 노드 2대로 구성한다.





## 1) 참고링크

* https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
* 영문버젼을 참고할것.
* 한글버젼은 잘 설치 안됨



## 2) VM 기본 설정

쿠버네티스 클러스터를 초기화하려면 최소 2개의 CPU가 필요함







# 2. 시스템 준비

파드에서 컨테이너를 실행하기 위해, 쿠버네티스는 컨테이너 런타임을 사용한다.

기본적으로, 쿠버네티스는 CRI 를 사용하여 사용자가 택한 CR 과 인터페이스 한다.



컨테이너 런타임별 엔드포인트

```sh

런타임                       유닉스 도메인 소켓 경로
containerd	               unix:///var/run/containerd/containerd.sock
CRI-O                      unix:///var/run/crio/crio.sock
도커 엔진 (cri-dockerd 사용)	unix:///var/run/cri-dockerd.sock

```





**모든 VM에서** 기본적인 시스템 업데이트와 Container runtime 을 먼저 설치한다.



## 1) Container Runtime

쿠버네티스 설치 시 Docker, containerd나 CRI-O 같은 Container Runtime 이 필요하다. 최근에는 Docker 대신 containerd나 CRI-O 같은 다른 런타임을 사용하는 것이 더 권장된다.



#### Containerd 설치

**containerd**는 경량화된 컨테이너 런타임으로, 쿠버네티스에서 사용되는 주요 컨테이너 런타임 중 하나입니다. Docker와 비슷하게 컨테이너를 실행하고 관리하지만, 쿠버네티스에서 Docker보다 가볍고 최적화된 환경을 제공합니다. 특히, **containerd**는 쿠버네티스의 컨테이너 런타임 인터페이스(CRI)를 직접 지원하여 별도의 브릿지 없이 동작합니다.

```sh

# 1) 각 노드에서 containerd를 설치
sudo apt-get update
sudo apt-get install -y containerd


# 2) containerd 설정 파일을 생성하고 적용
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml


# 3) Systemd Cgroup 설정 변경
# /etc/containerd/config.toml 파일에서 SystemdCgroup을 true로 설정해야 쿠버네티스와의 호환성이 높아진다.

sudo vi /etc/containerd/config.toml
---
...
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
...
---
# 137 line


# containerd 서비스를 재시작
sudo systemctl restart containerd


```





####  Docker 설치

Containerd 대신 다른 container 를 설치할 수 있다.

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```





## 2) kubeadm, kubelet 및 kubectl 설치

모든 머신에 다음 패키지들을 설치한다.

- `kubeadm`: 클러스터를 부트스트랩하는 명령이다.
- `kubelet`: 클러스터의 모든 머신에서 실행되는 파드와 컨테이너 시작과 같은 작업을 수행하는 컴포넌트이다.
- `kubectl`: 클러스터와 통신하기 위한 커맨드 라인 유틸리티이다.



```bash

# 1) 필수 패키지 설치
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

# 2) 구글 클라우드의 공개 사이닝 키 다운로드
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg


# 3) 쿠버네티스 apt 리포지터리를 추가
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# 4) kubelet, kubeadm, kubectl을 설치하고 해당 버전을 고정
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl


# socat은 쿠버네티스가 네트워킹에 사용되는 유틸리티
sudo apt-get install socat -y

```





## 3) IP 포워딩

쿠버네티스를 설치할 때, IP 포워딩은 필수적이다.

이를 해결하기 위해서는 net.ipv4.ip_forward 값을 1로 설정해야 한다.

```sh

# IP 포워딩을 활성화하는 설정을 추가
sudo vi /etc/sysctl.conf

# 파일의 끝에 다음 줄을 추가
net.ipv4.ip_forward=1

# 변경 사항을 적용
sudo sysctl -p


# 확인
cat /proc/sys/net/ipv4/ip_forward

# 1이 리턴되어야 함


```







# 2. 마스터 노드 설정

**마스터 노드에서** 쿠버네티스 클러스터를 초기화합니다. 이때, 내부 네트워크 서브넷을 지정합니다.

#### 클러스터 초기화
```bash

$ sudo kubeadm init --pod-network-cidr=192.168.0.0/16

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.0.1.4:6443 --token ljzh65.nem1uu09mf8xzm31 \
        --discovery-token-ca-cert-hash sha256:e71b6caefd8750e416f1ed55873a77b837173f73e2c67df59bd870704990004b

```



#### 클러스터 설정

초기화가 완료되면, 다음 명령어로 `kubectl`을 사용하도록 설정합니다.
```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```



#### 네트워크 플러그인 설치

Calico와 같은 네트워크 플러그인을 설치해야 합니다. 여기서는 Calico를 사용합니다.
```bash

# 네트워크 플러그인을 설치
$ kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml


# 확인
$ kubectl -n kube-system get pod
NAME                                       READY   STATUS    RESTARTS   AGE
calico-kube-controllers-6879d4fcdc-fntn7   1/1     Running   0          57s
calico-node-kh4x5                          1/1     Running   0          57s
coredns-7c65d6cfc9-c44bg                   1/1     Running   0          6m52s
coredns-7c65d6cfc9-cs8fk                   1/1     Running   0          6m52s


```





# 3. 워커 노드 설정

각 워커 노드에서 마스터 노드에 가입(join)할 수 있도록 `kubeadm join` 명령을 사용해야 합니다.

마스터 노드에서 `kubeadm init` 명령어가 완료되면, 출력되는 `kubeadm join` 명령을 복사한 후 워커 노드에서 실행합니다. 예시:

```bash

sudo kubeadm join <master-node-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>


$ sudo kubeadm join 10.0.1.4:6443 --token ljzh65.nem1uu09mf8xzm31 \
        --discovery-token-ca-cert-hash sha256:e71b6caefd8750e416f1ed55873a77b837173f73e2c67df59bd870704990004b



# 확인
$ kubectl get nodes
NAME     STATUS   ROLES           AGE   VERSION
yjvm01   Ready    control-plane   33m   v1.31.1
yjvm02   Ready    <none>          17m   v1.31.1
yjvm03   Ready    <none>          15m   v1.31.1


# worker role 추가
kubectl label node yjvm02 node-role.kubernetes.io/worker=worker
kubectl label node yjvm03 node-role.kubernetes.io/worker=worker

# 확인
$ kubectl get nodes
NAME     STATUS   ROLES           AGE   VERSION
yjvm01   Ready    control-plane   35m   v1.31.1
yjvm02   Ready    worker          19m   v1.31.1
yjvm03   Ready    worker          17m   v1.31.1


```

이 명령어를 **각 워커 노드에서** 실행하면 클러스터에 워커 노드들이 추가됩니다.



# 4. **kubelet 및 API 접근**

외부에서 `kubectl`을 이용해 API 서버에 접근하려면 **L4 로드 밸런서**를 통해 **6443 포트**를 마스터 노드의 IP 주소와 매핑하여, 외부에서 API 서버에 접근할 수 있게 만듭니다.



클라이언트는 L4 로드 밸런서의 공인 IP를 통해 쿠버네티스 API 서버에 접근합니다.

​	•	예를 들어, kubectl 명령을 사용할 때 다음과 같이 **로드 밸런서의 공인 IP**를 사용합니다.

```sh

$ kubectl --kubeconfig=config.yaml --server=https://<L4-loadbalancer-public-ip>:6443 cluster-info

```



```sh

# 쿠버네티스 API 서버의 주소를 확인
$ kubectl cluster-info
Kubernetes control plane is running at https://10.0.1.4:6443
CoreDNS is running at https://10.0.1.4:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.


# 기본적으로 6443 port 를 사용
```





# 5. 기타

기본적으로 클러스터는 보안상의 이유로 Control-plane 에서는 AP pod 가 스케쥴되지 않는다.  그럼에도 불구하고 스케쥴되게 하려면 아래 명령어를 이용한다.

```sh

$ kubectl taint nodes --all node-role.kubernetes.io/control-plane-

```





# 6. Remove the node

```sh


$ kubectl drain <node name> --delete-emptydir-data --force --ignore-daemonsets

$ kubeadm reset

$ kubectl delete node <node name>

```



