# < Docker Registry >





# 1. 개요

참고링크 : https://velog.io/@haerong22/Nexus%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-Docker-Registry







# 2. Container Registry 생성

* 접속 url
  * http://nexus.ssongman.duckdns.org/



## 1) Blob Store 생성

- Blob Store는 파일들을 저장하는 공간이다.
- Type
  - File

- Name
  - docker-hosted

- Path
  - 기본




## 2) Repository 생성

- proxy는 docker hub의 이미지들을 연결하여 사용
- hosted는 서버내에서 이미지 관리
- group은 합쳐서 사용



- 보안상 https를 사용하는 것이 좋다.
  - 5000번 포트를 사용



* 접속 url
  * http://nexus.ssongman.duckdns.org/repository/docker-registry/



## 3) Realms 설정

- docker bearer token 활성화





# 3. Registry 계정생성



## 1) 계정명

```
dockerpushuser / songpass

```







# 4. [Client] Docker Registry 로그인



## 1) Ingress 확인



```sh
$ kubectl -n nexus  get ingress
NAME                 CLASS     HOSTS                             ADDRESS                               PORTS   AGE
ingress-nexus        traefik   nexus.ssongman.duckdns.org        172.30.1.31,172.30.1.32,172.30.1.34   80      173d
ingress-nexus-repo   traefik   nexus-repo.ssongman.duckdns.org   172.30.1.31,172.30.1.32,172.30.1.34   80      173d



$ kubectl -n nexus  get ingress ingress-nexus-repo -o yaml
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  labels:
    app: nexus
    release: nexus
  name: ingress-nexus-repo
  namespace: nexus
spec:
  ingressClassName: traefik
  rules:
  - host: nexus-repo.ssongman.duckdns.org
    http:
      paths:
      - backend:
          service:
            name: nexus-repo
            port:
              number: 5000
        path: /
        pathType: Prefix
---

# 서비스
$ kubectl -n nexus  get service
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
nexus        ClusterIP   10.43.27.182   <none>        80/TCP     173d
nexus-repo   ClusterIP   10.43.45.250   <none>        5000/TCP   173d


# 방화벽 확인
$ nc -zv nexus-repo.ssongman.duckdns.org 80
Connection to nexus-repo.ssongman.duckdns.org (59.15.23.41) 80 port [tcp/http] succeeded!

```

* repogitory용도로 생성된  nexus-repo.ssongman.duckdns.org 를 사용한다.





## 2) Docker login



### docker login

```sh

$ docker login nexus-repo.ssongman.duckdns.org

Username: admin
Password:
WARNING! Your password will be stored unencrypted in /home/song/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded



# 아래 위치에 auth 정보가 저장되니 참고하자.
$ cat /home/song/.docker/config.json


$ docker logout nexus-repo.ssongman.duckdns.org


```





### [참고] x509 error 발생한다면 

기본적으로 https로 접속하기 때문에 다음과 같은 에러 발생한다.

아래와 같이 insecure-registres 에 등록해 줘야 한다.

```sh


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
    "nexus-repo.ssongman.duckdns.org"
  ]

}
-----

{
  "insecure-registries" : [
    "nexus-repo.ssongman.duckdns.org:80",
    "nexus-repo.ssongman.duckdns.org"
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







# < Docker Cache >





```sh
nexus.ssongman.duckdns.org
```





# 1. Container Proxy 생성

* 접속 url
  * http://nexus.ssongman.duckdns.org/



## 1) Blob Store 생성

- Blob Store는 파일들을 저장하는 공간이다.
- Type
  - File
- Name
  - docker-hosted
- Path
  - 기본



## 2) Proxy 생성

- proxy는 docker hub의 이미지들을 연결하여 사용
- hosted는 서버내에서 이미지 관리
- group은 합쳐서 사용
- Name
  - docker-proxy

- HTTP
  - 보안상 https를 사용하는 것이 좋다.
  - 5000번 포트를 사용

- Allow anonymous docker pull : check
- v1 : no check
- Proxy
  - Remote storage
    - http://nexus-repo.ssongman.duckdns.org

  - Foreign Layer Cacing : no check
  - Blocked: no check
  - Auto blocking enabled  : no check

- **Storage**
  - Blob store
    - docker-hosted

- http
  - authenctication
    - type : username
    - username : dockerpushuser
    - pass : song****


* 접속 url
  * http://nexus-cache.ssongman.duckdns.org/repository/docker-proxy/
  * repo
    * nexus-cache-repo.ssongman.duckdns.org



## 3) Realms 설정

- docker bearer token 활성화
- 메뉴
  - Configutaion > Security > Realms > `Docker Bearer Token Realm` Active로 이동 > Save






# 2. repo svc/ingress 등록



```sh
$ cd ~/song/nexus

$ cat > 15.nexus-cahe-repo.yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: nexus
  name: nexus-repo
spec:
  ports:
  - port: 5000
    protocol: TCP
    targetPort: 5000
  selector:
    app.kubernetes.io/instance: nxrm-cache
    app.kubernetes.io/name: nexus-repository-manager
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  labels:
    app: nexus
    release: nexus
  name: ingress-nexus-repo
spec:
  ingressClassName: traefik
  rules:
  - host: nexus-cache-repo.ssongman.duckdns.org
    http:
      paths:
      - backend:
          service:
            name: nexus-repo
            port:
              number: 5000
        path: /
        pathType: Prefix
--


$ kubectl -n nexus-cache apply -f 15.nexus-cahe-repo.yaml


```





# 3. [Client] Docker pull

wsl 에서 docker pull 테스트를 해 보자.



## 1) insecure 등록

```sh
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "insecure-registries": [
    "nexus-repo.ssongman.duckdns.org",
    "nexus-cache-repo.ssongman.duckdns.org"
  ]
}

```



## 2) login 확인

```sh
$ docker login nexus-cache-repo.ssongman.duckdns.org

Username: admin
Password:
Login Succeeded


```





## 3) pull

```sh
$ docker rmi nexus-repo.ssongman.duckdns.org/ssongman/userlist:v1.0.1

$ docker images



$ docker pull nexus-cache-repo.ssongman.duckdns.org/ssongman/userlist:v1
# 성공




$ docker pull nexus-cache-repo.ssongman.duckdns.org/ssongman/userlist:v1.0.1

Error response from daemon: received unexpected HTTP status: 502 Bad Gateway

???
```












## docker pull/push



```sh
docker pull ssongman/userlist:v1

docker tag ssongman/userlist:v1 nexus-repo.ssongman.duckdns.org:80/ssongman/userlist:v1 

docker push nexus-repo.ssongman.duckdns.org:80/ssongman/userlist:v1 




```