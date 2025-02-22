#  KubeSphere 설치 



KubeSphere는 엔터프라이즈급 멀티 테넌트 Kubernetes 관리 플랫폼으로, Web UI를 통해 Kubernetes 클러스터를 쉽게 관리할 수 있도록 해준다.



# 1. 설치 전 사전 요구 사항



## 1) 클러스터 환경 확인



​	•	Kubernetes 1.20 이상 버전이 필요함

​	•	kubectl 및 helm이 설치되어 있어야 함

​	•	4코어 / 8GB RAM 이상의 노드 리소스 필요





# 2. KubeSphere 설치

* 참고문서:
  * https://kubesphere.io/docs/v4.1/02-quickstart/01-install-kubesphere/



## 1) KubeSphere 설치 with helm

### (1) helm 저장소 추가

```sh

$ helm repo add kubesphere https://charts.kubesphere.io/main
  helm repo update

$ helm search repo kubesphere
NAME                                    CHART VERSION   APP VERSION                     DESCRIPTION
kubesphere/apisix                       0.7.2           2.10.0                          A Helm chart for Apache APISIX
kubesphere/apisix-dashboard             0.3.0           2.9.0                           A Helm chart for Apache APISIX Dashboard
kubesphere/apisix-ingress-controller    0.8.0           1.3.0                           Apache APISIX Ingress Controller for Kubernetes
kubesphere/elasticsearch-exporter       3.4.0           1.1.0                           Elasticsearch stats exporter for Prometheus
kubesphere/fluentbit-operator           0.1.0           0.9.0                           A Helm chart for Kubernetes
kubesphere/gitlab                       4.2.3           13.2.2                          Web-based Git-repository manager with wiki and ...
kubesphere/harbor                       1.9.3           2.5.3                           An open source trusted cloud native registry th...
kubesphere/ks-core                      1.1.3           v4.1.2                          A Helm chart for KubeSphere Core components
kubesphere/ks-installer                 0.3.1           3.2.1                           The helm chart of KubeSphere, supports installi...
kubesphere/memcached                    3.2.5           1.5.20                          Free & open source, high-performance, distribut...
kubesphere/minio                        6.0.5           RELEASE.2020-08-08T04-50-06Z    High Performance, Kubernetes Native Object Storage
kubesphere/mysql                        1.6.8           5.7.31                          Fast, reliable, scalable, and easy to use open-...
kubesphere/mysql-exporter               0.5.6           v0.11.0                         A Helm chart for prometheus mysql exporter with...
kubesphere/nfs-client-provisioner       4.0.11          4.0.2                           nfs-client is an automatic provisioner that use...
kubesphere/nginx                        1.3.5           1.18.0                          nginx is an HTTP and reverse proxy server, a ma...
kubesphere/pvc-autoresizer              0.1.0           v0.1                            Auto-resize PersistentVolumeClaim objects based...
kubesphere/redis-exporter               3.4.6           1.3.4                           Prometheus exporter for Redis metrics
kubesphere/sonarqube                    6.7.0           8.9-community                   SonarQube is an open sourced code quality scann...
kubesphere/storageclass-accessor        0.1.0           v0.1.1                          The storageclass-accessor webhook is an HTTP ca...
kubesphere/tomcat                       0.4.3           8.5.41                          Deploy a basic tomcat application server with s...


# helm values.yaml 확인
$ helm show values kubesphere/ks-core



```



### (2) Install

```sh

$ kubectl create ns kubesphere-system


# If you are accessing charts.kubesphere.io from a restricted location, 
# replace charts.kubesphere.io with charts.kubesphere.com.cn

$ helm -n kubesphere-system upgrade --install kubesphere kubesphere/ks-core \
    --set portal.hostname=ks.ssongman.com \
    --set ingress.enabled=true \
    --set ingress.ingresClassName=traefik

# []---------------------
    --debug --wait
    --set ingress.tls.enabled=true    # letsEncrypte 에서 자동으로 인증서를 만들어 주나?
# []---------------------










# 확인
$ helm -n kubesphere-system ls


# 설치 상태 확인
$ kubectl get pods -n kubesphere-system


## 삭제시...
$ helm uninstall kubesphere -n kubesphere-system

```







### (3) KubeSphere 웹 콘솔 접속

```sh

http://ks.ssongman.com/password/confirm

admin / Adminpass1!


```







# 3. KubeSphere 기능 확장

추가 기능(Observability, DevOps, Service Mesh 등)을 활성화하려면 다음 메뉴에서 확인



* 메뉴 : Extensions Center