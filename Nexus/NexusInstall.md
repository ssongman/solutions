# Nexus Install



# 1. 개요

nexus 설치하는 방법



# 2. 사전작업

```sh

$ kubectl create namespace nexus-cache


$ helm repo add sonatype https://sonatype.github.io/helm3-charts/
"sonatype" has been added to your repositories



$ helm repo ls

$ helm repo update

$ helm search repo nexus


NAME                                    CHART VERSION   APP VERSION     DESCRIPTION
sonatype/nexus-iq-server                174.0.0         1.174.0         Sonatype Nexus IQ Server continuously monitors ...
sonatype/nexus-iq-server-ha             174.0.0         1.174.0         A cluster of Sonatype Nexus IQ Servers to conti...
sonatype/nexus-repository-manager       64.2.0          3.64.0          DEPRECATED Sonatype Nexus Repository Manager - ...
sonatype/nxrm-aws-resiliency            64.2.0          3.64.0          DEPRECATED Resilient AWS Deployment of Sonatype...
sonatype/nxrm-ha                        66.0.0          3.66.0          Resilient Deployment of Sonatype Nexus Reposito...
sonatype/nxrm-ha-aws                    61.0.3          3.61.0          DEPRECATED Resilient AWS Deployment of Sonatype...
sonatype/nxrm-ha-azure                  61.0.3          3.61.0          DEPRECATED Resilient Azure Deployment of Sonaty...


# sonatype/nexus-repository-manager 는 deprecated 되었다.
# 그래도 이걸로 설치하자.


```





# 3. nexus rm(성공)

nexus repository manager 설치

```sh
$ cd ~/song/helm/charts

$ helm fetch sonatype/nexus-repository-manager

$ ll
-rw-r--r-- 1 song song  27490 Mar 16 19:28 nxrm-ha-66.0.0.tgz
-rw-r--r-- 1 song song   9289 Mar 16 20:47 nexus-repository-manager-64.2.0.tgz


$ tar -xzvf nexus-repository-manager-64.2.0.tgz


$ cd ~/song/helm/charts/nexus-repository-manager/


$ vi values.yaml
...




# Nexus Repository Manager
$ helm -n nexus-cache install nxrm-cache . \
    --set ingress.enabled=true \
    --set ingress.ingressClassName=traefik \
    --set ingress.hostRepo=nexus-cache.ssongman.duckdns.org \
    --set persistence.enabled=false \
    --dry-run=true
    

NAME: nxrm-cache
LAST DEPLOYED: Sat Mar 16 20:55:32 2024
NAMESPACE: nexus-cache
STATUS: deployed
REVISION: 1
NOTES:
1. Your ingresses are available here:
  http://nexus-cache.ssongman.duckdns.org/



$ helm -n nexus-cache ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                                 APP VERSION
nxrm-cache      nexus-cache     1               2024-03-16 20:55:32.229726143 +0900 KST deployed        nexus-repository-manager-64.2.0       3.64.0



$ helm -n nexus-cache delete nxrm-cache


```







# [참고] nxrm-ha(실패)

https://support.sonatype.com/hc/en-us/articles/9358729673363-How-to-install-Nexus-IQ-instance-using-Sonatype-helm3-chart



```sh
$ cd ~/song/helm/charts


$ helm fetch sonatype/nxrm-ha

$ ll
-rw-r--r-- 1 song song  27490 Mar 16 19:28 nxrm-ha-66.0.0.tgz

$ tar -xzvf nxrm-ha-66.0.0.tgz

$ cd ~/song/helm/charts/nxrm-ha

$ cd ~/song/helm/charts

$ helm fetch sonatype/nexus-repository-manager

$ ll
-rw-r--r-- 1 song song  27490 Mar 16 19:28 nxrm-ha-66.0.0.tgz
-rw-r--r-- 1 song song   9289 Mar 16 20:47 nexus-repository-manager-64.2.0.tgz


$ tar -xzvf nexus-repository-manager-64.2.0.tgz

$ cd ~/song/helm/charts/nexus-repository-manager/



$ cd ~/song/helm/charts/nxrm-ha

# Nexus Repository Manager
$ helm -n nexus-cache install nxrm-cache . \
    --set namespaces.nexusNs.enabled=false \
    --set namespaces.nexusNs.name=nexus-cache \
    --set statefulset.replicaCount=1 \
    --set statefulset.container.resources.requests.cpu=1      \
    --set statefulset.container.resources.requests.memory=1Gi \
    --set statefulset.container.resources.limits.cpu=1        \
    --set statefulset.container.resources.limits.memory=1Gi   \
    --set service.nexus.enabled=true \
    --set service.nexus.type=ClusterIP \
    --set ingress.enabled=true \
    --set ingress.host=nexus-cache.ssongman.duckdns.org \
    --set ingress.defaultRule=true \
    --set ingress.ingressClassName=traefik \
    --dry-run=true


NAME: nxrm-cache
LAST DEPLOYED: Sat Mar 16 19:47:08 2024
NAMESPACE: nexus-cache
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing nxrm-ha.




$ helm -n nexus-cache ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
nxrm-cache      nexus-cache     1               2024-03-16 19:47:08.663867853 +0900 KST deployed        nxrm-ha-66.0.0  3.66.0




$ helm -n nexus-cache delete nxrm-cache



```







# 4. login



## 초기 admin pass 확인

```sh


$ cat /nexus-data/admin.password

a376ccf1-979d-4a32-9b76-d6be6e95c7a0


# admin password 변경

id : admin
pass : adminpass


```







# 5. 확인



## nexus version / edition 확인하는 방법



* 메뉴
  * login
  * Configuration > System Information
  * nexus-status > edition
* edition 종류
  * OSS
    * 
  * PRO
    * 유료버젼



### header값 확인

```sh
$ curl -sSkI http://nexus.ssongman.duckdns.org


HTTP/1.1 200 OK
Cache-Control: no-cache, no-store, max-age=0, must-revalidate, post-check=0, pre-check=0
Content-Length: 7927
Content-Type: text/html
Date: Sat, 16 Mar 2024 11:10:03 GMT
Expires: 0
Last-Modified: Sat, 16 Mar 2024 11:10:03 GMT
Pragma: no-cache
Server: Nexus/3.63.0-01 (OSS)
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-Xss-Protection: 1; mode=block

```





