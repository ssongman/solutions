### k8s-setup



# 1. 개요

바닐라 쿠버네티스(Vanilla Kubernetes)를 3대의 Ubuntu VM에 설치한다. 마스터 노드 1대와 워커 노드 2대로 구성한다.



## 1) 시스템 준비

**모든 VM에서** 기본적인 시스템 업데이트와 Container runtime 을 먼저설치한다.



### (1) Container Runtime

쿠버네티스 설치 시 Docker, containerd나 CRI-O 같은 Container Runtime 이 필요하다. 최근에는 Docker 대신 containerd나 CRI-O 같은 다른 런타임을 사용하는 것이 더 권장된다.



####  Docker 설치

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```



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
# /etc/containerd/config.toml 파일에서 SystemdCgroup을 true로 설정해야 쿠버네티스와의 호환성이 높아집니다.

sudo vi /etc/containerd/config.toml
---
...
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
...
---
# containerd 서비스를 재시작
sudo systemctl restart containerd


```





### (2) 쿠버네티스의 의존성 설치

```bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```





### 2. 마스터 노드 설정

**마스터 노드에서** 쿠버네티스 클러스터를 초기화합니다. 이때, 내부 네트워크 서브넷을 지정합니다.

#### 클러스터 초기화
```bash
sudo kubeadm init --pod-network-cidr=192.168.0.0/16
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
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
```





### 3. 워커 노드 설정

각 워커 노드에서 마스터 노드에 가입(join)할 수 있도록 `kubeadm join` 명령을 사용해야 합니다.

마스터 노드에서 `kubeadm init` 명령어가 완료되면, 출력되는 `kubeadm join` 명령을 복사한 후 워커 노드에서 실행합니다. 예시:

```bash
sudo kubeadm join <master-node-ip>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

이 명령어를 **각 워커 노드에서** 실행하면 클러스터에 워커 노드들이 추가됩니다.



### 4. **kubelet 및 API 접근**

외부에서 `kubectl`을 이용해 API 서버에 접근하려면 **L4 로드 밸런서**를 통해 **6443 포트**를 마스터 노드의 IP 주소와 매핑하여, 외부에서 API 서버에 접근할 수 있게 만듭니다.



클라이언트는 L4 로드 밸런서의 공인 IP를 통해 쿠버네티스 API 서버에 접근합니다.

​	•	예를 들어, kubectl 명령을 사용할 때 다음과 같이 **로드 밸런서의 공인 IP**를 사용합니다.

```sh

$ kubectl --kubeconfig=config.yaml --server=https://<L4-loadbalancer-public-ip>:6443 cluster-info

```



```sh

# 쿠버네티스 API 서버의 주소를 확인
$ kubectl cluster-info

# 기본적으로 6443 port 를 사용
```





### 5. Ingress Controller 공인 IP 매핑

Ingress Controller를 설치한 후 **공인 IP**를 매핑하려면, 서비스 타입을 `LoadBalancer`로 설정하여 Azure나 AWS 등 클라우드 환경에서는 자동으로 공인 IP가 할당되도록 할 수 있습니다. 예시는 다음과 같습니다:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx
  namespace: ingress-nginx
spec:
  type: LoadBalancer
  selector:
    app: ingress-nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
    - protocol: TCP
      port: 443
      targetPort: 443
```

서비스 타입이 `LoadBalancer`인 경우, 클라우드 프로바이더에서 자동으로 공인 IP가 할당되고, `kubectl get svc -n <namespace>` 명령으로 공인 IP를 확인할 수 있습니다.

### 결론

- **공인 IP**가 필요하면, 마스터 노드에 공인 IP를 할당하고 API 서버 설정을 수정해야 합니다.
- Ingress Controller 설치 시, `LoadBalancer` 서비스 타입을 이용하면 자동으로 공인 IP가 할당됩니다.

이 방법을 통해 외부에서 Kube API 및 Ingress를 통한 트래픽을 처리할 수 있습니다.