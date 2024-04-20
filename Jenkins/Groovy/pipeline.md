# pipeline



# 1. Pipeline



### 1) **Declarative VS Scripted Pipeline syntax**

Jenkinsfile은 두 형태의 구분을 사용하여 쓰여질 수 있다.

  

| 구분        | 장단점                                                       |
| ----------- | ------------------------------------------------------------ |
| Declarative | 보다 쉽게 작성할 수 있고, 커스텀 되어 있다. Groovy 몰라도 쓸 수 있다. 젠킨스 파이프라인의 최신 기능이다. 더 가독성이 좋다. |
| Scripted    | Groovy 기반, Declarative 보다 효과적으로 많은 기능 포함하여 작성 가능하지만, Groovy를 잘알아야 함. Scripted 파이프라인 구문보다 풍부한 구문 기능을 제공한다. |





## 1) Sample



### (1) job1-Declarative

선언적 파이프라인 구문에서, pipeline 블록은 전체 파이프라인 내내 완료된 모든 작업을 정의한다. 

```
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any //1
    stages {
        stage('Build') { //2
            steps {
                // 3
                echo 'Build'
            }
        }
        stage('Test') { //4
            steps {
                // 5
                echo 'Test'
            }
        }
        stage('Deploy') { //6
            steps {
                // 7
                echo 'Deploy'
            }
        }
    }
}
```

1. 이용가능한 agent가 이 파이프라인 또는 파이프라인의 어느 스테이지를 실행한다.
   1. "agent" 키워드는 반드시 있어야 하며, 파이프라인에 대한 수행 및 작업 공간을 할당한다. agent가 없으면 선언적 파이프라인이 유효하지 않으며, 어떠한 작업도 수행할 수 없다. 
2. "Bulid" 스테이지를 정의한다.
3. 빌드와 관련된 몇가지 스텝을 수행한다.
4. "Test" 스테이지를 정의한다.
5. 테스트와 관련된 몇 가지 스텝을 수행한다.
6. "Deploy" 스테이지를 정의한다.
7. 배포와 관련된 몇 가지 스텝을 수행한다.





### (2) job2-Scripted

스크립트 파이프라인 구문에서, 하나이상의 node 블럭이 핵심 작업을 파이프라인 내내 수행한다. 비록 스크립트 파이프라인 구문의 의무적인 요구는 아니지만, 파이프라인의 작업을 node 블록 내부로 제한하면 두 가지 작업이 수행된다.

- Jenkins 대기열에 항목을 추가하여 실행할 블록에 포함된 단계를 예약한다. 실행기가 노드에서 사용가능하게 되면 단계가 실행된다.
- 소스 제어에서 체크 아웃된파일에서 작업을 수행할 수 있는 작업공간을 만든다.

```groovy
node {         // 사용 가능한 에이전트에서 이 파이프라인 또는 해당 단계를 실행
    stage('Build') { 
        //
        sh 'echo Build'
    }
    stage('Test') { 
        // 
        sh 'echo Test'
    }
    stage('Deploy') { 
        // 
        sh 'echo Deploy'
    }
}

```







# 2. kubernetes pod template

참조링크 : https://plugins.jenkins.io/kubernetes/



jenkins slave 를 pod 로 수행하기 위해서는 pod template을 사전에 정의해 놓은후   node(POD_LABEL) 처럼 사용한다.



## 1) 기본 형식

### (1) sample1

```groovy

podTemplate {
    node(POD_LABEL) {
        stage('Run shell') {
            sh 'echo hello world'
        }
    }
}
```



### (2) template 추가

사용되는 기본 jnlp 에이전트 이미지는 템플릿에 추가하여 사용자 정의할 수 있다.

```groovy
containerTemplate(name: 'jnlp', image: 'jenkins/inbound-agent', args: '${computer.jnlpmac} ${computer.name}'),
```



또는 yaml 구문을 사용한다. pod 모델의 거의 모든 필드는 yaml 구문을 통해 지정할 수 있다.

```groovy
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: 'jenkins/inbound-agent'
    args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
```



### (3) Multiple containers

```groovy

podTemplate(containers: [
    containerTemplate(name: 'maven', image: 'maven:3.8.1-jdk-8', command: 'sleep', args: '99d'),
    containerTemplate(name: 'golang', image: 'golang:1.16.5', command: 'sleep', args: '99d')
  ]) {

    node(POD_LABEL) {
        stage('Get a Maven project') {
            git 'https://github.com/jenkinsci/kubernetes-plugin.git'
            container('maven') {
                stage('Build a Maven project') {
                    sh 'mvn -B -ntp clean install'
                }
            }
        }

        stage('Get a Golang project') {
            git url: 'https://github.com/hashicorp/terraform.git', branch: 'main'
            container('golang') {
                stage('Build a Go project') {
                    sh '''
                    mkdir -p /go/src/github.com/hashicorp
                    ln -s `pwd` /go/src/github.com/hashicorp/terraform
                    cd /go/src/github.com/hashicorp/terraform && make
                    '''
                }
            }
        }

    }
}

```

or

```groovy

podTemplate(yaml: '''
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: maven
        image: maven:3.8.1-jdk-8
        command:
        - sleep
        args:
        - 99d
      - name: golang
        image: golang:1.16.5
        command:
        - sleep
        args:
        - 99d
''') {
  node(POD_LABEL) {
    stage('Get a Maven project') {
      git 'https://github.com/jenkinsci/kubernetes-plugin.git'
      container('maven') {
        stage('Build a Maven project') {
          sh 'mvn -B -ntp clean install'
        }
      }
    }

    stage('Get a Golang project') {
      git url: 'https://github.com/hashicorp/terraform-provider-google.git', branch: 'main'
      container('golang') {
        stage('Build a Go project') {
          sh '''
            mkdir -p /go/src/github.com/hashicorp
            ln -s `pwd` /go/src/github.com/hashicorp/terraform
            cd /go/src/github.com/hashicorp/terraform && make
          '''
        }
      }
    }

  }
}

```





## 2) Sample

### 

https://plugins.jenkins.io/kubernetes/



### sample1

```sh

def label = "jenkins-agent-${UUID.randomUUID().toString()}"

podTemplate(label: label, serviceAccount: G_SA, namespace: G_NAMESPACE, 
containers: [
    containerTemplate(name: 'maven', image: 'maven:3.8.1-jdk-8', command: 'sleep', args: '99d'),
    containerTemplate(name: 'golang', image: 'golang:1.16.5', command: 'sleep', args: '99d')
  ]) {
    node('jenkins-agent') {
        stage('Run shell1') {
            sh 'echo hello world'
        }
        stage('Run shell2') {
            container('jnlp') {
                stage('Build a Maven project') {
                    sh 'echo hello world2'
                }
            }
        }
    }
}

```



### sample2

```groovy
podTemplate(containers: [
    containerTemplate(name: 'maven', image: 'maven:3.8.1-jdk-8', command: 'sleep', args: '99d'),
    containerTemplate(name: 'golang', image: 'golang:1.16.5', command: 'sleep', args: '99d')
  ]) {

    node('jenkins-agent') {
        stage('Get a Maven project') {
            git 'https://github.com/jenkinsci/kubernetes-plugin.git'
            container('maven') {
                stage('Build a Maven project') {
                    sh 'mvn -B -ntp clean install'
                }
            }
        }

        stage('Get a Golang project') {
            git url: 'https://github.com/hashicorp/terraform.git', branch: 'main'
            container('golang') {
                stage('Build a Go project') {
                    sh '''
                    mkdir -p /go/src/github.com/hashicorp
                    ln -s `pwd` /go/src/github.com/hashicorp/terraform
                    cd /go/src/github.com/hashicorp/terraform && make
                    '''
                }
            }
        }

    }
}

```



```groovy
podTemplate(label: 'hello',
	containers: [
        containerTemplate(name: 'maven', image: 'maven:alpine', ttyEnabled: true, command: 'cat'),
        containerTemplate(name: 'busybox', image: 'busybox', ttyEnabled: true, command: 'cat')
  ]) {

    node('hello') {
        stage('Maven') {
            container('maven') {
                    sh 'mvn -version'
               
            }
        }

        stage('Busybox') {
            container('busybox') {
                    sh '/bin/busybox'
            }
        }
    }
}
```





```groovy
pipeline {
  agent {
    kubernetes {
      label 'hello'
      yamlFile 'hello-pod-template.yaml'
    }
  }
    stages {
        stage('Maven') {
          steps {
            container('maven') {
              sh 'mvn -version'
            }
          }
        }
        stage('Busybox') {
            steps {
                container('busybox') {
                    sh '/bin/busybox'
                }
            }
        }
    }
}

```



