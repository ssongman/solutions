# gitlab ce install





# 1.helm install



## 1) helm fetch

```sh

$ helm repo add gitlab https://charts.gitlab.io/

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

```
secret 에서 확인

$ echo OEh0S3RrWVhQZmtua3dtMk9SUzl2MTlwUk9zUXpJbVFtUzR4UkZuNXVvSDdaY1drVXVsc0pCZHRKdFZpMzBhWg== | base64 -d

8HtKtkYXPfknkwm2ORS9v19pROsQzImQmS4xRFn5uoH7ZcWkUulsJBdtJtVi30aZ
----


user : root 
password: 8HtKtkYXPfknkwm2ORS9v19pROsQzImQmS4xRFn5uoH7ZcWkUulsJBdtJtVi30aZ
password: new****!




login : root
password : ******


```









# 2. 초기 설정 작업

## 1) Sign-up restrictions

사용자들이 마음대로 등록하지 못하도록 설정해야 함

* 메뉴 : Settings > Admin Area > General

* 항목 : Sign-up enabled  false





