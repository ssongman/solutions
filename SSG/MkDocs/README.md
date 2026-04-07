# MkDocs - Static Site Generator

## MkDocs란?

**MkDocs**는 Markdown 파일을 정적 문서 사이트로 변환하는 Python 기반 Static Site Generator입니다.  
설정 파일(`mkdocs.yml`) 하나로 전체 사이트 구조를 정의하며, **Material for MkDocs** 테마를 사용하면 깔끔한 문서 사이트를 빠르게 구성할 수 있습니다.

---

## 이 프로젝트 구조

```
SSG/MkDocs/
  mkdocs.yml        ← 사이트 설정 (테마, 네비게이션, 플러그인 등)
  docs/             ← 원본 Markdown 파일 (편집 대상)
    index.md
    01.개요/
      01.랜딩존이란.md
      02.설계원칙.md
    02.관리그룹/
    03.네트워킹/
    04.보안/
    05.운영/
  site/             ← 빌드 결과물 (배포 대상, git 제외)
```

---

## 사전 준비 (설치)

```sh
pip3 install mkdocs-material
```

> `mkdocs-material` 을 설치하면 `mkdocs` 본체도 함께 설치됩니다.

설치 확인:

```sh
$ mkdocs --version

mkdocs, version 1.6.1 from /opt/homebrew/lib/python3.13/site-packages/mkdocs (Python 3.13)
```

---

## 로컬 실행 명령

### 개발 서버 (Hot Reload)

```sh
cd SSG/MkDocs
mkdocs serve
# http://127.0.0.1:8000
```

Markdown 파일 저장 시 브라우저가 자동으로 새로고침됩니다.

### 정적 빌드

```sh
cd SSG/MkDocs
mkdocs build
# docs/ → site/ 로 HTML 변환
```

빌드 후 `site/` 폴더의 `index.html` 을 브라우저에서 직접 열 수 있습니다.

```sh
open site/index.html   # macOS
```

---

## mkdocs serve 의 실체

`mkdocs serve` 는 Python 내장 라이브러리인 **`http.server` + `watchdog`** 조합으로 동작합니다.

```sh
mkdocs serve
# 내부적으로: Python http.server (포트 8000) + watchdog (파일 변경 감지)
```

### 익숙한 서버들과 비교

| | mkdocs serve | nginx | FastAPI (uvicorn) | npm run dev (Vite) |
|--|--|--|--|--|
| **언어** | Python | C | Python | Node.js |
| **역할** | 개발용 정적 서버 | 프로덕션 정적/프록시 서버 | 동적 API 서버 | 개발용 정적 서버 |
| **정적 파일 서빙** | ✅ | ✅ | △ | ✅ |
| **Hot Reload** | ✅ | ❌ | ❌ | ✅ |
| **프로덕션 사용** | ❌ | ✅ | ✅ | ❌ |
| **동적 처리** | ❌ | △ (모듈로 가능) | ✅ | ❌ |
| **성능** | 낮음 (단일 스레드) | 매우 높음 | 높음 | 중간 |

### 핵심 차이

```
mkdocs serve / npm run dev
  → "개발 편의용" 서버
  → Hot Reload (파일 저장 시 자동 반영)
  → 단일 사용자 로컬 전용
  → 프로덕션 절대 사용 금지

nginx / Apache
  → "프로덕션용" 서버
  → 정적 파일을 빠르고 안정적으로 다수 클라이언트에게 서빙
  → mkdocs build 결과물(site/)을 올리는 대상
```

### 실제 배포 흐름

```
[개발 중]
  mkdocs serve  → Python http.server 가 docs/ 를 실시간 변환해서 서빙

[배포 시]
  mkdocs build  → site/ 생성
                     └→ nginx / Azure Static Web Apps / AKS 에 올림
```

---

## MkDocs vs 다른 SSG 비교

| | MkDocs | Astro | VitePress | Jekyll |
|--|--------|-------|-----------|--------|
| 언어 | Python | Node.js | Node.js | Ruby |
| 문서 특화 | ✅ | △ | ✅ | △ |
| 설정 난이도 | 낮음 | 중간 | 중간 | 낮음 |
| 사이드바 자동 생성 | ✅ | ❌ | △ | ❌ |
| Markdown 상대경로 | ✅ | ✅ | ✅ | △ |
| `file://` 직접 열기 | ✅ | ❌ | ❌ | ✅ |
| Azure / AKS 배포 | ✅ | ✅ | ✅ | ✅ |
