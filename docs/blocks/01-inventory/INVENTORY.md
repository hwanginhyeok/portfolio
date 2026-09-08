# 자산 마스터 인벤토리

> 최종 수정: 2026-04-26 (수치 검증 완료 + 사진 정책 변경)
> 목적: 쓸지 말지 판단 전, 있는 것을 전부 나열한다.

## 범례

- **상태**: 🟢 확보 / 🟡 대기 / 🔵 잠재
- **등급**: A (그대로) / B (가공 필요) / C (대체·보충 필요)

---

## 1. 케이스 콘텐츠 (cases/)

| ID | 자산 | 상태 | 등급 | 위치 | 비고 |
|----|------|:---:|:---:|------|------|
| C01 | D1 커리어 내러티브 | 🟢 | A | `cases/D1_career_narrative.md` | |
| C02 | D2 배터리 호환성 케이스 | 🟢 | A | `cases/D2_battery_compatibility_case.md` | |
| C03 | D3 상태머신 케이스 | 🟢 | A | `cases/D3_state_machine_case.md` | |
| C04 | D4 펌프 파워 케이스 | 🟢 | A | `cases/D4_pump_power_case.md` | |
| C05 | D12 시험 주도 엔지니어 | 🟢 | A | `cases/D12_test_driven_engineer.md` | |

## 2. 통합 문서 (docs/포트폴리오/)

| ID | 자산 | 상태 | 등급 | 위치 | 비고 |
|----|------|:---:|:---:|------|------|
| D01 | CONTENT_V2 통합본 | 🟢 | A | `docs/포트폴리오/CONTENT_V2.md` | B2 참조 |
| D02 | THEME_MAP_V3 재구성안 | 🟢 | A | `docs/포트폴리오/THEME_MAP_V3.md` | B3 시작점 |
| D03 | FACT_CHECK V1~V6 | 🟢 | A | `docs/포트폴리오/FACT_CHECK_V1_V6.md` | 수치 검증 |
| D04 | WEB_STRUCTURE | 🟢 | B | `docs/포트폴리오/WEB_STRUCTURE.md` | 구조 초안 |

## 3. 이미지 자산

> 2026-04-24 전수 결정: 유지 52 / 컷 14 / 확인 필요 2 / 중복 3 (물리 파일 69개).
> 기준: `public/images/` 하위 파일 전수 분류. 카테고리별로 정리.

### 3-1. 확정 유지 (52개)

#### About / Hero / Battery (4)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-A01 | 프로필 증명사진 | A | `public/images/about/profile.webp` |
| I-H01 | 제품 전면 (Hero) | A | `public/images/hero/product-front.webp` |
| I-H02 | 제품 후면 (Hero) | A | `public/images/hero/product-rear.webp` |
| I-B01 | 배터리 팩 상면 | A | `public/images/cases/battery/battery-pack-top.webp` |

#### EOP-400W (14 — `eop-400w/` 전체)

| ID | 자산 | 등급 | 위치 | 비고 |
|----|------|:---:|------|------|
| I-E01 | BEMF 관측기 블록도 | A | `public/images/cases/eop-400w/bemf-observer.webp` | |
| I-E02 | CAN 슬립 테스트 | A | `public/images/cases/eop-400w/can-sleep-test.webp` | |
| I-E03 | CAN 웨이크업 패턴 | A | `public/images/cases/eop-400w/can-wakeup-pattern.webp` | |
| I-E04 | 다이나모 응답성 시험 | A | `public/images/cases/eop-400w/dynamo-response.webp` | |
| I-E05 | 다이나모 회로도 | A | `public/images/cases/eop-400w/dynamo-schematic.webp` | |
| I-E06 | EEMF 추정기 블록도 | A | `public/images/cases/eop-400w/eemf-estimator.webp` | |
| I-E07 | 위치/속도 추정기 블록도 | A | `public/images/cases/eop-400w/position-speed-estimator.webp` | |
| I-E08 | PWM 120℃ 평형점 차트 | A | `public/images/cases/eop-400w/pwm-chart-120c-equilibrium.jpg` | 🔁 test-engineering/ 중복 |
| I-E09 | PWM 120℃ 차트 | A | `public/images/cases/eop-400w/pwm-chart-120c.webp` | 🔁 test-engineering/ 중복 |
| I-E10 | PWM 55℃ 차트 | A | `public/images/cases/eop-400w/pwm-chart-55c.webp` | 🔁 test-engineering/ 중복 |
| I-E11 | 센서리스 전류 파형 | A | `public/images/cases/eop-400w/scope-sensorless-current.png` | |
| I-E12 | 기동 EEMF 파형 | A | `public/images/cases/eop-400w/scope-startup-eemf.png` | |
| I-E13 | 기동 위치 파형 | A | `public/images/cases/eop-400w/scope-startup-position.png` | |
| I-E14 | 기동 파형 종합 | A | `public/images/cases/eop-400w/startup-waveform.webp` | |

#### Patent (2)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-P01 | DQ 인덕턴스 측정 | A | `public/images/cases/patent/dq-inductance.webp` |
| I-P02 | 초기 위치 측정 파형 | A | `public/images/cases/patent/initial-position-scope.webp` |

#### State Machine (5 — `state-machine/` 전체)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-S01 | 제어 박스 외관 | A | `public/images/cases/state-machine/control-box-external.webp` |
| I-S02 | DM 로직 다이어그램 | A | `public/images/cases/state-machine/dm-logic.jpg` |
| I-S03 | 정션 박스 CAD | A | `public/images/cases/state-machine/junction-box-cad.webp` |
| I-S04 | LCD 패널 | A | `public/images/cases/state-machine/lcd-panel.webp` |
| I-S05 | 테스트 결과 | A | `public/images/cases/state-machine/테스트결과.png` |

#### Test Engineering — 펌프 벤치 (3)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-T01 | 펌프 벤치 1 | A | `public/images/cases/test-engineering/pump-bench-1.webp` |
| I-T02 | 펌프 벤치 2 | A | `public/images/cases/test-engineering/pump-bench-2.webp` |
| I-T03 | 펌프 HW 블록 다이어그램 | A | `public/images/cases/test-engineering/pump-hw-blockdiagram.png` |

#### Test Engineering — 팬 벤치 + 필드 (4)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-T04 | 팬 벤치 결과 | A | `public/images/cases/test-engineering/fan-bench-result.webp` |
| I-T05 | 팬 벤치 셋업 | A | `public/images/cases/test-engineering/fan-bench-setup.webp` |
| I-T06 | 팬 필드 개선 전 | A | `public/images/cases/test-engineering/fan-field-before.jpg` |
| I-T07 | 팬 필드 개선 후 | A | `public/images/cases/test-engineering/fan-field-after.jpg` |

#### Test Engineering — 노즐 (6)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-T08 | 노즐 시험 1 | A | `public/images/cases/test-engineering/nozzle-test-1.webp` |
| I-T09 | 노즐 시험 2 | A | `public/images/cases/test-engineering/nozzle-test-2.webp` |
| I-T10 | 노즐 비교 IMG_7290 | A | `public/images/cases/test-engineering/nozzle-comparison/IMG_7290.jpg` |
| I-T11 | 노즐 비교 IMG_7291 | A | `public/images/cases/test-engineering/nozzle-comparison/IMG_7291.jpg` |
| I-T12 | 노즐 비교 IMG_7292 | A | `public/images/cases/test-engineering/nozzle-comparison/IMG_7292.jpg` |
| I-T13 | 노즐 비교 IMG_7293 | A | `public/images/cases/test-engineering/nozzle-comparison/IMG_7293.jpg` |

#### Test Engineering — 스프레이 + 분사압력 (5)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-T14 | 스프레이 시험 1 | A | `public/images/cases/test-engineering/spray-test-1.webp` |
| I-T15 | 스프레이 시험 2 | A | `public/images/cases/test-engineering/spray-test-2.webp` |
| I-T16 | 스프레이 시험 3 | A | `public/images/cases/test-engineering/spray-test-3.webp` |
| I-T17 | 스프레이 시험 4 | A | `public/images/cases/test-engineering/spray-test-4.webp` |
| I-T18 | 분사압력 비교 | A | `public/images/cases/test-engineering/분사압력비교.png` |

#### Test Engineering — PID / PWM / Controller (7)

| ID | 자산 | 등급 | 위치 | 비고 |
|----|------|:---:|------|------|
| I-T19 | PID_8 | A | `public/images/cases/test-engineering/PID_8.png` | |
| I-T20 | PID_8_1 | A | `public/images/cases/test-engineering/PID_8_1.png` | |
| I-T21 | PID_16 | A | `public/images/cases/test-engineering/PID_16.png` | |
| I-T22 | PID_16_1 | A | `public/images/cases/test-engineering/PID_16_1.png` | |
| I-T23 | PWM 55℃ 차트 | A | `public/images/cases/test-engineering/pwm-chart-55c.webp` | 🔁 eop-400w/ 중복 |
| I-T24 | PWM 120℃ 차트 | A | `public/images/cases/test-engineering/pwm-chart-120c.webp` | 🔁 eop-400w/ 중복 |
| I-T25 | CC 컨트롤러 특성 | A | `public/images/cases/test-engineering/CC_Controller_Characteristics.png` | |

#### Test Engineering — 궤도 내구 (4)

| ID | 자산 | 등급 | 위치 |
|----|------|:---:|------|
| I-T26 | 내구 시험 전 | A | `public/images/cases/test-engineering/durability-before.webp` |
| I-T27 | 내구 시험 후 | A | `public/images/cases/test-engineering/durability-after.jpg` |
| I-T28 | 블랙탄 부하 spd5 | A | `public/images/cases/test-engineering/blacktan-load-spd5.webp` |
| I-T29 | 블랙탄 무부하 spd5 | A | `public/images/cases/test-engineering/blacktan-noload-spd5.webp` |

> **카운트 확인**: 4 + 14 + 2 + 5 + 3 + 4 + 6 + 5 + 7 + 4 = **54 물리 파일 / 52 고유 이미지** (3개 중복 처리 후)

### 3-2. 컷 (14개 — 포트폴리오 미사용)

| 사유 | 파일 |
|------|------|
| 오링/솔레노이드/여과기 (부품 불량 상세 — 톤 부적합) | `01_Alpha1_여과기파손.webp`, `02_Pilot2_솔레노이드.webp`, `03_Alpha1_솔레노이드.webp`, `04_Pilot3_솔레노이드.webp`, `05_Alpha2_솔레노이드.webp`, `06_오링불량_좌하분해.webp`, `07_오링리크.webp`, `08_오링depth가공불량.webp`, `09_오링wall가공불량.webp` |
| TR_260220 시험보고 (5장) | `TR_260220_사진_01_시험환경_전기식.png`, `TR_260220_사진_02_시험환경_기계식.png`, `TR_260220_사진_03_시험결과테이블.png`, `TR_260220_사진_04_설계변경_기존갭45mm.png`, `TR_260220_사진_05_설계변경_개선갭9mm.png` |

모두 `public/images/cases/test-engineering/` 하위. **물리 삭제는 별도 태스크로 진행** (혹시 나중에 재사용 가능성 대비해 일단 보존).

### 3-3. 확인 필요 (2개 — 🟡)

| ID | 파일 | 질문 |
|----|------|------|
| I-Q01 | `test-engineering/durability-test.webp` | 궤도 내구 사진인가, 펌프 내구 사진인가? 내용 미상 |
| I-Q02 | `test-engineering/230530_120053.png` | 무슨 장면/시험인지 불명 — 사용 여부 결정 필요 |

→ 사용자 확인 후 유지/컷/이동 결정.

### 3-4. 중복 — 단일화 필요 (3개)

동일 파일이 `eop-400w/`와 `test-engineering/` 양쪽에 존재. 어느 폴더를 정본(SSOT)으로 할지 결정 후 한쪽 삭제.

| 파일명 | 경로 A | 경로 B |
|--------|--------|--------|
| `pwm-chart-55c.webp` | `eop-400w/` | `test-engineering/` |
| `pwm-chart-120c.webp` | `eop-400w/` | `test-engineering/` |
| `pwm-chart-120c-equilibrium.jpg` | `eop-400w/` | `test-engineering/` |

→ **권장**: 케이스 매핑(B3) 확정 후 해당 케이스 폴더로 단일화.

### 3-5. 대기 — 정책 변경 (W)

> 2026-04-26 정책 변경: **신규 촬영 안 함. 관련 자료(PPTX/HIH_2/시험보고서)에서 대체 자료 발굴**.
> 각 항목 필요 시 사용자와 함께 자료 출처를 1:1 매칭.

| ID | 자산 | 대체 출처 후보 | 비고 |
|----|------|---------------|------|
| W01 | 범퍼 실차시험 사진 | PPTX 원본 (X01~X03) / 시험보고서 / HIH_2 | 1:1 매칭 필요 |
| W02 | 다이나모미터 장비 사진 | I-E04(다이나모 응답성) / I-E05(회로도) 활용 검토 | 기존 자산으로 대체 가능성 |
| W03 | 팬 벤치 장비 사진 | I-T05(팬 벤치 셋업) 활용 가능 | 기존 자산 활용 |
| W04 | 범퍼 시험 장비 사진 | TR_260220 시리즈 (컷 처리분 재검토) | 컷에서 부활 검토 |
| W05 | 양산 전장함 사진 | PPTX / HIH_2 검색 | 1:1 매칭 필요 |
| W06 | VCU PCB 실물 사진 | PPTX / HIH_2 검색 | 1:1 매칭 필요 |
| W07 | CAN 분석 장비 작업 화면 | I-E02(CAN 슬립) / I-E03(웨이크업) 활용 | 기존 자산으로 대체 가능성 |
| W08 | 펌프 내구 시험 사진 | 시험 기록 / PPTX 검색 | 1:1 매칭 필요 |

## 4. 수치 데이터

| ID | 자산 | 상태 | 등급 | 위치 | 비고 |
|----|------|:---:|:---:|------|------|
| N01 | SVPWM 효율 +1%/+4% 검증 | 🟢 | A | FACT_CHECK_V1_V6 | 2026-04-26 검증 완료 |
| N02 | SVPWM 온도 저감 데이터 | 🟢 | A | FACT_CHECK_V1_V6 | 2026-04-26 검증 완료 |
| N03 | EOP 응답성 수치 | 🟢 | A | CONTENT_V2 내 | |
| N04 | 펌프 파워 케이스 수치 | 🟢 | A | D4 내 | |

## 4A. 활동·지식 (2026-09-06 신설)

> 학력·경력 갱신 상태 + 2026-04 이후의 공학 사이드 프로젝트·AI 운영·제품 빌드·지식 베이스.
> 별도 문서: [`ACTIVITY_INVENTORY.md`](ACTIVITY_INVENTORY.md) — 저장소·커밋·테스트 실측 기반.
> 소팅·각색 방향: [`../02-usage/EXPERIENCE_SORT.md`](../02-usage/EXPERIENCE_SORT.md)

## 5. 경험·스토리 (잠재 콘텐츠)

> 2026-04-26 진행: AI 에이전트가 5개 초안 작성 중 (`cases/E01~E05_*.md`). 사용자가 검토 후 확정.

| ID | 자산 | 상태 | 등급 | 출력 위치 | 비고 |
|----|------|:---:|:---:|----------|------|
| E01 | GT-SS500 PM 경험 (APQP/WBS/이슈관리/BOM) | 🟡 | B | `cases/E01_pm_experience.md` | AI 초안 작성 중 |
| E02 | AI 활용 사례 (Claude Code 개발 자동화) | 🟡 | B | `cases/E02_ai_workflow.md` | AI 초안 작성 중 |
| E03 | 사이드 프로젝트 3종 (자율주행/정치통계/주식분석) | 🟡 | B | `cases/E03_side_projects.md` | AI 초안 작성 중 |
| E04 | 엔지니어링 철학 | 🟡 | B | `cases/E04_engineering_philosophy.md` | AI 초안 작성 중 |
| E05 | 기술 스택 시각화 (역량 맵) | 🟡 | B | `cases/E05_tech_stack_map.md` | AI 초안 작성 중 |

## 6. 특허·공식 자료

| ID | 자산 | 상태 | 등급 | 위치 | 비고 |
|----|------|:---:|:---:|------|------|
| P01 | 특허 페이지 콘텐츠 | 🟢 | A | `src/pages/patent/` | 검토 완료 |

## 7. PPTX (원본)

| ID | 자산 | 상태 | 등급 | 위치 | 비고 |
|----|------|:---:|:---:|------|------|
| X01 | 포트폴리오_황인혁_2026.pptx | 🟢 | B | 루트 | 이미지 원천 |
| X02 | 대학원_포트폴리오_황인혁.pptx | 🟢 | B | 루트 | 대학원 원천 |
| X03 | 대학원_포트폴리오_황인혁_리뉴얼.pptx | 🟢 | B | 루트 | 리뉴얼본 |

---

## 통계

### 전체

| 상태 | 개수 | 세부 |
|------|:---:|------|
| 🟢 확보 | 66 | 케이스 5 + 통합 문서 4 + 이미지 52 + 수치 4 + 특허 1 |
| 🟡 대기 | 15 | 이미지 확인 필요 2 + 사진 자료 매칭 8 (W01~W08) + 경험·스토리 초안 5 (E01~E05) |
| 🔵 잠재 | 0 | (E01~E05 → 초안 작성 단계로 이동) |
| **합계** | **81** | |

### 이미지 세부 (public/images/ 기준)

| 구분 | 개수 | 비고 |
|------|:---:|------|
| 물리 파일 총계 | 68 | `public/images/` 하위 이미지 |
| 확정 유지 (고유) | 52 | 3-1 섹션 |
| 컷 | 14 | 3-2 섹션 (물리 보존, 포트폴리오 미사용) |
| 확인 필요 | 2 | 3-3 섹션 |
| 중복 (단일화 필요) | 3 | 3-4 섹션 — 52개 고유에는 이미 중복 제거됨 |

## 다음 액션

B1 완료 게이트를 통과하면 → [B2 활용 전략](../02-usage/USAGE_STRATEGY.md)으로 이동
