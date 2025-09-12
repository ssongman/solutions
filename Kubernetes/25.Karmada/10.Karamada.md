# Karmada



# 1. Karmada 개요

Karmada(Kubernetes Armada) 는 멀티 클러스터 Kubernetes 관리 플랫폼

CNCF 산하 오픈소스 프로젝트이고, 여러 개의 쿠버네티스 클러스터를 마치 하나의 클러스터처럼 통합적으로 관리할 수 있게 함

Karmada는 쿠버네티스의 멀티 클러스터 버전 관리자

“쿠버네티스 하나로도 복잡한데, 여러 개를 묶어서 하나처럼 다루자”는 목적



- 이름 뜻: *Kubernetes* + *Armada* (함대, 여러 대의 배 → 여러 클러스터)
- 소속: CNCF Sandbox → 현재 Incubating 단계
- 목표: 멀티 클러스터 환경에서 애플리케이션과 리소스를 일관되게 배포·운영·관제





# 2. 주요 기능



## 1) 멀티 클러스터 관리

- 여러 개의 쿠버네티스 클러스터를 한 곳에서 등록 및 관리
- 클러스터 간 이질성(클라우드/온프레미스, 버전 차이 등) 추상화



## 2) Cross-Cluster 스케줄링

- 워크로드를 여러 클러스터에 자동 분산 배포
- 자원 상태(CPU, 메모리), 지리적 위치, 가용성 등을 고려한 스케줄링



## 3) 정책 기반 배포



- PropagationPolicy, OverridePolicy 등을 사용해 리소스를 어디, 어떻게 배포할지 정의
- 예: nginx를 모든 클러스터에 배포하되, 중국 리전에선 이미지 레지스트리 주소를 변경



## 4) 클러스터 게이트웨이 (Cluster Gateway)

- 멀티 클러스터 간 서비스 디스커버리 및 통신 지원
- 원격 클러스터의 서비스를 로컬에서 접근 가능



## 5) HA/DR(고가용성/재해복구)

- 클러스터 장애 시 다른 클러스터에서 워크로드 자동 복구 가능
- 지역 단위 DR 시나리오 구현 가능



## 6) 표준 Kubernetes API 호환

- kubectl 같은 기존 도구 그대로 사용 가능
- 새로운 CRD (예: PropagationPolicy, Cluster, Work)를 추가 제공





# 3. 아키텍처 (간단 버전)

- Karmada Control Plane: 중앙 제어(멀티클러스터 리소스 관리)
- Member Clusters: 실제 워크로드가 실행되는 개별 K8s 클러스터
- Karmada Agent: 각 클러스터와 Control Plane을 연결
- Policy Engine: 리소스 배포 규칙(Propagation/Override) 해석





# 4. 활용 시나리오

- 멀티 클라우드 (AWS, Azure, GCP, On-Premise 혼합)

- 글로벌 서비스 배포

  - 예: 미국 리전은 영어 서비스, 한국 리전은 한국어 서비스

- 리소스 최적화

  - 클러스터별 자원 여유분에 따라 워크로드 자동 분산

- 재해 복구

  - 특정 리전 장애 시 다른 클러스터로 Failover

  

