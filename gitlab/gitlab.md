# < GitLab >

# 1. Install

## 1.1 with yaml - gitlab-ce



### 1) deployment and service

```sh

$ cat > 11.gitlab-deployment-svc.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gitlab
  labels:
    app: gitlab
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gitlab
  template:
    metadata:
      labels:
        app: gitlab
    spec:
      containers:
      - name: gitlab
        image: gitlab/gitlab-ce:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: gitlab-svc
spec:
  selector:
    app: gitlab
  ports:
  - name: http
    protocol: TCP
    port: 80
    #targetPort: 8181
  #type: NodePort
---

```



### 2) ingress

```sh


$ cat > 12.gitlab-ingress.yaml
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.provider: "traefik"
  labels:
    app: gitlab
    release: gitlab
  name: ingress-gitlab
spec:
  rules:
  - host: "gitlab.35.209.207.26.nip.io"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: gitlab-svc
            port:
              number: 80
              
---



```





### 3) [참고] route

```sh

$ cat > 13.gitlab-route.yaml
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: gitlab-route
spec:
  host: gitlab.apps.211-34-231-82.nip.io
  port:
    targetPort: http
  to:
    kind: Service
    name: gitlab-svc
    weight: 100
  wildcardPolicy: None         
---


```





### 4) 권한부여

```sh

# pod list 를 읽을 수 있는 권한이 있어야 한다.  그냥 cluster-admin 주자.
# cluster role binding 

$ cat > 10.gitlab-clusterrolebinding.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: devops-gitlab
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: default
  namespace: gitlab
---


```



### 5) 초기 root 패스워드

```sh
# log...

Set up the initial password
Introduced in Omnibus GitLab 14.0.

By default, Omnibus GitLab automatically generates a password for the initial administrator user account (root) and stores it to /etc/gitlab/initial_root_password for at least 24 hours. For security reasons, after 24 hours, this file is automatically removed by the first gitlab-ctl reconfigure.

—--

cat /etc/gitlab/initial_root_password

yBTdTn9SmJ3V36V2vypW4sludaordc2FJG8S86BX1N0=

id : root
password : 양근xx1!

Password must not contain commonly used combinations of words and letters


```

