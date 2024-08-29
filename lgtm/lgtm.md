
# LGTM


# 1.개요

LGTM 스택은 Loki, Grafana, Tempo, Mimir의 약자로, 로그, 메트릭, 트레이싱 및 모니터링 데이터를 수집하고 시각화하는 데 사용되는 도구들로 구성된 모니터링 솔루션이다.
이 스택을 Kubernetes에 설치하는 방법을 살펴본다.




# 2. 준비 작업

#### 1.1 Helm 설치 (필요한 경우)
Helm이 설치되어 있지 않다면, 아래 명령어로 설치합니다.

```bash
$ curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```



#### 1.2 Kubernetes 클러스터 확인

Kubernetes 클러스터가 준비되었는지 확인합니다.

```bash
kubectl get nodes
```



#### 1.2 Namespace 생성

```bash
kubectl create ns lgtm

```



# 2. LGTM 스택 설치

Grafana Labs에서 제공하는 Helm 차트를 사용해 LGTM 스택을 설치할 수 있습니다. Grafana의 Helm 리포지토리를 추가하고 업데이트합니다.

```bash
$ helm repo add grafana https://grafana.github.io/helm-charts
$ helm repo update

```




## 1) Loki 설치
Loki는 로그 수집 시스템이다.



### (1) Loki-stack

```bash

$ helm search repo loki

NAME                            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/grafana-loki            4.6.11          3.1.1           Grafana Loki is a horizontally scalable, highly...
grafana/loki                    6.10.0          3.1.1           Helm chart for Grafana Loki and Grafana Enterpr...
grafana/loki-canary             0.14.0          2.9.1           Helm chart for Grafana Loki Canary
grafana/loki-distributed        0.79.3          2.9.8           Helm chart for Grafana Loki in microservices mode
grafana/loki-simple-scalable    1.8.11          2.6.1           Helm chart for Grafana Loki in simple, scalable...
grafana/loki-stack              2.10.2          v2.9.3          Loki: like Prometheus, but for logs.


$ cd ~/helm/charts
$ helm fetch grafana/loki-stack

$ ll
-rw-r--r--  1 song song 154549 Aug 29 13:45 loki-stack-2.10.2.tgz


$ cd ~/helm/charts/loki-stack

$ helm -n lgtm install loki . \
    --dry-run=true > 11.dry-run.yaml




# 확인
$ helm -n lgtm list
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
grafana lgtm            1               2024-08-29 14:03:55.493480546 +0900 KST deployed        grafana-8.4.6           11.1.4
loki    lgtm            1               2024-08-21 00:39:08.070467545 +0900 KST deployed        loki-stack-2.10.2       v2.9.3



# 삭제시...
$ helm -n lgtm delete loki


```

 Loki를 설치면 loki와 loki-promtail이 daemonset 으로 설치된다.







### (2) Loki



```sh

helm repo add grafana https://grafana.github.io/helm-charts

helm repo update


```



values.yaml

```
loki:
  schemaConfig:
    configs:
      - from: 2024-04-01
        store: tsdb
        object_store: s3
        schema: v13
        index:
          prefix: loki_index_
          period: 24h
  ingester:
    chunk_encoding: snappy
  tracing:
    enabled: true
  querier:
    # Default is 4, if you have enough memory and CPU you can increase, reduce if OOMing
    max_concurrent: 4

#gateway:
#  ingress:
#    enabled: true
#    hosts:
#      - host: FIXME
#        paths:
#          - path: /
#            pathType: Prefix

deploymentMode: Distributed

ingester:
  replicas: 3
querier:
  replicas: 3
  maxUnavailable: 2
queryFrontend:
  replicas: 2
  maxUnavailable: 1
queryScheduler:
  replicas: 2
distributor:
  replicas: 3
  maxUnavailable: 2
compactor:
  replicas: 1
indexGateway:
  replicas: 2
  maxUnavailable: 1

bloomCompactor:
  replicas: 0
bloomGateway:
  replicas: 0

# Enable minio for storage
minio:
  enabled: true

# Zero out replica counts of other deployment modes
backend:
  replicas: 0
read:
  replicas: 0
write:
  replicas: 0

singleBinary:
  replicas: 0 
```







```sh


helm install --values values.yaml loki grafana/loki


# 참고 Upgrade 시...
helm upgrade --values values.yaml loki grafana/loki




```



```sh


kubectl get pods -n loki




```



Object storage config

```sh

# Example configuration for Loki with Azure Blob Storage

loki:
  schemaConfig:
    configs:
      - from: 2024-04-01
        store: tsdb
        object_store: azure
        schema: v13
        index:
          prefix: loki_index_
          period: 24h
  ingester:
    chunk_encoding: snappy
  tracing:
    enabled: true
  querier:
    max_concurrent: 4

  storage:
    type: azure
    azure:
      # Name of the Azure Blob Storage account
      accountName: <your-account-name>
      # Key associated with the Azure Blob Storage account
      accountKey: <your-account-key>
      # Comprehensive connection string for Azure Blob Storage account (Can be used to replace endpoint, accountName, and accountKey)
      connectionString: <your-connection-string>
      # Flag indicating whether to use Azure Managed Identity for authentication
      useManagedIdentity: false
      # Flag indicating whether to use a federated token for authentication
      useFederatedToken: false
      # Client ID of the user-assigned managed identity (if applicable)
      userAssignedId: <your-user-assigned-id>
      # Timeout duration for requests made to the Azure Blob Storage account (in seconds)
      requestTimeout: <your-request-timeout>
      # Domain suffix of the Azure Blob Storage service endpoint (e.g., core.windows.net)
      endpointSuffix: <your-endpoint-suffix>
    bucketNames:
      chunks: "chunks"
      ruler: "ruler"
      admin: "admin"
deploymentMode: Distributed

ingester:
  replicas: 3
querier:
  replicas: 3
  maxUnavailable: 2
queryFrontend:
  replicas: 2
  maxUnavailable: 1
queryScheduler:
  replicas: 2
distributor:
  replicas: 3
  maxUnavailable: 2
compactor:
  replicas: 1
indexGateway:
  replicas: 2
  maxUnavailable: 1

bloomCompactor:
  replicas: 0
bloomGateway:
  replicas: 0

backend:
  replicas: 0
read:
  replicas: 0
write:
  replicas: 0

singleBinary:
  replicas: 0

```







## 2) Grafana 설치

Grafana는 시각화 도구로, 다양한 데이터 소스를 연결할 수 있습니다. Grafana를 설치하려면 아래 명령어를 사용합니다.

```bash


$ helm search repo grafana

NAME                            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/grafana-loki            4.6.11          3.1.1           Grafana Loki is a horizontally scalable, highly...
grafana/loki                    6.10.0          3.1.1           Helm chart for Grafana Loki and Grafana Enterpr...
grafana/loki-canary             0.14.0          2.9.1           Helm chart for Grafana Loki Canary
grafana/loki-distributed        0.79.3          2.9.8           Helm chart for Grafana Loki in microservices mode
grafana/loki-simple-scalable    1.8.11          2.6.1           Helm chart for Grafana Loki in simple, scalable...
grafana/loki-stack              2.10.2          v2.9.3          Loki: like Prometheus, but for logs.

$ cd ~/helm/charts
$ helm fetch grafana/grafana



$ cd ~/helm/charts/grafana


$ helm -n lgtm install grafana . \
    --set ingress.enabled=true \
    --set ingress.enabled=true \
    --set ingress.hosts[0]=grafana.lgtm.ssongman.com \
    --set adminUser=admin \
    --set adminPassword=adminpass123! \
    --dry-run=true > 12.dry-run.yaml
    
    
    --set admin.userKey=admin \
    --set admin.passwordKey=adminpass \


$ helm -n lgtm list

NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
grafana lgtm            1               2024-08-29 13:59:46.119197926 +0900 KST deployed        grafana-8.4.6           11.1.4
loki    lgtm            1               2024-08-21 00:39:08.070467545 +0900 KST deployed        loki-stack-2.10.2       v2.9.3


# 삭제시...
$ helm -n lgtm delete grafana












```





## 3) Tempo 설치

Tempo는 트레이싱 데이터를 수집하는 데 사용됩니다. Tempo를 설치하려면 다음 명령어를 실행합니다.

```bash
helm install tempo grafana/tempo
```



## 4) Mimir 설치

Mimir는 메트릭을 수집하고 처리하는 솔루션입니다. Mimir를 설치하려면 아래 명령어를 사용합니다.

```bash
helm install mimir grafana/mimir
```



## 5) 배포 상태 확인

각각의 설치가 완료되면, 배포된 파드들이 정상적으로 실행 중인지 확인합니다.

```bash
kubectl get pods
```

여기서 각 파드가 정상 상태(`Running`)인지 확인하세요.









# 3. Grafana 설정 및 접속

## 1) Grafana 서비스 노출
Grafana 대시보드에 접근하기 위해, NodePort 또는 LoadBalancer로 서비스를 노출합니다.

```bash
kubectl expose deployment grafana --type=NodePort --name=grafana-service
```

노출된 포트를 확인합니다.

```bash
kubectl get services grafana-service
```

## 2) Grafana 초기 암호 확인
Grafana의 기본 관리자 암호를 확인하려면 아래 명령어를 사용하세요.

```bash
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

## 3) Grafana 대시보드 접속
브라우저에서 `http://<External-IP>:<Port>`로 Grafana에 접속하고, `admin` 사용자와 위에서 확인한 비밀번호로 로그인합니다.





## 4) 데이터 소스 설정 및 대시보드 구성

Grafana 대시보드에 접속한 후, 아래와 같이 각 데이터 소스를 설정합니다.

1. **Loki**: 로그를 시각화하기 위해 Loki를 데이터 소스로 추가합니다.
2. **Mimir**: 메트릭을 시각화하기 위해 Mimir를 데이터 소스로 추가합니다.
3. **Tempo**: 트레이싱 데이터를 시각화하기 위해 Tempo를 데이터 소스로 추가합니다.

이후, 각 데이터 소스를 바탕으로 대시보드를 구성하여 로그, 메트릭, 트레이싱 데이터를 모니터링할 수 있습니다.





# 6. 간단한 테스트

각 구성 요소가 정상적으로 동작하는지 확인하기 위해, 예시 애플리케이션을 배포하여 로그 및 메트릭 데이터를 수집하고, Grafana에서 시각화해 볼 수 있습니다.

## 6.1 예시 애플리케이션 배포
간단한 애플리케이션을 Kubernetes에 배포합니다.

```bash
kubectl run test-app --image=nginx --port=80
kubectl expose deployment test-app --type=ClusterIP
```

## 6.2 데이터 수집 확인
몇 분 후, Grafana 대시보드에서 Loki를 통해 로그를, Mimir를 통해 메트릭을, Tempo를 통해 트레이싱 데이터를 확인할 수 있습니다.

### 마무리

이제 LGTM 스택을 통해 Kubernetes 환경에서 통합 모니터링을 수행할 수 있습니다. Grafana 대시보드에서 다양한 데이터 소스를 추가하고 시각화를 구성하여 클러스터의 상태를 지속적으로 모니터링하세요.
