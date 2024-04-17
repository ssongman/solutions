



# 1. Jenkins Install



## 1) 사전준비



```sh
$ kubectl create ns jenkins-system

```





## 2) helm chart



```sh
$ helm search repo jenkins
NAME            CHART VERSION   APP VERSION     DESCRIPTION                                       
bitnami/jenkins 12.11.0         2.440.1         Jenkins is an open source Continuous Integratio...
stable/jenkins  2.5.4           lts             DEPRECATED - Open source continuous integration...



$ cd ~/song/helm/charts

$ helm pull bitnami/jenkins

$ ll
-rw-r--r--  1 song song  49783 Apr 17 17:27 jenkins-12.11.0.tgz

$ tar -xzvf jenkins-12.11.0.tgz
```





### dry-run

```sh

$ cd ~/song/helm/charts/jenkins

$ helm -n jenkins-system install jenkins . \
    --set jenkinsUser=jenkins \
    --set jenkinsPassword=jenkinspass \
    --set service.type=ClusterIP \
    --set ingress.enabled=true \
    --set ingress.hostname=jenkins.ssongman.duckdns.org \
    --set ingress.ingressClassName=traefik \
    --set persistence.enabled=true \
    --dry-run=true

=============================================

    --set agent.image 

=============================================


NAME: jenkins
LAST DEPLOYED: Wed Apr 17 17:38:29 2024
NAMESPACE: jenkins-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: jenkins
CHART VERSION: 12.11.0
APP VERSION: 2.440.1

** Please be patient while the chart is being deployed **

1. Get the Jenkins URL and associate its hostname to your cluster external IP:

   export CLUSTER_IP=$(minikube ip) # On Minikube. Use: `kubectl cluster-info` on others K8s clusters
   echo "Jenkins URL: http://jenkins.ssongman.duckdns.org"
   echo "$CLUSTER_IP  jenkins.ssongman.duckdns.org" | sudo tee -a /etc/hosts

2. Login with the following credentials

  echo Username: jenkins
  echo Password: $(kubectl get secret --namespace jenkins-system jenkins -o jsonpath="{.data.jenkins-password}" | base64 -d)

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - resources
  - tls.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/



# 확인
$ helm -n jenkins-system list
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
jenkins jenkins-system  1               2024-04-17 17:38:29.254902403 +0900 KST deployed        jenkins-12.11.0 2.440.1


# 삭제시...
$ helm -n jenkins-system delete jenkins



```





### 확인



```


http://jenkins.ssongman.duckdns.org

jenkins / jankins****


```













# 2. 환경설정



## 1) Kubernetes Pod로 Jenkins Agent 동적 생성



https://www.whatap.io/ko/blog/77/









# 3. 환경설정2







## 1) 시스템설정

Jenkins 관리 → 시스템 설정 (Configure System)

Global properties







## 2) Global Pipeline Libraries



## 3) Plugin Manager





## 4) Manage nodes and clouds

#### Configure Clouds - Kubernetes 설정



Kubernetes URL : https://kubernetes.default

Jenkins URL : [http://jenkins.sa-test.svc.cluster.local:8080](http://jenkins.sa-test.svc.cluster.local:8080/)

Jenkins tunnel : [jenkins-agent.sa](http://jenkins-agent.sa/)-test.svc.cluster.local:50000 

Pod Label Key : jenkins/maven-agent





## 5) Pod Template 설정

### (1) agent



### (2) Build-tools

Labels : maven-agent

build-tools  → nexus.dspace.kt.co.kr/icis/build-tools:1.0.4

jnlp → nexus.dspace.kt.co.kr/icis/jenkins/jnlp-slave:latest-jdk11

NFS Volume → 10.217.137.11 / /sit_sa_common04 / /root/.m2 (SIT)



### (3) Podman-agent







## 6) Credentials 생성



메뉴 : Jenkins 관리 - Manage Credentials이동



### (1) Nexus 공용 계정 설정 

  Nexus

- ID : icistr_sa
- PW : ******_**



### (2) Git 계정 설정



## 7) Manage and Assign Roles

#### 도메인별 권한 분리

Jenkins 관리 → Configure Global Security → Authentication → Authorization 을 **Role-Based Strategy** 로 변경한다.

Jenkins관리 → Manage and Assign Roles → Manage Roles







# 3. 추가 셋팅



## 1) build-tools

### (1) Dockerfile

```sh

FROM eclipse-temurin:17.0.2_8-jdk AS base
############ [Build] #####################
FROM base AS build-base
# Installing basic packages
RUN apt-get update && \
   apt-get install -y zip unzip curl && \
   apt-get install -y docker && \
   rm -rf /var/lib/apt/lists/* && \
   rm -rf /tmp/*
    
RUN curl -k -fsSL https://download.docker.com/linux/static/stable/x86_64/docker-20.10.7.tgz | tar zxvf - --strip 1 -C /usr/local/bin docker/docker
############ [Production] #####################
### Runtime
FROM base AS production
RUN apt-get update && \
   apt-get install -y git && \
   rm -rf /var/lib/apt/lists/* && \
   rm -rf /tmp/*
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
 
 
 
################################################################################ setting.xml
RUN mkdir -p /root/.m2
COPY ./settings.xml /root/.m2
################################################################################ kustomize
COPY ./kustomize /usr/local/bin/kustomize
 
 
 
################################################################################ Maven
# Downloading and installing Maven
# 1- Define a constant with the version of maven you want to install
ARG MAVEN_VERSION=3.6.3
 
# 2- Define a constant with the working directory
ARG USER_HOME_DIR="/root"
 
# 3- Define the SHA key to validate the maven download
#ARG SHA=b4880fb7a3d81edd190a029440cdf17f308621af68475a4fe976296e71ff4a4b546dd6d8a58aaafba334d309cc11e638c52808a4b0e818fc0fd544226d952544
 
# 4- Define the URL where maven can be downloaded from
ARG BASE_URL=https://apache.osuosl.org/maven/maven-3/${MAVEN_VERSION}/binaries
 
# 5- Create the directories, download maven, validate the download, install it, remove downloaded file and set links
RUN mkdir -p /usr/share/maven /usr/share/maven/ref \
  && echo "Downlaoding maven" \
#  maven 접근 오류로 강제 지정함.
#  && curl -sSL -o /tmp/apache-maven.tar.gz ${BASE_URL}/apache-maven-${MAVEN_VERSION}-bin.tar.gz -k \
  && curl -fsSL -o /tmp/apache-maven.tar.gz https://downloads.apache.org/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz -k \
  \
#  && echo "Checking download hash" \
# && echo "${SHA}  /tmp/apache-maven.tar.gz" | sha512sum -c - \
  \
  && echo "Unziping maven" \
  && tar -xzf /tmp/apache-maven.tar.gz -C /usr/share/maven --strip-components=1 \
  \
  && echo "Cleaning and setting links" \
  && rm -f /tmp/apache-maven.tar.gz \
  && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn
 
# 6- Define environmental variables required by Maven, like Maven_Home directory and where the maven repo is located
#ENV MAVEN_HOME /usr/share/maven
#ENV MAVEN_CONFIG "$USER_HOME_DIR/.m2"



# Installing basic packages
RUN apt-get update && \
   apt-get install -y jq && \
   rm -rf /var/lib/apt/lists/* && \
   rm -rf /tmp/*



```







### (2) Settting_xml 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/settings/1.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
    <servers>
        <server>
            <id>sw-central</id>
            <username>icistr-cmmn-readonly</username>
            <password>****</password>
        </server>
        <server>
            <id>common-lib</id>
            <username>admin</username>
            <password>****</password>
        </server>
    </servers>
    <profiles>
        <profile>
            <id>nexus</id>
            <repositories>
                <repository>
                    <id>sw-central</id>
                    <url>https://nexus.dspace.kt.co.kr/repository/maven-public/</url>
                </repository>
                <repository>
                    <id>common-lib</id>
                    <url>http://nexus.dev.icis.kt.co.kr/repository/common-repository/</url>
                </repository>
            </repositories>
        </profile>
    </profiles>
    <activeProfiles>
        <activeProfile>nexus</activeProfile>
    </activeProfiles>
    <mirrors>
        <mirror>
            <id>sw-central</id>
            <mirrorOf>external:*,!common-lib</mirrorOf>
            <url>https://nexus.dspace.kt.co.kr/repository/maven-public/</url>
        </mirror>
        <mirror>
            <id>common-lib</id>
            <mirrorOf>common-lib</mirrorOf>
            <url>http://nexus.dev.icis.kt.co.kr/repository/common-repository/</url>
        </mirror>
    </mirrors>
</settings>
 

```

