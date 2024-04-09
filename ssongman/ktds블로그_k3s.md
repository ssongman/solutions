



# k3s(경량 Kubernetes) 클러스터 구성하기



최근 컨테이너 오케스트레이션의 필수 도구로 자리 잡은 Kubernetes는 많은 기업들이 채택하고 있다. 그러나 Kubernetes를 사용하기 위해서는 상당한 리소스와 시간을 투자해야 한다. 하지만, 이를 구성하고 운영하는 것은 어려운 과정이다. 이에 대한 대안으로 등장한 k3s는 경량화된 Kubernetes로, 간편한 설치와 운영, 그리고 작은 리소스 사용으로 초보자부터 전문가까지 널리 활용되고 있다.





# 1. k3s란 무엇인가?

k3s는 Rancher Labs에서 개발한 경량 Kubernetes 클러스터이다. 기존의 Kubernetes와 비교하여 설치 및 운영이 훨씬 간편하며, 적은 리소스만으로 사용이 가능하다. k3s는 단일 바이너리로 구성되어 있으며, 작은 장비나 IoT 기기와 같이 리소스가 제한된 환경에서도 잘 동작한다.



## 1) k3s의 특징

### (1) 가벼움과 간편성

- k3s는 경량화된 Kubernetes로, 단일 바이너리로 구성되어 있어 설치와 운영이 간편하다.
- 작은 장비나 리소스 제한이 있는 환경에서도 빠르고 효율적으로 동작한다.

### (2) 완전한 기능

- k3s는 Kubernetes의 핵심 기능을 모두 제공하면서도 불필요한 기능을 최소화하여 가볍게 유지된다.
- 이로 인해 필요한 기능만 사용하면서도 성능을 유지할 수 있다.

### (3) 보안과 안정성

- k3s는 Kubernetes의 보안 및 안정성을 유지하면서도 사용자 편의성을 최대화한다.
- 적은 구성 요소로 인해 취약점이 적고, 보안 업데이트가 간편하다.





## 2) k3s와 함께 제공되는 Solution

K3s는 다음과 같은 필수 종속성을 패키지로 제공한다.

- Containerd
- Flannel (CNI)
- CoreDNS
- Traefik (인그레스)
- Klipper-lb (서비스 로드밸런서)
- 임베디드 네트워크 정책 컨트롤러
- 임베디드 로컬 경로 프로비저너
- 호스트 유틸리티(iptables, socat 등)







### 1. kubectl

- **설명**: kubectl은 Kubernetes 클러스터를 관리하기 위한 커맨드 라인 인터페이스(CLI)입니다. k3s는 kubectl을 기본적으로 제공하여 사용자가 클러스터를 제어하고 관리할 수 있도록 합니다.
- **활용**: 리소스 생성, 조회, 수정, 삭제 등 Kubernetes 클러스터 관리 작업을 수행할 때 사용됩니다.

### 2. Traefik

- **설명**: k3s는 기본적으로 로드 밸런서 및 DNS 서비스를 제공하기 위해 Traefik 또는 CoreDNS를 함께 제공합니다. Traefik은 리버스 프록시 및 로드 밸런서로 사용되며, CoreDNS는 클러스터 내 DNS 쿼리를 처리합니다.
- **활용**: 서비스 디스커버리, 내부 네트워킹, 외부 접근 등의 기능을 지원합니다.



### 3. CoreDNS

- **설명**: k3s는 기본적으로 로드 밸런서 및 DNS 서비스를 제공하기 위해 Traefik 또는 CoreDNS를 함께 제공합니다. Traefik은 리버스 프록시 및 로드 밸런서로 사용되며, CoreDNS는 클러스터 내 DNS 쿼리를 처리합니다.
- **활용**: 서비스 디스커버리, 내부 네트워킹, 외부 접근 등의 기능을 지원합니다.

### 4. kubernetes-dashboard

- **설명**: kubernetes-dashboard는 Kubernetes 클러스터를 시각적으로 관리하기 위한 웹 대시보드입니다. k3s는 기본적으로 Kubernetes 대시보드를 함께 제공하여 사용자가 클러스터를 모니터링하고 관리할 수 있도록 합니다.
- **활용**: 클러스터 리소스 모니터링, 파드 및 서비스 관리, 이벤트 확인 등에 사용됩니다.

### 5. metrics-server

- **설명**: metrics-server는 Kubernetes 클러스터의 리소스 사용량 및 성능 데이터를 수집하고 노출하는 역할을 합니다. 이를 통해 리소스 사용량을 모니터링하고 스케일링을 수행할 수 있습니다.
- **활용**: 리소스 사용량 모니터링, 수평 스케일링 결정 등에 사용됩니다.

















## 3) K3s 아키텍처





![img](Untitled.assets/how-it-works-k3s-revised-9c025ef482404bca2e53a89a0ba7a3c5.svg)



- 서버 노드는 `k3s server` 명령을 실행하는 호스트로 정의되며, 컨트롤 플레인 및 데이터스토어 구성 요소는 K3s에서 관리한다.
- 에이전트 노드는 데이터스토어 또는 컨트롤 플레인 구성 요소 없이 `k3s agent` 명령을 실행하는 호스트로 정의된다.
- 서버와 에이전트 모두 kubelet, Container runtime(Containerd) 및 CNI가 실행된다. 





#  2. k3s 설치



k3s는 설치는 명령어 한줄만 실행하는 방식이므로 매우 간단하다.  

Stand Alone 모드가 아닌 확장된 클러스터 형태로 구성하더라도 Master / Worker Node 별로 설치후 연결하는 구조로 복잡하지 않다.

설치하는 모습을 살펴보자.



## 1) Stand Alone Mode

> Stand Alone mode 로 설치

- k3s install

```sh
## root 권한으로 수행한다.
$ sudo -s

# k3s 설치
$ curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
```



설치가 잘 되었는지 확인해보자.

```sh
$ k3s kubectl version
Client Version: v1.28.6+k3s2
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.28.6+k3s2
```

Client 와 Server 의 Version 이 각각 보인다면 설치가 잘 된 것이다.



아래와 같이 k3s 데몬으로 설치여부를 확인 할 수 있다.

```sh

$ ps -ef|grep k3s
root         590     405  0 13:05 pts/0    00:00:00 sudo k3s server
root         591     590 76 13:05 pts/0    00:00:26 k3s server
root         626     591  5 13:05 pts/0    00:00:01 containerd -c /var/lib/rancher/k3s/agent/etc/containerd/config.toml -a /run/k3s/containerd/containerd.sock --state /run/k3s/containerd --root /var/lib/rancher/k3s/agent/containerd
...

```







## 2) Cluster Mode

k3s 는 확장성을 위해서 N개의 worker node 를 추가할 수 있다.



- 

```sh
## root 권한으로 수행한다.
$ sudo -s

# k3s 설치
$ curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644

$ curl -sfL https://get.k3s.io | K3S_URL=https://myserver:6443 K3S_TOKEN=mynodetoken sh -


```



asASdASDSADAsdsaD





asdsaDASD





### (3) kubeconfig 설정



일반 User가 직접 kubctl 명령 실행을 위해서는 kube config 정보(~/.kube/config) 가 필요하다.

k3s 를 설치하면 /etc/rancher/k3s/k3s.yaml 에 정보가 존재하므로 이를 복사한다. 또한 모든 사용자가 읽을 수 있도록 권한을 부여 한다.

- 일반 user 로 수행

- - kubectl 명령을 수행하기를 원하는 특정 사용자로 아래 작업을 진행한다.

```
## 일반 user 권한으로 실행

$ mkdir -p ~/.kube

$ cp /etc/rancher/k3s/k3s.yaml ~/.kube/config

$ ll ~/.kube/config
-rw-r--r-- 1 song song 2957 May 14 03:44 /home/song/.kube/config

# 보안을 위해 자신만 RW 권한 부여( 644 --> 600)
$ chmod 600 ~/.kube/config


$ ls -ltr ~/.kube/config
-rw------- 1 song song 2957 May 14 03:44 /home/song/.kube/config


## 확인
$ kubectl version
Client Version: v1.28.6+k3s2
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
Server Version: v1.28.6+k3s2


$ kubectl get ns
NAME              STATUS   AGE
kube-system       Active   4m2s
kube-public       Active   4m2s
kube-node-lease   Active   4m2s
default           Active   4m2s


$ kubectl get nodes
NAME        STATUS   ROLES                  AGE     VERSION
bastion02   Ready    control-plane,master   4m10s   v1.28.6+k3s2
```



이제 root 권한자가 아닌 다른 사용자도 kubectl 명령을 사용할 수 있다.





## 3) [참고] k3s 삭제



```
# root 권한으로
$ sudo -s

## k3s 삭제
$ sh /usr/local/bin/k3s-killall.sh
  sh /usr/local/bin/k3s-uninstall.sh

# 확인
$ ps -ef|grep k3s

# 사용자 권한으로
$ eixt
```











# 9. 결론

k3s는 경량 Kubernetes로써 간편한 설치와 운영, 그리고 다양한 환경에서의 활용성으로 많은 관심을 받고 있다. 초보자부터 전문가까지 다양한 사용자들이 쉽게 접근할 수 있으며, 작은 규모부터 대규모까지 다양한 환경에서 유연하게 활용할 수 있다. 이를 통해 컨테이너 오케스트레이션에 대한 역량을 향상시키고, 더욱 쉽고 안정적으로 애플리케이션을 관리할 수 있게 된다.





