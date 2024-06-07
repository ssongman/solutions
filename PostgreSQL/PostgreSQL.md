

# 1. postgreSQL



## 1) Helm Install

```sh

$ helm search repo postgresql
NAME                    CHART VERSION   APP VERSION     DESCRIPTION
bitnami/postgresql      15.5.1          16.3.0          PostgreSQL (Postgres) is an open source object-...
bitnami/postgresql-ha   14.1.3          16.3.0          This PostgreSQL cluster solution includes the P...
bitnami/supabase        5.2.0           1.24.4          Supabase is an open source Firebase alternative...



$ cd ~/helm/charts/postgresql



# namespace 생성
$ kubectl create ns postgressql

# Helm install
$ helm -n postgressql install mypost . \
    --set global.postgresql.auth.postgresPassword=New1234! \
    --set global.postgresql.auth.username=diopro \
    --set global.postgresql.auth.password=new1234 \
    --set global.postgresql.auth.database=mypage \
    --dry-run=true

NAME: mypost
LAST DEPLOYED: Sun Jun  2 13:25:17 2024
NAMESPACE: postgressql
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: postgresql
CHART VERSION: 15.5.1
APP VERSION: 16.3.0


# 확인
$ helm -n postgressql ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
mypost  postgressql     1               2024-06-02 13:25:17.742202171 +0000 UTC deployed        postgresql-15.5.1       16.3.0


# 삭제시...
$ helm -n postgressql delete mypost

```





## 2) 확인

```sh

$ kubectl -n postgressql get all
NAME                                   READY   STATUS    RESTARTS   AGE
pod/mypost-postgresql-0                1/1     Running   0          12m

NAME                           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/mypost-postgresql      ClusterIP   10.43.235.48   <none>        5432/TCP   12m
service/mypost-postgresql-hl   ClusterIP   None           <none>        5432/TCP   12m

NAME                                 READY   AGE
statefulset.apps/mypost-postgresql   1/1     12m


```





# 2. pgadmin 



## 1) pgadmin install with helm



### (1) install

```sh


$ helm repo add runix https://helm.runix.net

$ helm search repo pgadmin
NAME            CHART VERSION   APP VERSION     DESCRIPTION
runix/pgadmin4  1.24.0          8.4             pgAdmin4 is a web based administration tool for...
stable/pgadmin  1.2.3           4.18.0          DEPRECATED - moved to new repo, see source for ...
---
NAME            CHART VERSION   APP VERSION     DESCRIPTION
runix/pgadmin4  1.25.3          8.6             pgAdmin4 is a web based administration tool for...



# values yaml 확인
$ helm show values runix/pgadmin4




# Helm install
$ helm -n postgressql install pgadmin runix/pgadmin4 \
    --set ingress.enabled=true \
    --set ingress.hosts[0].host=pgadmin.diopro.duckdns.org \
    --set ingress.hosts[0].paths[0].path=/ \
    --set ingress.hosts[0].paths[0].pathType=Prefix \
    --set env.email=ssongmantop@gmail.com \
    --set env.password=pgadminpass \
    --set persistentVolume.enabled=false \
    --dry-run=true


# 확인
$ helm -n postgressql ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
mypost  postgressql     1               2024-06-02 13:25:17.742202171 +0000 UTC deployed        postgresql-15.5.1       16.3.0
pgadmin postgressql     1               2024-06-02 13:28:53.45368528 +0000 UTC  deployed        pgadmin4-1.25.3         8.6


# 삭제시...
$ helm -n postgressql delete pgadmin


```





### (2) 확인

```
http://pgadmin.diopro.duckdns.org

```





## 2) 서버추가

* 서버 : mypost-postgresql
* database: mypage
* username: diopro
* password: new1234

