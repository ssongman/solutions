



# 1. 개요

## 1) StackStorm이란?

StackStorm은 DevOps & SRE 자동화**에 강력한 기능을 제공하는 **이벤트 기반 자동화 플랫폼이다. 이벤트를 감지하고 대응하는 **Rules**, **Actions**, **Workflows**를 조합하여 IT 운영을 효율적으로 자동화할 수 있다.





## 2) StackStorm 주요 기능



**1️⃣ Event-Driven Automation (이벤트 기반 자동화)**

​	•	특정 이벤트가 발생하면 사전 정의된 액션을 자동 실행

​	•	예: 서버 장애 감지 시 자동으로 재부팅



**2️⃣ Rules (규칙)**

​	•	이벤트가 발생했을 때 어떤 액션을 실행할지 결정하는 규칙

​	•	예: “CPU 사용량 90% 초과” → “추가 VM 자동 생성”



**3️⃣ Actions (액션)**

​	•	실행 가능한 개별 작업 (스크립트, API 호출 등)

​	•	예: 서버 재시작, Slack 알림 전송



**4️⃣ Workflows (워크플로우)**

​	•	여러 개의 액션을 조합하여 자동화 프로세스 구성

​	•	예: 장애 감지 → 알림 전송 → 문제 해결 → 보고서 작성



**5️⃣ Packs (확장 모듈)**

​	•	StackStorm은 다양한 **Packs**(플러그인) 제공

​	•	AWS, Kubernetes, GitHub, Slack, Ansible 등과 쉽게 연동 가능



**6️⃣ API & CLI 지원**

​	•	REST API 및 CLI(Command Line Interface) 지원

​	•	다른 시스템과 쉽게 통합 가능



**7️⃣ RBAC (Role-Based Access Control)**

​	•	역할 기반 접근 제어 지원 (사용자별 권한 관리 가능)



**8️⃣ Web UI 제공**

​	•	시각적인 관리 대시보드를 제공하여 자동화 상태 확인 가능



## 3) StackStorm 아키텍처



StackStorm은 여러 개의 주요 컴포넌트로 구성됩니다.

1.	**st2sensorcontainer**: 이벤트를 감지하고 규칙에 따라 트리거 실행

2.	**st2rulesengine**: 트리거된 이벤트를 분석하고 규칙 적용

3.	**st2actionrunner**: 실행할 액션을 담당하는 컴포넌트

4.	**st2auth**: 인증 및 접근 제어 담당

5.	**st2api**: REST API를 제공하여 외부 시스템과 연동 가능

 6. **st2web**: Web UI 제공 (웹 기반 관리 도구)

    





# 2. Helm Install

Kubernetes에 **StackStorm**을 Helm Chart를 사용하여 설치한다.



## 1) Helm Chart

StackStorm Helm Chart는 공식적으로 stackstorm Helm Repo에서 제공된다.

```sh



$ helm repo add stackstorm https://helm.stackstorm.com/
  helm repo update



$ helm search repo stackstorm

NAME                            CHART VERSION   APP VERSION     DESCRIPTION
stackstorm/stackstorm-ha        1.1.0           3.8             StackStorm K8s Helm Chart, optimized for runnin...
stackstorm/stackstorm           0.60.0          3.6.0           StackStorm - IFTTT for DevOps and SREs


# values.yaml 추출
$ helm show values stackstorm/stackstorm-ha --repo https://helm.stackstorm.com/
$ helm show values stackstorm/stackstorm-ha > 11.st_values.yaml

```





## 2) StackStorm 설치



```sh


kubectl create namespace stackstorm


# install
helm -n stackstorm upgrade --install st2 stackstorm/stackstorm-ha \
 --set st2.username=st2admin \
 --set st2chatops.enabled=false \
 --set ingress.enabled=true \
 --set ingress.ingressClassName=traefik \
 --set ingress.hosts[0].host=st2.ssongman.com \
 --set ingress.hosts[0].paths[0].path="/" \
 --set ingress.hosts[0].paths[0].serviceName="st2-st2web" \
 --set ingress.hosts[0].paths[0].servicePort="80"


# [기타]---------------------------------
helm install st2 stackstorm/stackstorm --namespace stackstorm \
 --set service.api.type=NodePort \
 --set service.auth.type=NodePort

 --set ingress.enabled=true \
 --set ingress.ingressClassName=traefik \
 --set ingress.hosts[0].host=st2.example.com \
 --set ingress.hosts[0].paths[0].path="/" \
 --set ingress.hosts[0].paths[0].serviceName="st2-st2web" \
 --set ingress.hosts[0].paths[0].servicePort="80" \
# [기타]---------------------------------
 

Release "st2" has been upgraded. Happy Helming!
NAME: st2
LAST DEPLOYED: Sun Feb 16 14:26:32 2025
NAMESPACE: stackstorm
STATUS: deployed
REVISION: 2
NOTES:
Congratulations! You have just deployed StackStorm HA!

  ███████╗████████╗██████╗     ██╗  ██╗ █████╗      ██████╗ ██╗  ██╗
  ██╔════╝╚══██╔══╝╚════██╗    ██║  ██║██╔══██╗    ██╔═══██╗██║ ██╔╝
  ███████╗   ██║    █████╔╝    ███████║███████║    ██║   ██║█████╔╝
  ╚════██║   ██║   ██╔═══╝     ██╔══██║██╔══██║    ██║   ██║██╔═██╗
  ███████║   ██║   ███████╗    ██║  ██║██║  ██║    ╚██████╔╝██║  ██╗
  ╚══════╝   ╚═╝   ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝ ╚═╝  ╚═╝

1. Get the StackStorm Web UI URL:

export ST2WEB_IP=$(minikube ip 2>/dev/null || kubectl get nodes --namespace stackstorm -o jsonpath="{.items[0].status.addresses[0].address}")
export ST2WEB_PORT="$(kubectl get --namespace stackstorm -o jsonpath="{.spec.ports[0].nodePort}" services st2-st2web)"
echo http://${ST2WEB_IP}:${ST2WEB_PORT}/Ingress is enabled. You may access following endpoints:
  http://st2.ssongman.com/

2. Get the password needed to login:
kubectl get --namespace stackstorm -o jsonpath="{.data.ST2_AUTH_PASSWORD}" secret st2-st2-auth | base64 --decode

3. Login with this username and the password retrieved above:
username: st2admin

4. Use st2 CLI:
export ST2CLIENT=$(kubectl get --namespace stackstorm pod -l app.kubernetes.io/name=st2client,app.kubernetes.io/instance=st2 -o jsonpath="{.items[0].metadata.name}")
kubectl exec -it ${ST2CLIENT} --namespace stackstorm -- st2 --version

-----------------------------------------------------
Thanks for trying StackStorm!
Need help?
* Forum: https://forum.stackstorm.com/
* Slack: https://stackstorm.com/#community




# 확인1
helm -n stackstorm ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
st2     stackstorm      2               2025-02-16 14:26:32.530615165 +0900 KST deployed        stackstorm-ha-1.1.0     3.8




# 확인1
helm -n stackstorm history st2
REVISION        UPDATED                         STATUS          CHART                   APP VERSION     DESCRIPTION
1               Sun Feb 16 14:22:45 2025        superseded      stackstorm-ha-1.1.0     3.8             Release "st2" failed: 1 error occurred:
                                                                                                                * Ingress.extensions "st2-st2web-ingress" is invalid: [spec.rules[0].http.paths[0].backend.service.name: Required value, spec.rules[0].http.paths[0].backend: Requir...
2               Sun Feb 16 14:26:32 2025        deployed        stackstorm-ha-1.1.0     3.8             Upgrade complete

# values 확인
helm -n stackstorm get values st2 --revision 2



# 확인2
$ kubectl get pods -n stackstorm


NAME                 READY  STATUS  RESTARTS  AGE

st2-actionrunner-0          1/1   Running  0     2m

st2-api-7f7c98c4b4-wqf2n       1/1   Running  0     2m

st2-auth-67999fbb89-dbgk2      1/1   Running  0     2m

st2-rabbitmq-0            1/1   Running  0     2m

st2-postgresql-0           1/1   Running  0     2m


```





## 3) 삭제시...



```sh


$ helm -n stackstorm uninstall st2


```







# **4. StackStorm Web UI 접속**



```sh


http://st2.ssongman.com

stadmin / fRLHZLSO3Yjg
Nd0xOjDhoeQI
fRLHZLSO3Yjg




```





# **5. StackStorm CLI 사용**

https://docs.stackstorm.com/start.html



StackStorm CLI를 사용하려면 StackStorm Pod에 직접 접근할 수 있다.

```sh


# StackStorm Pod에 직접 접근
$ kubectl exec -it deployment/st2-st2client -n stackstorm -- /bin/bash



# CLI 실행 예제:
$ st2 --version
st2 3.8.1, on Python 3.8.10


$ st2 auth st2admin -p fRLHZLSO3Yjg

+----------+----------------------------------+
| Property | Value                            |
+----------+----------------------------------+
| user     | st2admin                         |
| token    | 28c0e44bdfdb4f4087efc28bed5441ea |
| expiry   | 2025-02-17T06:39:07.336300Z      |
+----------+----------------------------------+


$ st2 action list

+---------------------------------+---------+--------------------------------------------+
| ref                             | pack    | description                                |
+---------------------------------+---------+--------------------------------------------+
| chatops.format_execution_result | chatops | Format an execution result for chatops     |
| chatops.match                   | chatops | Match a string to an action alias          |
| chatops.match_and_execute       | chatops | Execute a chatops string to an action      |
|                                 |         | alias                                      |
| chatops.post_message            | chatops | Post a message to stream for chatops       |
| chatops.post_result             | chatops | Post an execution result to stream for     |




   st2 action list --pack=core
   st2 run core.local cmd=date
   st2 run core.local_sudo cmd='apt-get update' --tail
   st2 execution list





```





# 6. Hello World



StackStorm을 설치했으니, 간단한 **“Hello World”** 액션을 만들어 실행해 보자.



## 1) 생성



### (1) Pack 생성



먼저, StackStorm에서 액션을 관리하는 단위인 **Pack**을 생성해야 합니다.



**📌 Pack 디렉토리 생성**

```sh 

sudo mkdir -p /opt/stackstorm/packs/helloworld
sudo chown -R st2:st2 /opt/stackstorm/packs/helloworld
cd /opt/stackstorm/packs/helloworld

```





**📌 Pack 메타데이터 생성**

```sh

cat <<EOF | sudo tee /opt/stackstorm/packs/helloworld/pack.yaml
---
name: "helloworld"
description: "My first StackStorm pack"
version: "1.0.0"
author: "ssongman"
email: "ssongmantop@gmail.com"
EOF

```







### (2) 액션(Action) 생성



StackStorm의 액션은 Python 또는 Bash Script로 작성할 수 있습니다.



**📌 Hello World 액션 스크립트 생성**



```sh

mkdir -p /opt/stackstorm/packs/helloworld/actions

cat <<EOF | sudo tee /opt/stackstorm/packs/helloworld/actions/say_hello.py
import sys

def run(name="World"):
  return f"Hello, {name}!"

if __name__ == "__main__":
  name = sys.argv[1] if len(sys.argv) > 1 else "World"
  print(run(name))
EOF

```





**권한 변경**

```sh

sudo chown -R st2:st2 /opt/stackstorm/packs/helloworld
sudo chmod +x /opt/stackstorm/packs/helloworld/actions/say_hello.py

```







### (3) Action 등록



이제 작성한 액션을 StackStorm에 등록해야 합니다.



**📌 액션 메타데이터 생성**

```sh

cat <<EOF | sudo tee /opt/stackstorm/packs/helloworld/actions/say_hello.yaml
---
name: "say_hello"
pack: "helloworld"
description: "Say Hello to someone"
runner_type: "python-script"
entry_point: "say_hello.py"
parameters:
 name:
  type: "string"
  description: "Name to say hello"
  required: false
EOF

```





```sh

# Pack 등록
st2ctl reload

st2ctl reload --register-actions

# 다른 방식으로 등록
st2 action create /opt/stackstorm/packs/helloworld/actions/say_hello.yaml


# 액션 목록 확인
st2 action list | grep helloworld

| helloworld.say_hello | Say Hello to someone |

```





### (4) 액션 실행



이제 우리가 만든 “Hello World” 액션을 실행

```sh


# 기본 실행
$ st2 run helloworld.say_hello
id: 1234567890abcdef
status: succeeded
parameters: None
result:
 stdout: Hello, World!
 
 
```



```sh

# 이름을 지정하여 실행**
st2 run helloworld.say_hello name="StackStorm"
id: 0987654321abcdef
status: succeeded
parameters:
 name: StackStorm
result:
 stdout: Hello, StackStorm!
```





## 2) trouble shooting

```sh

root@st2-st2client-55fbb694fc-h6dhd:/opt/stackstorm/packs/helloworld# st2 run helloworld.say_hello

.
id: 67b1982ba65148275079b07d
action.ref: helloworld.say_hello
context.user: st2admin
parameters: None
status: failed
start_timestamp: Sun, 16 Feb 2025 07:47:55 UTC
end_timestamp: Sun, 16 Feb 2025 07:47:56 UTC
result:
  error: '
    The virtual environment (/opt/stackstorm/virtualenvs/helloworld) for pack "helloworld" does not exist. Normally this is
    created when you install a pack using "st2 pack install". If you installed your pack by some other
    means, you can create a new virtual environment using the command:
    "st2 run packs.setup_virtualenv packs=helloworld"
    '
  traceback: "  File "/opt/stackstorm/st2/lib/python3.8/site-packages/st2actions/container/base.py", line 132, in _do_run
    (status, result, context) = runner.run(action_params)
  File "/opt/stackstorm/st2/lib/python3.8/site-packages/python_runner/python_runner.py", line 154, in run
    raise Exception(msg)
"


```

이 오류 메시지는 helloworld **Pack의 가상 환경 (virtual environment, venv)이 존재하지 않아서 실행할 수 없다는 의미**.

StackStorm에서 Python 기반 액션을 실행하려면 각 Pack마다 별도의 가상 환경을 생성한다.



```sh

$ st2 run packs.setup_virtualenv packs=helloworld

```



