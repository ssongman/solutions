
# LGTM


# 1.개요

LGTM 스택은 Loki, Grafana, Tempo, Mimir의 약자로, 로그, 메트릭, 트레이싱 및 모니터링 데이터를 수집하고 시각화하는 데 사용되는 도구들로 구성된 모니터링 솔루션이다.
이 스택을 Kubernetes에 설치하는 방법을 살펴본다.









Loki는 대규모 로그 수집 및 분석을 위한 분산형 로그 관리 시스템으로, 여러 구성 요소(Pod)로 이루어져 있습니다. 각 구성 요소는 특정 역할을 수행하며, 전체 시스템이 원활하게 동작하도록 협력합니다. 아래는 Loki를 구성하는 주요 Pod들의 역할에 대한 설명입니다:

### 1. **Ingester**
   - **역할**: Ingester는 Loki에서 로그를 실제로 저장하는 역할을 합니다. 로그 데이터를 수신하고, 이를 메모리와 저장소에 보관합니다. 새로운 로그가 들어오면 이 로그를 인덱싱하고, 설정된 보존 기간이 지나면 이를 삭제합니다.
   - **특징**: Ingester는 로그 데이터의 일관성을 유지하고, 시스템 장애 시 데이터를 복구할 수 있도록 데이터를 분산 저장합니다.

### 2. **Querier**
   - **역할**: Querier는 Loki의 쿼리 엔진 역할을 합니다. 사용자나 애플리케이션에서 오는 로그 쿼리를 처리하며, 필요한 로그 데이터를 검색하고 반환합니다.
   - **특징**: Querier는 대량의 데이터를 빠르게 검색할 수 있도록 최적화되어 있으며, 쿼리 결과를 효율적으로 제공하기 위해 인덱싱된 데이터를 활용합니다.

### 3. **Query Frontend**
   - **역할**: Query Frontend는 사용자의 쿼리를 수신하고, 이를 Querier에게 전달하는 역할을 합니다. 쿼리 요청을 처리하는 데 있어 캐싱, 페이징, 결과 집계를 지원하며, 쿼리 성능을 향상시킵니다.
   - **특징**: Query Frontend는 여러 쿼리 요청을 병렬로 처리하여 성능을 최적화하고, 복잡한 쿼리를 효율적으로 실행할 수 있도록 돕습니다.

### 4. **Query Scheduler**
   - **역할**: Query Scheduler는 쿼리 작업을 스케줄링하고 분산하는 역할을 합니다. 쿼리 요청이 여러 개의 Querier에 효율적으로 분배되도록 관리하며, 시스템 전체의 부하를 조정합니다.
   - **특징**: 이 구성 요소는 대규모 쿼리 요청 처리 시 성능을 극대화하기 위해 필수적입니다.

### 5. **Distributor**
   - **역할**: Distributor는 로그 데이터를 수집하는 역할을 하며, 수집된 로그를 인제스터(Ingester)로 분배합니다. 로그 데이터를 수신한 후, 이를 여러 인제스터에 분산하여 저장합니다.
   - **특징**: 로그의 수집 및 분산 과정을 담당하며, 시스템의 가용성과 확장성을 보장합니다.

### 6. **Compactor**
   - **역할**: Compactor는 로그 데이터를 압축하고, 오래된 데이터를 정리하는 역할을 합니다. 이 구성 요소는 시간이 지나면서 축적된 로그 데이터를 효율적으로 관리하기 위해 필요합니다.
   - **특징**: Compactor는 저장소의 효율성을 높이고, 데이터를 압축하여 디스크 사용량을 줄이며, 오래된 데이터의 보존 정책을 적용합니다.

### 7. **Index Gateway**
   - **역할**: Index Gateway는 Loki의 인덱스 데이터를 관리하는 구성 요소입니다. 로그 데이터를 더 쉽게 검색할 수 있도록 인덱스를 생성하고, 이를 관리합니다.
   - **특징**: 효율적인 인덱스 관리를 통해 쿼리 성능을 향상시키고, 데이터 조회 속도를 개선합니다.

이들 구성 요소는 함께 작동하여 Loki가 대규모 로그 데이터를 효과적으로 수집, 저장, 분석할 수 있도록 지원합니다. 각 구성 요소는 특정 역할에 최적화되어 있으며, 전체 시스템의 성능과 확장성을 보장하는 데 중요한 역할을 합니다.










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



# 2. Loki Grafana 설치

Grafana Labs에서 제공하는 Helm 차트를 사용해 LGTM 스택을 설치할 수 있습니다. Grafana의 Helm 리포지토리를 추가하고 업데이트합니다.

```bash
$ helm repo add grafana https://grafana.github.io/helm-charts
$ helm repo update

```




## 1) Loki 설치
Loki는 로그 수집 시스템이다.



### (1) Loki-stack(Monolithic방식)

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







### (2) Loki(MSA방식)

#### helm repo 준비

```sh

helm repo add grafana https://grafana.github.io/helm-charts

helm repo update


```



#### values_v1.yaml

```
loki:
  schemaConfig:
    configs:
      - from: 2024-08-01
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

gateway:
  ingress:
    enabled: true
    hosts:
      - host: loki.lgtm.ssongman.com
        paths:
          - path: /
            pathType: Prefix

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



#### helm install

```sh


helm -n lgtm install --values values_v1.yaml loki grafana/loki


# 참고 Upgrade 시...
helm -n lgtm upgrade --values values.yaml loki grafana/loki



# 확인
helm -n lgtm list


# 삭제시...
helm -n lgtm delete loki

```





### (3) helm upgrade 

일부 내용추가시 아래와 같이 수정한다.



#### values_v2.yaml

```
loki:
  schemaConfig:
    configs:
      - from: 2024-08-01
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

gateway:
  ingress:
    enabled: true
    hosts:
      - host: loki.lgtm.ssongman.com
        paths:
          - path: /
            pathType: Prefix

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
  ingress:
    enabled: true
    hosts
      - minio.lgtm.ssongman.com
  consoleIngress:
    enabled: true
    hosts
      - minioconsole.lgtm.ssongman.com

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





#### helm update

```sh

# 참고 Upgrade 시...
helm -n lgtm upgrade loki grafana/loki --values values_v2.yaml 



# 확인
helm -n lgtm list


# 삭제시...
helm -n lgtm delete loki


```





```sh

kubectl -n lgtm get pods

NAME                                    READY   STATUS    RESTARTS   AGE
curl-648df9bcbd-9g44w                   1/1     Running   0          9h
grafana-6dbf6b5cc8-mn5g2                1/1     Running   0          9h
loki-canary-8tzbt                       1/1     Running   0          3m20s
loki-canary-bxfcq                       1/1     Running   0          3m20s
loki-canary-lmksb                       1/1     Running   0          3m20s
loki-chunks-cache-0                     2/2     Running   0          3m20s
loki-compactor-0                        1/1     Running   0          3m20s
loki-distributor-5847df65b8-g2q9v       1/1     Running   0          3m20s
loki-distributor-5847df65b8-kcvfp       1/1     Running   0          3m20s
loki-distributor-5847df65b8-khk44       1/1     Running   0          3m20s
loki-gateway-5dfbfdc747-57tsj           1/1     Running   0          3m20s
loki-index-gateway-0                    1/1     Running   0          3m19s
loki-index-gateway-1                    1/1     Running   0          2m27s
loki-ingester-zone-a-0                  1/1     Running   0          3m20s
loki-ingester-zone-b-0                  1/1     Running   0          3m19s
loki-ingester-zone-c-0                  1/1     Running   0          3m19s
loki-minio-0                            1/1     Running   0          3m20s
loki-querier-c449d4bc8-4vwnz            1/1     Running   0          3m20s
loki-querier-c449d4bc8-qcd9f            1/1     Running   0          3m19s
loki-querier-c449d4bc8-qlv7g            1/1     Running   0          3m19s
loki-query-frontend-5b8c88bd79-999h6    1/1     Running   0          3m19s
loki-query-frontend-5b8c88bd79-fxlrt    1/1     Running   0          3m20s
loki-query-scheduler-5686d65bcc-j7kgf   1/1     Running   0          3m19s
loki-query-scheduler-5686d65bcc-vpvc2   1/1     Running   0          3m20s
loki-results-cache-0                    2/2     Running   0          3m20s


```



#### Object storage config

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



## 2) Promtail 설치



### Install using Helm



helm repo

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```



Create the configuration file `values_promql.yaml`. 



```yaml
config:
# publish data to loki
  clients:
    - url: http://loki-gateway/loki/api/v1/push
      tenant_id: 1
```



Promtail deployed

```bash

# The default helm configuration deploys promtail as a daemonSet (recommended)
helm -n lgtm install promtail grafana/promtail --values values_promql.yaml


# 확인
helm -n lgtm list

helm -n lgtm list
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
grafana         lgtm            1               2024-08-29 14:03:55.493480546 +0900 KST deployed        grafana-8.4.6   11.1.4
loki            lgtm            1               2024-08-29 23:28:38.823732968 +0900 KST deployed        loki-6.10.0     3.1.1
promtail        lgtm            1               2024-08-30 00:30:33.880967616 +0900 KST deployed        promtail-6.16.5 3.0.0


# 삭제시...
helm -n lgtm delete promtail



```



## 3) Grafana 설치

### (1) Grafana 설치

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





### (2) Grafana 초기 암호 확인

Grafana의 기본 관리자 암호를 확인하려면 아래 명령어를 사용하세요.

```bash
kubectl -n lgtm get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

```

### (3) Grafana 대시보드 접속
브라우저에서 `http://<External-IP>:<Port>`로 Grafana에 접속하고, `admin` 사용자와 위에서 확인한 비밀번호로 로그인합니다.



### (9) trouble shooting



```sh

curl http://loki-gateway/loki/api/v1/query
no org id

```

이 에러 메시지는 Grafana가 Loki와 통신할 때 “no org id”라는 오류 메시지를 반환받아 발생한 것입니다. 이 문제는 보통 Loki의 멀티테넌시 설정 또는 Grafana와 Loki 간의 인증 문제에서 발생할 수 있다.





## 4) Grafana 설정



### (1) Connection 추가

* 메뉴 :  new Conection

```sh

loki 추가

```



### (2) Dashboard 추가

* 메뉴 : Dashboard
  * new > import
  * 번호 : 13639




## 5) Minio 확인

**MinIO**는 고성능의 객체 스토리지 솔루션으로, Amazon S3 API와 호환되는 오픈 소스 소프트웨어이다. 이 솔루션은 클라우드 환경에서 대규모 데이터를 저장하고 관리하는 데 사용되며, 특히 고속 데이터 처리와 스케일링이 중요한 환경에서 활용된다.



### (1) 접속방법



* **MinIO Browser**: MinIO는 기본적으로 웹 기반 관리 인터페이스를 제공한다. MinIO 서버에 접속하면 웹 브라우저를 통해 데이터 버킷과 객체를 탐색하고 관리할 수 있다.

* **접속 방법**: http://<minio-server-ip>:<minio-port>로 접속하여 MinIO에 로그인한 후, 웹 인터페이스에서 파일을 업로드, 다운로드, 삭제 및 탐색할 수 있다.



#### User/pass 확인

secret 을 통해서 확인한다.

```sh

$ kubectl -n lgtm get secret loki-minio -o jsonpath="{.data.rootUser}" | base64 --decode ; echo
enterprise-logs

$ kubectl -n lgtm get secret loki-minio -o jsonpath="{.data.rootPassword}" | base64 --decode ; echo
supersecret


# user/pass
# enterprise-logs / supersecret

```





#### ingress

* service

```

loki-minio.lgtm.svc:9000

loki-minio-console.lgtm.svc:9001

```







# 3. Tempo 설치

Tempo는 트레이싱 데이터를 수집하는 데 사용됩니다. 

```bash
helm install tempo grafana/tempo
```







# 4. Mimir 설치

Mimir는 메트릭을 수집하고 처리하는 솔루션이다. 

```bash
helm install mimir grafana/mimir
```





