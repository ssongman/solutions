#  < Harbor >





# 1. 개요

harbor registry install



Harbor는 CNCF를 졸업한 프로젝트로, 대표적인 사설 레지스트리 (Private Registry) 오픈소스이다.



## Private Registry

보통 hub.docker.com에서 제공하거나 오픈소스 프로젝트에서 제공하는 컨테이너 이미지는 인터넷이 되는 모든 곳에서 풀을 받아 사용이 가능하다. 이러한 컨테이너 이미지를 제공해주는 레지스트리를 Public Registry라고 한다.

 

하지만, 회사와 같이 프로젝트가 오픈되지 않아야 하는 환경에서는 회사 환경 내부에서만 접근이 가능해야 하고, 큰 회사의 경우에는 특정 부서에서만 특정 이미지를 푸쉬하거나 풀 할 수 있도록 권한을 제어해야 한다. 이렇게 특정 환경에서만 접근이 가능해야 하는 레지스트리를 Private Registry라고 한다.



Harbor는 대표적인 Private registry 오픈소스이며, 컨테이너 이미지 저장 외에도 여러가지의 기능을 제공하고 있다.

 

- 컨테이너 이미지에 대한 보안 및 취약점 분석
- RBAC (Role based access control)
- 정책 기반 복제 (Replication)
- 여러 방식의 인증기능 제공 (LDAP / AD / OIDC)
- 이미지 삭제 및 가비지 컬렉션을 통해 주기적으로 리소스 확보
- Web 기반의 GUI
- 감사(Audit)기능 제공
- RESTful API 제공
- docker-compose, helm 등 여러가지 배포 방식 제공
- 



관련링크 : [[Docker\] Harbor를 이용한 Private Registry 구축 :: Simple is Beautiful. (tistory.com)](https://smoh.tistory.com/291)







# 2. Harbor Install(helm)



## 1) Namespace

```sh

$ kubectl create ns harbor

```





## 2) Helm install

###  (1) bitnami chart (실패)

```sh


$ helm search repo harbor
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
    
    
######## [nginx tls]
    --set nginx.tls.enabled=true \
    --set nginx.tls.existingSecret=_____ \
      # tls.crt
      # tls.key
      # ca.crt
    
    
    
    

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





#### [참고] helm upgrade 

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





###  (2) harbor chart(성공)

```sh

# helm repo 등록
$ helm repo add harbor https://helm.goharbor.io

$ helm repo update



# 
$ cd ~/song/helm/chart
$ helm search repo harbor

NAME            CHART VERSION   APP VERSION     DESCRIPTION                                       
bitnami/harbor  20.1.2          2.10.0          Harbor is an open source trusted cloud-native r...
harbor/harbor   1.14.0          2.10.0          An open source trusted cloud native registry th...


$ helm fetch harbor/harbor

$ ll
-rw-r--r-- 1 song song 255670 Mar 17 22:48 harbor-1.14.0.tgz

$ tar -xzvf harbor-1.14.0.tgz

$ cd ~/song/helm/charts/harbor


$ helm -n harbor install harbor . \
    --set expose.type=ingress \
    --set expose.tls.enabled=true \
    --set expose.ingress.hosts.core=harbor.ssongman.duckdns.org \
    --set expose.ingress.className=traefik \
    --set externalURL=https://harbor.ssongman.duckdns.org \
    --set persistence.enabled=false \
    --set harborAdminPassword=adminpass \
    --dry-run=true


############################################################
    
######## [nginx tls]
    --set nginx.tls.enabled=true \
    --set nginx.tls.existingSecret=_____ \
      # tls.crt
      # tls.key
      # ca.crt
    

############################################################




NAME: harbor
LAST DEPLOYED: Mon Mar 18 13:48:44 2024
NAMESPACE: harbor
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Please wait for several minutes for Harbor deployment to complete.
Then you should be able to visit the Harbor portal at https://core.harbor.domain
For more details, please visit https://github.com/goharbor/harbor


############################################################

  echo Username: "admin"
  echo Password: $(kubectl -n harbor get secret --namespace harbor harbor-core -o jsonpath="{.data.HARBOR_ADMIN_PASSWORD}" | base64 -d)

Username: admin
Password: adminpass

############################################################


$ helm -n harbor ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
harbor  harbor          1               2024-03-17 23:17:27.369035119 +0900 KST deployed        harbor-20.1.2   2.10.0


# 삭제시...
$ helm -n harbor delete harbor

$ helm -n harbor uninstall harbor



```





### (3) [참고] CA 인증서1



#### 관련링크1

- https://nangman14.tistory.com/78



* 브라우저의 경고를 무시하고 HTTP 접속을 할 수는 있지만 Production 환경에서는 **HTTPS**를 통해 Harbor로 접근하는 것을 권장함

* **self-signed certificate**로 Harbor에 HTTPS 설정 가능





### (4) [참고] CA 인증서2



#### 관련링크2

* https://kyh0703.github.io/install/post-install-harbor/





#### CA Certificates 생성

```sh
$ mkdir -p ~/song/harbor/certs
  cd ~/song/harbor/certs
  
  
# Root CA의 비밀키 생성
$ openssl genrsa -out ca.key 4096

# Root CA의 비밀키와 짝을 이룰 공개키 생성
# * CN은 도메인이나 아이피 입력
$ openssl req -x509 -new -nodes -sha512 -days 3650 \
    -subj "/C=CN/ST=seoul/L=seoul/O=kyh0703/OU=tester/CN=harbor.ssongman.duckdns.org" \
    -key ca.key \
    -out ca.crt
```



#### Server Certificates 생성

```sh
# Server의 비밀키 생성
$ openssl genrsa -out harbor.ssongman.duckdns.org.key 4096

# Server의 CSR 파일 생성
# * CN은 도메인이나 아이피 입력
$ openssl req -sha512 -new \
    -subj "/C=CN/ST=seoul/L=seoul/O=kyh0703/OU=tester/CN=harbor.ssongman.duckdns.org" \
    -key 100.100.103.167.key \
    -out 100.100.103.167.csr
```



#### 인증

```sh
$ cat > v3ext.cnf <<-EOF
subjectAltName = IP:100.100.103.167,IP:127.0.0.1
EOF
```



#### 인증키 생성

```sh
$ openssl x509 -req -sha512 -days 3650 \
    -extfile v3.ext \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -in 100.100.103.167.csr \
    -out 100.100.103.167.crt
```



#### 인증서 복사

```sh
$ sudo mkdir -p /data/cert
$ cp 100.100.103.167.crt /data/cert/
$ cp 100.100.103.167.key /data/cert/
```



#### Cert 파일 생성

```sh
$ openssl x509 -inform PEM -in 100.100.103.167.crt -out 100.100.103.167.cert
```



#### Docker 인증서 복사

```sh
sudo mkdir -p /etc/docker/certs.d/100.100.103.167
cp 100.100.103.167.cert /etc/docker/certs.d/100.100.103.167/
cp 100.100.103.167.key /etc/docker/certs.d/100.100.103.167/
cp ca.crt /etc/docker/certs.d/100.100.103.167/
```

#### 













## 3) 확인



```sh



$ kubectl -n harbor get pod
NAME                                 READY   STATUS    RESTARTS      AGE
harbor-core-7c59bd7465-k6skn         1/1     Running   0             16m
harbor-database-0                    1/1     Running   0             16m
harbor-jobservice-65dd4c87d7-2hshj   1/1     Running   3 (16m ago)   16m
harbor-portal-5d4889f845-q78hb       1/1     Running   0             16m
harbor-redis-0                       1/1     Running   0             16m
harbor-registry-8454dd47c9-476hn     2/2     Running   0             16m
harbor-trivy-0                       1/1     Running   0             16m



$ kubectl -n harbor get svc
NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
harbor-core         ClusterIP   10.43.128.39    <none>        80/TCP              17m
harbor-database     ClusterIP   10.43.96.158    <none>        5432/TCP            17m
harbor-jobservice   ClusterIP   10.43.8.243     <none>        80/TCP              17m
harbor-portal       ClusterIP   10.43.151.22    <none>        80/TCP              17m
harbor-redis        ClusterIP   10.43.220.175   <none>        6379/TCP            17m
harbor-registry     ClusterIP   10.43.144.50    <none>        5000/TCP,8080/TCP   17m
harbor-trivy        ClusterIP   10.43.133.6     <none>        8080/TCP            17m


## curl test 를 위해...
$ kubectl -n yjsong exec -it deploy/userlist -- bash

$ curl http://harbor-core.harbor.svc -i     # 성공
$ curl http://harbor-portal.harbor.svc -i    # 성공



$ echo aGFyYm9yX3JlZ2lzdHJ5X3VzZXI= | base64 -d
harbor_registry_user


$ echo aGFyYm9yX3JlZ2lzdHJ5X3Bhc3N3b3Jk | base64 -d
harbor_registry_password




```







## 4) 접속 url



* 접속 url
  * https://harbor.ssongman.duckdns.org/
* ID/Pass
  * admin / adminpass



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











# 3.[Client] Docker push/pull

bastion 에서 pull / push 해 보자.



## 1) insecure 등록



### (1) login 

```sh

$ docker login https://harbor.ssongman.duckdns.org
Username: admin
Password: 
WARNING! Your password will be stored unencrypted in /home/song/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

```





### [참고] x509 error 발생한다면 

기본적으로 https로 접속하기 때문에 다음과 같은 에러 발생한다.

아래와 같이 insecure-registres 에 등록해 줘야 한다.

```sh

$ docker login harbor.ssongman.duckdns.org/app/userlist:v1
Username: admin
Password: 
Error response from daemon: Get "https://harbor.ssongman.duckdns.org/v2/": tls: failed to verify certificate: x509: certificate signed by unknown authority


# error 내용

Error response from daemon: Get "https://nexus-repo.ssongman.duckdns.org/v2/": tls: failed to verify certificate: x509: certificate is valid for 441717dbb6ed0fbbe78d42337f4e3b55.6562afbd2d52dbbc07e0a02556dc8168.traefik.default, not nexus-repo.ssongman.duckdns.org



$ sudo vi /etc/docker/daemon.json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  },
  "insecure-registries": [                             # <-- 추가
    "nexus-repo.ssongman.duckdns.org:80",
    "nexus-repo.ssongman.duckdns.org",
    "harbor.ssongman.duckdns.org"
  ]

}

```


- docker daemon 재시작


```sh
# flush changes
$ sudo systemctl daemon-reload

# restart docker
$ sudo systemctl restart docker


# 수작업으로 한다면...
sudo service docker stop

# 재기동 옵션
sudo dockerd
sudo dockerd --insecure-registry [nexus.ssongman.duckdns.org:5000] 
sudo dockerd --insecure-registry [nexus.ssongman.duckdns.org:5000] -tls=false

```





## 2) push



### (1) push test

```sh

$ docker pull ssongman/userlist:v1
$ docker pull nginx

$ docker tag ssongman/userlist:v1 harbor.ssongman.duckdns.org/app/userlist:v1
$ docker tag ssongman/userlist:v1 harbor.ssongman.duckdns.org/app/userlist:v1.0.1

$ docker tag nginx harbor.ssongman.duckdns.org/app/nginx



$ docker images
REPOSITORY                                             TAG               IMAGE ID       CREATED         SIZE
ssongman/userlist                                      v1                bf0cd99d0bad   5 years ago     680MB
nexus-repo.ssongman.duckdns.org:80/ssongman/userlist   v1                bf0cd99d0bad   5 years ago     680MB
nexus-repo.ssongman.duckdns.org/ssongman/userlist      v1                bf0cd99d0bad   5 years ago     680MB


$ docker push harbor.ssongman.duckdns.org/app/userlist:v1
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



$ docker push harbor.ssongman.duckdns.org/app/userlist:v1.0.1
The push refers to repository [harbor.ssongman.duckdns.org/app/userlist]
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





$ docker push harbor.ssongman.duckdns.org/app/nginx



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





## 3) pull



```sh


# 확인
$ docker images
REPOSITORY                                             TAG               IMAGE ID       CREATED         SIZE
ssongman/userlist                                      v1                bf0cd99d0bad   5 years ago     680MB
harbor.ssongman.duckdns.org/app/userlist               v1                bf0cd99d0bad   5 years ago     680MB
harbor.ssongman.duckdns.org/app/userlist               v1.0.1            bf0cd99d0bad   5 years ago     680MB


# 존재하는 image 삭제
$ docker rmi harbor.ssongman.duckdns.org/app/userlist:v1
$ docker rmi harbor.ssongman.duckdns.org/app/userlist:v1.0.1


# image pull
$ docker pull harbor.ssongman.duckdns.org/app/userlist:v1.0.1
$ docker pull harbor.ssongman.duckdns.org/app/userlist:v1
$ docker pull harbor.ssongman.duckdns.org/app/nginx



# 확인
$ docker images
REPOSITORY                                             TAG               IMAGE ID       CREATED         SIZE
harbor.ssongman.duckdns.org/app/userlist               v1                bf0cd99d0bad   5 years ago     680MB
harbor.ssongman.duckdns.org/app/userlist               v1.0.1            bf0cd99d0bad   5 years ago     680MB

```











# 4. Harbor OCI helm registry



## 1) helm command sample

### sample

```sh

$ helm version
version.BuildInfo{Version:"v3.12.0", GitCommit:"c9f554d75773799f72ceef38c51210f1842a1dea", GitTreeState:"clean", GoVersion:"go1.20.3"}


$ helm repo add --ca-file ca.crt --username=admin --password=Passw0rd myrepo https://xx.xx.xx.xx/chartrepo

$ helm repo add --ca-file ca.crt --username=admin --password=Passw0rd myrepo https://xx.xx.xx.xx/chartrepo/myproject

$ helm plugin install https://github.com/chartmuseum/helm-push

$ helm install --ca-file=ca.crt --username=admin --password=Passw0rd --version 0.1.10 repo248/chart_repo/hello-helm

```





## 2) helm pull/push



### smaple(nginx) pull

```sh

$ cd ~/song/del

$ helm pull nginx \
  --version 15.14.0 \
  --repo https://charts.bitnami.com/bitnami/


$ cd ~/song/del
$ ll
-rw-r--r--  1 song song 45460 Mar 20 17:59 nginx-15.14.0.tgz

```



### login / push

```sh

$ helm registry login -u admin https://harbor.ssongman.duckdns.org --ca-file ca.crt 


# helm push [chart] [remote] [flags]

# push
$ ll
-rw-r--r--  1 song song 45460 Mar 20 17:59 nginx-15.14.0.tgz


$ helm push nginx-15.14.0.tgz oci://harbor.ssongman.duckdns.org/charts/ --ca-file ca.crt 


```





### repo add

```sh
$ helm version
version.BuildInfo{Version:"v3.12.0", GitCommit:"c9f554d75773799f72ceef38c51210f1842a1dea", GitTreeState:"clean", GoVersion:"go1.20.3"}


# repo 등록1
$ helm repo add \
    --ca-file ca.crt \
    --username=admin \
    --password=adminpass \
    ssongmanrepo \
    oci://harbor.ssongman.duckdns.org/charts/

# repo 등록2
$ helm repo add \
    --ca-file ca.crt \
    ssongmanrepo \
    https://harbor.ssongman.duckdns.org/charts

```





### package

```sh

# Chart.yaml의 이름 및 버전을 사용하여 파일로 저장
$ helm package .

```





### ca.crt

harbor에서 다운로드 가능

```sh

$ cd ~/song/del/ca.crt

-----BEGIN CERTIFICATE-----
MIIDFDCCAfygAwIBAgIRAOumWyTpE2lUFu2iv4kFo+UwDQYJKoZIhvcNAQELBQAw
FDESMBAGA1UEAxMJaGFyYm9yLWNhMB4XDTI0MDMxODA1MzE0N1oXDTI1MDMxODA1
MzE0N1owFDESMBAGA1UEAxMJaGFyYm9yLWNhMIIBIjANBgkqhkiG9w0BAQEFAAOC
AQ8AMIIBCgKCAQEAtMaFw1rECrdmNx2y70AoZVIWa+0pBHKfkhFjxZ0eZMN0YBib
cKdh/XmLloPOW3bSNhfc+Mb8EQxcFYRiyhS5RgIZPdNWoVZivicJUE3YBMfUV35G
yhtDAEkSSr2xVUsd8Nd1+bq4rf08tPnTU7DO2g44WekabVAD7jn709+XSGWd5ROz
cdn3RGu0WZN7eGMgnCz7PM6P9CgD8xvrjlP4DtcK077LwiMx5Kpu2M+8KQwr2Bvi
tvQuVvFZrjWuhTDKohBPZHMg+299IIxwoKP8tIKfp93ZjzL5dn3lBLlrRTm/qV+7
Rwe14hNDXQf21FYhAzvKSapAVRvG8eF2FXdzGwIDAQABo2EwXzAOBgNVHQ8BAf8E
BAMCAqQwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMA8GA1UdEwEB/wQF
MAMBAf8wHQYDVR0OBBYEFEZjplQoEJUehGDsGRtCMS+z/P7DMA0GCSqGSIb3DQEB
CwUAA4IBAQCzmwSfCHiounaAc4rdpj8iHGjuKiMzebta+CINX9GYQn4qgc7VHwD/
ec1Vnc2dP7yYkcgkjt9s6pQwyPe/+vPkNWCVCc066iFATEieshY8XRPraerRD99D
/lYEwY2mEazWfxCQN/OAb/6t/snqLNrY5R2dRRbhYIMBe3dUYs4O5U/uhQqQ11Hf
ky8wr9W5O6MT7CTyMNW8q/7J/BXpZ7YrSGh+u731gMXDcBCvp7aPP+BZif1CK659
Zgv/2IS942Eij11laVoWwDmE6QIT4d9py2MuyLfgLPLznz2/3K7mQo9Wa0Oqrvnm
enWIlpIQ4mRSnbaxl3mrwqPA6/HjfJiS
-----END CERTIFICATE-----


```



















# 5. Proxy Cache 설정

## 1) 설정

### endpoint 설정

### cache 용 project 설정





## 2) pull test



```sh


$ docker pull harbor.ssongman.duckdns.org/app2/userlist:v1.0.1

Error response from daemon: unknown: resource not found: repo app2/userlist, tag v1 not found
Error response from daemon: Head "https://harbor.ssongman.duckdns.org/v2/app2/userlist/manifests/v1.0.1": Get "https://harbor.ssongman.duckdns.org/service/token?account=admin&scope=repository%3Aapp2%2Fuserlist%3Apull&service=harbor-registry": dial tcp: lookup harbor.ssongman.duckdns.org on 127.0.0.53:53: read udp 127.0.0.1:53994->127.0.0.53:53: i/o timeout


-------


$ docker pull harbor.ssongman.duckdns.org/ssongman/userlist:v1.0.1
Error response from daemon: unknown: resource not found: repo ssongman/userlist, tag v1.0.1 not found


$ docker pull harbor.ssongman.duckdns.org/ssongman/userlist:v1
Error response from daemon: unknown: resource not found: repo ssongman/userlist, tag v1 not found






```







# 6. Image 확인

## 1) brower 에서 확인하는 방법

```sh

http://nexus.ssongman.duckdns.org/#browse/browse:docker-registry

http://nexus.ssongman.duckdns.org/repository/docker-registry/v2/ssongman/userlist/manifests/v1


$ curl --user "dockerpushuser:songpass" \
    http://nexus.ssongman.duckdns.org/service/rest/repository/browse/docker-registry/v2/ssongman/userlist/tags/


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

$ curl --user "admin:adminpass" \
     https://harbor.ssongman.duckdns.org/v2/_catalog -k
     
{"repositories":["ssongman/userlist"]}
 


# http 도 잘 된다.
$ curl --user "admin:adminpass" \
     http://harbor.ssongman.duckdns.org/v2/_catalog
{"repositories":["ssongman/userlist"]}
     
```









# 7. kubernetes pull



## 1) pull-image-private-registry 등록

https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/



```sh
$ kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson


```



secret 등록

```sh
apiVersion: v1
kind: Secret
metadata:
  name: myregistrykey
  namespace: awesomeapps
data:
  .dockerconfigjson: UmVhbGx5IHJlYWxseSByZWVlZWVlZWVlZWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGx5eXl5eXl5eXl5eXl5eXl5eXl5eSBsbGxsbGxsbGxsbGxsbG9vb29vb29vb29vb29vb29vb29vb29vb29vb25ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubmdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cgYXV0aCBrZXlzCg==
type: kubernetes.io/dockerconfigjson

```









# 11. Module 검증

maven module Upload/Download 가능여부를 확인한다.



### [참고] 

* git

  * gitops
    * https://gitlab.dspace.kt.co.kr/icis/sa/cmmn-lib/icis-sa-cmmn-lib-gitops-dev.git
  * module sample
    * https://gitlab.dspace.kt.co.kr/icis/sa/cmmn-lib/icis-cmmn-frwk-core

* jenkins 

  * https://jenkins.sit.icis.kt.co.kr/job/icis-sa-cmmn-lib-rel/job/icis-sa-cmmn-lib-frwk-core/configure

    



#### jenkins build pipeline sample

```groovy


def moduleBuildOnlyJar(version){
	return """
		
		cd ${P_PRJ_NM}
		
		mvn clean install -Drevision="""+version+""" --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
		ls target
		mvn -X deploy:deploy-file -DgroupId=com.kt.icis -DartifactId=${P_PRJ_NM} -Dversion="""+version+""" -Dpackaging=jar -DgeneratePom=false -Dfile=target/${P_PRJ_NM}-"""+version+""".jar -Durl=http://nexus.dev.icis.kt.co.kr/repository/common-repository -DrepositoryId=common-lib --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
	"""
}

```





#### pom.xml sample

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		 xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.6.6</version>
		<relativePath/> <!-- lookup parent from repository -->
	</parent>

	<groupId>com.kt.icis</groupId>
	<artifactId>icis-cmmn-frwk</artifactId>
	<version>${revision}</version>
	<name>icis-cmmn-frwk</name>
	<description>ICISTR Core project</description>
	<properties>
		<revision>0.0.9-SNAPSHOT</revision>
		<java.version>17</java.version>
		<deploy.path>../deploy</deploy.path>
		<spring-cloud.version>2021.0.0</spring-cloud.version>
	</properties>
	<dependencies>
		<dependency>
			<groupId>org.projectlombok</groupId>
			<artifactId>lombok</artifactId>
			<optional>true</optional>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-web</artifactId>
			<exclusions>
				<exclusion>
					<groupId>org.springframework.boot</groupId>
					<artifactId>spring-boot-starter-logging</artifactId>
				</exclusion>
				<exclusion>
					<groupId>ch.qos.logback</groupId>
					<artifactId>logback-classic</artifactId>
				</exclusion>
				<exclusion>
					<groupId>ch.qos.logback</groupId>
					<artifactId>logback-core</artifactId>
				</exclusion>
			</exclusions>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-aop</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.integration</groupId>
			<artifactId>spring-integration-core</artifactId>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-log4j2</artifactId>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-data-jdbc</artifactId>
		</dependency>

		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-data-redis</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-openfeign</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-configuration-processor</artifactId>
			<optional>true</optional>
		</dependency>
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-lang3</artifactId>
			<version>3.12.0</version>
		</dependency>
		<dependency>
			<groupId>commons-io</groupId>
			<artifactId>commons-io</artifactId>
			<version>2.11.0</version>
		</dependency>
		<dependency>
			<groupId>com.google.guava</groupId>
			<artifactId>guava</artifactId>
			<version>31.1-jre</version>
		</dependency>
		<dependency>
			<groupId>kt.hmac.sa</groupId>
			<artifactId>security-cbc-hmac</artifactId>
			<version>1.0.0</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/security-cbc-hmac.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>kt.com.util.TA256</groupId>
			<artifactId>TA256</artifactId>
			<version>1.0.0</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/TA256.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>org.apache.xmlbeans</groupId>
			<artifactId>xmlbeans</artifactId>
			<version>5.0.3</version>
		</dependency>
		<dependency>
			<groupId>org.jdom</groupId>
			<artifactId>jdom2</artifactId>
		</dependency>
		<dependency>
			<groupId>com.kt.nbss.esb.meta</groupId>
			<artifactId>esbMeta</artifactId>
			<version>RELEASE</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/KT_NBSS_ESB_META.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>com.kt.nbss.esb.meta</groupId>
			<artifactId>ESBMetaSchemas</artifactId>
			<version>RELEASE</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/ESBMetaSchemas.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>ktf.sso</groupId>
			<artifactId>ssocommon</artifactId>
			<version>RELEASE</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/ssocommon.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>org.jetbrains</groupId>
			<artifactId>annotations</artifactId>
			<version>RELEASE</version>
			<scope>compile</scope>
		</dependency>
		<dependency>
			<groupId>jakarta.xml.bind</groupId>
			<artifactId>jakarta.xml.bind-api</artifactId>
		</dependency>
		<dependency>
			<groupId>org.bouncycastle</groupId>
			<artifactId>bcprov-jdk15on</artifactId>
			<version>1.68</version>
		</dependency>
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.hamcrest</groupId>
			<artifactId>hamcrest</artifactId>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.junit.vintage</groupId>
			<artifactId>junit-vintage-engine</artifactId>
			<scope>test</scope>
		</dependency>

		<dependency>
			<groupId>org.springdoc</groupId>
			<artifactId>springdoc-openapi-ui</artifactId>
			<version>1.6.6</version>
		</dependency>

		<dependency>
			<groupId>com.fasterxml.jackson.dataformat</groupId>
			<artifactId>jackson-dataformat-xml</artifactId>
			<version>2.13.1</version>
		</dependency>

		<!-- For SafeDB SDK : S -->
		<dependency>
			<groupId>commons-beanutils</groupId>
			<artifactId>commons-beanutils</artifactId>
			<version>1.7.0</version>
		</dependency>
		<dependency>
			<groupId>commons-logging</groupId>
			<artifactId>commons-logging</artifactId>
			<version>1.1</version>
		</dependency>
		<dependency>
			<groupId>net.sf.ezmorph</groupId>
			<artifactId>ezmorph</artifactId>
			<version>1.0.6</version>
		</dependency>
		<dependency>
			<groupId>net.sf.json-lib</groupId>
			<artifactId>json-lib</artifactId>
			<version>2.4</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/json-lib-2.4.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>org.apache.xerces</groupId>
			<artifactId>xercesImpl</artifactId>
			<version>2.9.1</version>
			<scope>runtime</scope>
		</dependency>
		<dependency>
			<groupId>xml-apis</groupId>
			<artifactId>xml-apis</artifactId>
			<version>1.4.01</version>
		</dependency>

		<dependency>
			<groupId>com.initech</groupId>
			<artifactId>INICrypto</artifactId>
			<version>4.1.16</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/INICrypto_v4.1.16.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>com.initech</groupId>
			<artifactId>INISAFECore</artifactId>
			<version>2.2.12</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/INISAFECore_v2.2.12.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>com.initech.inisafent</groupId>
			<artifactId>INISAFENet</artifactId>
			<version>7.2.44</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/INISAFENet_v7.2.44_NS.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>com.initech</groupId>
			<artifactId>INISAFEPKI</artifactId>
			<version>1.1.29</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/INISAFEPKI_v1.1.29.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>com.initech.safedb.core</groupId>
			<artifactId>SafeDBCore</artifactId>
			<version>3.2.19</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/SafeDBCore_v3.2.19.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>com.initech.safedb.crypto</groupId>
			<artifactId>SafeDBCrypto</artifactId>
			<version>3.2.19</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/SafeDBCrypto_v3.2.19.jar</systemPath>
		</dependency>
		<dependency>
			<groupId>com.initech.safedb</groupId>
			<artifactId>SafeDBSDK</artifactId>
			<version>3.2.19</version>
			<scope>system</scope>
			<systemPath>${basedir}/lib/SafeDBSDK_v3.2.19.jar</systemPath>
		</dependency>
		<!-- // For SafeDB SDK : E -->

	</dependencies>

	<dependencyManagement>
		<dependencies>
			<dependency>
				<groupId>org.springframework.cloud</groupId>
				<artifactId>spring-cloud-dependencies</artifactId>
				<version>${spring-cloud.version}</version>
				<type>pom</type>
				<scope>import</scope>
			</dependency>
		</dependencies>
	</dependencyManagement>

	<build>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-assembly-plugin</artifactId>
				<version>3.3.0</version>
				<configuration>
					<descriptorRefs>
						<descriptorRef>jar-with-dependencies</descriptorRef>
					</descriptorRefs>
					<finalName>icis-cmmn-frwk-0.0.9-SNAPSHOT.jar</finalName>
				</configuration>
				<executions>
					<execution>
						<phase>package</phase>
						<goals>
							<goal>single</goal>
						</goals>
					</execution>
				</executions>
			</plugin>
		</plugins>
	</build>


</project>

```





# 21. Harbor API



```
Base URL: harbor.ssongman.duckdns.org/api/v2.0
```





### projects list

```bash
$ curl -X 'GET' \
  'https://harbor.ssongman.duckdns.org/api/v2.0/projects?page=1&page_size=10&with_detail=true' \
  -H 'accept: application/json'

[
  {
    "creation_time": "2024-03-18T05:32:51.436Z",
    "current_user_role_id": 1,
    "current_user_role_ids": [
      1
    ],
    "cve_allowlist": {
      "creation_time": "0001-01-01T00:00:00.000Z",
      "id": 2,
      "items": [],
      "project_id": 2,
      "update_time": "0001-01-01T00:00:00.000Z"
    },
    "metadata": {
      "public": "false"
    },
    "name": "app",
    "owner_id": 1,
    "owner_name": "admin",
    "project_id": 2,
    "repo_count": 2,
    "update_time": "2024-03-18T05:32:51.436Z"
  },
  {
    "creation_time": "2024-03-18T06:08:50.415Z",
    "current_user_role_id": 1,
    "current_user_role_ids": [
      1
    ],
    "cve_allowlist": {
      "creation_time": "0001-01-01T00:00:00.000Z",
      "id": 3,
      "items": [],
      "project_id": 3,
      "update_time": "0001-01-01T00:00:00.000Z"
    },
    "metadata": {
      "public": "true",
      "retention_id": "1"
    },
    "name": "app2",
    "owner_id": 1,
    "owner_name": "admin",
    "project_id": 3,
    "registry_id": 1,
    "repo_count": 0,
    "update_time": "2024-03-18T06:08:50.415Z"
  },
 ---
```





### Project infomation

```sh


$ curl -X 'GET' \
  'https://harbor.ssongman.duckdns.org/api/v2.0/projects/app' \
  -H 'accept: application/json' \
  -H 'X-Is-Resource-Name: false'

{
  "creation_time": "2024-03-18T05:32:51.436Z",
  "current_user_role_id": 1,
  "current_user_role_ids": [
    1
  ],
  "cve_allowlist": {
    "creation_time": "0001-01-01T00:00:00.000Z",
    "id": 2,
    "items": [],
    "project_id": 2,
    "update_time": "0001-01-01T00:00:00.000Z"
  },
  "metadata": {
    "public": "false"
  },
  "name": "app",
  "owner_id": 1,
  "owner_name": "admin",
  "project_id": 2,
  "repo_count": 2,
  "update_time": "2024-03-18T05:32:51.436Z"
}



```



### Repository 목록

```sh

$ curl -X 'GET' \
  'https://harbor.ssongman.duckdns.org/api/v2.0/projects/app/repositories?page=1&page_size=10' \
  -H 'accept: application/json'


[
  {
    "artifact_count": 1,
    "creation_time": "2024-03-22T06:04:51.135Z",
    "id": 3,
    "name": "app/nginx",
    "project_id": 2,
    "pull_count": 1,
    "update_time": "2024-03-22T06:14:20.895Z"
  },
  {
    "artifact_count": 1,
    "creation_time": "2024-03-18T05:35:37.274Z",
    "id": 1,
    "name": "app/userlist",
    "project_id": 2,
    "pull_count": 2,
    "update_time": "2024-03-18T05:44:15.328Z"
  }
]

```









### arifact info

```sh

$ curl -X 'GET' \
  'https://harbor.ssongman.duckdns.org/api/v2.0/projects/app/repositories/userlist/artifacts?page=1&page_size=10&with_tag=true&with_label=false&with_scan_overview=false&with_signature=false&with_immutable_status=false&with_accessory=false' \
  -H 'accept: application/json' \
  -H 'X-Accept-Vulnerabilities: application/vnd.security.vulnerability.report; version=1.1, application/vnd.scanner.adapter.vuln.report.harbor+json; version=1.0'

[
  {
    "accessories": null,
    "addition_links": {
      "build_history": {
        "absolute": false,
        "href": "/api/v2.0/projects/app/repositories/userlist/artifacts/sha256:b0d5a3b6022623b71f09b866a8d612d71118ff9de54c966db91d900c03b31bcc/additions/build_history"
      },
      "vulnerabilities": {
        "absolute": false,
        "href": "/api/v2.0/projects/app/repositories/userlist/artifacts/sha256:b0d5a3b6022623b71f09b866a8d612d71118ff9de54c966db91d900c03b31bcc/additions/vulnerabilities"
      }
    },
    "digest": "sha256:b0d5a3b6022623b71f09b866a8d612d71118ff9de54c966db91d900c03b31bcc",
    "extra_attrs": {
      "architecture": "amd64",
      "author": "ssongmantop@gmail.com",
      "config": {
        "ArgsEscaped": true,
        "Cmd": [
          "/bin/sh",
          "-c",
          "java -jar UserList.jar"
        ],
        "Env": [
          "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
          "LANG=C.UTF-8",
          "JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64",
          "JAVA_VERSION=8u111",
          "JAVA_DEBIAN_VERSION=8u111-b14-2~bpo8+1",
          "CA_CERTIFICATES_JAVA_VERSION=20140324"
        ],
        "ExposedPorts": {
          "8181/tcp": {}
        },
        "WorkingDir": "/usr/src/app"
      },
      "created": "2018-11-13T00:22:52.621679073Z",
      "os": "linux"
    },
    "icon": "sha256:0048162a053eef4d4ce3fe7518615bef084403614f8bca43b40ae2e762e11e06",
    "id": 1,
    "labels": null,
    "manifest_media_type": "application/vnd.docker.distribution.manifest.v2+json",
    "media_type": "application/vnd.docker.container.image.v1+json",
    "project_id": 2,
    "pull_time": "2024-03-18T05:44:06.564Z",
    "push_time": "2024-03-18T05:35:37.352Z",
    "references": null,
    "repository_id": 1,
    "size": 280958537,
    "tags": [
      {
        "artifact_id": 1,
        "id": 1,
        "immutable": false,
        "name": "v1",
        "pull_time": "0001-01-01T00:00:00.000Z",
        "push_time": "2024-03-18T05:35:37.488Z",
        "repository_id": 1
      }
    ],
    "type": "IMAGE"
  }
]
    
  
```





### arifact reference

```sh

```





### arifact tags

```sh

$ curl -X 'GET' \
  'https://harbor.ssongman.duckdns.org/api/v2.0/projects/app/repositories/userlist/artifacts/v1/tags?page=1&page_size=10&with_signature=false&with_immutable_status=false' \
  -H 'accept: application/json'
  

[
  {
    "artifact_id": 1,
    "id": 5,
    "immutable": false,
    "name": "v1.0.1",
    "pull_time": "0001-01-01T00:00:00.000Z",
    "push_time": "2024-03-22T10:30:44.210Z",
    "repository_id": 1
  },
  {
    "artifact_id": 1,
    "id": 1,
    "immutable": false,
    "name": "v1",
    "pull_time": "0001-01-01T00:00:00.000Z",
    "push_time": "2024-03-18T05:35:37.488Z",
    "repository_id": 1
  }
]
```









### arifact tags delete



```sh


$ curl -X 'DELETE' \
  'https://harbor.ssongman.duckdns.org/api/v2.0/projects/app/repositories/userlist/artifacts/v1.0.1/tags/v1.0.1' \
  -H 'accept: application/json' \
  -H 'X-Harbor-CSRF-Token: aNgxQDn6kcRhcDMCnzKRyiTBzsnhVKUL+hifurX3N5Vp6CHB03P5jE7N7XmQX+9svNwG96bF9/cTkIJaq2X1hw=='
  

OK
 content-length: 0 
 date: Fri,22 Mar 2024 10:38:16 GMT 
 vary: Cookie 
 x-harbor-csrf-token: ffkuGMZBdK8/48IImNqqRvkV6ykD7klHKle5YonQpfF8yT6ZLMgc5xBeHHOXt9TgYQgjF0R/G7vD36SCl0Jn4w== 
 x-request-id: f3d3eacd-3428-4379-8f7c-b7545e7be513 
 

```



