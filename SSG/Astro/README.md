# Astro - Static Site Generator

## Astro란?

**Astro**는 콘텐츠 중심 웹사이트를 위한 차세대 Static Site Generator입니다.  
2022년 등장한 오픈소스 프레임워크로, **"Islands Architecture"** 를 기반으로 필요한 곳에만 JavaScript를 로드해 성능을 극대화합니다.

```
빌드 시 → 순수 HTML/CSS/JS 정적 파일 생성
런타임  → JavaScript 최소화 (필요한 컴포넌트만 활성화)
```

---

## 주요 특징

| 특징 | 내용 |
|------|------|
| **Zero JS by default** | 기본적으로 JavaScript 없음, 필요한 곳만 활성화 |
| **파일 기반 라우팅** | `src/pages/` 구조가 그대로 URL이 됨 |
| **Markdown 지원** | `.md` 파일을 HTML 페이지로 자동 변환 |
| **동적 라우팅** | `[...slug].astro` 로 모든 경로를 하나의 파일로 처리 |
| **프레임워크 무관** | React, Vue, Svelte 등 어떤 UI 프레임워크도 함께 사용 가능 |
| **빠른 빌드** | Vite 기반, HMR 지원 |

---

## 이 프로젝트 구조

```
SSG/Astro/
  docs/                       ← 원본 Markdown 파일 (frontmatter 없음)
    index.md
    01.개요/
      01.랜딩존이란.md
      02.설계원칙.md
    02.관리그룹/
    03.네트워킹/
    04.보안/
    05.운영/
  src/
    layouts/
      DocLayout.astro         ← 공통 레이아웃 (3단 구조: 사이드바 / 본문 / TOC)
    pages/
      [...slug].astro         ← docs/ 의 모든 .md 파일을 동적으로 처리
  astro.config.mjs
  package.json
  dist/                       ← 빌드 결과물 (배포 대상)
```

### 동작 방식

```
docs/*.md (순수 Markdown)
    │
    │  빌드 시 [...slug].astro 가 처리
    │   ├─ 파일 읽기
    │   ├─ # 제목 → title 자동 추출
    │   ├─ ## ### → TOC 자동 생성
    │   └─ .md 링크 → .html 변환
    ▼
dist/*.html (정적 HTML)
```

---

## 로컬 실행 명령

### 패키지 설치

```sh
npm install
```

### 개발 서버 (Hot Reload)

```sh
npm run dev
# http://localhost:4321
```

파일 저장 시 브라우저가 자동으로 새로고침됩니다.

### 정적 빌드

```sh
npm run build
# dist/ 폴더에 정적 파일 생성
```

### 빌드 결과 미리보기

```sh
# Astro 내장 preview 서버
npm run preview
# http://localhost:4321

# 또는 Python HTTP 서버 (npm 불필요)
python3 -m http.server 8080 --directory dist
# http://localhost:8080
```

---

## Git 관리 (.gitignore)

아래 항목들은 git에 포함되지 않습니다. clone 후 재생성이 필요합니다.

| 제외 항목 | 이유 | 재생성 방법 |
|----------|------|------------|
| `node_modules/` | npm 의존성 (용량 큼) | `npm install` |
| `package-lock.json` | 로컬 환경 의존적 | `npm install` 시 자동 생성 |
| `dist/` | 빌드 결과물 | `npm run build` |

### clone 후 초기 실행 순서

```sh
git clone <repo>
cd SSG/Astro

npm install       # 의존성 설치
npm run build     # dist/ 생성
npm run preview   # 확인
```

---

## Astro vs 다른 SSG 비교

| | Astro | MkDocs | VitePress | Jekyll |
|--|-------|--------|-----------|--------|
| 언어 | Node.js | Python | Node.js | Ruby |
| JS 번들 크기 | 최소 | 없음 | 중간 | 없음 |
| 커스텀 레이아웃 | ✅ 완전 자유 | △ 테마 범위 | △ Vue 기반 | △ Liquid |
| Markdown 상대경로 | ✅ | ✅ | ✅ | △ 플러그인 |
| file:// 직접 열기 | ❌ (서버 필요) | ✅ | ❌ | ✅ |
| Azure / AKS 배포 | ✅ | ✅ | ✅ | ✅ |
