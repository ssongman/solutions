# gitlab ce install



# 1. 개요

helm chart 를 이용하여 gitlab 을 설치한다.



## 1) gitaly  사용

gitaly 란? Git 레파지토리에 대한 RPC 기반의 빠른 읽기쓰기를 가능하게 하느느 오픈소스임

Gitaly 노드를 포함시 Git 레파지토리는 클러스터의 모든 노드에 저장됨. 노드 하나가 중단되면 다른 노드로 인계되어서 사용됨.

Git 레파지토리가 A-A 로 이중화된 솔루션으로 안정적으로 유지될 수 있다.





# 2. public 환경



## 1) helm fetch

```sh

$ helm repo list

## helm repo add
$ helm repo add gitlab https://charts.gitlab.io/

$ helm repo add gitlab https://charts.gitlab.io/ --insecure-skip-tls-verify


## helm repo update
$ helm repo update


$ helm search repo gitlab
NAME                            CHART VERSION   APP VERSION     DESCRIPTION
gitlab/gitlab                   7.7.0           v16.7.0         GitLab is the most comprehensive AI-powered Dev...
gitlab/gitlab-agent             1.22.0          v16.7.0         GitLab Agent for Kubernetes is a way to integra...
gitlab/gitlab-omnibus           0.1.37                          GitLab Omnibus all-in-one bundle
gitlab/gitlab-runner            0.60.0          16.7.0          GitLab Runner
gitlab/gitlab-zoekt             1.0.0           0.2.0           A Helm chart for deploying Zoekt as a search en...
gitlab/kubernetes-gitlab-demo   0.1.29                          GitLab running on Kubernetes suitable for demos
gitlab/apparmor                 0.2.0           0.1.0           AppArmor profile loader for Kubernetes
gitlab/auto-deploy-app          0.8.1                           GitLab's Auto-deploy Helm Chart
gitlab/elastic-stack            3.0.0           7.6.2           A Helm chart for Elastic Stack
gitlab/fluentd-elasticsearch    6.2.8           2.8.0           A Fluentd Helm chart for Kubernetes with Elasti...
gitlab/knative                  0.10.0          0.9.0           A Helm chart for Knative
gitlab/plantuml                 0.1.17          1.0             PlantUML server




# 안되면 직접 git clone 해야 한다.
# $ git config --global http.sslVerify false
# $ git clone https://gitlab.com/helmcharts2/gitlab

  
  
$ ~/song/helm/gitlab

$ helm fetch gitlab/gitlab


$ tar -xzvf gitlab-7.7.0.tgz


```





## 2) helm install

### (1) install

```sh

$ helm -n gitlab ls 

$ cd ~/song/helm/gitlab
$ helm -n gitlab install gitlab . \
  --timeout 600s \
  --set certmanager-issuer.email=ssongmantop@gmail.com \
  --set global.edition=ce \
  --set global.hosts.https=false \
  --set global.hosts.gitlab.name=gitlab16.ssongman.duckdns.org \
  --set global.hosts.gitlab.https=false            \
  --set global.ingress.provider=traefik            \
  --set global.ingress.class=traefik               \
  --set global.ingress.tls.enabled=false           \
  --set global.gitaly.enabled=true             \
  --set global.minio.enabled=false                 \
  --set global.kas.enabled=false                   \
  --set global.registry.enabled=false              \
  --set global.appConfig.lfs.enabled=false         \
  --set global.appConfig.artifacts.enabled=false   \
  --set global.appConfig.uploads.enabled=false     \
  --set global.appConfig.packages.enabled=false    \
  --set upgradeCheck.enabled=false                 \
  --set certmanager.install=false                  \
  --set certmanager.installCRDs=false              \
  --set nginx-ingress.enabled=false                \
  --set prometheus.install=false                   \
  --set gitlab-runner.install=false                \
  --set gitlab.toolbox.enabled=false               \
  --set gitlab.gitlab-runner.enabled=false         \
  --set gitlab.gitlab-exporter.enabled=false       \
  --set gitlab.gitlab-shell.enabled=false          \
  --set gitlab.sidekiq.enabled=false               \
  --set gitlab.migrations.enabled=true             \
  --set gitlab.gitaly.global.gitaly.enabled=false  \
  --set registry.enabled=false \
  --dry-run=true > dry-run_01.yaml
  
---


NAME: gitlab
LAST DEPLOYED: Wed Jan 10 00:37:03 2024
NAMESPACE: gitlab
STATUS: deployed
REVISION: 1
NOTES:
=== CRITICAL
The following charts are included for evaluation purposes only. They will not be supported by GitLab Support
for production workloads. Use Cloud Native Hybrid deployments for production. For more information visit
https://docs.gitlab.com/charts/installation/index.html#use-the-reference-architectures.
- PostgreSQL
- Redis
- Gitaly

=== NOTICE
The minimum required version of PostgreSQL is now 13. See https://gitlab.com/gitlab-org/charts/gitlab/-/blob/master/doc/installation/upgrade.md for more details.
Help us improve the installation experience, let us know how we did with a 1 minute survey:https://gitlab.fra1.qualtrics.com/jfe/form/SV_6kVqZANThUQ1bZb?installation=helm&release=1                      6-7

  
  
```





### (2) upgrade install

```sh
$ helm -n gitlab ls 

$ helm -n gitlab upgrade --install gitlab . \
  --timeout 600s \
  --set certmanager-issuer.email=ssongmantop@gmail.com \
  --set global.edition=ce \
  --set global.hosts.https=false \
  --set global.hosts.gitlab.name=gitlab16.ssongman.duckdns.org \
  --set global.hosts.gitlab.https=false            \
  --set global.ingress.provider=traefik            \
  --set global.ingress.class=traefik               \
  --set global.ingress.tls.enabled=false           \
  --set global.gitaly.enabled=true             \
  --set global.minio.enabled=false                 \
  --set global.kas.enabled=false                   \
  --set global.registry.enabled=false              \
  --set global.appConfig.lfs.enabled=false         \
  --set global.appConfig.artifacts.enabled=false   \
  --set global.appConfig.uploads.enabled=false     \
  --set global.appConfig.packages.enabled=false    \
  --set upgradeCheck.enabled=false                 \
  --set certmanager.install=false                  \
  --set certmanager.installCRDs=false              \
  --set nginx-ingress.enabled=false                \
  --set prometheus.install=false                   \
  --set gitlab-runner.install=false                \
  --set gitlab.toolbox.enabled=false               \
  --set gitlab.gitlab-runner.enabled=false         \
  --set gitlab.gitlab-exporter.enabled=false       \
  --set gitlab.gitlab-shell.enabled=false          \
  --set gitlab.sidekiq.enabled=false               \
  --set gitlab.gitaly.global.gitaly.enabled=false \
  --set registry.enabled=false \
  --dry-run=true
  
  #--set gitlab.migrations.enabled=false            \
  
---


$ helm -n gitlab list
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
gitlab  gitlab          2               2024-01-10 00:54:07.695846165 +0900 KST deployed        gitlab-7.7.0    v16.7.0



```











## 3) 첫 로그인

### (1) URL

```
http://gitlab16.ssongman.duckdns.org


```







### (2) 인증정보

* 초기 패스워드 확인 및 변경

```sh

$ kubectl -n gitlab-system get secret gitlab-gitlab-initial-root-password

NAME                                  TYPE     DATA   AGE
gitlab-gitlab-initial-root-password   Opaque   1      3m41s

---

# secret 에서 확인
$ echo OEh0S3RrWVhQZmtua3dtMk9SUzl2MTlwUk9zUXpJbVFtUzR4UkZuNXVvSDdaY1drVXVsc0pCZHRKdFZpMzBhWg== | base64 -d
8HtKtkYXPfknkwm2ORS9v19pROsQzImQmS4xRFn5uoH7ZcWkUulsJBdtJtVi30aZ
----


user : root 
password: 8HtKtkYXPfknkwm2ORS9v19pROsQzImQmS4xRFn5uoH7ZcWkUulsJBdtJtVi30aZ


# password 변경
# 메뉴 : User Settings > Edit Password
login : root
password: new****!


```







## 4) 초기 설정 작업

### (1) Sign-up restrictions

사용자들이 마음대로 등록하지 못하도록 설정해야 함

* 메뉴 : Settings > Admin Area > General

* 항목 : Sign-up enabled  false











# 3. private 환경

좀 복잡하다.



## 1) dry-run

```sh
$ helm -n gitlab-system ls 

$ cd ~/song/helm/charts/gitlab

$ helm -n gitlab-system install gitlab . \
  --timeout 600s \
  --set certmanager-issuer.email=ssongmantop@gmail.com \
  --set global.edition=ce \
  --set global.hosts.https=false \
  --set global.hosts.gitlab.name=gitlab.dev.icis.kt.co.kr \
  --set global.hosts.gitlab.https=false            \
  --set global.ingress.provider=traefik            \
  --set global.ingress.class=traefik               \
  --set global.ingress.tls.enabled=false           \
  --set global.gitaly.enabled=true                 \
  --set global.minio.enabled=false                 \
  --set global.kas.enabled=false                   \
  --set global.registry.enabled=false              \
  --set global.appConfig.lfs.enabled=false         \
  --set global.appConfig.artifacts.enabled=false   \
  --set global.appConfig.uploads.enabled=false     \
  --set global.appConfig.packages.enabled=false    \
  --set global.image.registry=nexus.dspace.kt.co.kr    \
  --set upgradeCheck.enabled=false                 \
  --set certmanager.install=false                  \
  --set certmanager.installCRDs=false              \
  --set nginx-ingress.enabled=false                \
  --set prometheus.install=false                   \
  --set gitlab-runner.install=false                \
  --set gitlab.toolbox.enabled=false               \
  --set gitlab.gitlab-runner.enabled=false         \
  --set gitlab.gitlab-exporter.enabled=false       \
  --set gitlab.gitlab-shell.enabled=false          \
  --set gitlab.sidekiq.enabled=false               \
  --set gitlab.migrations.enabled=true             \
  --set registry.enabled=false \
  --set gitlab.webservice.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-webservice-ce \
  --set gitlab.webservice.workhorse.image=nexus.dspace.kt.co.kr/icis/gitlab-workhorse-ce   \
  --set gitlab.gitaly.image.repository=nexus.dspace.kt.co.kr/icis/gitaly                   \
  --set gitlab.migrations.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-toolbox-ce    \
  --set global.certificates.image.repository=nexus.dspace.kt.co.kr/icis/certificates       \
  --set global.kubectl.image.repository=nexus.dspace.kt.co.kr/icis/kubectl                 \
  --set global.gitlabBase.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-base          \
  --set postgresql.image.registry=nexus.dspace.kt.co.kr            \
  --set postgresql.image.repository=icis/postgresql                \
  --set postgresql.image.tag=14.8.0                                \
  --set postgresql.metrics.image.registry=nexus.dspace.kt.co.kr    \
  --set postgresql.metrics.image.repository=icis/postgres-exporter \
  --set postgresql.metrics.image.tag=0.12.0-debian-11-r86          \
  --set redis.image.registry=nexus.dspace.kt.co.kr                 \
  --set redis.image.repository=icis/redis                          \
  --set redis.image.tag=6.2.7-debian-11-r11                        \
  --set redis.metrics.image.registry=nexus.dspace.kt.co.kr         \
  --set redis.metrics.image.repository=icis/redis-exporter         \
  --set redis.metrics.image.tag=1.43.0-debian-11-r4                \
  --set gitlab.gitaly.persistence.enabled=true  \
  --set gitlab.gitaly.persistence.size=50Gi     \
  --set gitlab.gitaly.containerSecurityContext.runAsUser=0        \
  --set gitlab.gitaly.containerSecurityContext.privileged=true    \
  --set postgresql.persistence.enabled=false    \
  --set postgresql.persistence.size=8Gi         \
  --set postgresql.metrics.enabled=false                            \
  --set postgresql.primary.containerSecurityContext.runAsUser=0     \
  --set postgresql.primary.containerSecurityContext.privileged=true \
  --set redis.master.containerSecurityContext.runAsUser=0           \
  --set redis.master.containerSecurityContext.privileged=true       \
  --dry-run=true > dry-run_08.yaml
  
  
---


  
```



## 2) image pull

### (1) image 목록

```sh

$ cat dry-run_02.yaml | grep image:
    image: nexus.dspace.kt.co.kr:v16.7.0
          image: registry.gitlab.com/gitlab-org/build/cng/kubectl:v16.7.0
          image: registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0"
          image: nexus.dspace.kt.co.kr:v16.7.0
          image: nexus.dspace.kt.co.kr:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-workhorse-ce:v16.7.0"
          image: registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0"
          image: "nexus.dspace.kt.co.kr:v16.7.0"
          image: docker.io/bitnami/postgresql:14.8.0
          image: docker.io/bitnami/postgres-exporter:0.12.0-debian-11-r86
          image: docker.io/bitnami/redis:6.2.7-debian-11-r11
          image: docker.io/bitnami/redis-exporter:1.43.0-debian-11-r4
          image: registry.gitlab.com/gitlab-org/build/cng/kubectl:v16.7.0
          image: registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0"
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-toolbox-ce:v16.7.0"

$ cat dry-run_03.yaml | grep image:
    image: nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
          image: registry.gitlab.com/gitlab-org/build/cng/kubectl:v16.7.0
          image: registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0"
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-workhorse-ce:v16.7.0"
          image: registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0"
          image: "nexus.dspace.kt.co.kr/icis/gitlab-org/gitaly:v16.7.0"
          image: docker.io/bitnami/postgresql:14.8.0
          image: docker.io/bitnami/postgres-exporter:0.12.0-debian-11-r86
          image: docker.io/bitnami/redis:6.2.7-debian-11-r11
          image: docker.io/bitnami/redis-exporter:1.43.0-debian-11-r4
          image: registry.gitlab.com/gitlab-org/build/cng/kubectl:v16.7.0
          image: registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0"
          image: "registry.gitlab.com/gitlab-org/build/cng/gitlab-toolbox-ce:v16.7.0"

$ cat dry-run_04.yaml | grep image:
    image: nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/kubectl:v16.7.0
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/certificates:v16.7.0
          image: "nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-base:v16.7.0"
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
          image: "nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-workhorse-ce:v16.7.0"
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/certificates:v16.7.0
          image: "nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-base:v16.7.0"
          image: "nexus.dspace.kt.co.kr/icis/gitlab-org/gitaly:v16.7.0"
          image: nexus.dspace.kt.co.kr/icis/bitnami/postgresql:14.8.0
          image: nexus.dspace.kt.co.kr/icis/bitnami/postgres-exporter:0.12.0-debian-11-r86
          image: nexus.dspace.kt.co.kr/icis/bitnami/redis:6.2.7-debian-11-r11
          image: nexus.dspace.kt.co.kr/icis/bitnami/redis-exporter:1.43.0-debian-11-r4
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/kubectl:v16.7.0
          image: nexus.dspace.kt.co.kr/icis/gitlab-org/certificates:v16.7.0
          image: "nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-base:v16.7.0"
          image: "nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-toolbox-ce:v16.7.0"

$ cat dry-run_05.yaml | grep image:
```





### (2) tagging

```sh


docker pull registry.gitlab.com/gitlab-org/build/cng/gitlab-webservice-ce:v16.7.0
docker pull registry.gitlab.com/gitlab-org/build/cng/kubectl:v16.7.0
docker pull registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0
docker pull registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0
docker pull registry.gitlab.com/gitlab-org/build/cng/gitlab-workhorse-ce:v16.7.0
docker pull registry.gitlab.com/gitlab-org/build/cng/gitaly:v16.7.0
docker pull registry.gitlab.com/gitlab-org/build/cng/gitlab-toolbox-ce:v16.7.0
docker pull docker.io/bitnami/postgresql:14.8.0
docker pull docker.io/bitnami/postgres-exporter:0.12.0-debian-11-r86
docker pull docker.io/bitnami/redis:6.2.7-debian-11-r11
docker pull docker.io/bitnami/redis-exporter:1.43.0-debian-11-r4


docker tag registry.gitlab.com/gitlab-org/build/cng/gitlab-webservice-ce:v16.7.0  nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
docker tag registry.gitlab.com/gitlab-org/build/cng/kubectl:v16.7.0               nexus.dspace.kt.co.kr/icis/gitlab-org/kubectl:v16.7.0
docker tag registry.gitlab.com/gitlab-org/build/cng/certificates:v16.7.0          nexus.dspace.kt.co.kr/icis/gitlab-org/certificates:v16.7.0
docker tag registry.gitlab.com/gitlab-org/build/cng/gitlab-base:v16.7.0           nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-base:v16.7.0
docker tag registry.gitlab.com/gitlab-org/build/cng/gitlab-workhorse-ce:v16.7.0   nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-workhorse-ce:v16.7.0
docker tag registry.gitlab.com/gitlab-org/build/cng/gitaly:v16.7.0                nexus.dspace.kt.co.kr/icis/gitlab-org/gitaly:v16.7.0
docker tag registry.gitlab.com/gitlab-org/build/cng/gitlab-toolbox-ce:v16.7.0     nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-toolbox-ce:v16.7.0
docker tag docker.io/bitnami/postgresql:14.8.0                                    nexus.dspace.kt.co.kr/icis/bitnami/postgresql:14.8.0
docker tag docker.io/bitnami/postgres-exporter:0.12.0-debian-11-r86               nexus.dspace.kt.co.kr/icis/bitnami/postgres-exporter:0.12.0-debian-11-r86
docker tag docker.io/bitnami/redis:6.2.7-debian-11-r11                            nexus.dspace.kt.co.kr/icis/bitnami/redis:6.2.7-debian-11-r11
docker tag docker.io/bitnami/redis-exporter:1.43.0-debian-11-r4                   nexus.dspace.kt.co.kr/icis/bitnami/redis-exporter:1.43.0-debian-11-r4

docker push nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-org/kubectl:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-org/certificates:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-base:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-workhorse-ce:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-org/gitaly:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-toolbox-ce:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/bitnami/postgresql:14.8.0
docker push nexus.dspace.kt.co.kr/icis/bitnami/postgres-exporter:0.12.0-debian-11-r86
docker push nexus.dspace.kt.co.kr/icis/bitnami/redis:6.2.7-debian-11-r11
docker push nexus.dspace.kt.co.kr/icis/bitnami/redis-exporter:1.43.0-debian-11-r4



```





```

docker tag nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-webservice-ce:v16.7.0         nexus.dspace.kt.co.kr/icis/gitlab-webservice-ce:v16.7.0
docker tag nexus.dspace.kt.co.kr/icis/gitlab-org/kubectl:v16.7.0                      nexus.dspace.kt.co.kr/icis/kubectl:v16.7.0
docker tag nexus.dspace.kt.co.kr/icis/gitlab-org/certificates:v16.7.0                 nexus.dspace.kt.co.kr/icis/certificates:v16.7.0
docker tag nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-base:v16.7.0                  nexus.dspace.kt.co.kr/icis/gitlab-base:v16.7.0
docker tag nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-workhorse-ce:v16.7.0          nexus.dspace.kt.co.kr/icis/gitlab-workhorse-ce:v16.7.0
docker tag nexus.dspace.kt.co.kr/icis/gitlab-org/gitaly:v16.7.0                       nexus.dspace.kt.co.kr/icis/gitaly:v16.7.0
docker tag nexus.dspace.kt.co.kr/icis/gitlab-org/gitlab-toolbox-ce:v16.7.0            nexus.dspace.kt.co.kr/icis/gitlab-toolbox-ce:v16.7.0
docker tag nexus.dspace.kt.co.kr/icis/bitnami/postgresql:14.8.0                       nexus.dspace.kt.co.kr/icis/postgresql:14.8.0
docker tag nexus.dspace.kt.co.kr/icis/bitnami/postgres-exporter:0.12.0-debian-11-r86  nexus.dspace.kt.co.kr/icis/postgres-exporter:0.12.0-debian-11-r86
docker tag nexus.dspace.kt.co.kr/icis/bitnami/redis:6.2.7-debian-11-r11               nexus.dspace.kt.co.kr/icis/redis:6.2.7-debian-11-r11
docker tag nexus.dspace.kt.co.kr/icis/bitnami/redis-exporter:1.43.0-debian-11-r4      nexus.dspace.kt.co.kr/icis/redis-exporter:1.43.0-debian-11-r4

docker push nexus.dspace.kt.co.kr/icis/gitlab-webservice-ce:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/kubectl:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/certificates:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-base:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-workhorse-ce:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitaly:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/gitlab-toolbox-ce:v16.7.0
docker push nexus.dspace.kt.co.kr/icis/postgresql:14.8.0
docker push nexus.dspace.kt.co.kr/icis/postgres-exporter:0.12.0-debian-11-r86
docker push nexus.dspace.kt.co.kr/icis/redis:6.2.7-debian-11-r11
docker push nexus.dspace.kt.co.kr/icis/redis-exporter:1.43.0-debian-11-r4


```





## 3) install



### (1) service account 권한

```sh

# 확인
$ oc -n gitlab-system get sa gitlab-shared-secrets

NAME                                 SECRETS   AGE
builder                              2         458d
default                              2         458d
deployer                             2         458d
gitlab-certmanager-startupapicheck   2         445d
gitlab-dev-shared-secrets            2         440d
gitlab-shared-secrets                2         6m39s
jenkins-admin                        2         67d


# 권한 부여
$
oc patch serviceaccount gitlab-certmanager-startupapicheck -p '{"imagePullSecrets": [{"name": "dspace-nexus"}]}' -n gitlab-system
oc patch serviceaccount gitlab-dev-shared-secrets          -p '{"imagePullSecrets": [{"name": "dspace-nexus"}]}' -n gitlab-system
oc patch serviceaccount gitlab-shared-secrets              -p '{"imagePullSecrets": [{"name": "dspace-nexus"}]}' -n gitlab-system



# anyuid/privileged 권한 부여
$ oc adm policy add-scc-to-user anyuid     -z default -n gitlab-system
$ oc adm policy add-scc-to-user privileged -z default -n gitlab-system

$ oc adm policy add-scc-to-user anyuid     -z gitlab-redis -n gitlab-system
$ oc adm policy add-scc-to-user privileged -z gitlab-redis -n gitlab-system



anyuid




```





### (2) pvc

```pvc

data-gitlab-postgresql-0          8Gi
redis-data-gitlab-redis-master-0  8Gi
repo-data-gitlab-gitaly-0        50Gi


repo-data-gitlab-gitaly-0
data-gitlab-postgresql-0

```







### (3) install

```sh
$ helm -n gitlab-system ls 

$ cd ~/song/helm/charts/gitlab


$ helm -n gitlab-system install gitlab . \
  --timeout 600s \
  --set certmanager-issuer.email=ssongmantop@gmail.com \
  --set global.edition=ce \
  --set global.hosts.https=false \
  --set global.hosts.gitlab.name=gitlab.dev.icis.kt.co.kr \
  --set global.hosts.gitlab.https=false            \
  --set global.ingress.provider=traefik            \
  --set global.ingress.class=traefik               \
  --set global.ingress.tls.enabled=false           \
  --set global.gitaly.enabled=true                 \
  --set global.minio.enabled=false                 \
  --set global.kas.enabled=false                   \
  --set global.registry.enabled=false              \
  --set global.appConfig.lfs.enabled=false         \
  --set global.appConfig.artifacts.enabled=false   \
  --set global.appConfig.uploads.enabled=false     \
  --set global.appConfig.packages.enabled=false    \
  --set global.image.registry=nexus.dspace.kt.co.kr    \
  --set upgradeCheck.enabled=false                 \
  --set certmanager.install=false                  \
  --set certmanager.installCRDs=false              \
  --set nginx-ingress.enabled=false                \
  --set prometheus.install=false                   \
  --set gitlab-runner.install=false                \
  --set gitlab.toolbox.enabled=false               \
  --set gitlab.gitlab-runner.enabled=false         \
  --set gitlab.gitlab-exporter.enabled=false       \
  --set gitlab.gitlab-shell.enabled=false          \
  --set gitlab.sidekiq.enabled=false               \
  --set gitlab.migrations.enabled=true             \
  --set registry.enabled=false \
  --set gitlab.webservice.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-webservice-ce \
  --set gitlab.webservice.workhorse.image=nexus.dspace.kt.co.kr/icis/gitlab-workhorse-ce   \
  --set gitlab.gitaly.image.repository=nexus.dspace.kt.co.kr/icis/gitaly                   \
  --set gitlab.migrations.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-toolbox-ce    \
  --set global.certificates.image.repository=nexus.dspace.kt.co.kr/icis/certificates       \
  --set global.kubectl.image.repository=nexus.dspace.kt.co.kr/icis/kubectl                 \
  --set global.gitlabBase.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-base          \
  --set postgresql.image.registry=nexus.dspace.kt.co.kr            \
  --set postgresql.image.repository=icis/postgresql                \
  --set postgresql.image.tag=14.8.0                                \
  --set postgresql.metrics.image.registry=nexus.dspace.kt.co.kr    \
  --set postgresql.metrics.image.repository=icis/postgres-exporter \
  --set postgresql.metrics.image.tag=0.12.0-debian-11-r86          \
  --set redis.image.registry=nexus.dspace.kt.co.kr                 \
  --set redis.image.repository=icis/redis                          \
  --set redis.image.tag=6.2.7-debian-11-r11                        \
  --set redis.metrics.image.registry=nexus.dspace.kt.co.kr         \
  --set redis.metrics.image.repository=icis/redis-exporter         \
  --set redis.metrics.image.tag=1.43.0-debian-11-r4                \
  --set gitlab.gitaly.persistence.enabled=true  \
  --set gitlab.gitaly.persistence.size=50Gi     \
  --set gitlab.gitaly.containerSecurityContext.runAsUser=0        \
  --set gitlab.gitaly.containerSecurityContext.privileged=true    \
  --set postgresql.persistence.enabled=false    \
  --set postgresql.persistence.size=8Gi         \
  --set postgresql.metrics.enabled=false                            \
  --set postgresql.primary.containerSecurityContext.runAsUser=0     \
  --set postgresql.primary.containerSecurityContext.privileged=true \
  --set redis.master.containerSecurityContext.runAsUser=0           \
  --set redis.master.containerSecurityContext.privileged=true
  



NAME: gitlab
LAST DEPLOYED: Mon Jan 15 15:46:29 2024
NAMESPACE: gitlab-system
STATUS: deployed
REVISION: 1
NOTES:
=== CRITICAL
The following charts are included for evaluation purposes only. They will not be supported by GitLab Support
for production workloads. Use Cloud Native Hybrid deployments for production. For more information visit
https://docs.gitlab.com/charts/installation/index.html#use-the-reference-architectures.
- PostgreSQL
- Redis
- Gitaly

=== NOTICE
The minimum required version of PostgreSQL is now 13. See https://gitlab.com/gitlab-org/charts/gitlab/-/blob/master/doc/installation/upgrade.md for more details.
Help us improve the installation experience, let us know how we did with a 1 minute survey:https://gitlab.fra1.qualtrics.com/jfe/form/SV_6kVqZANThUQ1bZb?installation=helm&release=16-7

  
  
```



### (4) 확인/삭제

```sh


# 삭제
$ helm -n gitlab-system delete gitlab


# 확인
$ helm -n gitlab-system list
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
gitlab  gitlab-system   1               2024-01-16 18:50:16.2069651 +0900 KST   deployed        gitlab-7.7.0    v16.7.0





```





### (5) [참고] upgrade

```sh


$ helm -n gitlab-system upgrade gitlab . \
  --timeout 600s \
  --set certmanager-issuer.email=ssongmantop@gmail.com \
  --set global.edition=ce \
  --set global.hosts.https=false \
  --set global.hosts.gitlab.name=gitlab.dev.icis.kt.co.kr \
  --set global.hosts.gitlab.https=false            \
  --set global.ingress.provider=traefik            \
  --set global.ingress.class=traefik               \
  --set global.ingress.tls.enabled=false           \
  --set global.gitaly.enabled=true                 \
  --set global.minio.enabled=false                 \
  --set global.kas.enabled=false                   \
  --set global.registry.enabled=false              \
  --set global.appConfig.lfs.enabled=false         \
  --set global.appConfig.artifacts.enabled=false   \
  --set global.appConfig.uploads.enabled=false     \
  --set global.appConfig.packages.enabled=false    \
  --set global.image.registry=nexus.dspace.kt.co.kr    \
  --set upgradeCheck.enabled=false                 \
  --set certmanager.install=false                  \
  --set certmanager.installCRDs=false              \
  --set nginx-ingress.enabled=false                \
  --set prometheus.install=false                   \
  --set gitlab-runner.install=false                \
  --set gitlab.toolbox.enabled=false               \
  --set gitlab.gitlab-runner.enabled=false         \
  --set gitlab.gitlab-exporter.enabled=false       \
  --set gitlab.gitlab-shell.enabled=false          \
  --set gitlab.sidekiq.enabled=false               \
  --set gitlab.migrations.enabled=true             \
  --set registry.enabled=false \
  --set gitlab.webservice.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-webservice-ce \
  --set gitlab.webservice.workhorse.image=nexus.dspace.kt.co.kr/icis/gitlab-workhorse-ce   \
  --set gitlab.gitaly.image.repository=nexus.dspace.kt.co.kr/icis/gitaly                   \
  --set gitlab.migrations.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-toolbox-ce    \
  --set global.certificates.image.repository=nexus.dspace.kt.co.kr/icis/certificates       \
  --set global.kubectl.image.repository=nexus.dspace.kt.co.kr/icis/kubectl                 \
  --set global.gitlabBase.image.repository=nexus.dspace.kt.co.kr/icis/gitlab-base          \
  --set postgresql.image.registry=nexus.dspace.kt.co.kr            \
  --set postgresql.image.repository=icis/postgresql                \
  --set postgresql.image.tag=14.8.0                                \
  --set postgresql.metrics.image.registry=nexus.dspace.kt.co.kr    \
  --set postgresql.metrics.image.repository=icis/postgres-exporter \
  --set postgresql.metrics.image.tag=0.12.0-debian-11-r86          \
  --set redis.image.registry=nexus.dspace.kt.co.kr                 \
  --set redis.image.repository=icis/redis                          \
  --set redis.image.tag=6.2.7-debian-11-r11                        \
  --set redis.metrics.image.registry=nexus.dspace.kt.co.kr         \
  --set redis.metrics.image.repository=icis/redis-exporter         \
  --set redis.metrics.image.tag=1.43.0-debian-11-r4                \
  --set gitlab.gitaly.persistence.enabled=true  \
  --set gitlab.gitaly.persistence.size=50Gi     \
  --set gitlab.gitaly.containerSecurityContext.runAsUser=0        \
  --set gitlab.gitaly.containerSecurityContext.privileged=true    \
  --set postgresql.persistence.enabled=true     \
  --set postgresql.persistence.size=8Gi         \
  --set postgresql.metrics.enabled=false                            \
  --set postgresql.primary.containerSecurityContext.runAsUser=0     \
  --set postgresql.primary.containerSecurityContext.privileged=true \
  --set redis.master.containerSecurityContext.runAsUser=0           \
  --set redis.master.containerSecurityContext.privileged=true
  



NAME: gitlab
LAST DEPLOYED: Mon Jan 15 15:46:29 2024
NAMESPACE: gitlab-system
STATUS: deployed
REVISION: 1
NOTES:
=== CRITICAL
The following charts are included for evaluation purposes only. They will not be supported by GitLab Support
for production workloads. Use Cloud Native Hybrid deployments for production. For more information visit
https://docs.gitlab.com/charts/installation/index.html#use-the-reference-architectures.
- PostgreSQL
- Redis
- Gitaly

=== NOTICE
The minimum required version of PostgreSQL is now 13. See https://gitlab.com/gitlab-org/charts/gitlab/-/blob/master/doc/installation/upgrade.md for more details.
Help us improve the installation experience, let us know how we did with a 1 minute survey:https://gitlab.fra1.qualtrics.com/jfe/form/SV_6kVqZANThUQ1bZb?installation=helm&release=16-7




# 확인
$ helm -n gitlab-system list

NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
gitlab  gitlab-system   1               2024-01-16 18:50:16.2069651 +0900 KST   deployed        gitlab-7.7.0    v16.7.0
gitlab  gitlab-system   2               2024-01-16 19:02:44.261947 +0900 KST    deployed        gitlab-7.7.0    v16.7.0
gitlab  gitlab-system   3               2024-01-16 19:07:28.8890048 +0900 KST   deployed        gitlab-7.7.0    v16.7.0
gitlab  gitlab-system   4               2024-01-16 19:12:51.216409 +0900 KST    deployed        gitlab-7.7.0    v16.7.0
gitlab  gitlab-system   5               2024-01-17 17:12:52.8043812 +0900 KST   deployed        gitlab-7.7.0    v16.7.0



```







## 4) route



```yaml

kind: Route
apiVersion: route.openshift.io/v1
metadata:
  name: gitlabce-route
  namespace: gitlab-system
spec:
  host: gitlabce.dev.icis.kt.co.kr
  to:
    kind: Service
    name: gitlab-webservice-default
    weight: 100
  port:
    targetPort: http-workhorse
  wildcardPolicy: None
---

```



## 5) web service 확인

```

http://gitlabce.dev.icis.kt.co.kr/users/sign_in

```







## 9) trouble shooting



### (1) postgresql

#### postgres permissiono denied

```
...
postgresql 07:46:04.43
postgresql 07:46:04.43 Welcome to the Bitnami postgresql container
postgresql 07:46:04.44 Subscribe to project updates by watching https://github.com/bitnami/containers
postgresql 07:46:04.44 Submit issues and feature requests at https://github.com/bitnami/containers/issues
postgresql 07:46:04.44
postgresql 07:46:04.44 INFO ==> ** Starting PostgreSQL setup **
postgresql 07:46:04.45 INFO ==> Validating settings in POSTGRESQL_* env vars..
postgresql 07:46:04.46 INFO ==> Loading custom pre-init scripts...
postgresql 07:46:04.46 INFO ==> Loading user's custom files from /docker-entrypoint-preinitdb.d ...
touch: cannot touch '/bitnami/postgresql/.gitlab_1_scripts_initialized': Permission denied

```



```
runAsUser: 0 으로 수정
```



### 

#### postgres permissiono denied

```
...
postgresql 09:01:57.46
postgresql 09:01:57.46 Welcome to the Bitnami postgresql container
postgresql 09:01:57.46 Subscribe to project updates by watching https://github.com/bitnami/containers
postgresql 09:01:57.46 Submit issues and feature requests at https://github.com/bitnami/containers/issues
postgresql 09:01:57.46
postgresql 09:01:57.46 INFO ==> ** Starting PostgreSQL setup **
postgresql 09:01:57.48 INFO ==> Validating settings in POSTGRESQL_* env vars..
chmod: changing permissions of '/proc/self/fd/1': Permission denied
```



```

      securityContext:
        runAsUser: 0
        privileged: true    <-- 추가
```





### (2) redis Permission denied

```

1:C 15 Jan 2024 09:17:16.453 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
1:C 15 Jan 2024 09:17:16.453 # Redis version=6.2.7, bits=64, commit=00000000, modified=0, pid=1, just started
1:C 15 Jan 2024 09:17:16.453 # Configuration loaded
1:M 15 Jan 2024 09:17:16.454 * monotonic clock: POSIX clock_gettime
1:M 15 Jan 2024 09:17:16.454 # Can't open the append-only file: Permission denied

```



```

          securityContext:
            runAsUser: 1001

에서 아래로 변경
            
          securityContext:
            runAsUser: 0
            privileged: true 
```



### (3) webservice

```
...
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
Checking: main
Database Schema - main (gitlabhq_production) - current: 0, codebase: 20231218062505
NOTICE: Database has not been initialized yet.
WARNING: Not all services were operational, with data migrations completed.
If this container continues to fail, please see: https://docs.gitlab.com/charts/troubleshooting/index.html#application-containers-constantly-initializing

```





### (4) gitaly

```
Begin parsing .tpl templates from /etc/gitaly/templates
Writing /etc/gitaly/config.toml
Copying other config files found in /etc/gitaly/templates to /etc/gitaly
Starting Gitaly
{"component": "gitaly","subcomponent":"gitaly","latencies":[0.001,0.005,0.025,0.1,0.5,1,10,30,60,300,1500],"level":"info","msg":"grpc prometheus histograms enabled","pid":1,"time":"2024-01-16T09:53:41.645Z"}
{"component": "gitaly","subcomponent":"gitaly","level":"info","msg":"Starting Gitaly","pid":1,"time":"2024-01-16T09:53:41.646Z","version":"16.7.0"}
{"component": "gitaly","subcomponent":"gitaly","duration_ms":0,"level":"info","msg":"finished initializing cgroups","pid":1,"time":"2024-01-16T09:53:41.658Z"}
{"component": "gitaly","subcomponent":"gitaly","duration_ms":23,"level":"info","msg":"finished unpacking auxiliary binaries","pid":1,"time":"2024-01-16T09:53:41.681Z"}
{"component": "gitaly","subcomponent":"gitaly","duration_ms":0,"level":"info","msg":"finished initializing bootstrap","pid":1,"time":"2024-01-16T09:53:41.681Z"}
{"component": "gitaly","subcomponent":"gitaly","duration_ms":0,"level":"info","msg":"finished initializing command factory","pid":1,"time":"2024-01-16T09:53:41.682Z"}
{"component": "gitaly","subcomponent":"gitaly","duration_ms":1,"level":"info","msg":"finished detecting git version","pid":1,"time":"2024-01-16T09:53:41.684Z"}
{"component": "gitaly","subcomponent":"gitaly","level":"info","msg":"clearing disk cache object folder","pid":1,"storage":"default","time":"2024-01-16T09:53:41.684Z"}

이후 아무 메세지 없이 재기동....

```





```

          securityContext:
            runAsUser: 1000

에서 아래로 변경

            privileged: true
            runAsUser: 0
            
            
```



