# B5-02 GitHub 프로필 정비 가이드

> 최종 작성: 2026-04-26 (B5-02 신규)
> 위치: `docs/blocks/05-extra/GITHUB_PROFILE.md`
> 입력 SSOT:
> - `docs/포트폴리오/EXPERT_REVIEW_20260426.md` §4 (스타트업 갭: GitHub 활동 위젯 / 사이드 프로젝트 demo URL / AI 자동화 절약시간)
> - `docs/blocks/02-usage/USAGE_STRATEGY.md` §2.1 (메시지 후보 MC-A ~ MC-H)
> - `docs/blocks/03-layout/LAYOUT.md` §1 (5섹션 와이어프레임 + Footer GitHub 링크)
> - `src/pages/index.astro` 사이드 프로젝트 3종 (자율주행 ROS2+Gazebo · AI 개발 자동화 · 포트폴리오)
> - GitHub: `hwanginhyeok` / `dlsgur5560@gmail.com`
>
> **목표**: 채용담당자가 GitHub만 봐도 포트폴리오 사이트와 동일 인상. EXPERT_REVIEW 스타트업 도메인 갭(활동 위젯/demo URL/AI 절약시간)을 GitHub 측에서 직접 메운다.

---

## §0. 문서 구조

본 문서는 **가이드 + 체크리스트** 형식이다.

- §1 GitHub 프로필 README 템플릿 (KO/EN)
- §2 핀 레포 6개 슬롯 선택
- §3 레포별 README 표준 양식
- §4 GitHub 활동 정량화 (placeholder + 갱신 정책)
- §5 사이트 ↔ GitHub 링크 정책
- §6 비공개 자료 가이드 (영업 비밀 / 회사 IP)
- §7 우선 작업 순서 (P1~P3)

각 섹션 머리에 **"이 항목이 중요한 이유"**를 EXPERT_REVIEW 도메인 갭과 연결해 명시한다.

---

## §1. GitHub 프로필 README 템플릿

### 1.0 이 항목이 중요한 이유

EXPERT_REVIEW §4 스타트업 갭 1순위가 "사업 임팩트 정량 부재"이고, 그 다음이 "사이드 프로젝트 demo URL/GitHub 임팩트 없음"이다. 프로필 README는 **GitHub 첫 방문 5초 안에 사이트와 동일 메시지**를 전달해야 ATS 수동 검토 단계에서 톤이 흔들리지 않는다.

> 핵심 원칙: **사이트 Hero 카피와 GitHub 헤드라인은 같은 문장이어야 한다.** 다르면 채용자는 둘 중 어느 것이 진짜인지 의심한다.

### 1.1 한국어 버전 (기본)

레포 생성: `https://github.com/hwanginhyeok/hwanginhyeok` (사용자명 = 레포명 → 자동으로 프로필 README가 됨)

```markdown
# 황인혁 · 물리 세계의 문제를 데이터로 해결하는 엔지니어

> Full-stack Hardware · 0→1 Builder · AI-Augmented
> EOP 모터 제어 / GT-SS500 양산 PM / IEEE TIM 공저 / AI 워크플로우 설계자

## 지금 작업 중

- 자율주행 모빌리티 사이드 (ROS2 + Gazebo + Nav2) — Sim2Real precursor
- 포트폴리오 사이트 v2 (Astro + Tailwind, 5섹션 V3 구조)
- AI 개발 자동화 13 모듈 (hih-skills) + PM 오케스트레이터 (8개 프로젝트 통합)

## 관심 분야

Physical AI · 로보틱스 시스템 통합 · 모터 PHM · APQP 풀사이클 PM · LLM 3계층 (Head/Worker/Drone)

## 핵심 기술

![C](https://img.shields.io/badge/C-A8B9CC?style=flat&logo=c&logoColor=black) ![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=c%2B%2B&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![MATLAB](https://img.shields.io/badge/MATLAB-0076A8?style=flat&logo=mathworks&logoColor=white) ![ROS2](https://img.shields.io/badge/ROS2-22314E?style=flat&logo=ros&logoColor=white) ![STM32](https://img.shields.io/badge/STM32-03234B?style=flat&logo=stmicroelectronics&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black) ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) ![Claude](https://img.shields.io/badge/Claude%20Code-D97757?style=flat)

도메인: BLDC/PMSM · FOC/SVPWM · CAN/CAN-FD · DFMEA/APQP · Ansys Maxwell · Co-simulation · RTK GNSS+IMU 융합

## 핵심 프로젝트

| 프로젝트 | 한 줄 | 사이트 |
|---------|------|--------|
| **EOP 400W (절환 알고리즘)** | SVPWM/DPWM 절환으로 FET 1~6°C↓, 입력전력 1~3.8%↓ (NXP/C, 2,932 데이터 포인트) | [/cases/eop-400w](https://hwanginhyeok.github.io/portfolio/cases/eop-400w) |
| **GT-SS500 풀사이클 양산 PM** | 알고리즘→파일럿→양산 7단계 Lifecycle. APQP Phase 2~3 단독 PM | [/cases/ss500-state-machine](https://hwanginhyeok.github.io/portfolio/cases/ss500-state-machine) |
| **시험 기획 7종 단독 구축** | 다이나모 0.008%, 팬 +57%, 범퍼 0.082m. 장비가 없으면 만든다 | [/cases/test-engineering](https://hwanginhyeok.github.io/portfolio/cases/test-engineering) |
| **특허 2건 (정직 기재)** | PN231067KR 초기위치 검출 (공동 발명) + 저온 기동 -40°C 300→100s | [/cases/patent](https://hwanginhyeok.github.io/portfolio/cases/patent) |

## 연구·수상

- **IEEE TIM 2024** — 본드와이어 고장 진단 공저 (DOI: 10.1109/TIM.2024.3472910)
- 학회 수상 2건 — PHM 2021 우수포스터상 / 신뢰성학회 2022 최우수발표상
- 논문 6편 (학위 1 + 공저 5)
- 자세히: [/research](https://hwanginhyeok.github.io/portfolio/#research)

## AI 워크플로우

- 8개 프로젝트 통합 PM 오케스트레이터 (cron + tmux + LLM 3계층)
- hih-skills 13 모듈 — 야간 무인 자동화
- Obsidian 297 노트 + 지식그래프
- 절약시간: <!-- TODO §4 placeholder 갱신 후 채움 -->

## 연락

- Site: https://hwanginhyeok.github.io/portfolio
- Email: dlsgur5560@gmail.com
- Blog: <!-- TODO 블로그 운영 시 채움 -->

<!-- 위젯 (선택) — §4에서 갱신 정책 -->
<!--
![hwanginhyeok's GitHub stats](https://github-readme-stats.vercel.app/api?username=hwanginhyeok&show_icons=true&theme=default)
![GitHub Streak](https://github-readme-streak-stats.herokuapp.com/?user=hwanginhyeok)
-->
```

### 1.2 영문 버전 (외국계 회사 지원 시 / 같은 레포에 토글로 또는 `/profile-en/README.md`)

```markdown
# Inhyeok Hwang — Physical-world problems, solved with data
> Full-stack Hardware · 0-to-1 Builder · AI-Augmented
> Motor control (EOP 400W) · GT-SS500 production PM · IEEE TIM co-author · LLM workflow architect

**Working on**: outdoor autonomous mobility (ROS2 + Gazebo + Nav2, Sim2Real precursor) · Portfolio v2 (Astro + Tailwind) · 13 hih-skills modules + 8-project PM orchestrator (cron + tmux + 3-tier LLM)

**Interests**: Physical AI · Robotics systems integration · Motor PHM · APQP full-cycle PM · 3-tier LLM (Head/Worker/Drone)

**Tech**: C · C++ · Python · MATLAB/Simulink · ROS2 · STM32 / NXP MCU · Linux · Git · Claude Code
**Domain**: BLDC/PMSM · FOC/SVPWM · CAN/CAN-FD · DFMEA/APQP · Ansys Maxwell · Co-simulation · RTK GNSS+IMU fusion

## Selected projects
| Project | One-line | Site |
|---|---|---|
| **EOP 400W** | SVPWM/DPWM switching: FET -1~6°C, input -1~3.8% (NXP/C, 2,932 data points) | /cases/eop-400w |
| **GT-SS500 Production PM** | Full 7-stage lifecycle. APQP Phase 2~3 sole PM | /cases/ss500-state-machine |
| **In-house test rigs (7)** | Dyno 0.008%, fan +57%, bumper 0.082m. "If the rig doesn't exist, build it." | /cases/test-engineering |
| **Patents (2, honest authorship)** | PN231067KR initial position (co-inventor) + cold-start -40°C 300→100s | /cases/patent |

**Research**: IEEE TIM 2024 (DOI 10.1109/TIM.2024.3472910) · PHM 2021 best poster · KSR 2022 best presentation · 6 papers
**Contact**: Site https://hwanginhyeok.github.io/portfolio · dlsgur5560@gmail.com
```

### 1.3 작성 규칙

- **Hero 카피 = 사이트 Hero 카피** (B3 LAYOUT §1 `#hero`와 글자 단위 동일)
- shields.io 배지는 알려진 색상만 / 링크는 모두 절대 URL / 위젯은 §4 결정 / 이모지 금지 (사이트 톤 일관)

---

## §2. 핀 레포 (Pinned Repositories) — 6개 슬롯 선택

### 2.0 이 항목이 중요한 이유

GitHub 핀 레포 6개는 **방문자가 보는 첫 번째 그리드**다. 사이트 핵심 케이스 4개와 사이드 3개가 동시에 보여야 EXPERT_REVIEW 갭("GitHub 임팩트 없음")이 닫힌다. 6 슬롯 한정이므로 우선순위 결정이 핵심.

### 2.1 후보 6개 + 채용 가치 / 공개 가능성

| 순위 | 레포 | 채용 가치 | 공개 가능성 | 메시지 매핑 (USAGE_STRATEGY §2.1) | 슬롯 |
|:---:|---|---|---|---|:---:|
| 1 | **portfolio** (이 사이트) | 사이트와 동일 인상 진입점. README가 본인 소개 그 자체 | 공개 가능 (이미 공개) | 전 메시지 | ⭐ |
| 2 | **hih-skills** (AI 자동화 13 모듈) | MC-E AI 워크플로우 설계자 직접 증거. 스타트업 갭 직격 | 공개 가능 (개인 도구) | MC-E ⭐ | ⭐ |
| 3 | **autonomy-stack** (ROS2 + Gazebo 사이드) | EXPERT_REVIEW Physical AI/로보틱스 갭 1번 — ROS2 어휘 부재 해소 | 공개 가능 (신규 사이드) | MC-G 보조 + 신규 도메인 | ⭐ |
| 4 | **project-manager** (PM 오케스트레이터) | MC-E 보조. 8개 프로젝트 통합 모니터링 = 자본 효율성 시그널 | 공개 가능 (개인 도구) | MC-E 보조 | ⭐ |
| 5 | **knowledge-base** (Obsidian 297노트) | 학습/사고 깊이 시그널. AI-Augmented의 base | **부분 공개 권장** (영업 정보 분리 필요) | MC-E 보조 / About | △ (정리 후) |
| 6 | **GINT 업무 레포** | GT-SS500 / EOP 직결. 가장 강한 증거 | **대부분 비공개** (회사 IP) — 공개 가능 슬라이스 추출 시 | MC-A/B/C/D ⭐ | ✕ (§6 가이드 참조) |

### 2.2 슬롯 6개 확정안 (P1)

EXPERT_REVIEW 스타트업 갭 우선순위로:

| 슬롯 | 레포 | 위치 |
|:---:|---|---|
| 1 | `portfolio` | 진입점. 사이트로 이어주는 README |
| 2 | `hih-skills` | MC-E 직접 증거 |
| 3 | `autonomy-stack` (신규 생성 필요) | Physical AI/로보틱스 갭 |
| 4 | `project-manager` | MC-E 보조 + AI 절약시간 정량화 |
| 5 | `knowledge-base-public` (분기 필요) | 학습 깊이 |
| 6 | (예비) `eop-400w-demo` 또는 `motor-control-tutorial` (회사 IP 분리해 만든 공개 데모) | MC-D 공개 슬라이스 |

### 2.3 슬롯 6번 — 회사 IP 공개 슬라이스 만드는 기준

EOP 400W / GT-SS500은 직접 공개 불가. 대신 **공개 가능 슬라이스**를 별도 레포로:

- `motor-control-tutorial` — SVPWM/DPWM 비교 시뮬레이션 (회사 데이터 0건, 본인이 다시 작성한 교육 코드)
- `apqp-template` — APQP Phase × RACI 빈 템플릿 (회사 정보 0건)
- `dfmea-checklist` — DFMEA 작성 체크리스트 + 공개 케이스 1건

기준: **§6 비공개 자료 가이드의 4개 항목 모두 0건이어야 슬라이스 공개 가능**.

---

## §3. 레포별 README 표준 양식

### 3.0 이 항목이 중요한 이유

핀 레포를 클릭한 채용자가 처음 보는 게 README. 사이트의 케이스 페이지와 **동일 구조 + 동일 톤**이어야 톤 일관성이 유지된다 (B4 DESIGN_SYSTEM 톤 정책: "담담하게, 수치로 말한다").

### 3.1 표준 양식 (모든 핀 레포 공통)

```markdown
# {레포명} — {one-sentence pitch (스크롤 멈추는 한 줄)}

> {부제 — 한 줄. 무엇을 어떻게 어디에 쓰는지} (예: "Astro 5섹션 포트폴리오. Tailwind + V3 테마 매핑.")

## 무엇을 (What)

{2~3줄. 이 레포가 무엇인지. 명사 위주.}

## 왜 (Why)

{2~3줄. 어떤 문제를 풀려고 만들었는지. 사이트 케이스 페이지의 "이 레포에서 보여주려는 것"과 매핑.}

## 어떻게 (How)

{3~5줄. 핵심 기술/아키텍처/의사결정. 이미지/다이어그램 1장 권장.}

## 데모

- Live: <!-- URL or "(N/A — local only)" -->
- Screenshot: ![demo](docs/demo.png) <!-- 또는 GIF -->

## 기술 스택

![tech](https://img.shields.io/badge/{T}-{color}?style=flat)

## 사용 예시

```bash
# 핵심 명령어 1~3줄
npm run dev
```

## 설치

```bash
git clone https://github.com/hwanginhyeok/{레포}
cd {레포}
{install}
```

## 이 레포에서 보여주려는 것 (채용 시각)

- {메시지 매핑 — 예: "MC-E AI 워크플로우 설계자 — Opus/GLM/Ollama 3계층 라우팅 직접 구현"}
- {정량 — 예: "8개 프로젝트 통합. 야간 무인 cron 실행. 주 평균 X시간 절약"}
- {차별화 — 예: "PM 도구가 아니라 오케스트레이터: 직접 수정 안 하고 tmux로 지시만 전달"}

## 라이선스

MIT (또는 사정에 맞게)
```

### 3.2 레포별 적용 가이드

#### portfolio (이 사이트)
- pitch: "Astro 기반 5섹션 포트폴리오. CONTENT_V2 SSOT + V3 테마 매핑."
- 보여주려는 것: 사이트 자체가 산출물. README는 빌드/구조 안내만 간결히.
- 데모: 라이브 URL + Hero 스크린샷 1장.

#### hih-skills
- pitch: "13 모듈 AI 자동화 스킬셋. /hih-task /hih-clear /hih-git 등."
- 보여주려는 것: MC-E. 모듈별 트리거/정책 표 1장 + cron 야간 실행 로그 GIF.
- 절약시간 정량 표 (§4.3) 직접 임베드.

#### autonomy-stack (신규)
- pitch: "ROS2 + Gazebo + Nav2 outdoor mobility — Sim2Real precursor."
- 보여주려는 것: EXPERT_REVIEW Physical AI 갭 직격. 노드 그래프 1장 + tf 트리 + Gazebo 캡처.
- "GT-SS500 차동조향 → turtlebot3/Gazebo 이식" 1줄.

#### project-manager
- pitch: "8 프로젝트 통합 PM 오케스트레이터. cron + tmux + 3-tier LLM."
- 보여주려는 것: MC-E. SSOT 심링크 구조 다이어그램 + daily/weekly 리포트 샘플 1장.

#### knowledge-base-public
- pitch: "Obsidian 공개 가능 노트. 엔지니어링 학습 패턴."
- 보여주려는 것: About 깊이. 그래프뷰 스크린샷 1장.
- ⚠️ §6 비공개 가이드 통과 노트만.

#### motor-control-tutorial (예비)
- pitch: "SVPWM vs DPWM 비교 — 본인이 다시 작성한 교육 코드 (회사 데이터 0건)."
- 보여주려는 것: MC-D 공개 슬라이스. 시뮬레이션 결과 + 사이트 EOP 케이스 링크.

---

## §4. GitHub 활동 정량화

### 4.0 이 항목이 중요한 이유

EXPERT_REVIEW §4 스타트업 갭 명시: "GitHub 활동 위젯", "AI 자동화 절약시간". 위젯만 임베드하면 숫자가 자기 강화되지만, **현재 시점 placeholder를 명시**해 둬야 갱신 시 누락이 안 된다.

### 4.1 위젯 권장안

| 위젯 | URL 패턴 | 권장 여부 |
|---|---|---|
| GitHub Stats | `https://github-readme-stats.vercel.app/api?username=hwanginhyeok&show_icons=true&theme=default` | ⭕ 권장 (커밋/스타/PR 한 장) |
| Streak | `https://github-readme-streak-stats.herokuapp.com/?user=hwanginhyeok` | △ 선택 (스트릭이 끊기면 역효과) |
| Top Languages | `https://github-readme-stats.vercel.app/api/top-langs/?username=hwanginhyeok&layout=compact` | △ (회사 비공개 코드 빠져 왜곡 가능) |
| Activity Graph | `https://github-readme-activity-graph.vercel.app/graph?username=hwanginhyeok&theme=minimal` | ⭕ (커밋 시각화) |

**스트릭이 약한 시기**에는 Streak 위젯 빼고 Stats + Activity Graph 2개만 노출.

### 4.2 현재 시점 기록 (placeholder — 갱신 필요)

> 사용자가 GitHub 프로필 페이지에서 직접 확인 후 채움. 갱신일 명기.

| 항목 | 값 | 갱신일 |
|---|---|---|
| 공개 레포 수 | <!-- TODO --> | <!-- TODO --> |
| 총 스타 | <!-- TODO --> | <!-- TODO --> |
| 최근 1년 커밋 (포크 제외) | <!-- TODO --> | <!-- TODO --> |
| 최장 스트릭 | <!-- TODO --> | <!-- TODO --> |
| 주간 평균 커밋 | <!-- TODO --> | <!-- TODO --> |
| Followers | <!-- TODO --> | <!-- TODO --> |

> 이 표는 **이력서 / 사이트 About 섹션**에 인용할 때 바로 가져다 쓸 수 있게 유지한다.

### 4.3 AI 워크플로우 절약시간 정량화 표 (EXPERT_REVIEW 갭 직격)

> "주 N시간 절약 → 연 환산 M개월" 프레임. 추정치라도 명시. 정확도보다 **존재 자체가 임팩트**.

| 워크플로우 | 도입 전 (시간/주) | 도입 후 (시간/주) | 절감 (시간/주) | 도구 |
|---|---:|---:|---:|---|
| 일간 리포트 (8개 프로젝트 git/task 점검) | <!-- 예: 3.0 --> | <!-- 예: 0.2 --> | <!-- 예: 2.8 --> | `daily_report.py` |
| 주간 회고 (커밋 통계 / 디스크 / 아티클) | <!-- 예: 2.5 --> | <!-- 예: 0.3 --> | <!-- 예: 2.2 --> | `weekly_report.py` |
| 야간 작업 자동 실행 (cron 00:00) | <!-- 예: 4.0 --> | <!-- 예: 0.0 --> | <!-- 예: 4.0 --> | `overnight_runner.py` |
| 입고검사 리포트 자동화 (회사) | <!-- 예: 1.5 --> | <!-- 예: 0.1 --> | <!-- 예: 1.4 --> | xlsx 자동화 (PM-65/66/68) |
| 세션 정리 / 태스크 갱신 | <!-- 예: 2.0 --> | <!-- 예: 0.4 --> | <!-- 예: 1.6 --> | `/hih-clear` `/hih-task` |
| **합계 (주)** | | | <!-- 예: 12 시간/주 --> | |
| **연 환산 (52주, 1.5개월 ≈ 240시간)** | | | <!-- 예: 624시간 ≈ 3.9개월/년 --> | |

> 이 표는 **사이트 §AI-Native 섹션 + 이력서 1줄 + GitHub README**에 동일 수치로 사용한다 (SSOT). 갱신 시 3곳 모두 갱신.

---

## §5. 사이트 ↔ GitHub 링크 정책

### 5.0 이 항목이 중요한 이유

방문자가 사이트→GitHub 또는 GitHub→사이트로 자유롭게 오가야 한다. 한 방향만 열려 있으면 인상이 끊긴다. B3 LAYOUT §1 결정사항(Footer GitHub 아이콘)을 사이트 측에서 보장하고, GitHub README는 항상 사이트 URL을 노출.

### 5.1 사이트 → GitHub (사이트 측 추가 권장 위치)

| 위치 | 무엇 | 우선순위 | B3 LAYOUT 매핑 |
|---|---|:---:|---|
| Hero 우측 / 또는 About 상단 | GitHub Stats 위젯 임베드 (Activity Graph 1장) | P2 | §1 Hero 또는 §1 #about |
| Footer | GitHub 아이콘 + URL ✅ (이미 있음) | P0 | §1 #footer (이미 적용) |
| 케이스 페이지 (eop-400w / patent / ss500-state-machine / test-engineering) | "관련 레포" 박스 — 공개 슬라이스 또는 회사 IP 보호 안내 1줄 | P2 | §3 신규 케이스 페이지 명세 |
| About → 기술 스택 | shields.io 배지 (README와 동일 색상) | P3 | §1 #about |
| 사이드 프로젝트 카드 (3종) | 각 카드에 "GitHub →" 링크 (autonomy-stack 등) | P1 | `index.astro` L88~98 직접 수정 |

> ⚠️ B3 LAYOUT 결정사항 위반 금지: Hero 위젯은 옵션이고 Footer 링크는 필수.

### 5.2 GitHub → 사이트 (README 측)

| 위치 | 무엇 | 필수 |
|---|---|:---:|
| 프로필 README 상단 | `[Site](https://hwanginhyeok.github.io/portfolio)` 1줄 | ⭕ |
| 핵심 프로젝트 표 | 각 프로젝트 행에 사이트 케이스 페이지 딥링크 | ⭕ |
| 연구·수상 | 사이트 #research 앵커 | ⭕ |
| 연락 | Site / Email / Blog | ⭕ |

### 5.3 도메인 확정 후 일괄 치환

현재 placeholder: `https://hwanginhyeok.github.io/portfolio`. 사용자 도메인 확정 시 (사이트 배포 결정 후) 본 문서 + 모든 README에서 한 번에 치환.

---

## §6. 비공개 자료 가이드

### 6.0 이 항목이 중요한 이유

회사 IP / 영업 비밀 / 협력사 정보를 GitHub에 올리면 단 1줄로도 채용 신뢰가 무너진다. EXPERT_REVIEW §4 정직 기재 패턴(특허 #2 발명자 미기재)과 같은 톤으로 **명시적 거리두기**가 더 점수가 높다.

### 6.1 절대 공개 금지 항목 (체크리스트)

- [ ] 회사 도면 / 회로도 / BOM (제품 ID 식별 가능한 모든 것)
- [ ] 펌웨어 소스 코드 (회사 저장소에서 추출한 것)
- [ ] APQP / DFMEA / 시험보고서 원본 (체크리스트는 OK, 실제 데이터 NOT OK)
- [ ] CAN DBC 파일 / 프로토콜 (회사 정의)
- [ ] 협력사 명 + 거래조건 + 단가
- [ ] 고객사 / 농민 / 사용자 식별 가능한 사진
- [ ] 회사 메일 / 슬랙 캡처
- [ ] 특허 출원 전 발명 (출원 후만 공개. 그것도 공개공보 등록 후)
- [ ] 미공개 논문 (저자 합의 전)

### 6.2 공개 가능 영역 (체크리스트)

- [x] **본인이 다시 작성한** 교육용 코드 (회사 데이터 0건)
- [x] 공개 논문 / 공개 특허 (출원번호 명시)
- [x] 회사명 + 직무 + 기간 + 본인 기여 (수치 추상화)
- [x] APQP / DFMEA **빈 템플릿 / 체크리스트** (회사 정보 0건)
- [x] 사이드 프로젝트 (개인 시간 / 개인 장비)
- [x] 오픈소스 기여 (회사 외부)

### 6.3 회색 영역 처리 원칙

- 공개 가능성이 모호하면 → **공개하지 않는다**.
- 사이트 케이스 페이지에 "회사 IP 보호로 공개 불가, 면접 시 노트북 시연 가능" 1줄 명시 (USAGE_STRATEGY §4 면접 채널 자산 참조).
- 추출한 슬라이스는 반드시 **새 레포 + 처음부터 재작성** (회사 저장소 git 히스토리 0).

### 6.4 정직 기재 패턴 (특허 #2 톤 일관)

EXPERT_REVIEW §4 / CONTENT_V2 §5.4 정직 기재 톤을 GitHub에도 적용:

> "GT-SS500 / EOP 400W는 회사 IP로 코드 비공개. 본 사이트 케이스 페이지에 알고리즘/수치 공개 가능 범위만 기재. 면접 시 노트북 시연 가능."

이 1줄을 프로필 README 하단에 두면 신뢰가 오히려 오른다.

---

## §7. 우선 작업 순서 (P1 ~ P3)

### P1 — 즉시 (사이트 v2 배포 전 / 또는 동시)

1. `hwanginhyeok/hwanginhyeok` 프로필 레포 생성 + §1.1 한국어 README 적용
2. 핀 레포 4개 슬롯 채우기 (portfolio · hih-skills · project-manager · 사이드 1)
3. 각 핀 레포 README를 §3.1 표준 양식으로 정비 (portfolio부터)
4. §6.4 정직 기재 1줄 프로필 README에 추가
5. 사이트 Footer GitHub 링크 ✅ 확인 (이미 적용됨)

### P2 — 1주 내

6. `autonomy-stack` 신규 레포 생성 + ROS2 + Gazebo PoC 1건 + README
7. §4.2 placeholder 채워넣기 (현재 시점 GitHub 활동 수치 기록)
8. §4.3 AI 워크플로우 절약시간 표 추정치 채워서 README + 사이트 §AI-Native + 이력서 동기화
9. 영문 README §1.2 작성 (외국계 대상)
10. 사이트 사이드 프로젝트 카드 3종에 GitHub 레포 링크 추가 (`index.astro` L88~98)

### P3 — 2~4주 (선택 / 점진)

11. `knowledge-base-public` 분기 — Obsidian 공개 가능 노트만 추출
12. `motor-control-tutorial` 슬라이스 — SVPWM/DPWM 비교 교육 코드 (회사 데이터 0건)
13. GitHub Stats / Activity Graph 위젯 사이트 About에 임베드 (B3 LAYOUT §1 옵션)
14. 케이스 페이지 4개에 "관련 레포" 박스 추가
15. 월 1회 §4.2 / §4.3 갱신 (cron으로 알림 자동화 — `~/.pm_logs/` 활용)

### 게이트 체크리스트 (P1 완료 시)

- [ ] 프로필 README 5초 룩에서 사이트 Hero와 동일 인상이 나는가
- [ ] 핀 레포 4개가 모두 §3.1 양식을 따르는가
- [ ] 모든 README의 사이트 URL이 동일한 절대 URL인가
- [ ] 회사 IP / 영업 비밀이 새어 나간 곳이 단 한 줄도 없는가 (§6.1 체크리스트)
- [ ] §6.4 정직 기재 1줄이 프로필에 노출되는가

---

## §8. 갱신 정책 + 사용 가이드

### 갱신 주기
- §4.2 (현재 시점 수치): 월 1회. 갱신일 명기.
- §4.3 (AI 절약시간): 분기 1회. 사이트 / 이력서 / README 3곳 동기화.
- §1.1 (프로필 README): 사이트 Hero 카피 변경 시 즉시 동기화 (B3 LAYOUT §1 트리거).
- §2 (핀 레포): 새 사이드 추가 시 슬롯 재평가.
- §6.1: 새 회사 / 새 협력사 추가 시 갱신.

> 갱신 SSOT: 본 문서. 다른 곳에 수치 복사 시 `<!-- SSOT: GITHUB_PROFILE.md §4.3 -->` 주석.

### 작성 순서
1. **§1 먼저** — 사이트 Hero 카피 확정 후 작성.
2. **§2** — 핀 레포 4개 먼저, 회사 IP 슬라이스(슬롯 6)는 마지막.
3. **§3** — 모든 핀 레포가 같은 양식이어야 일관성 유지.
4. **§4** — placeholder 빈 채로 두지 않는다. 추정치라도 채운다.
5. **§5** — 양방향 링크. 한 방향만 열려 있으면 끊긴다.
6. **§6** — 모호하면 공개 안 한다. 정직 기재가 더 점수 높다.
7. **§7 P1만 1주 내** 완료해도 EXPERT_REVIEW 스타트업 갭 60%가 닫힌다.
