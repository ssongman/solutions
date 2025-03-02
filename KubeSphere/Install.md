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



## 1) helm repo 추가

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



values 확인

```sh


$ helm show values 


$ helm get values ks-core -n kubesphere-system

```













## 2) ks-core 기본



### (1) install

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

NAME            NAMESPACE               REVISION        UPDATED                                 STATUS          CHART           APP VERSION
kubesphere      kubesphere-system       1               2025-02-22 23:05:13.70062837 +0900 KST  deployed        ks-core-1.1.3   v4.1.2


$ helm -n kubesphere-system get values kubesphere
USER-SUPPLIED VALUES:
ingress:
  enabled: true
  ingresClassName: traefik
portal:
  hostname: ks.ssongman.com



# 설치 상태 확인
$ kubectl get pods -n kubesphere-system


## 삭제시...
$ helm uninstall kubesphere -n kubesphere-system

```







### (2) KubeSphere 웹 콘솔 접속

```sh

http://ks.ssongman.com/password/confirm

admin / Adminpass1!

```





## 3) ks-installer

kubesphere/ks-installer 는 helm 없이 다양한 extention 들을 설치할때 필요한 기능이다.



### 1) ks-installer 역할 및 필요성

예를들면 아래와 같이  설치할 수 있다.

```sh

$ kubectl patch cc ks-installer -n kubesphere-system --type merge -p '{
  "spec": {
    "monitoring": {
      "storageClass": "default"
    },
    "logging": {
      "enabled": true
    }
  }
}'

$ kubectl rollout restart deployment ks-installer -n kubesphere-system

```



위 명령은 아래와 같이 helm 명령으로도 설치 가능하다.

```sh

[예시] $ helm upgrade --install kubesphere kubesphere/ks-core \
  --namespace kubesphere-system \
  --set monitoring.enabled=true \
  --set f.enabled=true

```

그러므로 helm 에 익숙하다면 굳이 ks-installer 를 설치할 필요는 없다.









## 4) KubeSphere 기능 확장

**모니터링 대시보드**를 비롯한 다양한 기능(Observability, DevOps, Service Mesh, Storage, Network 등)을 활성화하려면 **추가적인 KubeSphere 컴포넌트를 설치**한다.



### (1) UI 에서  기능 확장 

다음 메뉴에서 확인

* 메뉴 : Extensions Center



### (2) helm 명령으로 확장

monitoring, logging 등의 기능을 확장 할 수 있다.

```sh
$ helm -n kubesphere-system get values kubesphere
USER-SUPPLIED VALUES:
ingress:
  enabled: true
  ingresClassName: traefik
portal:
  hostname: ks.ssongman.com



$ helm -n kubesphere-system upgrade --install kubesphere kubesphere/ks-core \
    --set portal.hostname=ks.ssongman.com \
    --set ingress.enabled=true \
    --set ingress.ingresClassName=traefik \
    --set monitoring.enabled=true \
    --set logging.enabled=true


# 
$ kubectl -n kubesphere-system get pod
NAME                                       READY   STATUS      RESTARTS   AGE
extensions-museum-d754fdc58-58rh8          1/1     Running     0          9m14s
ks-apiserver-57bc466678-5wlzt              1/1     Running     0          9m14s
ks-console-68bddc67b-jqmlh                 1/1     Running     0          7d15h
ks-controller-manager-7d758b5fc4-9mnkf     1/1     Running     0          9m12s
restart-extensions-museum-29011140-ngltm   0/1     Completed   0          2d14h
restart-extensions-museum-29012580-d4mf4   0/1     Completed   0          38h
restart-extensions-museum-29014020-z8whm   0/1     Completed   0          14h

```







# 3. Cluster 추가

KubeSphere에서 특정 클러스터를 추가하여 직접 모니터링하고 관리할 수 있다.


KubeSphere에 AKS 클러스터 추가해보자.

KubeSphere에서 **AKS(Azure Kubernetes Service) 클러스터**를 추가하려면, **Agent**를 설치하고 KubeSphere에 등록해야 한다.

이 과정에서는 **ks-agent**를 사용하여 원격 클러스터를 추가한다.



## 1) AKS 클러스터 정보 확인



### (1) AKS 생성

존재한다면 생략

```sh

# aks 확인
$ az aks list -o table
Name             Location      ResourceGroup        KubernetesVersion    CurrentKubernetesVersion    ProvisioningState    Fqdn
---------------  ------------  -------------------  -------------------  --------------------------  -------------------  --------------------------------------------------------------------


# 그룹 생성
$ az group create --name yj-rg --location koreacentral

# aks 생성
$ az aks create \
  --resource-group yj-rg \
  --name yj-aks \
  --node-count 2 \
  --node-vm-size Standard_D2s_v3 \
  --generate-ssh-keys
  

# aks 확인
$ az aks list -o table
Name             Location      ResourceGroup        KubernetesVersion    CurrentKubernetesVersion    ProvisioningState    Fqdn
---------------  ------------  -------------------  -------------------  --------------------------  -------------------  --------------------------------------------------------------------
yj-aks           koreacentral  yj-rg                1.30                 1.30.9                      Succeeded            yj-aks-yj-rg-1d6c45-ep3kzgjr.hcp.koreacentral.azmk8s.io



```







### (2) AKS 연결

```sh


# AKS 클러스터에 연결
$ az aks get-credentials --resource-group yj-rg --name yj-aks


# 연결되었는지 확인:
$ kubectl get nodes
NAME                                STATUS   ROLES    AGE    VERSION
aks-nodepool1-24310777-vmss000000   Ready    <none>   3m9s   v1.30.9
aks-nodepool1-24310777-vmss000001   Ready    <none>   3m5s   v1.30.9


```



### (3) AKS stop/start

사용하지 않을때 AKS stop 해 놓자.

```sh

# stop
$ az aks stop -n yj-aks -g yj-rg

# start
$ az aks start -n yj-aks -g yj-rg

```







## 2) KubeSphere에서 클러스터 추가



### (1) Add Cluster



* **KubeSphere Web UI 접속**

  * KubeSphere Admin 콘솔에 접속

  * **“Cluster Management”** > **“Add Cluster”** 선택

  * Basic Infomation
    * Cluster Name
    * Alias
    * 기타정보
  * Connection Setting
    * aks - kubeconfig 정보( yaml) 그대로 입력
    * 외부에서 접속 가능한 상태여야 함
  * Cluster Configuration
  * 확인



kubeconfig 정보가 정상적이고 Cluster가 정상적으로 추가되면 AKS 내부에서 ks-agent pod 가 생성될 것이다.



### [참고] aks kubeconfig

```sh

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUU2VENDQXRHZ0F3SUJBZ0lSQU9UaFVGcUNwZzN2VHFDNUtjRU1HdDB3RFFZSktvWklodmNOQVFFTEJRQXcKRFRFTE1Ba0dBMVVFQXhNQ1kyRXdJQmNOTWpVd016QXlNRFl3T0RRNVdoZ1BNakExTlRBek1ESXdOakU0TkRsYQpNQTB4Q3pBSkJnTlZCQU1UQW1OaE1JSUNJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBZzhBTUlJQ0NnS0NBZ0VBCnIyREc4TXlPVHgvL0xYNFYrTzlmYkxFVjYvWE4xR0YzS0tPTTNoZ2tFZWNvWDgzYnZQRUxaazQ1bEZhYVVSNVUKNmVPenBOWGZTemZSL3h0aW1LWU5WSEhmYXBxVzNYckw3TkxIQzE1L2hkVnpqL1Y2REF1SkxrL2FwVTVFNHpPRQpFZGRoNTJYMjAzTVlnNGF3bjRZNTZLN21PVjVmcEpyYmF4RGduTi9IYWlsaUxBckZ3c3RHbkpKMlA4ZzhXOXp0CjNDc1ZEamZPRy9zL3Z3TU9SM1dvZG5IUStXRVZENGRFa04zeWtoS25TdEdGbXZONDVVSUt3d1VxZ005OER6MlUKYU1BUVJ3eXBGVVIwbyt1SzYwd0NaeWk4ZFlsM0V0OW55K1FRZkRrRjVBMFdZd0hCN2p1R2FQTzhTYU81T0ZsdQphTlRCWG1zRFdXN0xmOSt5ZzB3TEoyTjZUYk5iNVB1RVgvOXB2WlNMdFF0YkVzMHpYNFVueWhSMnhUa0xoam82CkR2cWFRWi81cnNpZHRDODVRYnFhempmWG93ZXg2VFN2d1BjVkxxcEFlS3JhcjJ5dlpYVTcyOEVmaDlCeTRMcmgKbk9iTU9NbllidDFuQlJZbDVIRVhMYXNrODMraFJFQS9WVlVmQVE4c0Y4VVRZQTJGb2FuN2hLOTVSekVqZEN1ZwpHL0V0MUE3SHB4d01FbTg5WmFwSGpZQWZqK0M3OEVtNDBnVkJmT2x4eW0wd0o4RnF1eUo2YnEreTNqN0toT1UvCk83YUptQ1hvbUxkejBxUlNmclR2RmhmRCtiZjhCL0txai9ZUDZZYTdSYkE2QU5OUW9RakRPSzloU0ErVG9DRXUKZHFOeXdablFuS2ticXZ4c0FjblhhSUxIYVJsZ3FpL2t1Um9oSkZ5Q1dsTUNBd0VBQWFOQ01FQXdEZ1lEVlIwUApBUUgvQkFRREFnS2tNQThHQTFVZEV3RUIvd1FGTUFNQkFmOHdIUVlEVlIwT0JCWUVGSEJHRnZVc05NU0szRnR3Cmw5ZTd4QzFEMFg0bk1BMEdDU3FHU0liM0RRRUJDd1VBQTRJQ0FRQUNzSkN3bjkrWVE0V1FTeUdQeFBWMmVpTGgKZjJtNzhWcVI2YUY1aEg0Zk4vd1FnTG9jbFVVMS85R3FDZkdkVzN5M3F2QXBCaFY3YTRHMjd1UWdNaW8rd0xSRQpxU1ZPSGdHYUhjK0R0RnVtRWVpMGtLa2QwY2VHREk3R2xlSWc1dHY4Y2NHQ1FVdHJKbk5zZkNpRTBBSHp2R0phCkMrZ0pCNENkanJDUWkvSmg3VStWcnYyVVViYVMxTHFtTmZLaVkzcjZtcno5dlJPbVEzT2o0Q1dtaFBWRDFRYlgKMWRMdW0wTXlOUEpocDFMQ2JzVHN2T3dvMFVUcU1TYUlLOFA5M3VwRHh0MytFUjRVNzB5RXpOdTl1b1VOeThtVQpqZTlBbHRlUG5MZFR3emhidy9zdVh1RGRwcWJvK241MG5HRDRmVzZ0Szc2S2Z6dWoyU0NKSzdQUjU2N3RWeEV6Cjk5Slh2d1ViUTd1ZUlpVUI0bVczS3dVd3FrQThUNVpJbklKOXp3c3EwZStlU2thYkM3anB6S0NobnZCRFJlb0EKY0M3MStJYlNWaTAvWWhkcFFmYzl0QVl4Z09OQ2ViNUVKQmRwUEtVNkI2dGM1cllFL1JpYXB5d0hFZ2p2amk1Sgp3VDNYVElYTndNQkFrelMzTEE0cEZRcjZkZnVnKy9TQU50N3JqM1dnekNub1JVTWVCa1dKcUJaTG0zYTdNcC92CnVPVnFaNEp1ZStQN1NPRFhFK2kybExvbVFuTjY4aElJeEdTK083WWNBQzFYQmVuVzdjZHZPeFlKVE8wdzBFYnQKckpoaUNweFpZdTJkZnl0czY0S25QaCtRR3AyR2piTHRpQVZtOTRVdjlsZ3h3WXBwVDVFaHNXVzU0U2dEK2RMSgowbUU4RVJzTnh3NlpvVVBiZXc9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://yj-aks-yj-rg-1d6c45-ep3kzgjr.hcp.koreacentral.azmk8s.io:443
  name: yj-aks
contexts:
- context:
    cluster: yj-aks
    user: clusterUser_yj-rg_yj-aks
  name: yj-aks
current-context: yj-aks
kind: Config
preferences: {}
users:
- name: clusterUser_yj-rg_yj-aks
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUZIakNDQXdhZ0F3SUJBZ0lSQVBKbnE4VGtJMllnQ1FSOTVpNHk1ZEF3RFFZSktvWklodmNOQVFFTEJRQXcKRFRFTE1Ba0dBMVVFQXhNQ1kyRXdIaGNOTWpVd016QXlNRFl3T0RRNVdoY05NamN3TXpBeU1EWXhPRFE1V2pBdwpNUmN3RlFZRFZRUUtFdzV6ZVhOMFpXMDZiV0Z6ZEdWeWN6RVZNQk1HQTFVRUF4TU1iV0Z6ZEdWeVkyeHBaVzUwCk1JSUNJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBZzhBTUlJQ0NnS0NBZ0VBdXJ3M21MQzZXdTU1dzgwNzYzSGoKeTVVeWg0SVZhSzMyaFR0ZHhaL2V5VU5yemo1bHJQejdZM0xraWlzNml5cEdTTkJ2ZENUMFJYYnRBWWVtS1BIMApUdVc4R0wyQ3NjbFBaSVFaWnhyQ2JtdVdDVXdCY0RIck5qUjJ4UkZNU284RmdVN1hEOEhnQmpqZFRKZkxpdWxDCmxqRWxIUU9zL1JxMy85MEwxaDFDb2JQQnp2SklFem1ZK2FEMWgrem16aW9ib3dIcm5sWGtUcDVKUlBZSU5jcDYKMk1RNC9TWStwOVRyaHFCNnZWMHBqRXIxVDBnYWV1QytXczZuZ3MrMWtBNG9ySkF0dWsyM09KS3BkMUJlU0JCawppSHd1NXBpeis3REN1Zi9DMTBCY2RsWGRLMUhLbys4S2EwTFdNRE9BMDRpM0dCUzhJQ3NWc1NQYWgzZ1hxQkVOCnl0YnlhNXZJYyt0NDYzNUZoYUxwRDVielUzbjBsU0IwWEZXWHZlU3l5WE9YcmpEUTZDek5kTkgxSzgwL3dMcHYKMWV2ZklFN25Nb0lDeFc2S1ZKVUhDdDhEYnlDb0ZSV3dKWlkrSTJLRnZ0dmdQeVBNNWkrWEdwZDBhYVYwbkdOTgowZHBOWFlLUHdFVUdTZEsyRklNUXNhaUJVM0JFa2ZKcHRvVnVCYXNaQktMYzQyelNES1BKMkR5S0VmNExONjZNCkZXM3RNU0xMTXIzWjNPSlJ3bWxQaVJNTHZlTE0xZTJLbTNyclQwVFNXV01UaFZlVUh1TW5Wcy9vYURVVnJhemIKU0pjdVM2MVV5dVJEeEZIZFl4eU1pd2tIK2lKZ2xtRjBQbFNLTlBKRFR2ZTB3bEZGNXJxV0lOQ0FsOWdSUmlybgpRWVNMcUpLa2tIZlVaUDFOZTE4MUQxOENBd0VBQWFOV01GUXdEZ1lEVlIwUEFRSC9CQVFEQWdXZ01CTUdBMVVkCkpRUU1NQW9HQ0NzR0FRVUZCd01DTUF3R0ExVWRFd0VCL3dRQ01BQXdId1lEVlIwakJCZ3dGb0FVY0VZVzlTdzAKeElyY1czQ1gxN3ZFTFVQUmZpY3dEUVlKS29aSWh2Y05BUUVMQlFBRGdnSUJBQ3FUMHgvbXdLNnV6TkxLdFU3bgpVQjNBbUJwN0lpVUw0RW9zd0IyazBMZ2NVWnNrZHJLaGRmbWFRQkF5VEhUcWJJcmJLQVUyY0l1cEROem9FcE5tCksxRnQ4dEd4VmxGS3ZGZGpoQ0J2Wi9DSFRCOWo0bmJEQU02bWlRb3RmeWI0cHBDTCt1N0pON3M1ZTQyV0Q4K1YKTEZNNnRWZUlMS3pSbGQ5b2I4TFVSSldKY053N3dGMmpyUFVRSFYvUkYvVmplRzlkK3puYzZNNXZGbnhpV1NmcgphVUwrZDQxVVo5U1psVTV2cFQ4NGpud3JPZFRXY2w1WFZhaFk4OGkwYjhiZWM2TjJOU2xETHh4UmxQaFJ3U25QCldtd2hzZEg0QUMvNXhnY3hZa0toT2J5VFY4V3BUckJGRWxsaUJkdTIxOFV2Sm03cGxhSEVVYTA0NEtuamVpQ3MKc0hNYjh2NXBDNldtcUhybjB4RFZZanVES2JncFk5UUZoZ09OVkdDQ2VpZTZETHBBdFhHOXJGcUN5YUF4MzlrZgp3VXBDckxPUFlic1lVTkVtWUw0NURGbTl5MjlwbkFVZnJLblNGS3VtaUxFUW8xaGJ4eVhYMWxsTENvTHhMZy9XCldXNVpuZ2FYQk44S3RDZzhsWUtRTlhXb3VYZENmZ05VQXUvQ3AxT3VZNXV4Mk5oSC9Na080SktvZk41OFpHNTgKempYY0x6TTdHMWJOZCtINTFac2QxWjZxUHNZais4cHJNb2xlcnVERndHb0k1c1dieU5MWVF6OER3YWRWRFBEQgp4c09wbWxuODVCMHdSNmxmSm5kWVRlLzk3UDhuR1dmS1ZFM3dtbzNTd2VWdnBKZVZ1eWdzdy8yYTZzV2ZwT1BrCklnOUxvTjdDUGc4d2ZLTzhGWUZ3bjlFTwotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlKSndJQkFBS0NBZ0VBdXJ3M21MQzZXdTU1dzgwNzYzSGp5NVV5aDRJVmFLMzJoVHRkeFovZXlVTnJ6ajVsCnJQejdZM0xraWlzNml5cEdTTkJ2ZENUMFJYYnRBWWVtS1BIMFR1VzhHTDJDc2NsUFpJUVpaeHJDYm11V0NVd0IKY0RIck5qUjJ4UkZNU284RmdVN1hEOEhnQmpqZFRKZkxpdWxDbGpFbEhRT3MvUnEzLzkwTDFoMUNvYlBCenZKSQpFem1ZK2FEMWgrem16aW9ib3dIcm5sWGtUcDVKUlBZSU5jcDYyTVE0L1NZK3A5VHJocUI2dlYwcGpFcjFUMGdhCmV1QytXczZuZ3MrMWtBNG9ySkF0dWsyM09KS3BkMUJlU0JCa2lId3U1cGl6KzdEQ3VmL0MxMEJjZGxYZEsxSEsKbys4S2EwTFdNRE9BMDRpM0dCUzhJQ3NWc1NQYWgzZ1hxQkVOeXRieWE1dkljK3Q0NjM1RmhhTHBENWJ6VTNuMApsU0IwWEZXWHZlU3l5WE9YcmpEUTZDek5kTkgxSzgwL3dMcHYxZXZmSUU3bk1vSUN4VzZLVkpVSEN0OERieUNvCkZSV3dKWlkrSTJLRnZ0dmdQeVBNNWkrWEdwZDBhYVYwbkdOTjBkcE5YWUtQd0VVR1NkSzJGSU1Rc2FpQlUzQkUKa2ZKcHRvVnVCYXNaQktMYzQyelNES1BKMkR5S0VmNExONjZNRlczdE1TTExNcjNaM09KUndtbFBpUk1MdmVMTQoxZTJLbTNyclQwVFNXV01UaFZlVUh1TW5Wcy9vYURVVnJhemJTSmN1UzYxVXl1UkR4RkhkWXh5TWl3a0graUpnCmxtRjBQbFNLTlBKRFR2ZTB3bEZGNXJxV0lOQ0FsOWdSUmlyblFZU0xxSktra0hmVVpQMU5lMTgxRDE4Q0F3RUEKQVFLQ0FnQTNUNURZTldDOWxtMlN4Yk85NVpvbnJ5V3NaYWVadmcyTElTNkJYdjFLZUNIeWtTRGt3SHBsMXA1RApIdExVYmMwcnZER0hJWHNKS0ZURFl6NmdXaXFYUkEwVzl1dERaZkdTUUY2VjM2TS91YlpUUXFRYWEyN1VPMjRDCnFVRUR4S0ZJeitWNzBWMWQrbkh5UWZRVVRVdGYyV2E0MVdIa0Jvb0J5Nk81NUNqY1pMWS9haHhYTlhST1hKTGQKbEJvNWJ0ZUl6UVRSZlhlR29mUHA3VVk1U0tSaW1KeVl2ejlIenhXRVp2eDBJcWd2MmZRWGE3QU1QWTJrc0JtRgo4YWhCNXkrOURXZStDMDc5L3RNYmVENjA4Y1lWZDFNZEVwWWRNeG82cGJzOHJ0KzBYWEtKWmt5emloWjM5dkFpCmp0N1Z5V1VTU1BJQVJVTERtVzhkT1VFb2t3U1dVcjdzYkpmM3NOWnQ5UlU3dVU5cmJOM2ZRaXlDc04xOGs0RzYKbncxVlI3aFlpV3Y1ZFQ1enoyZWk2TkJoTnpxUDN2WmpXVS9mSU1jaXlXcHhoMlRodFJLMUZIaTZaQ3NlQkRZYgpXNkxlT2dCL3l5bXBBaEVQRW0xbTNxZWNxdnJ0eUtKSEl6NjNMYzBxak9sNnk0VXJqTmxDRTU1cm5PRHR2T1pECnNNeHVyb0dNSTBDNitZSXNSSjJKRTIrYnBYWWtuaHNTdUwwREhtYWtzbTdTMG53cUdqSXdIVTM3dXF1K1N2UlAKcWcvTWY2RlhNVEVSQmlqMXJ0TlhjZDNNZXNhbmpNdStTK2hLVVo5ZHBacVBHOGd5aUZGSVIwY2xoSWRsTEtWcQp1S0dQQ000czBKODk2WXFIZkN5bXRHZkIrR1NsN0NvQktoNEluMTNibStJMzdPcDhBUUtDQVFFQTR3SjA0NE0vClNFNUh5YXZQZHF3WDlmRkFvdGpZdWMzaWFHMUhDa2pYdVU0SUdDczNuOWF4Q24wbGpTRXM3Vks1cUpmblJkaTcKR2hpZnNnS0sycGFCVDloRm03MWh4bHNPUkFpMmtMOERRc2NpaSs1dk0ydVpPWS85RmpIT0prYlA0bXRnUEVSWApYR2ttci9XSC84dFRiTU1OUXZhbERTTFNHNUpoSFlvMWF0REVoLzRCZnRERVdZdnMrVnYyMzVlcThFV1I3bFhkCnFXeHJKb0tja3RZMldnMXRQODdseEZtSEZhbCttaGJtOGNMd1cxZUlVc1AwMC9yS2dRRDNGeVloN1BtcTErNEwKVmRDamR2UXE5cnk3akhMYjA5dHpvSXlrV1VSUVVXZmpTR2Z5aGZMSWhReUxpdk5ZcHNDakxKcGFKNlVLRkI5VwpwTGlOeGR1OTE5bjEzd0tDQVFFQTBwVVZ2bUpmZzJId00xOFlRWUlQcmZlN2x2ZGhFakdkTkNOZUdrdTJyNEZNCkwzdEs3N2I1blFMK0VYRzlIRDR5YzJqejc0a052TUxORGhFcVNuaHZlWHVHc0NZUFpxNWVtSzZtK3cwR2NLZXMKY3dlYnRBaEFzM0t0RXJ4MVJDZHdmTFZxK2ZDS2M0NFpQbklxT1lhVWw4aHFuY05BNGw1VTliTlZWV0JsUWFVZAp1UWliVmZhZ3NkdWZpN2ZDRmpLVTg3Y2VwMHp0VTVtT1QzY1hETitaYmpCWVdGSmc3d096Z21UY0lxUmNjL3NXCm5SSVlMdURoRUZSS3cxeTliMUQveTNLczNZc3JkYUowbkZpRHAvVVRLTU9JQXhnSlZQYmdkTWJnbDU4OGZvclQKU3FvZm40SVVOUmQ0QzAxSU5RVnkwMVBaUWRDU0hIUFh1SnRxZ3FFV2dRS0NBUUJvVm5hM0kxbnd0OW9TL1Y3cgpvb21ZeHZ2NFhVYXZqOHVpUjZmQk9GMitrL2p3Y3R5c0lKZGF4TTUvb1dIdTZuamUzb0t6L2J0eGNTUGxRM25pCm9nNXBUblFmOHRsL3U5WkF1dWgrZXV6YXdvQkVaS0REdDQ3RGdFVEk4TGRackc1Y0dSSXdZUkR1TG41VG5ieVcKZXpPcTU3T3V0WUtER1NBTkFDaVcxVEZjR1B4YnJRbXU2ZkYxWHZUYVg4U0dYRVY3RGQ3VzlxeGM5TElERDBFNwoxQzFERXF6R0NTaGVLUEFIcXRHL3JRc1V6NDU5elN1aEx1UFdrb3lFNHBhdkV4M0F0N2dvYXdiV3VJQ0phZ3hkClA3M0wvZmEvMXp1NzdTaVV4dXRMbno0OXgxa1c2OUh5SlNQMkI0Y1ZqYkR5RFRlbXhScHV5VUNma1J2SWR3azQKcnJ0dEFvSUJBRHk4VHhjb0hGQXljU3IvNUdrUWNDRkc4RTNzYjR6bHptZDVRK3pscFgwZEY3SWlKMHpZUTBvcgowTWVMUEhYbTRub3k3UmhMT1RFV0pqcEdiU0lwZGsxZGVVMVl6Tnhhc21IckRiSWU0WnFnWWJhVG5TN2hxbmVYClBaL0h4ekt2QlZ5U25wWVQ4SHEvb3p4RmhUUXVRckU4VnJQRjJ2THZMaVhuWVZkTWhDZll6YWZPZWE3amdSbUwKTklzQnB2THNCOVg3SE5ZMzg4Tkc2S3EydUdrNEhIS1Jjd21XU09ybThHRk5ZY2lFQ3o1UVR3ZGlicU1tclFNZQpyS21JR0FNQkk2VzBIM09PYml4eGZKeVRVdldnVTdSUUlPeHpoRTJESHQzUGRudUVxOWY3aGxGa205WlBtREJ2CjRtbXdFb0ZvWHVQZ3JTcTBVMC90Z1d4M050TVNUd0VDZ2dFQURIYTl3UVFybkZFMUlZYW9QeTdiUGlSN0dOQmMKM0d0OVB0eUt4YitjWHZpZFA2N2JNV2oyZEpUT3B6d013R3FJdDVDTEZIb0pGbFZjZldVa3lobXZCb2crSDdWVgpxS1BFbHlmb1N2Z3ZRUDRBK054UWR4Y0U0RHR6RTc1aVlGOEI3c25rS3JVUTF1a0t4UFJxVVE1dGtTR2cybnFsCldFZ3pqb3h0MG9jMjFrNXQzL3VpdHVKTGNxTjd1N2pGTWttazFjb09nbXdKN3NHK3dBcHpuQVI1aGRZQXR4c0IKeUtQRVA5eEp4WHVvRER6VDI4dlR2c3BScVlnSlBMSStrcTNwT1RxT0kyZ0FnRngwY2cyUGt0engwSTdTSWpxOQp3MzBkbXRKWUFVQXgyZTdVY2dwdnRGYWhCa3ZTL2xTUE9YNE15aGt6V3FEbXFNQU1JR1h3WVl5b2J3PT0KLS0tLS1FTkQgUlNBIFBSSVZBVEUgS0VZLS0tLS0K
    token: 2wcipccw6lgs773fws4t2lbgekt30bp4v64yrj3pfs6kmxrzun9j1nxu72yrmduo8nlrfuzngmk4y5whez0jaebit1l39ybibkz5vy24b5b5ls697i9lcl1elhbfr99f

```





### (2) AKS 에서 확인

```sh

% kubectl -n kubesphere-system get deploy
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
extensions-museum   1/1     1            1           8m49s
ks-agent            1/1     1            1           8m49s

```



### (3) KubeSphere에서 클러스터 확인



* 메뉴
  * KubeSphere Web UI > Cluster Management
  * 추가된 AKS 클러스터가 정상적으로 표시되는지 확인





## 3) Extentions 확인

이미 설정된 Extention 에서 추가된 Aks 를 선택하여 동일하게 모니터링 되도록  설정할 수 있다.



* 메뉴

  * Workbench > Extentions Center

    * WhizardTelemetry Monitoring

      * **Cluster Agent Configs** 에서 추가된 클러스터를 선택

        

