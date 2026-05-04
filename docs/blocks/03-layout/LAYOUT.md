# B3 배치 — LAYOUT

> 최종 수정: 2026-04-26 (B3-01 골격 작성)
> 위치: `docs/blocks/03-layout/LAYOUT.md`
> 입력 SSOT:
> - `docs/포트폴리오/THEME_MAP_V3.md` — 5섹션 재구성안 (T-1 ~ T-5)
> - `docs/포트폴리오/CONTENT_V2.md` §11 Removal List · §12 섹션 순서
> - `docs/포트폴리오/EXPERT_REVIEW_20260426.md` — 4개 도메인 갭 분석
> - `docs/blocks/02-usage/USAGE_STRATEGY.md` — B2 메시지 후보 8개 (MC-A ~ MC-H)
> - `docs/포트폴리오/PAPERS.md` — 논문 6건 (학위 1 + 공저 5)
> - `src/pages/index.astro` + `src/pages/cases/{eop-400w,patent,ss500-state-machine,test-engineering}/index.astro`
> 출력 대상: B4 DESIGN_SYSTEM.md · 신규 케이스 페이지 생성 가이드
> 운영 원칙:
> - 사실은 SSOT(CONTENT_V2/PAPERS)에서만 수정. 본 문서는 **배치 결정**만.
> - 사용자 입력 영역은 `[사용자 입력 필요]` 또는 `<!-- TODO -->` 표시.
> - 후보·예시는 풍부하게 제시. 사용자가 고르기 쉽게.

---

## §0. 본 문서의 역할

B2가 "어떤 메시지를 누구에게"를 정했다면, B3는 **"그 메시지를 어디에, 어떤 순서로 배치할 것인가"**를 결정한다.

### 입력 SSOT 참조 정책
- 사실/수치/카피 원문은 **CONTENT_V2 / PAPERS / THEME_MAP_V3**에서만 수정. 본 문서는 위치/순서/딥링크 정책만 결정.
- 메시지 우선순위(M1~M5)는 **USAGE_STRATEGY §2.2**에서 가져옴. 본 문서가 메시지를 새로 만들지 않는다.
- 도메인 어휘 리프레임은 **EXPERT_REVIEW**의 4개 도메인 갭 분석을 §3 / §5에 적용한다.

### B3 산출물
1. 5섹션 와이어프레임 확정 (THEME_MAP_V3 T-1~T-5 기반)
2. Impact Dashboard 위치 결정 (옵션 A/B/C)
3. 신규 케이스 페이지 후보 명세 (autonomy-stack / apqp-rmci)
4. 페이지 간 내비게이션 정책
5. 표현/어휘 리프레임 적용 범위 (Hero / About / 케이스 톤)
6. B4·B5로 넘기는 결정사항

---

## §1. 5섹션 와이어프레임 (THEME_MAP_V3 기반)

### 1.1 섹션 정의표

| # | 섹션 ID | 테마 (THEME_MAP_V3) | 핵심 메시지 (CONTENT_V2 매핑) | 위치 | 추정 높이 (px) | 주요 컴포넌트 |
|---|---------|---------------------|------------------------------|------|----------------|--------------|
| 0 | `#hero` | — | Hero 헤드라인 + 수치카드 3장 | 최상단 | 540~640 | `Hero.astro` (V2 카피 교체) |
| 1 | `#lifecycle` | — (전이 블록) | 7단계 × 3프로젝트 매트릭스 | Hero 직하 | 280~340 | `LifecycleHeatmap.astro` (신규) |
| 2 | `#t1-dfmea` | T-1 현장에서 돌아오는 설계 | DFMEA 4건 (Track A) | 본문 1구획 | 720~900 | `DFMEAField.astro` (신규) + 기존 `StateMachine.astro` |
| 3 | `#t2-test` | T-2 기획에서 양산까지 | 시험으로 증명 (Track B + 4단계) | 본문 2구획 | 820~1000 | `PerformanceFlow.astro` + `TestProcess.astro` (신규) |
| 4 | `#t3-system` | T-3 시스템 아키텍처 | CAN 5노드 + 차세대 (Track C+E) | 본문 3구획 | 760~900 | `CanNetworkDiagram.astro` (기존) + `NextGen.astro` (신규) |
| 5 | `#t4-apqp` | T-4 양산 체계 | APQP/DFMEA/BOM (Track D 8건) | 본문 4구획 | 680~820 | `APQPSystem.astro` (신규) |
| 6 | `#t5-roots` | T-5 엔지니어의 뿌리 | EOP + Patents + Research + AI-Native | 본문 5구획 | 900~1100 | `Research.astro` + `Patents.astro` + `AINative.astro` (신규) |
| 7 | `#timeline` | — | 경력 타임라인 (최근순) | 본인 소개 | 320~420 | `Timeline.astro` (기존) |
| 8 | `#about` | — | About + 기술 스택 | 본인 소개 | 380~480 | About 섹션 (`index.astro` 인라인) |
| 9 | `#footer` | — | 연락처 (CTA 축약) | 최하단 | 120~160 | Footer (인라인) |

> 각 섹션은 `id`로 앵커. 상단 nav에서 `#t1-dfmea ~ #t5-roots` 5개를 노출, 그 외(`#lifecycle`, `#timeline`, `#about`)는 스크롤로만 접근.

### 1.2 SSOT 매핑

| 섹션 | CONTENT_V2 §번호 | THEME_MAP_V3 Track | USAGE_STRATEGY 메시지 |
|------|------------------|--------------------|----------------------|
| #hero | §2 | — | M1 한 줄 카피 |
| #lifecycle | §3.2 | — | MC-B 보강 |
| #t1-dfmea | §6 | A | MC-F (분야 무관) |
| #t2-test | §7 + 시험 4단계 | B + 시험 | MC-C (장비 자가 구축) |
| #t3-system | §7A + §7C | C + E | MC-B 시스템 측면 |
| #t4-apqp | §7B | D | MC-B 양산 측면 |
| #t5-roots | §4.2 + §4.3 + §5 + §8 | — | MC-A / MC-D / MC-G / MC-H / MC-E |

### 1.3 결정표 — 현 4 카드 vs THEME_MAP_V3 5 테마

| 항목 | 현재 (`index.astro`) | V3 5 테마 권장안 |
|------|---------------------|------------------|
| 케이스 카드 수 | 4장 (eop-400w / patent / ss500-state-machine / test-engineering) | **5 테마 섹션 + 4 딥링크 페이지 유지** |
| 카드 단위 | 프로젝트 (사람이 만든 것) | 테마 (사고방식) |
| 4 케이스 페이지 | 그대로 살림 | 그대로 살림 — T-1·T-2·T-5에서 딥링크 |
| 신규 페이지 후보 | — | `autonomy-stack/` (Physical AI/로보틱스) · `apqp-rmci/` (PM) — §3 참조 |
| ThemeHeatmap | 테마×프로젝트 | **LifecycleHeatmap** 7단계×3프로젝트로 교체 |

**결정**: V3 5 테마 섹션 채택. 기존 4 케이스 페이지는 유지하되 홈에서 테마 섹션의 카드/카드 그리드에서 딥링크로 연결. 신규 케이스 2종(`autonomy-stack` / `apqp-rmci`)은 §3에서 결정.

### 1.4 선형 와이어프레임 (텍스트)

```
┌──────────────────────────────────────────────────────────┐
│  [Nav]  로고  ·  T1  T2  T3  T4  T5  ·  GitHub          │
├──────────────────────────────────────────────────────────┤
│  #hero                                                   │
│  H1: <!-- §5.1 후보 3개 중 사용자 확정 -->              │
│  Sub: CONTENT_V2 §2.1 서브카피                          │
│  Cards: [논문·학회] [특허 참여] [현장 이슈]             │
│  └─ (옵션) Impact Dashboard — §2 결정에 따름            │
├──────────────────────────────────────────────────────────┤
│  #lifecycle  Lifecycle Heatmap (7단계 × 3프로젝트)      │
├──────────────────────────────────────────────────────────┤
│  #t1-dfmea  T-1 현장에서 돌아오는 설계                  │
│   - 4줄 프레임 카드 4장 (DFMEAField)                    │
│   - "더 보기" → cases/ss500-state-machine/              │
├──────────────────────────────────────────────────────────┤
│  #t2-test  T-2 기획에서 양산까지                        │
│   - PerformanceFlow 카드 3장 (팬/분사/범퍼)             │
│   - TestProcess 4단계 (기획·설계·증명·분석)             │
│   - "더 보기" → cases/test-engineering/                 │
├──────────────────────────────────────────────────────────┤
│  #t3-system  T-3 시스템 아키텍처                        │
│   - CanNetworkDiagram (기존)                            │
│   - NextGen (SS1000 3건)                                │
│   - (신규 후보) "Robotics Systems Integration" 한 줄    │
│     → cases/autonomy-stack/ 딥링크                      │
├──────────────────────────────────────────────────────────┤
│  #t4-apqp  T-4 양산 체계                                │
│   - APQPSystem 표 (Phase × 산출물)                      │
│   - (신규 후보) APQP × RACI 1장 → cases/apqp-rmci/      │
├──────────────────────────────────────────────────────────┤
│  #t5-roots  T-5 엔지니어의 뿌리                         │
│   - 인트로 1단락 ("훈련된 체질")                        │
│   - 4 카드 그리드:                                      │
│     [EOP 400W] [Patents 2] [Research] [AI-Native]      │
│   - 각 카드 → cases/eop-400w/ · cases/patent/ ·        │
│              Research 인페이지 · AI-Native 인페이지     │
├──────────────────────────────────────────────────────────┤
│  #timeline  Timeline (최근순)                           │
├──────────────────────────────────────────────────────────┤
│  #about  About + 기술 스택                              │
│   - 프로필 + 현재 / 학력 / AI 워크플로우                │
│   - 기술 스택 (§5.2 보강 항목 적용)                     │
│   - 사이드 프로젝트 (3종 유지)                          │
├──────────────────────────────────────────────────────────┤
│  #footer  Footer 연락처                                 │
└──────────────────────────────────────────────────────────┘
```

---

## §2. Impact Dashboard 위치 결정

### 2.1 옵션 비교

| 옵션 | 위치 | 장점 | 단점 | 메시지 우선순위와의 정합성 |
|------|------|------|------|---------------------------|
| **A. Hero 직하단** | `#hero` 안 또는 바로 다음 (`#lifecycle` 위) | 10초 룩 임팩트 극대화. 리크루터 시각에서 "수치"가 첫 페이지 끝나기 전에 보임 | Hero가 길어져 모바일 스크롤 부담. Lifecycle Heatmap과 시각적으로 경쟁 | M1이 정량 임팩트 메시지(MC-B/MC-D 등)일 때 ⭐ |
| **B. 케이스 그리드 위 (T-1 직전)** | `#lifecycle`과 `#t1-dfmea` 사이 | 스토리 흐름이 자연스러움 — Lifecycle로 폭넓게 본 후 핵심 수치로 진입 | 첫 화면에서 안 보임. "10초 룩"에 약함 | M1이 스토리 메시지(MC-B/MC-F)일 때 ✓ |
| **C. 별도 `/impact` 페이지** | 독립 라우트 | 리크루터용 원스톱. 이력서·LinkedIn에 공유 가능. 정량 데이터 풀세트 | 홈 첫 화면에서는 안 보임. 외부 트래픽 별도 유도 필요 | 리크루터 직접 링크 공유가 잦으면 ✓ |

### 2.2 추천 결정

> **권장: A (Hero 직하단) + C (별도 /impact 페이지) 병행**.
>
> 이유:
> - Hero 안에 이미 수치카드 3장(논문·특허·이슈)이 있음 (`CONTENT_V2 §2.2`). 여기에 EXPERT_REVIEW가 지적한 **사업 임팩트 1장**을 추가해 4장 그리드로 확장하면 옵션 A 효과 즉시 발생.
> - 별도 `/impact` 페이지는 리크루터가 LinkedIn/이력서에서 직접 링크할 수 있는 단일 URL — 옵션 C로 보완.
> - 옵션 B는 채택하지 않음 (Hero 수치카드와 중복).

### 2.3 Hero 수치카드 4장 후보 (현 3장 + 신규 1장)

| 카드 | 수치 (확정) | 서브 라벨 | 출처 |
|------|------------|-----------|------|
| 논문·학회 | 저널 1 · 학회 4 | 석사 연구 (모터 PHM) | PAPERS.md |
| 특허 참여 | 공동 1 · 기여 1 | 초기위치 검출 / 저온 기동 | CONTENT_V2 §5 |
| 현장 이슈 | 37건+ | 전력제어 담당 14건 | CONTENT_V2 §6 |
| **(신규) 사업 임팩트** | 초도 양산 **16대** | GT-SS500 · 0→1 풀사이클 완주 | EXPERT_REVIEW §4 권장 |

> 사업 임팩트 카드는 EXPERT_REVIEW 4번(스타트업 시각)의 가장 큰 갭. 1장 추가만으로 "시니어 엔지니어 → 0→1 Builder"로 톤 상승.

### 2.4 `/impact` 페이지 명세 (옵션 C 채택 시)

- 경로: `src/pages/impact/index.astro`
- 구성:
  - 상단: Hero 4 카드 확장판 (각 카드 클릭 → 상세 근거)
  - 중단: Lifecycle Heatmap (가로 풀폭)
  - 하단: 메시지별 정량표 (MC-A ~ MC-H 중 확정 메시지의 수치만 추려서)
- 인입: 상단 nav에 노출하지 않음. 이력서/LinkedIn에서만 공유.

---

## §3. 신규 케이스 페이지 후보 (EXPERT_REVIEW 기반)

### 3.1 `cases/autonomy-stack/` — Physical AI · 로보틱스

**근거**: EXPERT_REVIEW §1 (Physical AI 6/10) + §2 (로보틱스 5/10). 가장 큰 갭은 ROS2 + 인지 스택 + Sim2Real 어휘.

| 항목 | 내용 |
|------|------|
| 경로 | `src/pages/cases/autonomy-stack/index.astro` |
| 한 줄 요약 | "GT-SS500을 로봇 시스템 통합 케이스로 — 분산 임베디드 + Co-simulation + ADT PC 인터페이스" |
| 주요 콘텐츠 | (1) ROS2 노드 그래프 (사이드 프로젝트 turtlebot3+Gazebo+nav2) <br> (2) ADT PC 인터페이스 다이어그램 (좌표계·메시지 주기·페일세이프 핸드셰이크) <br> (3) Co-simulation 체질 (Ansys Maxwell + MATLAB/Simulink + 실험) → "Sim2Real precursor" 어휘 적용 <br> (4) 다중 신호 PHM (phase current·온도·shaft displacement·vibration) |
| 이미지 자산 | I-S01~S05 (상태머신) · I-T19~T25 (PID/PWM) 일부 재활용 + 신규 다이어그램 1~2장 (B4 단계) |
| 메시지 매핑 | MC-D 보조 + MC-E 보조 + (스타트업/Physical AI 도메인 면접 시 M1 후보) |
| 톤 | "어휘 리프레임" 중심. 새로운 사실 추가 없음. 기존 자산을 현대 어휘로 다시 묶는다. |
| B4 디자인 영향 | 다이어그램 1~2장(SVG) 신규 필요. 기존 컴포넌트(`SystemArchitecture`, `CanNetworkDiagram`) variant로 재사용 검토. |
| 우선순위 | **P1** — B4 디자인 단계에서 바로 제작 (Physical AI/로보틱스/드론 방향 확정) |

### 3.2 `cases/apqp-rmci/` — 제품 개발 PM (APQP × RACI)

**근거**: EXPERT_REVIEW §3 (제품 개발 PM 7/10). 가장 큰 갭은 "APQP Phase × 본인 RACI 매트릭스" 1장.

| 항목 | 내용 |
|------|------|
| 경로 | `src/pages/cases/apqp-rmci/index.astro` |
| 한 줄 요약 | "APQP 5 Phase × 본인 RACI — 모터제어 51% / PM 49%를 PM 60%로" |
| 주요 콘텐츠 | (1) APQP Phase 1~5 × Owner/Responsible/Consulted/Informed 매트릭스 1장 <br> (2) DFMEA RPN before/after 1건 (수치화) <br> (3) WBS/Gantt 게이트차트 1장 (알파→파일럿→양산) <br> (4) QCD KPI (이슈 평균 Closure 일수, NCR 재발률 등) |
| 이미지 자산 | 신규 매트릭스/차트 3~4장 필요 (B4 단계에서 SVG/Figma) |
| 메시지 매핑 | MC-B 핵심 보강 + (대기업 PM 트랙 면접 시 M1 후보) |
| 톤 | "정량 PM 산출물" — Q만 강하던 톤을 QCD로 확장 |
| B4 디자인 영향 | 매트릭스/Gantt 표 컴포넌트 신규 필요 (`APQPSystem.astro` 확장 또는 별도) |
| 우선순위 | **P2** — 대기업 PM 트랙 지원 확정 시 B5와 함께. 현재 보류. |

### 3.3 신설 시 B4 디자인 영향 요약

| 신규 페이지 | 신규 컴포넌트 | 신규 이미지 | T 섹션 영향 |
|-------------|--------------|------------|-------------|
| autonomy-stack | ROS2NodeGraph (옵션) · ADTInterface (옵션) | 1~2장 다이어그램 | T-3 카드 1개 추가 |
| apqp-rmci | APQPRACI · WBSGantt | 3~4장 표/차트 | T-4 카드 1개 추가 |

> 신설하지 않을 경우: EXPERT_REVIEW 권장은 **§5 어휘 리프레임만으로도 즉효**. 페이지 신설은 우선순위 낮음 (P2~P3).

---

## §4. 페이지 간 내비게이션

### 4.1 현 흐름 검토

현재 4 케이스 페이지는 서로 직접 링크가 거의 없음 (홈 ↔ 각 케이스만 양방향). "다음 케이스" 같은 선형 인덱스 없음.

```
[현재]
홈 ─┬─ cases/eop-400w/
    ├─ cases/patent/
    ├─ cases/ss500-state-machine/
    └─ cases/test-engineering/
```

### 4.2 V3 흐름 (테마 → 케이스)

```
[V3 권장]
홈 (5 테마 섹션)
 ├─ T-1 #t1-dfmea ──→ cases/ss500-state-machine/ (A-2 심화)
 ├─ T-2 #t2-test ──→ cases/test-engineering/
 ├─ T-3 #t3-system ─→ cases/autonomy-stack/ (신규, 옵션)
 ├─ T-4 #t4-apqp ──→ cases/apqp-rmci/ (신규, 옵션)
 └─ T-5 #t5-roots ─┬─ cases/eop-400w/
                   └─ cases/patent/

각 케이스 페이지 하단 "다음" 정책: §4.3 결정
```

### 4.3 "다음 케이스" 링크 정책

| 옵션 | 정책 | 장점 | 단점 |
|------|------|------|------|
| L1. 선형 (Prev/Next) | 케이스 5~6개를 일렬로 — 이전/다음 노출 | 리크루터 끝까지 읽기 유도 | 순서가 작위적이면 부자연 |
| L2. 자율 (홈으로만) | 각 케이스 하단 "← 홈으로" 1개만 | 단순. 자율적 탐색 | 페이지당 끝나는 느낌, 다음 행동 약함 |
| L3. 테마 기반 | 각 케이스 하단 "이 테마의 다른 케이스" 2~3개 카드 | 테마 응집력. 자연스러운 다음 단계 | 카드 디자인 추가 필요 |

> **권장: L3 (테마 기반)**. 케이스마다 하단에 "이 테마(T-x)의 다른 시각" 2~3장 카드 + "← 홈으로" 1개. 5섹션 구조와 일관.

### 4.4 상단 Nav 결정

| 안 | 항목 | 비고 |
|----|------|------|
| N1 (현행 유지) | 홈 / 케이스 / 특허 / 약력 | 메뉴 4개. 단순. |
| N2 (테마 노출) | 홈 / T1 / T2 / T3 / T4 / T5 / GitHub | 5 테마 직접 노출. 데스크톱 ok, 모바일 햄버거 |
| N3 (혼합) | 홈 / 케이스(드롭다운) / Impact / About / GitHub | Impact 강조. 드롭다운 처리 필요 |

> **권장: N2 (테마 노출)**. 모바일은 햄버거 메뉴로 같은 5 항목. T1~T5 클릭 시 `#t1-dfmea` 등 앵커 스크롤. `/impact` 옵션 C 채택 시 N2에 추가.

---

## §5. 표현/어휘 리프레임 적용 범위 (EXPERT_REVIEW 종합)

### 5.1 Hero 헤드라인 후보 3개

> 현행: `황인혁 / 분야를 막론하고 — 문제가 있으면 해결한다` (CONTENT_V2 §2.1)
>
> EXPERT_REVIEW의 어휘 리프레임 권장에 따라 도메인별 후보 3개 제시. 사용자 §1.1 타겟 회사 확정 후 1개 선택.

| 코드 | 헤드라인 후보 | 서브카피 후보 | 적합 도메인 |
|------|---------------|---------------|-------------|
| H-A (현행 유지) | 분야를 막론하고 — 문제가 있으면 해결한다 | 코드·HW·기구·전력·SW. 경계 없이 엔지니어링 관점에서 원인을 찾고, 시험으로 증명하고, 양산까지 끌고 간다. | 일반 / 모빌리티 / 가전 |
| H-B (스타트업 향) | Full-stack Hardware · 0→1 Builder · AI-Augmented | 알고리즘부터 양산까지. 장비가 없으면 만든다. AI 워크플로우로 1인=N인 효과. | 스타트업 / 풀스택 시니어 |
| H-C (Physical AI 향) | Physics-informed Engineering, from Co-simulation to Production | IPMSM digital twin · multi-sensor PHM · CAN distributed control · Sim2Real precursor. | Physical AI / 로보틱스 / 박사급 R&D |

### 5.2 About 기술 스택 보강 항목 리스트

> 현행 (`index.astro` line 79): `BLDC/PMSM 모터제어 · FOC/SVPWM · CAN/CAN-FD · STM32/NXP MCU · DFMEA/DRBFM·APQP · Python · C/C++ · Matlab/Simulink · Git · Claude Code`
>
> EXPERT_REVIEW §1 / §2가 지적한 부재 항목 + 사실 검증 통과 항목.

| 분류 | 추가 후보 (사용자 선택) | 근거 |
|------|------------------------|------|
| **시뮬레이션·해석** | Ansys Maxwell · Co-simulation · MIL/SIL/HIL | EXPERT_REVIEW §1, T-01 학위논문 |
| **로보틱스 스택** | ROS2 · Gazebo · nav2 · EKF (사이드) | EXPERT_REVIEW §2, 사이드 프로젝트 E03 |
| **신호처리·진단** | PHM · Anomaly Detection · multi-sensor fusion | EXPERT_REVIEW §1, P-01/T-01 |
| **시스템 설계** | RTK GNSS · IMU 융합 · Functional Safety (ISO 13849 reading) | EXPERT_REVIEW §2, GT-SS500 |
| **OS·툴체인** | Linux · Docker (학습 단계) · GitHub Actions | 사이드 프로젝트 / hih-skills |
| **데이터·AI** | PyTorch (학습 단계) · LangChain (라우팅 활용) | CONTENT_V2 §8, 정직 기재 — "활용 단계" 표기 |

> **결정 원칙**: 실제 사용 깊이가 낮은 항목은 "(학습 단계)" 또는 "(reading)" 표기로 정직 기재. CONTENT_V2 §1.3 톤 유지.

### 5.2.1 확정 추가 항목 (2026-05-04)

> 기존: `BLDC/PMSM · FOC/SVPWM · CAN/CAN-FD · STM32/NXP MCU · DFMEA/DRBFM·APQP · Python · C/C++ · Matlab/Simulink · Git · Claude Code`

| 추가 항목 | 근거 | 표기 |
|-----------|------|------|
| `Ansys Maxwell · Co-simulation` | 학위논문 실사용 | 그대로 |
| `HIL` | 다이나모 VCU 연동 벤치 시험 | 그대로 |
| `PHM · multi-sensor fusion` | 연구 실적 (P-01/T-01) | 그대로 |
| `RTK GNSS · IMU 융합` | GT-SS500 실제 통합 | 그대로 |
| `ROS2 · Gazebo · nav2` | 사이드 프로젝트 | `(사이드)` 표기 |
| `Linux` | 일상 사용 | 그대로 |

제외: Docker · GitHub Actions · PyTorch · LangChain (미사용)

### 5.3 케이스 페이지별 톤 조정 (한 줄 요약)

| 페이지 | 현재 톤 | 권장 톤 (EXPERT_REVIEW 적용) |
|--------|---------|------------------------------|
| `cases/eop-400w/` | "EOP 400W 모터제어 상세" | "BLDC/PMSM 깊이 — SVPWM 절환·CAN Sleep·-40°C 기동 · 다이나모 0.008%" (현행 유지로 충분) |
| `cases/patent/` | "특허 2건 + 관련 연구" | "정직 기재의 신뢰성 + 모터 PHM 연구 정본" (현행 유지) |
| `cases/ss500-state-machine/` | "RC/LCD/ADT 3모드 상태머신" | "분산 임베디드 시스템 통합 — 단일 노드가 아닌 시스템 설계 근육" (어휘 보강) |
| `cases/test-engineering/` | "시험 7종/9개 단독 구축" | "기획·설계·증명·분석 4단계 — 장비가 없으면 만든다" (개수 → 프로세스, CONTENT_V2 §11 확정) |
| `cases/autonomy-stack/` (신규) | — | "Sim2Real precursor + Robotics Systems Integration — Co-simulation에서 ADT까지" |
| `cases/apqp-rmci/` (신규) | — | "APQP 5 Phase × RACI — Q만 강하던 PM을 QCD로" |

### 5.4 컷/축약 (CONTENT_V2 §11 확정 항목 재확인)

| 항목 | 처리 | 출처 |
|------|------|------|
| SCU/ADT/WIA 콘텐츠 | 사이트에서 미노출 | CONTENT_V2 §11 |
| /contact 별도 페이지 | Footer 축약 | CONTENT_V2 §11 |
| "시험 7종/9개" 개수 표현 | 4단계 프로세스로 교체 | CONTENT_V2 §11 |
| BMS SOC 162% 에피소드 | 사이트 미노출 | CONTENT_V2 §11 |
| 한의학·동양철학 이력 | **컷 확정** — About/Timeline 미노출 | 2026-05-04 |

---

## §6. B4·B5로 넘기는 결정사항

### 6.1 B4 (디자인)로 넘기는 결정

- **5섹션 와이어프레임 확정**: §1.1 표 기준. 각 섹션 추정 높이/컴포넌트 매핑 채택.
- **Impact Dashboard 위치**: A (Hero 4장 확장) + C (`/impact` 별도) 병행. (§2.2)
- **Hero 헤드라인**: H-A / H-B / H-C 중 1개 (§5.1). 사용자 §1.1 타겟 회사 결정 후 확정.
- **Nav 구조**: N2 (T1~T5 노출). 모바일 햄버거. (§4.4)
- **케이스 하단 다음 링크**: L3 (테마 기반). (§4.3)
- **About 기술 스택 보강**: §5.2 6개 분류에서 사용자 선택. "(학습 단계)" 표기 정책.
- **이미지 비율 정책**: 시험 사진 16:9 / 블록도 원본 비율 유지 (USAGE_STRATEGY §6.2 재확인).
- **수치 강조**: Hero 카드 큰 숫자 + 라벨. T-2/T-4 카드 동일 패턴.
- **신규 컴포넌트 9종**: THEME_MAP_V3 §3 표 기준 (DFMEAField · PerformanceFlow · TestProcess · CANDesign · NextGen · APQPSystem · Research · Patents · AINative).
- **LifecycleHeatmap 신규** + 기존 `ThemeHeatmap.astro` 삭제.

### 6.2 B5 (부가 작업)로 넘기는 결정

- **신규 케이스 페이지 우선순위**: §3.1 / §3.2 사용자 결정. P1이면 B4와 병행, P2~P3이면 B5에서.
- **GitHub 활동 위젯**: 스타트업 도메인 타겟 시 추가 (EXPERT_REVIEW §4). About 또는 `/impact`에 임베드.
- **이력서 분기**: 대기업 PM 트랙 vs 스타트업 풀스택 (EXPERT_REVIEW §B5). 헤드라인 H-A/H-B/H-C와 동기.
- **영문 부제**: Physical AI/로보틱스 어휘 우선 (EXPERT_REVIEW §B5).
- **demo URL/스크린샷**: 사이드 프로젝트 3종 중 demo 가능한 것 1개 선정.

### 6.3 사용자 직접 결정 항목 (요약)

| # | 항목 | 결정 | 날짜 |
|---|------|------|------|
| 1 | Hero 4번째 수치카드 (사업 임팩트) | **초도 양산 16대 · GT-SS500 0→1 풀사이클 완주** | 2026-05-04 |
| 2 | `/impact` 페이지 신설 여부 | **A+C 병행** — Hero 카드 4장 확장 + `/impact` 독립 페이지 | 2026-05-04 |
| 3 | `cases/autonomy-stack/` 우선순위 | **P1** — B4 단계에서 바로 제작 | 2026-05-04 |
| 4 | `cases/apqp-rmci/` 우선순위 | **P2** — PM 트랙 지원 확정 시. 현재 보류 | 2026-05-04 |
| 5 | Nav 구조 (N1/N2/N3) | **N2** — T1~T5 직접 노출, 모바일 햄버거 | 2026-05-04 |
| 6 | Hero 헤드라인 (H-A/H-B/H-C) | ⏳ **B2 완료 후** — 타겟 회사 확정 시 H-A/H-B/H-C 중 1개 | — |
| 7 | About 기술 스택 보강 항목 | **확정** — §5.2.1 표 참조 (6개 분류 중 실사용 항목만) | 2026-05-04 |
| 8 | 한의학·동양철학 이력 컷 여부 | **컷** — Physical AI/로보틱스 방향 기준 미노출 | 2026-05-04 |

---

## §7. 완료 게이트 체크리스트

B3 완료 게이트 (B4 진입 전 확인):

- [x] §1.1 5섹션 와이어프레임 표 확정 (섹션 ID + 컴포넌트 매핑)
- [x] §1.3 결정표 (현 4 카드 vs V3 5 테마) 확정
- [x] §2.2 Impact Dashboard 위치 결정 (A+C 병행 채택)
- [x] §2.3 Hero 4번째 수치카드 — 초도 양산 16대 · GT-SS500 0→1 풀사이클 완주
- [x] §3.1 / §3.2 신규 케이스 페이지 — autonomy-stack P1 / apqp-rmci P2
- [x] §4.3 케이스 하단 "다음" 정책 — L3 (테마 기반)
- [x] §4.4 상단 Nav — N2 (T1~T5 노출)
- [ ] §5.1 Hero 헤드라인 1개 확정 ⏳ **B2 완료 후**
- [x] §5.2 About 기술 스택 보강 항목 — §5.2.1 확정 (6개 추가)
- [x] §5.4 한의학·동양철학 이력 — 컷 확정
- [x] §6.1 B4로 넘기는 결정 10항목 표기
- [x] §6.3 사용자 직접 결정 8항목 채움 (7/8 완료, §5.1만 B2 대기)

게이트 통과 후 → [B4 DESIGN_SYSTEM.md](../04-design/DESIGN_SYSTEM.md)

---

## §8. 메모 — 이 문서를 쓰는 방법

1. **먼저 §1.3 결정표**: V3 5 테마 채택을 확정해야 다른 결정이 흔들리지 않음.
2. **그다음 §2.2**: Impact Dashboard 위치를 정해야 Hero 영역 높이가 결정됨.
3. **§3 신규 케이스**: P1이면 B4와 병행, 아니면 B5로 넘김.
4. **§4 Nav/내비게이션**: 페이지 간 흐름을 정해야 케이스 페이지 하단 컴포넌트가 결정됨.
5. **§5 어휘 리프레임**: 코드 변경보다 ROI 최대 (EXPERT_REVIEW). 헤드라인·About부터 즉시 적용 가능.
6. **§6 인계**: B4·B5가 흔들리지 않도록 결정만 모아 적는다.

> 본 문서가 비어 있는 동안에는 B4 디자인 작업을 시작하지 않는다 — 5섹션이 흔들리면 컴포넌트도 흔들린다.
