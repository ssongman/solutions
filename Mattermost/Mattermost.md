

# 1. 개요

Kubernetes 클러스터에 Helm을 사용하여 Mattermost를 설치한다.





# 2. Helm Install

## 1) Mattermost 공식 Helm Chart 추가

```sh

helm repo add mattermost https://helm.mattermost.com
helm repo update

$ helm search repo mattermost

NAME                                            CHART VERSION   APP VERSION     DESCRIPTION
mattermost/mattermost-calls-offloader           0.2.1           0.9.0           A Helm chart for Kubernetes to deploy Mattermos...
mattermost/mattermost-chaos-engine              0.2.0                           A Helm chart for Kubernetes and Mattermost Appl...
mattermost/mattermost-enterprise-edition        2.6.73          10.7.1          Mattermost Enterprise server with high availiti...
mattermost/mattermost-operator                  1.0.2           1.22.0          A Helm chart for Mattermost Operator
mattermost/mattermost-push-proxy                0.14.0          6.3.0           Mattermost Push Proxy server
mattermost/mattermost-rtcd                      1.4.0           latest          A Helm chart for Kubernetes to deploy Mattermos...
mattermost/mattermost-team-edition              6.6.76          10.7.1          Mattermost Team Edition server.
mattermost/focalboard                           0.5.0           0.6.7           Focalboard Server


$ mkdir -p ~/song/mattermost
$ cd ~/song/mattermost

$ helm show values mattermost/mattermost-team-edition > 11.mattermost-values.yaml


```





------



## 2) 설치 옵션 확인



Mattermost의 Helm chart에 설정 가능한 값 확인:

```
helm show values mattermost/mattermost-team-edition > mattermost-values.yaml
```

이 파일을 편집하여 원하는 설정을 적용할 수 있습니다.



------



## 3) 기본 설치 명령어 (테스트용)

```sh

# NS 생성
$ kubectl create ns mattermost


$ helm -n mattermost install mattermost \
    mattermost/mattermost-team-edition \
    --set service.type=ClusterIP \
    --set persistence.data.enabled=false \
    --set persistence.data.size=10Gi \
    --set ingress.enabled=true \
    --set ingress.className=nginx \
    --set ingress.hosts\[0\]=mm.cbiz.kubepia.net \
    --set ingress.tls\[0\].secretName=mattermost-tls \
    --set ingress.tls\[0\].hosts\[0\]=mm.cbiz.kubepia.net \
    --set mysql.enabled=true \
    --set mysql.mysqlUser=ssongman \
    --set mysql.mysqlRootPassword=New1234! \
    --set mysql.mysqlUser=ssongman \
    --set mysql.mysqlPassword=New1234! \
    --set mysql.mysqlDatabase=mattermost \
    --set mysql.persistence.enabled=false \
    --set mysql.persistence.size=10Gi \
    --dry-run=true


NAME: mattermost
LAST DEPLOYED: Wed Apr 30 19:16:01 2025
NAMESPACE: mattermost
STATUS: deployed
REVISION: 1
NOTES:
You can easily connect to the remote instance from your browser. Forward the webserver port to localhost:8065

- kubectl port-forward --namespace mattermost $(kubectl get pods --namespace mattermost -l "app.kubernetes.io/name=mattermost-team-edition,app.kubernetes.io/instance=mattermost" -o jsonpath='{ .items[0].metadata.name }') 8080:8065

Mattermost will be available at the URL, if you setup the nginx-ingress or other type of ingress:

  https://mm.cbiz.kubepia.net
  






$ helm -n mattermost ls


# 삭제시...
$ helm -n mattermost 




```





## 4) 초기 관리자 계정 생성



Mattermost는 최초 접속 시 웹 UI를 통해 직접 관리자 계정을 생성하도록 유도합니다.

```

User: ssongman
Pass: New1234!


```



------



## 5) Ingress Controller 사용



Ingress NGINX 등을 사용하는 경우 mattermost-values.yaml에 다음을 추가:

```

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    kubernetes.io/tls-acme: "true"
    meta.helm.sh/release-name: mattermost
    meta.helm.sh/release-namespace: mattermost
    nginx.ingress.kubernetes.io/ssl-redirect: "true"


ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
  hosts:
    - name: mattermost.example.com
      path: /
  tls:
    - secretName: mattermost-tls
      hosts:
        - mattermost.example.com
```

