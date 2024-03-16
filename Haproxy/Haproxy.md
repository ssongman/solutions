

# 1. 개요

haproxy 를 이용해서 proxy 설정을 해보자.



# 2. haproxy 설정





```sh

# song@bastion

$ cd ~/song/haproxy/userlist-haproxy

$ ll
-rw-rw-r-- 1 song song 2354 Jan  7 22:48 10.proxymox-proxy.yaml
-rw-rw-r-- 1 song song 1087 Jan  8 00:53 11.userlist-haproxy.yaml
-rw-rw-r-- 1 song song  670 Jan  8 00:54 12.proxymox-proxy-deploy.yaml
-rw-rw-r-- 1 song song  250 Jan  8 00:54 13.proxymox-proxy-svc.yaml
-rw-rw-r-- 1 song song 4779 Jan  7 23:57 21.proxymox-proxy-secret.yaml
-rw-rw-r-- 1 song song  434 Jan  8 00:55 22.proxymox-proxy-ingress.yaml



$ cat *
apiVersion: v1
kind: ConfigMap
metadata:
  name: proxymox-proxy-config
data:
  haproxy.cfg: |
    defaults
      mode            tcp          # 인스턴스가 처리할 프로토콜
      log             global
      option          tcplog       # tcp 로그 포맷 사용
      option          dontlognull  # null connection(health check용 connection)에 대한 로깅 활성화
      timeout connect 10s
      timeout client  30s          # client와의 연결 최대 유지 시간
      timeout server  30s          # server와의 연결 최대 유지 시간
    frontend front
      mode tcp
      bind *:8006
      option tcplog
      default_backend backend_server
      timeout client 1m
    backend backend_server
      mode    tcp                # proxying의 기능 수행만을 위해 tcp 모드로 설정
      balance roundrobin
      option  ssl-hello-chk      # ssl connection health check
      # server  web01 59.15.23.41:8006
      # server  web01 172.30.1.21:8006
      server  web01 userlist-svc:80
      timeout connect 10s
      timeout server 1m
---
apiVersion: v1
kind: Pod
metadata:
  name: proxymox-proxy
  labels:
    app: proxymox-proxy
spec:
  containers:
    - image: haproxy:2.3
      name: proxymox-proxy
      ports:
        - containerPort: 8006
      volumeMounts:
        - name: proxy-config
          mountPath: /usr/local/etc/haproxy/haproxy.cfg
          readOnly: true
          subPath: haproxy.cfg
  volumes:
    - name: proxy-config
      configMap:
        name: proxymox-proxy-config
---
apiVersion: v1
kind: Service
metadata:
  name: proxymox-proxy-svc
  labels:
    app: proxymox
  namespace: yjsong
spec:
  ports:
  - name: https
    port: 8006
    protocol: TCP
    targetPort: 8006
  selector:
    app: proxymox-proxy
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: proxymox-proxy-ingress
  namespace: yjsong
  labels:
    app.kubernetes.io/instance: proxymox-proxy
  annotations:
    ingress.kubernetes.io/ssl-passthrough: "true"
spec:
  ingressClassName: traefik
  rules:
  - host: proxymox-proxy.ssongman.duckdns.org
    http:
      paths:
      - backend:
          service:
            name: proxymox-proxy-svc
            port:
              number: 8006
        path: /
        pathType: Prefix
  tls:
  - hosts:
    - proxymox-proxy.ssongman.duckdns.org
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: proxymox-proxy-config
data:
  haproxy.cfg: |
    defaults
      mode            tcp          # 인스턴스가 처리할 프로토콜
      log             global
      option          tcplog       # tcp 로그 포맷 사용
      option          dontlognull  # null connection(health check용 connection)에 대한 로깅 활성화
      timeout connect 10s
      timeout client  30s          # client와의 연결 최대 유지 시간
      timeout server  30s          # server와의 연결 최대 유지 시간
    frontend front
      mode tcp
      bind *:8006
      option tcplog
      default_backend backend_server
      timeout client 1m
    backend backend_server
      mode    tcp                # proxying의 기능 수행만을 위해 tcp 모드로 설정
      balance roundrobin
      option  ssl-hello-chk      # ssl connection health check
      # server  web01 59.15.23.41:8006
      # server  web01 userlist.ssongman.duckdns.org:80
      server  web01 userlist-svc:80
      timeout connect 10s
      timeout server 1m
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: proxymox-proxy
  name: proxymox-proxy
spec:
  selector:
    matchLabels:
      app: proxymox-proxy
  strategy:
  template:
    metadata:
      labels:
        app: proxymox-proxy
    spec:
      containers:
        - image: haproxy:2.3
          name: proxymox-proxy
          ports:
            - containerPort: 8006
          volumeMounts:
            - name: proxy-config
              mountPath: /usr/local/etc/haproxy/haproxy.cfg
              readOnly: true
              subPath: haproxy.cfg
      volumes:
        - name: proxy-config
          configMap:
            name: proxymox-proxy-config
---
apiVersion: v1
kind: Service
metadata:
  name: proxymox-proxy-svc
  labels:
    app: proxymox
  namespace: yjsong
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 8006
  selector:
    app: proxymox-proxy
  type: ClusterIP
---
apiVersion: v1
kind: Secret
metadata:
  name: proxymox-proxy-tls
data:
  tls.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUUvRENDQXVTZ0F3SUJBZ0lCQVRBTkJna3Foa2lHOXcwQkFRc0ZBREIyTVNRd0lnWURWUVFEREJ0UWNtOTQKYlc5NElGWnBjblIxWVd3Z1JXNTJhWEp2Ym0xbGJuUXhMVEFyQmdOVkJBc01KRGM0WVRZd00yWmlMVEk0Tm1VdApORE5sT0MwNU5qQXpMVEZsT0RNeU9XVm1PVFZqWXpFZk1CMEdBMVVFQ2d3V1VGWkZJRU5zZFhOMFpYSWdUV0Z1CllXZGxjaUJEUVRBZUZ3MHlNekE0TVRFd09UUXlNRGRhRncweU5UQTRNVEF3T1RReU1EZGFNRnd4R1RBWEJnTlYKQkFzVEVGQldSU0JEYkhWemRHVnlJRTV2WkdVeEpEQWlCZ05WQkFvVEcxQnliM2h0YjNnZ1ZtbHlkSFZoYkNCRgpiblpwY205dWJXVnVkREVaTUJjR0ExVUVBeE1RY0habExuTnpiMjVuYldGdUxtTnZiVENDQVNJd0RRWUpLb1pJCmh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTGJGTnhSQ0lqeWx6MmhyZFlFQlBpdVNYdksydlp6OTlLakEKK01Nek1vK09UamZpcXkwV0gwLzI4NXRPa25jeTNEeXZabDV6Vm9Xb1Q4VVo5c3NVVlk4YmVtUUplMktHeWVBOApXZXlaaEV0Z2JLUjNUSzZpcEFVdUZUbTBSRGZuSERsSHBJb2dMeWdmdlAzN29sc0M0QVd4YXdkbGJzMUZHMHdVCi9XR3h0aE1XUmh2MVhHSUViMlJlbEV0OG1EYThzbGRTZWRuNkZSYkFPYVVQSzRSMG80UVFhc3JDcXNhbE5iV0oKa21SZDJ6VmZDZzhob1B6Z05weFNJRU52Wkc2MU1LNTFPZ01ORUQvOVN5RFJMK2Y1S3B2Zmx0emFBNGVucG1NUgp4T2JGaFZ6ZER4V01iZmNxbDY1ZEc0UGRyZ2VTTlpaTjJiOEF3TXQ0Zkx0aHhQdnZhU3NDQXdFQUFhT0JyakNCCnF6QUpCZ05WSFJNRUFqQUFNQk1HQTFVZEpRUU1NQW9HQ0NzR0FRVUZCd01CTUVrR0ExVWRFUVJDTUVDSEJIOEEKQUFHSEVBQUFBQUFBQUFBQUFBQUFBQUFBQUFHQ0NXeHZZMkZzYUc5emRJY0VyQjRCRllJRGNIWmxnaEJ3ZG1VdQpjM052Ym1kdFlXNHVZMjl0TUIwR0ExVWREZ1FXQkJUYlprZVVFdWFMTjVReDFrMk50SW8wT05iWVdEQWZCZ05WCkhTTUVHREFXZ0JRQjRaaEEvQUNNaGpMdG5BOVpZalBzTit5VUR6QU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FnRUEKbWxWOFJGQzJSTlRnYkFKdW9aTGs0dHo5YzlPTy8xakFWMkp6MjBhZWxSd1ZtVDRhdWRjaGxmTDg5Tm9ESzlVdwpRN3lFTUxxKzkrMFJra0NoNFJMbHNoWDFsblJjWHM1cGR3R1k4c2l1ZXc4dWswV2FLNkZLdm5mTTVXTDJicE1NCmVMYUJCWW8wdUxhTmZTVTJORjU1MU9majlGU3I3MGgvNjZwM2N4NWRTaHYrTG1vRDF0MldEdytHVW5IRm1JWDMKdU9UOXRlaGptQmVDTS9IMWZnTXVCbmhwbUpnQlhWS0hXRFoyZTQ2cmIxSUZkS2VHcDYyTUxad3hmNnZzMnM0OAp5dDREcUxMSDlSUUswa0tjN3h6RDVGTThwQjBzNVFzcnNPU1M2MVlqdVpPNHRwcm9DR3kzSkJCM25WcndCaGJHClQyNW5EckNHM0FoWDI2SWxzYlNDbHpDMFpDbjZpSEQvQWhiUkZWeXAvRjBRczBjZE5rczVKanR5QjVqN1JyRlYKM0xrZFlKU0o2QzdiZ1VuUHpCVHF3NDE1elVYUGk4MWhsNFd1SWtGVjlRTUVTbTNXVEVsWDlGWkxVMFpRSVd5ZgppYVR5QWo5Sk5TT2xMeURiNVc2LzlCcG9TSnF4Q0JWN2VCMFZVWEJQZU1DNmRUQXZrS3V0bHVZRXlJYTYrWXNzCk1waHJZRVlWYk40TmlRS3FkQWxzTVd4MFdPNDZsTitUdXdGU0dkaC9VS3N4WlZXa0VaOC9TYkhSM1J0a3FwVnYKU2Y2Z0RvK3Q1RDNvRjBiOTE5SlZGYnUzcG94Y1Z2ejcvY1Z2ZGt5T3hSUnhKWktPZDM3a0NDZ2srRlYvcUcrWApEdkhLc1pFS01iRTAzK01iaGVPSjl6RzdOc3F3T3ZaaUVCTGRjZkcvYVc0PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
  tls.key: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2UUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktjd2dnU2pBZ0VBQW9JQkFRQzNiU2NlajNQWGpLbFIKVTE3b3Vpd3hxNmtpQmx3cDgrd2RGTGh2VE8zSTQ5VWY1VENSeXVxaXZZcWo2TGFuYWFPSXR4K0g2RE5CaWdtaApIbkIzZndXRDdYZGxqZ29SM2ZtLzhUNUpqNmZseG9DMHJTZEZ1MXd3ZTc1bExiZm53TEl2OGdvMVk5K1ltS01qCkwwelpVWVRremttYWhiOHhNcUdDNVg3cHlXRVBXQ3FkWm1tWWl5a0tuT0NQa21NK3pycUF0MDBRZVcyeFM2UXEKNDdIT3lqaTM0SUFnTlNQQW8rRlEraHY1aXdwQklZNngrbkdKT0tNdmhyZjZLOVBZeDRYUDQ4Y2tsTXgyeXprZQplWG9qcU9hQ0hYdnF1TzZFeExVdUVsbkNXbUtxeU1ISjN2M1RqSTA5bEJCT3dWazlvVlR0VUw4RXVzdGhWM0w3CndxNmR2ODV4QWdNQkFBRUNnZ0VBQVh0aXlRYnNyeTJtUW85ellWcjd0MjBGSVU2KzJPSHRJdkVEYW5iTEp3ZmMKTlhWREZySjJnZGtaTVNqVXJQYVlDU2M5bkhuK1RBWEMvU2ZEVGR2YlhnMEJuWEx2MXVRZHUvVEZoWStoRWlTdgo3b1hGbnZVY0VoSTE0QmhsOTN2aGxLeVdjNGI2aS8rVHRkbVFlK01DT1YwSFVEWExiU2pWRURzdGN0TWJNeVlHCk0zZitxbHJCS1RkNU5sS3hGR3N1dHVPM1NYTXE1YUZaNmJiVG1mNmh4VzJvSXZKKzlQL2haZDRjRHl2SDR2RDQKK0xVN3RtckVUdUcyMzhROHdmMzVoVVQ1OEFVSXdvelRPSGJqbitzVUk0Q2dTdmsvQUZGZTdzbVlTWGVnS05lMgorVUVmRG5ycUNtUkEzNy9wb2VkN1RhRjZleWhDdmtNOXFES0xWbFYvQVFLQmdRRG9rSHQvTzRZKzBMQUxRRGgzClZsZnBDdW1uZjFIOFlmeVN6REF1VUtySmZVUHNiQ1llaWtJZEttOVJ6c1VEQlNId0NVVVJQUWJYNDVBdXVzSTYKYTQreHJuS3MwMEFzRWxhQ0Fad01GWEl2SUoxR1MwUHlZTjBTY2J3Vnl1OEVYTEhvR1dQWmpkVndWM3RGWFFFTgo3RDk4djA4T2lGMU5Lb3pCbEozeEJ6M1NJUUtCZ1FESjZRdTZGclpYdjB5WWZaSFBWR1RkZ3lIdGhreEN3SkJRCjZrOUlISmIzVEVzVWY4ZURLT3hVMU5UTDl4NTU4OG1EUVdNNVRpTnNPTnJhdVBQY2hNdkVEdFJiV05hTHpjLzIKRVBkK2xqYXdWTTFzTlJMYUJqdWpvRWcxYnFOajRWNUFjVmQwdU12a2JSWUJWWE04cVJQbm1MZm54eS9hVGdHYgpNV0ZtWVNvU1VRS0JnQjVPL2hsRnk2Z1NFRzlXN2tUM05ydkRWVklqOEs1Z29zY0szMWlaNExnam9CK0d0SzBVClBhdUpaVHFYSk92UTFteHUrTlpYU3JZR0RUdFowWWhGamxPTXRaczZhTW1WbGpxWk5Sb0tEWGlBMnA1WG5zSk8KeDJEbys2Y25iR0Q0SjZOazg3TmRuYXhuYWtSTzY1MUI1Y0EvT25GZGFqTnRVU3pGVHBRajZuV2hBb0dCQUtDcgpnVGh3MEdNZENGK2tOTDV1WXVGZWMwWW5BMUp2RjZnNy9DRGZGMGJ0QUNYczFKL0xsZHlmakVKT2dJTDgreE1tCm1rWEVweTE4UkxPZVQvZmYrS0lvUnRYMTZLeFJkN1pRcEJHb2lSWmlOU0Z4VG5JT1diRUlYODJkSUFuZ0VmZG4KK2ZjWkFxN2dHNDJ1S01oUnAxUTVVOGJ0MjJkMWdaTzBoTlJLWjRjeEFvR0FBYmYxWmVoSFpIQmVuN2YrMWFiUQo3Y3JZQUg0aEZiUE03TnZGbm0xYVZxQW1WZERsT3hkeTZuOFdrdjdsWVRtNW9aQWg1MkNEM0pOYlpWOTEya0NICnJCelVhU21DWnV2TXhRT1l1WFBNVXJwek1sZWY5cEIzWHViSW03ajgrbk1PYjNZcG1nQzNWajdDaCt3NE0wdlEKTUtoRXVDY1hyVE5tQUlBQ0VSdXJyeU09Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K
type: kubernetes.io/tls
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: proxymox-proxy-ingress
  namespace: yjsong
  labels:
    app.kubernetes.io/instance: proxymox-proxy
spec:
  ingressClassName: traefik
  rules:
  - host: proxymox-proxy.ssongman.duckdns.org
    http:
      paths:
      - backend:
          service:
            name: proxymox-proxy-svc
            port:
              number: 80
        path: /
        pathType: Prefix




```

