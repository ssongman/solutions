# < Jira Comunity >



# 라이선스







# 1. helm install 1





```sh

$ kubectl create ns jira

$ helm search repo jira
NAME                            CHART VERSION   APP VERSION     DESCRIPTION
prometheus-community/jiralert   1.4.0           v1.3.0          A Helm chart for Kubernetes to install jiralert

# fetch
$ helm fetch prometheus-community/jiralert

$ cd ~/song/helm/charts/jiralert

# dry-run
$ helm -n jira install jira . \
    --set ingress.enabled=false \
    --dry-run=true



# install
$ helm -n jira install jira . \
    --set ingress.enabled=false
    
    
    
    #--set ingress.hosts[0].host=jira.211-253-28-14.nip.io \


# 확인
$ helm -n jira  ls

# 삭제
$ helm -n jira delete jira

$ kubectl -n jira get pod


```





## trouble shooting



- 현상

```

error loading configuration" path=/config/jiralert.yml err="no receivers defined"



```



* jiralert.yml 확인

```sh
$ k -n jira get secret jira-jiralert -o yaml
apiVersion: v1
data:
  jiralert.tmpl: e3sgZGVmaW5lICJqaXJhLnN1bW1hcnkiIH19W3t7IC5TdGF0dXMgfCB0b1VwcGVyIH19e3sgaWYgZXEgLlN0YXR1cyAiZmlyaW5nIiB9fTp7eyAuQWxlcnRzLkZpcmluZyB8IGxlbiB9fXt7IGVuZCB9fV0ge3sgLkdyb3VwTGFiZWxzLlNvcnRlZFBhaXJzLlZhbHVlcyB8IGpvaW4gIiAiIH19IHt7IGlmIGd0IChsZW4gLkNvbW1vbkxhYmVscykgKGxlbiAuR3JvdXBMYWJlbHMpIH19KHt7IHdpdGggLkNvbW1vbkxhYmVscy5SZW1vdmUgLkdyb3VwTGFiZWxzLk5hbWVzIH19e3sgLlZhbHVlcyB8IGpvaW4gIiAiIH19e3sgZW5kIH19KXt7IGVuZCB9fXt7IGVuZCB9fQoKe3sgZGVmaW5lICJqaXJhLmRlc2NyaXB0aW9uIiB9fXt7IHJhbmdlIC5BbGVydHMuRmlyaW5nIH19TGFiZWxzOgp7eyByYW5nZSAuTGFiZWxzLlNvcnRlZFBhaXJzIH19IC0ge3sgLk5hbWUgfX0gPSB7eyAuVmFsdWUgfX0Ke3sgZW5kIH19CkFubm90YXRpb25zOgp7eyByYW5nZSAuQW5ub3RhdGlvbnMuU29ydGVkUGFpcnMgfX0gLSB7eyAuTmFtZSB9fSA9IHt7IC5WYWx1ZSB9fQp7eyBlbmQgfX0KU291cmNlOiB7eyAuR2VuZXJhdG9yVVJMIH19Cnt7IGVuZCB9fXt7IGVuZCB9fQo=
  jiralert.yml: ZGVmYXVsdHM6CiAgYXBpX3VybDogaHR0cHM6Ly9leGFtcGxlLmF0bGFzc2lhbi5uZXQKICBkZXNjcmlwdGlvbjogJ3t7IHRlbXBsYXRlICJqaXJhLmRlc2NyaXB0aW9uIiAuIH19JwogIGlzc3VlX3R5cGU6IEJ1ZwogIHJlb3Blbl9kdXJhdGlvbjogMGgKICByZW9wZW5fc3RhdGU6IFRvIERvCiAgc3VtbWFyeTogJ3t7IHRlbXBsYXRlICJqaXJhLnN1bW1hcnkiIC4gfX0nCnJlY2VpdmVyczogW10KdGVtcGxhdGU6IGppcmFsZXJ0LnRtcGw=
kind: Secret
metadata:
  annotations:
    meta.helm.sh/release-name: jira
    meta.helm.sh/release-namespace: jira
  creationTimestamp: "2023-06-14T14:49:29Z"
  labels:
    app.kubernetes.io/component: metrics
    app.kubernetes.io/instance: jira
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: jiralert
    app.kubernetes.io/part-of: jiralert
    app.kubernetes.io/version: v1.3.0
    helm.sh/chart: jiralert-1.4.0
  name: jira-jiralert
  namespace: jira
  resourceVersion: "3018703"
  uid: 860b8e17-8128-4293-a748-9c022e366e7e
type: Opaque



$ echo ZGVmYXVsdHM6CiAgYXBpX3VybDogaHR0cHM6Ly9leGFtcGxlLmF0bGFzc2lhbi5uZXQKICBkZXNjcmlwdGlvbjogJ3t7IHRlbXBsYXRlICJqaXJhLmRlc2NyaXB0aW9uIiAuIH19JwogIGlzc3VlX3R5cGU6IEJ1ZwogIHJlb3Blbl9kdXJhdGlvbjogMGgKICByZW9wZW5fc3RhdGU6IFRvIERvCiAgc3VtbWFyeTogJ3t7IHRlbXBsYXRlICJqaXJhLnN1bW1hcnkiIC4gfX0nCnJlY2VpdmVyczogW10KdGVtcGxhdGU6IGppcmFsZXJ0LnRtcGw= | base64 -d
defaults:
  api_url: https://example.atlassian.net
  description: '{{ template "jira.description" . }}'
  issue_type: Bug
  reopen_duration: 0h
  reopen_state: To Do
  summary: '{{ template "jira.summary" . }}'
receivers: []
template: jiralert.tmpl




```





# 2. helm install 2



```sh

$ helm repo add atlassian-data-center https://atlassian.github.io/data-center-helm-charts

$ helm repo ls
NAME                    URL
bitnami                 https://charts.bitnami.com/bitnami
hashicorp               https://helm.releases.hashicorp.com
prometheus-community    https://prometheus-community.github.io/helm-charts
gin                     https://fallenangelblog.github.io/charts/
rhcharts                https://ricardo-aires.github.io/helm-charts/
atlassian-data-center   https://atlassian.github.io/data-center-helm-charts

$ helm search repo jira



NAME                            CHART VERSION   APP VERSION     DESCRIPTION
atlassian-data-center/jira      1.13.0          9.4.7           A chart for installing Jira Data Center on Kube...
prometheus-community/jiralert   1.4.0           v1.3.0          A Helm chart for Kubernetes to install jiralert


$ helm fetch atlassian-data-center/jira

$ tar -xzvf jira-1.13.0.tgz

$ cd ~/song/helm/charts/jira



$ helm -n jira install my-jira atlassian-data-center/jira --version 1.3.0


$ helm test my-jira -n jira



```



## ingress

```sh
$ mkdir -p ~/temp/jira
  cd ~/temp/jira

$ cat > 12.jira-ingress.yaml
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.provider: "traefik"
  labels:
    app: jira
    release: jira
  name: ingress-jira
spec:
  rules:
  - host: "jira.35.209.207.26.nip.io"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-jira
            port:
              number: 80
              
---

$ kubectl -n jira apply -f 12.jira-ingress.yaml


```



* 확

```

http://jira.35.209.207.26.nip.io/secure/SetupMode!default.jspa


```

