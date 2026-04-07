

# 20260407

## Take1. LB 연동



```

KT Cloud 에 VM 3개를 생성하여 MariaDB Galera Cluster 를 구성했어.

설치했던 이력은 아래와 같이 2개 파일이니 참고해.
Mariadb/GaleraCluster/10.Install/10.Init-set.md
Mariadb/GaleraCluster/10.Install/11.MariaDB-Galera.md

이제는 LB 를 만들고 싶어.

KT Cloud에서 LB 를 만들어서 붙이는 가이드가 필요해.

아래 파일에 작성해줘.
Mariadb/GaleraCluster/10.Install/15.LB연동.md



```





## Take2. Client설정

```sh

내 로컬에서 접속할 수 있도록 Docker 로 mariadb Client container 를 설치하는 가이드를 작성해줘.

sleep 365d 로 계속 유지 될 수 있도록 해줘.

작성 파일은 아래.
Mariadb/GaleraCluster/10.Install/21.Client설정.md




```





## Take3. 백업-복원

```sh

아래 DB를 백업 받고 복원 하는 테스트를 수행하자.

DB : loadtest

galera cluster 인 점을 고려하여 백업 및 복원하는 것을 가이드해줘.

아래 폴더에 작성해줘.
Mariadb/GaleraCluster/30.백업-복원




```

