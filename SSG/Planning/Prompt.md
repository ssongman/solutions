



# 2026.04.07



## Take1. 



### #1

```
github에 저장되어 있는 markdown 파일을 static web app으로 변환하는 프로세스를 만들려고 해.

어떤 솔루션을 이용하면 좋을지 몇몇 방안을 알려줘.


```



### #2

```


웹서비스는 아래와 같이 2가지 방안을 고려하고 있어.

1) Azure Static Web Apps
2) AKS POD (nginx)

그러므로 github workflow 를 통해서 CI/CD 가 되어야 해


그리고 markdown 내부에서 상대 경로로 연결된 하위 문서들도 정확히 변환 될 수 있어야 해.


아래 4개 후보로 분석해보자.

Jekyll, Astro, mkdocs, VitePress

각각 장단점을 분석해줘.

Markdown변환/Planning 아래에 작성해줘.


```



### #3

```

mkdocs를 이용해서 markdown 파일을 static web app 으로 변환해보자.

SSG/MkDocs 하위에서 작업해줘.


먼저 샘플 markdown 문서가 필요하니 작성해줘.
markdown 내부에서 상대 경로로 연결된 하위 문서들도 필요해
전체 10개 정도의 문서파일이 있으면 좋을것 같아.
주제는 Azure 랜딩존에 대한 내용이면 좋겠다.

이렇게 만들어진 markdown 을 MkDocs 로 변환해서 Static Site 로 만들어 보자.



```

