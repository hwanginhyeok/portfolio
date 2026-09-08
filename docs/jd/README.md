# docs/jd/ — 지원 회사 JD 관리 디렉토리

> 운영 원칙 최초 작성: 2026-05-04

## 디렉토리 구조

```
docs/jd/
├── README.md          ← 이 파일 (운영 원칙)
├── apple/             ← Apple Korea · Reliability Engineer
│   ├── APPLY.md
│   ├── JD_분석_Apple_Reliability_Engineer.md
│   └── materials/     ← resume_en.md 등
└── nearlab/           ← 니어스랩 · 임베디드/전장 엔지니어
    ├── README.md
    ├── APPLY.md
    ├── JD_매핑_니어스랩.md
    ├── 회사_직무_이해.md
    └── materials/
```

## 운영 원칙

### 원칙 1 — 회사별 디렉토리 완전 분리

지원하는 모든 회사는 `docs/jd/{회사}/` 디렉토리를 독립적으로 운영한다.
JD 분석, 자산 매핑, 면접 준비, 지원 트래킹은 **해당 디렉토리 내부에서만** 처리.
회사 간 파일 공유 금지 (중복이 생겨도 독립 관리가 SSOT 원칙에 부합).

### 원칙 2 — 포트폴리오 메인 사이트는 황인혁 본인의 정체성

`src/pages/` (메인 사이트)는 **모든 회사에 공통 노출되는 원본**이다.
회사별 JD에 맞춘 재정렬·재가공·번역 콘텐츠는 메인 사이트에 반영하지 않는다.
회사 맞춤 콘텐츠는 `docs/jd/{회사}/` 에서만 운영한다.

→ 메인 사이트가 특정 회사 JD에 끌려다니면 다른 회사에 어필할 때 일관성이 깨진다.

## 지원 이력 SSOT

지원 여부·지원일·다음 행동은 **[`applications.json`](applications.json)** 하나에서만 관리한다.
사람이 읽는 표는 [`APPLICATIONS.md`](APPLICATIONS.md)이며 `scripts/applications_report.py`가
자동 생성한다 — 직접 고치지 말 것. 매일 11:47 비서봇으로 같은 내용이 전송된다.

각 회사 디렉토리의 `APPLY.md`는 **그 회사의 지원 절차와 서류**를 담고, 상태 값은 담지 않는다.

## 현재 지원 디렉토리

| 회사 | 포지션 | 상태 |
|------|--------|:----:|
| [apple/](apple/) | Reliability Engineer, Core Technology Operations | 🔵 지원서 준비 완료 (JD-A3 제출 대기) |
| [aptiv/](aptiv/) | Manufacturing Engineering Engineer (아산) / CC Mfg. Engineer (울산) | 🟡 국문 이력서 완료, 근무지 결정 대기 |
| [tesla/](tesla/) | Field Support Engineer, Dongtan | 🔵 매핑·이력서 초안 완료, 제출 결정 대기 |
| [nvidia/](nvidia/) | Senior Automotive Software Program Manager | 🟠 매핑 완료 — 필수 요건 미달, 보류 권고 |
| [nearlab/](nearlab/) | 임베디드/전장 엔지니어 | 🟡 JD URL 미확보, 면접 자료 완료 |
| [xai/](xai/) | Mechanical Engineering Tutor | ✅ 제출 완료 (2026-05-15) |

## 신규 회사 추가 방법

```
mkdir docs/jd/{회사}/
mkdir docs/jd/{회사}/materials/
touch docs/jd/{회사}/materials/.gitkeep
# 파일 생성: README.md, APPLY.md, JD_매핑_{회사}.md
# CLAUDE.md docs/jd/README.md 테이블 갱신
```
