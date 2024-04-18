







# 1. 개요

k3s 에서 insecure registry 에서 imagepull 을 시도해 본다.



참조링크 : https://docs.k3s.io/kr/installation/private-registry



k3s 시작 시 `/etc/rancher/k3s/registries.yaml` 파일이 존재하는지 확인후 존재시 설정작업을 수행한다.



# 2. 기본구성

```yaml
mirrors:
  <REGISTRY>:
    endpoint:
      - https://<REGISTRY>/v2
configs:
  <REGISTRY>:
    auth:
      username: <BASIC AUTH USERNAME>
      password: <BASIC AUTH PASSWORD>
      token: <BEARER TOKEN>
    tls:
      ca_file: <PATH TO SERVER CA>
      cert_file: <PATH TO CLIENT CERT>
      key_file: <PATH TO CLIENT KEY>
      insecure_skip_verify: <SKIP TLS CERT VERIFICATION BOOLEAN>
      
```





### 1) harbor 셋팅



각 node 별로 구성해야 한다.

```sh

# root 계정으로...

$ cat > /etc/rancher/k3s/registries.yaml
---
configs:
  harbor.ssongman.duckdns.org:
    auth:
      username: admin
      password: adminpass
    tls:
      insecure_skip_verify: true
---


```



k3s를 다시 시작하여 /etc/rancher/k3s/registries.yaml의 변경사항을 적용

```sh

## 재시작
$ systemctl restart k3s

## 확인
$ systemctl status k3s

```







## sample deploy



```sh
$ kubectl -n yjsong create deploy userlist-harbor --image=harbor.ssongman.duckdns.org/app/userlist:v1 

# 성공

```

