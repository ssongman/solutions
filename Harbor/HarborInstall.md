#  < Harbor >





# 1. 개요

harbor registry install



관련링크 : [[Docker\] Harbor를 이용한 Private Registry 구축 :: Simple is Beautiful. (tistory.com)](https://smoh.tistory.com/291)







# 2. Harbor Install(helm)



## 1) Namespace

```sh

$ kubectl create ns harbor

```





## 2) 인증성 준비

harbor 는 반드시 인증서가 필요하다.





#### 디렉토리 이동

```
cd ~
mkdir -p ~/certs
cd ~/certs
```

#### CA Certificates 생성

```
# Root CA의 비밀키 생성
openssl genrsa -out ca.key 4096

# Root CA의 비밀키와 짝을 이룰 공개키 생성
# * CN은 도메인이나 아이피 입력
openssl req -x509 -new -nodes -sha512 -days 3650 \
 -subj "/C=CN/ST=seoul/L=seoul/O=kyh0703/OU=tester/CN=100.100.103.167" \
 -key ca.key \
 -out ca.crt
```



#### Server Certificates 생성

```
# Server의 비밀키 생성
openssl genrsa -out yourdomain.com.key 4096

# Server의 CSR 파일 생성
# * CN은 도메인이나 아이피 입력
openssl req -sha512 -new \
    -subj "/C=CN/ST=seoul/L=seoul/O=kyh0703/OU=tester/CN=100.100.103.167" \
    -key 100.100.103.167.key \
    -out 100.100.103.167.csr
```



#### 인증

```
cat > v3ext.cnf <<-EOF
subjectAltName = IP:100.100.103.167,IP:127.0.0.1
EOF
```



#### 인증키 생성

```
openssl x509 -req -sha512 -days 3650 \
    -extfile v3.ext \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -in 100.100.103.167.csr \
    -out 100.100.103.167.crt
```



#### 인증서 복사

```
sudo mkdir -p /data/cert
cp 100.100.103.167.crt /data/cert/
cp 100.100.103.167.key /data/cert/
```



#### Cert 파일 생성

```
openssl x509 -inform PEM -in 100.100.103.167.crt -out 100.100.103.167.cert
```



#### Docker 인증서 복사

```
sudo mkdir -p /etc/docker/certs.d/100.100.103.167
cp 100.100.103.167.cert /etc/docker/certs.d/100.100.103.167/
cp 100.100.103.167.key /etc/docker/certs.d/100.100.103.167/
cp ca.crt /etc/docker/certs.d/100.100.103.167/
```

#### 











## 3) Helm install

```sh

$ helm search repo harbo
NAME            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/harbor  20.1.2          2.10.0          Harbor is an open source trusted cloud-native r...


# 
$ cd ~/song/helm/chart
$ helm search repo harbo

$ ll
-rw-r--r-- 1 song song 255670 Mar 17 22:48 harbor-20.1.2.tgz

$ tar -xzvf harbor-20.1.2.tgz

$ cd ~/song/helm/charts/harbor


$ helm -n harbor install harbor . \
    --set adminPassword=adminpass \
    --set internalTLS.enabled=true \
    --set exposureType=ingress \
    --set externalURL=https://harbor-core.ssongman.duckdns.org \
    --set service.type=ClusterIP \
    --set ingress.core.ingressClassName=traefik \
    --set ingress.core.hostname=harbor.ssongman.duckdns.org \
    --set ingress.core.tls=true \
    --set persistence.enabled=false \
    --set nginx.replicaCount=1 \
    --set portal.replicaCount=1 \
    --set core.replicaCount=1 \
    --set jobservice.replicaCount=1 \
    --set registry.replicaCount=1 \
    --set trivy.enabled=false \
    --set trivy.replicaCount=1 \
    --set exporter.replicaCount=1 \
    --set metrics.enabled=false \
    --set postgresql.primary.persistence.enabled=false \
    --set redis.master.persistence.enabled=false \
    --set redis.replica.persistence.enabled=false \
    --dry-run=true
    
    

############################################################
    --set adminPassword=adminpass \
    
    --set ingress.core.tls=true \
    
    
    --set exposureType=ingress \
    --set externalURL=https://harbor-core.ssongman.duckdns.org \
    
    --set exposureType=proxy \
    --set service.type=LoadBalancer \

############################################################
NAME: harbor
LAST DEPLOYED: Mon Mar 18 00:04:53 2024
NAMESPACE: harbor
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: harbor
CHART VERSION: 20.1.2
APP VERSION: 2.10.0

** Please be patient while the chart is being deployed **

1. Get the Harbor URL:

  You should be able to access your new Harbor installation through https://harbor-core.ssongman.duckdns.org

2. Login with the following credentials to see your Harbor application

  echo Username: "admin"
  echo Password: $(kubectl get secret --namespace harbor harbor-core-envvars -o jsonpath="{.data.HARBOR_ADMIN_PASSWORD}" | base64 -d)

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - core.resources
  - exporter.resources
  - jobservice.resources
  - nginx.resources
  - portal.resources
  - registry.controller.resources
  - registry.server.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

############################################################

  echo Username: "admin"
  echo Password: $(kubectl -n harbor get secret --namespace harbor harbor-core-envvars -o jsonpath="{.data.HARBOR_ADMIN_PASSWORD}" | base64 -d)

Username: admin
Password: PMAWucnkqW

############################################################


$ helm -n harbor ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
harbor  harbor          1               2024-03-17 23:17:27.369035119 +0900 KST deployed        harbor-20.1.2   2.10.0


# 삭제시...
$ helm -n harbor delete harbor

$ helm -n harbor uninstall harbor



```





### [참고] helm upgrade 

```sh


$ helm -n harbor upgrade --install harbor . \
    --set adminPassword=adminpass \
    --set exposureType=ingress \
    --set externalURL=https://harbor-core.ssongman.duckdns.org \
    --set service.type=ClusterIP \
    --set ingress.core.ingressClassName=traefik \
    --set ingress.core.hostname=harbor.ssongman.duckdns.org \
    --set persistence.enabled=false \
    --set nginx.replicaCount=1 \
    --set portal.replicaCount=1 \
    --set core.replicaCount=1 \
    --set jobservice.replicaCount=1 \
    --set registry.replicaCount=1 \
    --set trivy.enabled=false \
    --set trivy.replicaCount=1 \
    --set exporter.replicaCount=1 \
    --set metrics.enabled=false \
    --set postgresql.primary.persistence.enabled=false \
    --set redis.master.persistence.enabled=false \
    --set redis.replica.persistence.enabled=false \
    --dry-run=true
    
############

Release "harbor" has been upgraded. Happy Helming!
NAME: harbor
LAST DEPLOYED: Sun Mar 17 23:37:33 2024
NAMESPACE: harbor
STATUS: deployed
REVISION: 2
TEST SUITE: None
NOTES:
CHART NAME: harbor
CHART VERSION: 20.1.2
APP VERSION: 2.10.0

** Please be patient while the chart is being deployed **

1. Get the Harbor URL:

  You should be able to access your new Harbor installation through https://harbor-core.ssongman.duckdns.org

2. Login with the following credentials to see your Harbor application

  echo Username: "admin"
  echo Password: $(kubectl -n harbor get secret --namespace harbor harbor-core-envvars -o jsonpath="{.data.HARBOR_ADMIN_PASSWORD}" | base64 -d)

adminpass





WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - core.resources
  - exporter.resources
  - jobservice.resources
  - nginx.resources
  - portal.resources
  - registry.controller.resources
  - registry.server.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/







$ helm -n harbor ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
harbor  harbor          1               2024-03-17 23:17:27.369035119 +0900 KST deployed        harbor-20.1.2   2.10.0

NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
harbor  harbor          2               2024-03-17 23:37:33.678058148 +0900 KST deployed        harbor-20.1.2   2.10.0

    
    
```





## 4) 확인



```sh



$ kubectl -n harbor get pod
NAME                                READY   STATUS    RESTARTS        AGE
harbor-core-774d46fb9-m4cr2         1/1     Running   0               4m13s
harbor-jobservice-ff8969667-j6fxw   1/1     Running   1 (2m13s ago)   4m13s
harbor-nginx-54d57848c9-sz945       1/1     Running   0               4m13s
harbor-portal-ff8f8c996-ccznz       1/1     Running   0               4m13s
harbor-postgresql-0                 1/1     Running   0               4m13s
harbor-redis-master-0               1/1     Running   0               4m13s
harbor-registry-5c9cc6658d-l8x9n    2/2     Running   0               4m13s





$ kubectl -n harbor get svc
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
harbor                  ClusterIP   10.43.239.39    <none>        80/TCP,443/TCP      6m21s
harbor-core             ClusterIP   10.43.75.65     <none>        80/TCP              6m21s
harbor-jobservice       ClusterIP   10.43.90.199    <none>        80/TCP              6m21s
harbor-portal           ClusterIP   10.43.238.67    <none>        80/TCP              6m21s
harbor-postgresql       ClusterIP   10.43.104.254   <none>        5432/TCP            6m21s
harbor-postgresql-hl    ClusterIP   None            <none>        5432/TCP            6m21s
harbor-redis-headless   ClusterIP   None            <none>        6379/TCP            6m21s
harbor-redis-master     ClusterIP   10.43.47.201    <none>        6379/TCP            6m21s
harbor-registry         ClusterIP   10.43.223.84    <none>        5000/TCP,8080/TCP   6m21s


## curl text 를 위해...
$ kubectl -n yjsong exec -it deploy/userlist -- bash

$ curl https://harbor.harbor.svc -k -i
$ curl http://harbor-core.harbor.svc -i
$ curl http://harbor-portal.harbor.svc -i






apiVersion: v1
data:
  _REDIS_URL_CORE: cmVkaXM6Ly9oYXJib3ItcmVkaXMtbWFzdGVyOjYzNzkvMA==
  _REDIS_URL_REG: cmVkaXM6Ly9oYXJib3ItcmVkaXMtbWFzdGVyOjYzNzkvMg==
  CSRF_KEY: T05tVjN1V0l3ZUcyRlhSbWo3cWFWQTZDQ3AySVg3eHU=
  HARBOR_ADMIN_PASSWORD: YWRtaW5wYXNz
  POSTGRESQL_PASSWORD: bm90LXNlY3VyZS1kYXRhYmFzZS1wYXNzd29yZA==
  REGISTRY_CREDENTIAL_PASSWORD: aGFyYm9yX3JlZ2lzdHJ5X3Bhc3N3b3Jk
  REGISTRY_CREDENTIAL_USERNAME: aGFyYm9yX3JlZ2lzdHJ5X3VzZXI=
kind: Secret
metadata:
  annotations:
    meta.helm.sh/release-name: harbor
    meta.helm.sh/release-namespace: harbor
  creationTimestamp: "2024-03-17T14:17:34Z"
  labels:
    app.kubernetes.io/component: core
    app.kubernetes.io/instance: harbor
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: harbor
    app.kubernetes.io/version: 2.10.0
    helm.sh/chart: harbor-20.1.2
  name: harbor-core-envvars
  namespace: harbor
  resourceVersion: "77497788"
  uid: c056e6ef-87a7-4ec6-ae89-4430f6debd91
type: Opaque


$ echo aGFyYm9yX3JlZ2lzdHJ5X3VzZXI= | base64 -d
harbor_registry_user


$ echo aGFyYm9yX3JlZ2lzdHJ5X3Bhc3N3b3Jk | base64 -d
harbor_registry_password




```









## 5) 접속 url



* 접속 url
  * http://harbor.ssongman.duckdns.org/
* ID/Pass
  * admin/1JgUA7F9t5



## 9) trouble shooting



### (1) CSRF (Cross-Site Request Forgery) 토큰 오류



로그인 안됨....

이상하다...

별짓을 다해도 안되네...

* harbor-core 로그

```sh


2024-03-18T01:58:20Z [DEBUG] [/server/middleware/log/log.go:31]: attach request id df0502cc-aefd-43a6-a3b3-76701bcb2180 to the logger for the request POST /c/login
2024-03-18T01:58:20Z [DEBUG] [/lib/http/error.go:62]: {"errors":[{"code":"FORBIDDEN","message":"CSRF token invalid"}]}

```



* 안되는 사항 정리
  * harbor를 helm chart로 설치후 첫 로그인을 시도하고 있는데 잘 안됨
  * harbor-core pod 의 로그를 살펴보니 Forbidden 이라는 코드가 표기
  * "CSRF token invalid"  라는 메세지가 보임



원인 분석



```
참고
https://blog.naver.com/anabaral/222024547186


이 csrf 토큰이란 게 쿠키로 전달되는데, 
크롬이 비보안 통신에서는 이 쿠키를 활성화하지 않으니 Request Header에도 그 쿠키가 다시 송신되지 않은 거였고, 
그래서 서버가 거부한 것이었음..

결국 https 로 설정 다시 하니 정상동작.


```



















# 5.[Client] Docker push

bastion 에서 push 해 보자.

## 1) push

```sh

$ docker pull ssongman/userlist:v1
$ docker tag ssongman/userlist:v1 nexus-repo.ssongman.duckdns.org:80/ssongman/userlist:v1

$ docker tag ssongman/userlist:v1 nexus-repo.ssongman.duckdns.org/ssongman/userlist:v1
$ docker tag ssongman/userlist:v1 nexus-repo.ssongman.duckdns.org/ssongman/userlist:v1.0.1



$ docker images
REPOSITORY                                             TAG               IMAGE ID       CREATED         SIZE
ssongman/userlist                                      v1                bf0cd99d0bad   5 years ago     680MB
nexus-repo.ssongman.duckdns.org:80/ssongman/userlist   v1                bf0cd99d0bad   5 years ago     680MB
nexus-repo.ssongman.duckdns.org/ssongman/userlist      v1                bf0cd99d0bad   5 years ago     680MB


$ docker push nexus-repo.ssongman.duckdns.org/ssongman/userlist:v1
The push refers to repository [nexus-repo.ssongman.duckdns.org/ssongman/userlist]
eec0e531f0de: Pushed
2a2b4c333b3a: Pushed
35c20f26d188: Pushed
c3fe59dd9556: Pushed
6ed1a81ba5b6: Pushed
a3483ce177ce: Pushed
ce6c8756685b: Pushed
30339f20ced0: Pushed
0eb22bfb707d: Pushed
a2ae92ffcd29: Pushed
v1: digest: sha256:b0d5a3b6022623b71f09b866a8d612d71118ff9de54c966db91d900c03b31bcc size: 2424




$ docker push nexus-repo.ssongman.duckdns.org/ssongman/userlist:v1.0.1

The push refers to repository [nexus-repo.ssongman.duckdns.org/ssongman/userlist]
eec0e531f0de: Layer already exists
2a2b4c333b3a: Layer already exists
35c20f26d188: Layer already exists
c3fe59dd9556: Layer already exists
6ed1a81ba5b6: Layer already exists
a3483ce177ce: Layer already exists
ce6c8756685b: Layer already exists
30339f20ced0: Layer already exists
0eb22bfb707d: Layer already exists
a2ae92ffcd29: Layer already exists
v1.0.1: digest: sha256:b0d5a3b6022623b71f09b866a8d612d71118ff9de54c966db91d900c03b31bcc size: 2424

```





### [참고] 404 response body error 발생시



```sh

# error 확인
$ docker push nexus-repo.ssongman.duckdns.org:80/ssongman/userlist:v1
eec0e531f0de: Preparing
2a2b4c333b3a: Preparing
35c20f26d188: Preparing
c3fe59dd9556: Preparing
6ed1a81ba5b6: Preparing
a3483ce177ce: Waiting
ce6c8756685b: Waiting
30339f20ced0: Waiting
0eb22bfb707d: Waiting
a2ae92ffcd29: Waiting
error parsing HTTP 404 response body: invalid character 'p' after top-level value: "404 page not found\n"



# journalctl 명령으로 좀더 상세히 보자.
$ journalctl -fu docker.service
24-03-16T17:53:59.416952880+09:00" level=info msg="Error logging in to endpoint, trying next endpoint" error="Get \"http://nexus-repo.ssongman.duckdns.org:80/v2/\": dial tcp: lookup nexus-repo.ssongman.duckdns.org on 127.0.0.53:53: read udp 127.0.0.1:37423->127.0.0.53:53: i/o timeout"
Mar 16 17:53:59 bastion dockerd[813210]: time="2024-03-16T17:53:59.417288495+09:00" level=error msg="Handler for POST /v1.43/auth returned error: Get \"http://nexus-repo.ssongman.duckdns.org:80/v2/\": dial tcp: lookup nexus-repo.ssongman.duckdns.org on 127.0.0.53:53: read udp 127.0.0.1:37423->127.0.0.53:53: i/o timeout"
Mar 16 17:55:16 bastion dockerd[813210]: time="2024-03-16T17:55:16.797415820+09:00" level=info msg="Error logging in to endpoint, trying next endpoint" error="login attempt to https://nexus-repo.ssongman.duckdns.org:80/v2/ failed with status: 404 Not Found"
Mar 16 17:55:34 bastion dockerd[813210]: time="2024-03-16T17:55:34.853052827+09:00" level=info msg="Error logging in to endpoint, trying next endpoint" error="login attempt to https://nexus-repo.ssongman.duckdns.org:80/v2/ failed with status: 404 Not Found"
Mar 16 18:00:55 bastion dockerd[813210]: time="2024-03-16T18:00:55.820553980+09:00" level=error msg="Upload failed: error parsing HTTP 404 response body: invalid character 'p' after top-level value: \"404 page not found\\n\""
Mar 16 18:00:55 bastion dockerd[813210]: time="2024-03-16T18:00:55.820619693+09:00" level=error msg="Upload failed: error parsing HTTP 404 response body: invalid character 'p' after top-level value: \"404 page not found\\n\""




$ curl https://nexus-repo.ssongman.duckdns.org/v2 -k 

<!DOCTYPE html>
<html lang="en">
<head>
  <title>404 - Sonatype Nexus Repository</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>


  <link rel="icon" type="image/png" href="../../static/rapture/resources/safari-favicon-32x32.png?3.63.0-01" sizes="32x32">
  <link rel="mask-icon" href="../../static/rapture/resources/favicon-white.svg?3.63.0-01" color="#00bb6c">
  <link rel="icon" type="image/png" href="../../static/rapture/resources/favicon.svg?3.63.0-01" sizes="16x16">

  <link rel="stylesheet" type="text/css" href="../../static/css/nexus-content.css?3.63.0-01"/>
</head>
<body>
<div class="nexus-header">
  <a href="../..">
    <div class="product-logo">
      <img src="../../static/rapture/resources/nxrm-reverse-icon.png?3.63.0-01" alt="Product logo"/>
    </div>
    <div class="product-id">
      <div class="product-id__line-1">
        <span class="product-name">Sonatype Nexus Repository</span>
      </div>
      <div class="product-id__line-2">
        <span class="product-spec">OSS 3.63.0-01</span>
      </div>
    </div>
  </a>
</div>

<div class="nexus-body">
  <div class="content-header">
    <img src="../../static/rapture/resources/icons/x32/exclamation.png?3.63.0-01" alt="Exclamation point" aria-role="presentation"/>
    <span class="title">Error 404</span>
    <span class="description">Not Found</span>
  </div>
  <div class="content-body">
    <div class="content-section">
      Not Found
    </div>
  </div>
</div>
</body>
</html>




## 확인
80 포트를 제외하자.  그럼 성공한다.


```



# 6. Image 확인

## 1) brower 에서 확인하는 방법

```sh

http://nexus.ssongman.duckdns.org/#browse/browse:docker-registry

http://nexus.ssongman.duckdns.org/repository/docker-registry/v2/ssongman/userlist/manifests/v1


$ curl --user "dockerpushuser:songpass" http://nexus.ssongman.duckdns.org/service/rest/repository/browse/docker-registry/v2/ssongman/userlist/tags/


<table cellspacing="10">
    <tr>
        <th align="left">Name</th>
        <th>Last Modified</th>
        <th>Size</th>
        <th>Description</th>
    </tr>
        <tr>
            <td><a href="../">Parent Directory</a></td>
        </tr>
        <tr>
            <td><a href="http://nexus.ssongman.duckdns.org/repository/docker-registry/v2/ssongman/userlist/manifests/v1">v1</a></td>
            <td>
                    Sat Mar 16 09:23:52 GMT 2024
            </td>
            <td align="right">
                    2424
            </td>
            <td></td>
        </tr>
        <tr>
            <td><a href="http://nexus.ssongman.duckdns.org/repository/docker-registry/v2/ssongman/userlist/manifests/v1.0.1">v1.0.1</a></td>
            <td>
                    Sat Mar 16 09:47:13 GMT 2024
            </td>
            <td align="right">
                    2424
            </td>
            <td></td>
        </tr>
</table>
</body>
</html>


```





## 2) api 확인

```sh

$ curl --user "dockerpushuser:songpass" \
 http://nexus-repo.ssongman.duckdns.org/v2/_catalog
{"repositories":["ssongman/userlist"]}
 
 



```





# 7. [Client] Docker pull

wsl 에서 docker pull 테스트를 해 보자.



## 1) insecure 등록



## 2) pull

```sh
$ docker pull nexus-repo.ssongman.duckdns.org/ssongman/userlist:v1.0.1

```



