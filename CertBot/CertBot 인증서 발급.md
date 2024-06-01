#  CertBot 인증서 발급



DuckDNS를 사용하여 Let's Encrypt 와일드카드 인증서를 발급받고, Kubernetes 클러스터에서 Traefik Ingress에

TLS 를 적용해 보자.



## 1) Certbot 설치



```sh

sudo apt-get update
sudo apt-get install certbot

# DNS 제공자 에 맞는 
sudo apt-get install python3-certbot-dns-<YOUR_DNS_PROVIDER>
sudo apt-get install python3-certbot-dns-duckdns

# duckdns 는 없을듯 한데 ... 역시 없다.


```





## 2) **DuckDNS API 토큰 확인**



```

account: ssongmantop@gmail.com
type : free
token : b96c3111-1d68-447f-a66c-3d7ac69ab34d
token generated : 9 months ago
created date : 12 Aug 2023, 03:53:35

```





## 3) **DuckDNS 인증 정보 파일 생성**

```sh

$ cd ~/song/certbot

$ cat > duckdns.ini
dns_duckdns_token = b96c3111-1d68-447f-a66c-3d7ac69ab34d


$ ll
-rw-r--r-- 1 song song   57 Jun  2 02:13 duckdns.ini

$ chmod 600 duckdns.ini

$ ll
-rw------- 1 song song   57 Jun  2 02:13 duckdns.ini

```



### TXT Record 정보 추출

```sh

# digweb site 로 확인
https://www.digwebinterface.com/?hostnames=diopro.duckdns.org&type=TXT&ns=resolver&useresolver=8.8.4.4

# dig commander 로 확인
$ dig diopro.duckdns.org TXT

$ dig diopro.duckdns.org TXT

; <<>> DiG 9.18.18-0ubuntu0.22.04.2-Ubuntu <<>> diopro.duckdns.org TXT
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40265
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;diopro.duckdns.org.            IN      TXT

;; ANSWER SECTION:
diopro.duckdns.org.     60      IN      TXT     "YgbFXH6coU-xTaZp7dXHw6q5yBE-2PpS-CwmfN4QMRQ"

;; Query time: 208 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Sat Jun 01 22:43:54 UTC 2024
;; MSG SIZE  rcvd: 103

song@dio-bastion01:~$
song@dio-bastion01:~$
song@dio-bastion01:~$ dig www.diopro.duckdns.org TXT

; <<>> DiG 9.18.18-0ubuntu0.22.04.2-Ubuntu <<>> www.diopro.duckdns.org TXT
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 58939
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;www.diopro.duckdns.org.                IN      TXT

;; ANSWER SECTION:
www.diopro.duckdns.org. 60      IN      TXT     "YgbFXH6coU-xTaZp7dXHw6q5yBE-2PpS-CwmfN4QMRQ"

;; Query time: 236 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Sat Jun 01 22:44:15 UTC 2024
;; MSG SIZE  rcvd: 107


## TXT record는 아래 와 같다.
# "YgbFXH6coU-xTaZp7dXHw6q5yBE-2PpS-CwmfN4QMRQ"

```



### TXT Record API 확인

```sh

# 예제
https://www.duckdns.org/update?domains=<your-domain>&token=<your-token>&txt=<your-txt-record>


# browser 에서 확인
https://www.duckdns.org/update?domains=diopro.duckdns.org&token=b96c3111-1d68-447f-a66c-3d7ac69ab34d&txt=YgbFXH6coU-xTaZp7dXHw6q5yBE-2PpS-CwmfN4QMRQ

OK

```







## 4) Certbot 스크립트 준비

Certbot DNS 플러그인 스크립트 준비

### 실행파일 작성

```sh
$ cat > certbot-dns-duckdns.sh
#!/bin/bash

set -euo pipefail

# DuckDNS API token
TOKEN=$(grep dns_duckdns_token duckdns.ini | cut -d '=' -f 2 | tr -d ' ')

# Base domain for DuckDNS (e.g., diopro.duckdns.org)
BASE_DOMAIN="diopro.duckdns.org"

# Extract the subdomain from the CERTBOT_DOMAIN
if [[ "$CERTBOT_DOMAIN" == "$BASE_DOMAIN" ]]; then
  SUBDOMAIN=""
else
  SUBDOMAIN="${CERTBOT_DOMAIN%.$BASE_DOMAIN}"
fi

# Create the TXT record for DNS-01 challenge
if [[ -z "$SUBDOMAIN" ]]; then
  RESPONSE=$(curl -s "https://www.duckdns.org/update?domains=$BASE_DOMAIN&token=$TOKEN&txt=$CERTBOT_VALIDATION&verbose=true")
else
  RESPONSE=$(curl -s "https://www.duckdns.org/update?domains=$SUBDOMAIN&token=$TOKEN&txt=$CERTBOT_VALIDATION&verbose=true")
fi

echo "DuckDNS update response: $RESPONSE"

# Wait for DNS propagation
sleep 30


```



### 실행권한 부여

```sh

$ chmod +x certbot-dns-duckdns.sh

```



### 발급전 확인

```sh

$
  export CERTBOT_DOMAIN="diopro.duckdns.org"
  export CERTBOT_VALIDATION="YgbFXH6coU-xTaZp7dXHw6q5yBE-2PpS-CwmfN4QMRQ"
  ./certbot-dns-duckdns.sh


DuckDNS update response: OK
test-validation-string
UPDATED

```





## 5) **와일드카드 인증서 발급**

```sh

$ sudo certbot certonly \
  --manual \
  --preferred-challenges=dns \
  --manual-auth-hook ./certbot-dns-duckdns.sh \
  -d diopro.duckdns.org \
  -d *.diopro.duckdns.org \
  --agree-tos \
  --email ssongmantop@gmail.com \
  --non-interactive
  
```



### 로그

```
...
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Requesting a certificate for diopro.duckdns.org and *.diopro.duckdns.org

Hook '--manual-auth-hook' for diopro.duckdns.org ran with output:
 DuckDNS update response: OK
 YgbFXH6coU-xTaZp7dXHw6q5yBE-2PpS-CwmfN4QMRQ
 UPDATED

Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/diopro.duckdns.org/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/diopro.duckdns.org/privkey.pem
This certificate expires on 2024-08-30.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
If you like Certbot, please consider supporting our work by:
 * Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
 * Donating to EFF:                    https://eff.org/donate-le
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

```



## 6) **Kubernetes 시크릿 생성**

발급된 인증서를 Kubernetes 시크릿으로 생성합니다.

```sh
$ kubectl -n yjsong get secret

$ kubectl -n yjsong create secret tls dio-wildcard-cert \
  --cert=/home/song/song/certbot/fullchain.pem \
  --key=/home/song/song/certbot/privkey.pem
  

# 확인
$ kubectl -n yjsong get secret
NAME                TYPE                DATA   AGE
dio-wildcard-cert   kubernetes.io/tls   2      13s


```



## 7) **Ingress 리소스 구성**

Traefik Ingress 리소스에서 생성한 시크릿을 사용하도록 설정합니다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: userlist-ingress
  namespace: yjsong
  annotations:
    kubernetes.io/ingress.class: "traefik"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: traefik
  rules:
  - host: userlist.diopro.duckdns.org
    http:
      paths:
      - backend:
          service:
            name: userlist-svc
            port:
              number: 80
        path: /
        pathType: Prefix
  ## 아래 추가
  tls:
  - hosts:
    - '*.diopro.duckdns.org'
    secretName: dio-wildcard-cert

```



### 확인

```

https://userlist.diopro.duckdns.org

```

성공





## 8) 자동 갱신 설정

Certbot 인증서를 자동 갱신하도록 크론잡을 설정한다.

```sh

# 매일 0시에 수행하는 예제
echo "0 0 * * 0 certbot renew --manual-auth-hook ./certbot-dns-duckdns.sh --quiet --renew-hook 'kubectl create secret tls wildcard-cert --cert=/etc/letsencrypt/live/diopro.duckdns.org/fullchain.pem --key=/etc/letsencrypt/live/diopro.duckdns.org/privkey.pem --namespace default --dry-run'" | sudo tee -a /etc/crontab > /dev/null


```

