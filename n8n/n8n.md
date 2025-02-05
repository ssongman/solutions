# **n8n 설치**



# 1. 개요

n8n은 자동화 및 워크플로우 관리를 위한 오픈소스 도구임

Helm을 사용하면 Kubernetes 클러스터에 쉽게 배포할 수 있음.



# 2. n8n install





## 1) n8n 기본 설치



참고 : https://github.com/8gears/n8n-helm-chart





### (1) namespace 생성

```sh

$ kubectl create ns n8n

```



### (2) Helm Repository 추가 및 업데이트

```sh
$ helm repo add n8n https://dl.n8n.io/helm-charts/

$ helm repo update

$ helm search repo n8n

$ helm fetch oci://8gears.container-registry.com/library/n8n --version 0.25.2


```



### (3) helm install

```sh




$ helm -n n8n upgrade --install my-n8n oci://8gears.container-registry.com/library/n8n --version 0.25.2 \
   --set ingress.enabled=true \
   --set ingress.className=traefik \
   --set ingress.hosts[0].host=n8n.ssongman.com \
   --set ingress.hosts[0].paths[0]=/ \
   --set persistence.enabled=false \
   --set persistence.size=10Gi \
   --set env.N8N_SECURE_COOKIE="false"


# [참고]-------------------------
   --set ingress.hosts[0].paths[0].path="/" \
   --set ingress.hosts[0].paths[0].pathType=ImplementationSpecific \
# [참고]-------------------------


# 설치확인
$ helm list -n n8n
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS  CHART           APP VERSION
my-n8n  n8n             1               2025-02-02 23:23:50.594331677 +0900 KST failed  n8n-0.25.2      1.58.2


# 삭제시...
$ helm uninstall my-n8n --namespace n8n

$ kubectl delete namespace n8n


```



## 2) 설치 옵션 커스터마이징



### (1) 환경 변수 설정

n8n의 API 및 UI를 사용할 도메인, DB 연결 정보 등을 설정할 수 있음.

```sh

$ helm install my-n8n n8n/n8n --namespace n8n \
    --set env.N8N_HOST=n8n.example.com \
    --set env.N8N_PORT=5678
    
    

```

* env.N8N_HOST: 서비스가 사용할 도메인
* env.N8N_PORT: 서비스 포트



### (2) Persistent Volume (데이터 유지)

```sh

$ helm install my-n8n n8n/n8n --namespace n8n \
    --set persistence.enabled=true \
    --set persistence.size=10Gi

```

* persistence.enabled=true: 영구 스토리지 활성화
* persistence.size=10Gi: 10GB 크기의 볼륨 할당



### (3) 외부 데이터베이스 연결 (PostgreSQL)

기본적으로 SQLite를 사용하지만, PostgreSQL과 연결할 수도 있음

```sh

$ helm install my-n8n n8n/n8n --namespace n8n \
 --set env.DB_TYPE=postgresdb \
 --set env.DB_POSTGRESDB_HOST=my-postgres \
 --set env.DB_POSTGRESDB_PORT=5432 \
 --set env.DB_POSTGRESDB_DATABASE=n8n \
 --set env.DB_POSTGRESDB_USER=n8n \
 --set env.DB_POSTGRESDB_PASSWORD=my-secret-password
 
```

* env.DB_TYPE=postgresdb: PostgreSQL 사용
* env.DB_POSTGRESDB_HOST: PostgreSQL 서비스 이름
* env.DB_POSTGRESDB_PORT: 기본 5432 포트
* env.DB_POSTGRESDB_DATABASE: 사용할 DB 이름
* env.DB_POSTGRESDB_USER: DB 사용자
* env.DB_POSTGRESDB_PASSWORD: DB 비밀번호



### (4) Ingress 설정 (도메인 연결)

Ingress를 설정하면 도메인으로 n8n에 접근할 수 있음.

```sh

$ helm install my-n8n n8n/n8n --namespace n8n \
 --set ingress.enabled=true \
 --set ingress.hosts[0].host=n8n.example.com \
 --set ingress.hosts[0].paths[0].path="/" \
 --set ingress.hosts[0].paths[0].pathType=ImplementationSpecific
 
```

* ingress.enabled=true: Ingress 활성화
* ingress.hosts[].host: 도메인 설정
* ingress.hosts[].paths[].path: 경로 설정 (/ 기본)



만약 **Let’s Encrypt (무료 SSL 인증서)** 를 적용하려면 Cert-Manager를 함께 설정하자.



## 3) 설치 확인 및 접속

```sh


# 설치된 Helm 릴리스 확인
$ helm list -n n8n

# Pod 상태 확인
$ kubectl get pods -n n8n

# Service 확인
$ kubectl get svc -n n8n

```



* ClusterIP 또는 LoadBalancer 타입인지 확인
* EXTERNAL-IP가 할당된 경우 http://EXTERNAL-IP:5678 로 접속



```


http://EXTERNAL-IP:5678


```





## 4) 업데이트



새로운 버전이 나오면 업데이트할 수 있음

```sh

$ helm upgrade my-n8n n8n/n8n --namespace n8n

```



# 3. n8n Setting



## 1) Set up owner account



* email
  * ssongmantop@gmail.com
* song
* song
* Songpass123!