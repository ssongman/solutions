# pgadmin 





## pgadmin install with helm



```sh
$ kubectl create ns pgadmin



$ helm repo add runix https://helm.runix.net

$ helm search repo pgadmin
NAME            CHART VERSION   APP VERSION     DESCRIPTION
runix/pgadmin4  1.24.0          8.4             pgAdmin4 is a web based administration tool for...
stable/pgadmin  1.2.3           4.18.0          DEPRECATED - moved to new repo, see source for ...

NAME            CHART VERSION   APP VERSION     DESCRIPTION
runix/pgadmin4  1.59.0          9.11            pgAdmin4 is a web based administration tool for...



# values yaml 확인
$ helm show values runix/pgadmin4

$ ll
-rw-r--r--  1 song song  13702 Mar 28 22:53 pgadmin4-1.24.0.tgz



# Helm install
$ helm -n pgadmin install my-admin runix/pgadmin4 \
    --set ingress.enabled=true \
    --set ingress.hosts[0].host=pgadmin.ssongman.com \
    --set ingress.hosts[0].paths[0].path=/ \
    --set ingress.hosts[0].paths[0].pathType=Prefix \
    --set env.email=ssongmantop@gmail.com \
    --set env.password=pgadminpass \
    --set persistentVolume.enabled=false \
    --dry-run=true




# 확인
$ helm -n pgadmin list
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
my-admin        pgadmin         1               2024-03-28 23:04:40.558942712 +0900 KST deployed        pgadmin4-1.24.0 8.4

NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART              APP VERSION
my-admin        pgadmin         1               2026-02-19 15:05:26.500634058 +0000 UTC deployed        pgadmin4-1.59.0    9.11




# 삭제시
$ helm -n pgadmin delete my-admin



```





## 확인



```

http://pgadmin.ssongman.com

```







## Clean up

```sh


$ helm -n pgadmin ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS  CHART           APP VERSION
my-admin        pgadmin         1               2024-03-28 23:01:40.010668538 +0900 KST failed  pgadmin4-1.24.0 8.4


# 삭제
$ helm -n pgadmin delete my-admin 


```

