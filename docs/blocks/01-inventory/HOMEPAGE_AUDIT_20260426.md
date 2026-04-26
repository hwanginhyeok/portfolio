# 홈페이지 점검 리포트 (B1 마무리)

> 작성일: 2026-04-26
> 범위: `src/pages/index.astro`, `src/pages/cases/*`, `src/components/*`
> 기준: `docs/blocks/01-inventory/INVENTORY.md` (SSOT) + `FACT_CHECK_V1_V6.md` + `CONTENT_V2.md` + `cases/D1_career_narrative.md`
> 원칙: B1 마무리 — **있는 자료를 정확하게**. 새 페이지/컴포넌트/대규모 재배치 금지(B3 영역).

---

## 1. 점검 결과 요약

| 분류 | 개수 |
|---|:---:|
| 명백한 사실 오류 (수정 대상) | 8 |
| 자체 모순 (수정 대상) | 3 |
| INVENTORY 컷 자산 사용 | 0 |
| INVENTORY 확인 필요 자산 사용 | 0 |
| 미사용 컴포넌트 | 0 |
| Removal List 위반 (B3 영역, 사용자 결정) | 2 |
| `[확인필요]` 주석으로 남길 항목 | 3 |

전체 빌드는 현재도 성공 — 수정 후 재검증 예정.

---

## 2. 명백한 사실 오류 (수정 진행)

### F-01. EOP 케이스 페이지 — SVPWM 결과 수치 과장
- **위치**: `src/pages/cases/eop-400w/index.astro` line 27, 31
- **현재**: "고온 효율 4% 향상", "FET 16~17°C 저감"
- **SSOT (CONTENT_V2 §4.2)**: "FET 온도 1~6°C 저감, 입력전력 1~3.8% 감소 (2,932 데이터 포인트)"
- **`test-engineering` Phase 2와도 불일치**: 같은 시험인데 "FET 1~6°C 저감"로 적혀 있음
- **조치**: CONTENT_V2 수치로 통일 — "효율 1~3.8% ↑", "FET 1~6°C ↓"
- **참고**: FACT_CHECK는 "PWM 절환 연구 / 55°/85°/120° 시험"까지만 명시. CONTENT_V2가 N01·N02 검증 완료(2026-04-26)로 등록된 SSOT임.

### F-02. EOP 케이스 — "협력사 현대 트랜시스, DIC" 표기
- **위치**: `src/pages/cases/eop-400w/index.astro` line 20, 67, patent/index.astro line 89
- **현재**: "협력사(현대 트랜시스, DIC) 요구조건 충족 필요"
- **SSOT (FACT_CHECK V-6)**: SCU가 DIC/현대 협력. **EOP는 국책과제** (정부 R&D).
- **CONTENT_V2 §1.1**: "SCU/ADT/WIA(본인 주도 아님) — 제거". EOP는 국책과제로 별도 명시.
- **조치**: "협력사 현대 트랜시스, DIC" 표현 제거. EOP 자체의 요구조건으로 표현. (단, patent 페이지 line 89의 SCU/현대 트랜시스 언급은 SCU 시기 발명 배경 설명이므로 유지하되 "현대 트랜시스" 출처 모호 → `[확인필요]` 주석)

### F-03. 특허 페이지 헤더 "직무발명 특허 1건 출원"
- **위치**: `src/pages/cases/patent/index.astro` line 12
- **현재**: "직무발명 특허 1건 출원 + 극저온 기동 실험적 검증"
- **본문**: 특허 카드가 2개 있음 (#1 본인 발명, #2 실험 담당)
- **SSOT (CONTENT_V2 §5.1)**: "특허 참여 2건 — 공동 발명 1 · 개발 기여 1"
- **조치**: 헤더를 "특허 참여 2건 — 공동 발명 1 · 개발 기여 1"로 정정 (CONTENT_V2 표현 그대로).

### F-04. 특허 #1 — "본인 발명" 배지
- **위치**: `src/pages/cases/patent/index.astro` line 19, `src/pages/cases/eop-400w/index.astro` line 136
- **현재**: 배지 "본인 발명"
- **SSOT (CONTENT_V2 §5.2)**: "**공동 발명자**" (정직 기재 원칙)
- **조치**: "본인 발명" → "공동 발명"으로 변경.

### F-05. cases.json — 특허 카드 metric "1건"
- **위치**: `src/data/cases.json` patent 항목, line 39
- **현재**: `"metric": "1건", "metricLabel": "특허 출원 (본인 발명)"`
- **SSOT**: 특허 2건 (공동/기여)
- **조치**: `"metric": "2건"`, `"metricLabel": "특허 참여 (공동 1·기여 1)"`로 정정. 카드 본문(role/result)도 2건 사실에 맞게 수정.

### F-06. SS500 상태머신 페이지 — "CAN 10노드"
- **위치**: `src/pages/cases/ss500-state-machine/index.astro` line 13
- **현재**: 헤더 "CAN 10노드"
- **본문 (line 113)**: "CAN 네트워크 — 6노드 메시지 구조"
- **SSOT (CONTENT_V2 §4.1, §7A.2)**: "**5노드** 분산 제어 (VCU ↔ 구동×2 ↔ 팬 ↔ 펌프 ↔ BMS)"
- **자체 모순 + SSOT 위반**: 페이지 안에서 10/6 다름.
- **조치**: 헤더 "CAN 5노드"로 통일. 본문 헤더는 "CAN 네트워크 — 5노드 + ADT" 또는 "5+1노드"로 정정 (테이블에 ADT PC 포함 시 6 row지만 분산 제어 노드는 5).

### F-07. EOP 페이지 — 하단 링크 "시험 기획 8종"
- **위치**: `src/pages/cases/eop-400w/index.astro` line 203
- **현재**: "다음: 시험 기획 8종 →"
- **다른 곳**: cases.json `"7종"`, test-engineering 페이지 헤더 `"7개 시험"`
- **조치**: "시험 기획 7종"으로 통일.

### F-08. Hero — "특허 1건"
- **위치**: `src/components/Hero.astro` line 32
- **현재**: "특허 1건 — 발명 + 논문·학회 7편"
- **SSOT (CONTENT_V2 §2.2)**: "특허 참여 — 공동 1 · 기여 1" (2건이지만 정직 기재)
- **D1**: "직무발명 특허 2건"
- **조치**: "특허 2건" + 서브 "공동 1 · 기여 1"로 정정. (논문·학회 수치는 F-09 참고)

---

## 3. 자체 모순 (수정 진행)

### F-09. 논문/학회 편수가 4개 문서에서 다 다름
- **Hero.astro**: "논문·학회 7편"
- **Timeline.astro**: "저널 2편 · 학회 5편(주저자 2)"
- **CONTENT_V2 §2.2 / §4.3**: "저널 1 · 학회 4"
- **D1 line 22**: 논문 편수 명시 없음
- **FACT_CHECK**: 학회 4건 확인 (PHM 2021/신뢰성 2022/PHM 2022/PCIM Asia 2022). CONTENT_V2 §15: "5번째 학회 발표 제목 — 빈칸. 1개 빈칸"
- **판단**: 가장 보수적이고 검증된 수치는 CONTENT_V2 §4.3 "저널 1 · 학회 4" (5번째는 미확인).
- **조치**: 
  - Hero "논문·학회 7편" → "저널 1·학회 4편" (혹은 합 "5편")
  - Timeline "저널 2편 · 학회 5편(주저자 2)" → "저널 1편 · 학회 4편(주저자)"
  - 두 문서 모두 같은 표현으로 통일.
- **`[확인필요]`**: 5번째 학회 발표 + 추가 저널이 있다면 사용자가 채울 것.

### F-10. test-engineering 카운트 — 7종 vs 8종 vs 7개
- **이미 F-07에서 "8종"은 오타로 확정** (다른 곳 모두 7).
- 페이지 "3년간 7개 시험 체계", cases.json "7종" → 통일됨. F-07만 수정하면 해결.

### F-11. 사이드 프로젝트 6개 (index.astro About)
- **위치**: `src/pages/index.astro` line 88-97
- **현재**: 6개 태그 (자율주행/정치통계/주식분석/음악프로덕션/AI개발자동화/포트폴리오)
- **CONTENT_V2 §11 Removal List**: "2-5 사이드 프로젝트 정리(PREPARED) — 사용자 지시로 제외"
- **Hero에도 "사이드 프로젝트 6개 진행 중"이 있음** (line 36)
- **판단**: §11은 "PREPARED 항목 제거"이지 About 섹션 자체 제거는 명시 X. **B3 영역에 가까움** — 사용자 결정 영역.
- **조치**: 그대로 두고 `[확인필요]` 주석으로 남김. 사용자가 B2/B3에서 결정.

---

## 4. 이미지 참조 정합성 (INVENTORY 3-1/3-2/3-3/3-4 대조)

전수 점검 결과 — **현재 사이트가 참조하는 이미지는 모두 INVENTORY 3-1 "확정 유지 52개" 안에 있음.**

| 참조 이미지 | INVENTORY ID | 상태 |
|---|:---:|---|
| `images/about/profile.webp` | I-A01 | OK |
| `images/hero/product-front.webp` | I-H01 | OK |
| `images/cases/state-machine/control-box-external.webp` | I-S01 | OK |
| `images/cases/eop-400w/pwm-chart-55c.webp` | I-E10 | OK (단, 3-4 중복: test-engineering/와 동일 파일) |
| `images/cases/eop-400w/pwm-chart-120c.webp` | I-E09 | OK (단, 3-4 중복) |
| `images/cases/eop-400w/pwm-chart-120c-equilibrium.jpg` | I-E08 | OK (단, 3-4 중복) — test-engineering 페이지가 이 파일 참조 시 eop-400w/ 경로 사용 |
| `images/cases/eop-400w/can-sleep-test.webp` | I-E02 | OK |
| `images/cases/eop-400w/can-wakeup-pattern.webp` | I-E03 | OK |
| `images/cases/eop-400w/eemf-estimator.webp` | I-E06 | OK |
| `images/cases/eop-400w/position-speed-estimator.webp` | I-E07 | OK |
| `images/cases/eop-400w/startup-waveform.webp` | I-E14 | OK |
| `images/cases/eop-400w/dynamo-schematic.webp` | I-E05 | OK |
| `images/cases/eop-400w/dynamo-response.webp` | I-E04 | OK |
| `images/cases/patent/dq-inductance.webp` | I-P01 | OK |
| `images/cases/patent/initial-position-scope.webp` | I-P02 | OK |
| test-engineering — `PID_16.png` | I-T21 | OK |
| test-engineering — `pwm-chart-120c-equilibrium.jpg` | (3-4 중복본) | OK (eop-400w/와 동일 파일 — 양 폴더 모두 존재) |
| test-engineering — `pump-bench-1.webp` | I-T01 | OK |
| test-engineering — `fan-bench-setup.webp` | I-T05 | OK |
| test-engineering — `fan-bench-result.webp` | I-T04 | OK |
| test-engineering — `nozzle-test-1.webp` | I-T08 | OK |
| test-engineering — `durability-before.webp` | I-T26 | OK |
| test-engineering — `durability-after.jpg` | I-T27 | OK |

### 4-1. 컷 14개 / 확인 필요 2개 사용 여부
- **컷 14개** (오링/솔레노이드/여과기 9 + TR_260220 5): **0건 사용** → OK
- **확인 필요 2개** (durability-test.webp, 230530_120053.png): **0건 사용** → OK

### 4-2. 중복 3개 (3-4)
- `pwm-chart-55c.webp`, `pwm-chart-120c.webp`, `pwm-chart-120c-equilibrium.jpg`: **양 폴더에 동일 파일 존재**.
- 사이트는 eop-400w/ 경로(eop-400w 케이스) + test-engineering/ 경로(test-engineering 케이스)를 각각 사용 중.
- INVENTORY 3-4: "권장 — 케이스 매핑(B3) 확정 후 해당 케이스 폴더로 단일화."
- **현재는 양쪽 모두 사용 중이라 단일화하면 한쪽이 깨짐**. **B3에서 정본 결정 후 단일화** — 지금은 그대로.
- 조치: `[TODO 중복단일화 B3]` 주석으로 남김.

### 4-3. 미사용 이미지
- `public/images/hero/product-rear.webp` — INVENTORY I-H02 "확정 유지"이지만 현 사이트 미사용.
- 판단: 미사용이지만 INVENTORY에 등록된 자산이고 B3에서 활용할 수 있음. 그대로 보존.

---

## 5. 컴포넌트 사용 현황

| 컴포넌트 | 사용처 | 상태 |
|---|---|---|
| `Hero.astro` | index.astro | 사용 중 |
| `CaseCard.astro` | index.astro | 사용 중 |
| `ThemeHeatmap.astro` | index.astro | 사용 중 (단, B3에서 LifecycleHeatmap으로 교체 예정 — THEME_MAP_V3 §3) |
| `Timeline.astro` | index.astro | 사용 중 |
| `SystemArchitecture.astro` | index.astro | 사용 중 |
| `StateMachine.astro` | ss500-state-machine/index.astro | 사용 중 |
| `BaseLayout.astro` | 모든 페이지 | 사용 중 |

**미사용 컴포넌트 0건**. `[UNUSED]` 주석 추가 대상 없음.

---

## 6. Removal List 위반 (B3 영역, 사용자 결정에 미룸)

CONTENT_V2 §11 / THEME_MAP_V3 §4 기준:

### R-01. ThemeHeatmap에 SCU/ADT/WIA 잔존
- **위치**: `src/data/theme-map.json` line 12-17
- **CONTENT_V2 §11**: "SCU/ADT/WIA — 본인 주도 아님, 제거"
- **THEME_MAP_V3 §4**: "SCU/ADT/WIA 관련 잔존 콘텐츠 — 삭제"
- **판단**: 데이터 교체는 B3 영역. **B3에서 LifecycleHeatmap.astro로 통째로 교체 예정** (THEME_MAP_V3 §3 "신규 필요 컴포넌트"). B1에서는 손대지 않음.
- **조치**: `[TODO Removal-B3]` 주석을 데이터 파일 상단에 추가만 함.

### R-02. cases.json 카드 4개 — v3 6 카드와 다름
- **현재**: `eop-400w / test-engineering / ss500-state-machine / patent` (프로젝트 단위)
- **CONTENT_V2 §13.2**: 5 Track 6 카드 (`dfmea-field / performance-flow / can-design / apqp-system / next-gen / eop-400w`)
- **THEME_MAP_V3**: 5 테마 섹션으로 재구성 — B3 영역
- **판단**: 카드 구조 자체 교체는 B3. B1에서는 사실 오류만 수정.

---

## 7. `[확인필요]` 주석 추가 대상

| 코드 위치 | 사유 |
|---|---|
| `src/pages/cases/patent/index.astro` 하단 메시지 | "현대 트랜시스 요구조건(-40°C)" 출처 — FACT_CHECK는 EOP를 국책과제로만 명시. SCU는 DIC/현대였으나 -40°C 요구가 SCU 것인지 EOP 것인지 사용자 확인 |
| `src/components/Hero.astro` 사이드 프로젝트 카운트 | CONTENT_V2 §11에 PREPARED 사이드 정리는 제거 명시 — Hero/About 표기 유지 여부 사용자 결정 |
| `src/components/Timeline.astro` 저널/학회 편수 | F-09에 따라 "저널 1·학회 4"로 통일하지만 5번째 학회 + 추가 저널이 있다면 사용자가 채울 것 |

---

## 8. 변경 계획 요약

| # | 파일 | 변경 |
|---|---|---|
| 1 | `src/components/Hero.astro` | 특허 "1건"→"2건"·서브 "공동 1·기여 1"; 논문·학회 카운트 정합성 |
| 2 | `src/components/Timeline.astro` | "저널 2편·학회 5편(주저자 2)" → "저널 1편·학회 4편(주저자)" + `[확인필요]` |
| 3 | `src/pages/cases/eop-400w/index.astro` | F-01 SVPWM 수치 정정, F-02 협력사 제거(국책과제 표현으로), F-04 "본인 발명"→"공동 발명", F-07 "8종"→"7종" |
| 4 | `src/pages/cases/patent/index.astro` | F-03 헤더 "특허 2건", F-04 "본인 발명"→"공동 발명", 하단 메시지 `[확인필요]` |
| 5 | `src/pages/cases/ss500-state-machine/index.astro` | F-06 헤더 "10노드"→"5노드", 본문 헤더 "6노드"→"5노드" |
| 6 | `src/data/cases.json` | F-05 patent 카드 "1건"→"2건"·라벨/role/result 정정; 상단 `[TODO Removal-B3]` 코멘트 |
| 7 | `src/data/theme-map.json` | `[TODO Removal-B3]` 주석 |
| 8 | `src/pages/index.astro` | 사이드 프로젝트 영역에 `[확인필요]` 주석 |

각 변경 위에 `// 변경: 사유 (참조 SSOT)` 형태로 한 줄 주석 추가.

빌드 재검증 후 보고.
