# Docker Registry를 위한 Nexus Set





# 1. 개요



참고링크 : https://velog.io/@haerong22/Nexus%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-Docker-Registry



Nexus 주소 : http://nexus.ssongman.duckdns.org





# 2. 





## 1) Blob Store 생성

- Blob Store는 파일들을 저장하는 공간이다.



## 2) Repository 생성

- proxy는 docker hub의 이미지들을 연결하여 사용
- hosted는 서버내에서 이미지 관리
- group은 합쳐서 사용
- 



- 보안상 https를 사용하는 것이 좋다.
- 5000번 포트를 사용
- 



* 접속 url
  * http://nexus.ssongman.duckdns.org/repository/docker-registry/



## 3) Realms

- docker bearer token 활성화





## 4) Docker Registry 로그인



```sh

$ docker login nexus.ssongman.duckdns.org:5000

$ docker login https://nexus.ssongman.duckdns.org:5000/

admin / adminpass




$ docker login http://nexus.ssongman.duckdns.org:5000/repository/docker-registry/

http://nexus.ssongman.duckdns.org:5000/repository/docker-registry/


```



기본적으로 https로 접속하기 때문에 다음과 같은 에러 발생

```sh
Error response from daemon: Get "https://nexus.ssongman.duckdns.org:5000/v2/": dial tcp 59.15.23.41:5000: connect: connection refused


# 위 에러는 5000 port 연결못해서 발생한 문제....

# ingress - server - container 관계를 보면 이해 됨.

```



```sh

$ vi .docker/daemon.json
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
  "insecure-registries": [
    "nexus.ssongman.duckdns.org:5000"
  ]
}


```





```bash
$ sudo vi .docker/daemon.json
{
  "insecure-registries" : ["nexus.ssongman.duckdns.org:5000", "59.15.23.41:5000", "nexus-repo.ssongman.duckdns.org:80"]
}



$ docker info
...
 Insecure Registries:
  nexus-repo.ssongman.duckdns.org:80
  nexus.ssongman.duckdns.org:5000
  59.15.23.41:5000
  127.0.0.0/8
 Live Restore Enabled: false
 
 

```

- docker daemon 재시작(docker desktop 사용 중이라 재시작)

```sh

# flush changes
$ sudo systemctl daemon-reload

# restart docker
$ sudo systemctl restart docker

$ sudo systemctl restart docker.service





# 수작업으로 해보자.

sudo service docker stop
sudo dockerd


sudo dockerd --insecure-registry [nexus.ssongman.duckdns.org:5000] 
sudo dockerd --insecure-registry [nexus.ssongman.duckdns.org:5000] -tls=false


```





### 로그인 다시 시도

```sh

$ docker login nexus-repo.ssongman.duckdns.org:80

Username: admin
Password: 
WARNING! Your password will be stored unencrypted in /home/song/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

```



로그인 성공!



## docker pull/push



```sh


docker pull ssongman/userlist:v1

docker tag ssongman/userlist:v1 nexus-repo.ssongman.duckdns.org:80/ssongman/userlist:v1 

docker push nexus-repo.ssongman.duckdns.org:80/ssongman/userlist:v1 




```













