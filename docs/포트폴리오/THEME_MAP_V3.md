# THEME_MAP V3 — 테마 중심 5섹션 재구성안

> 작성일: 2026-04-22
> 기반: CONTENT_V2.md v3 (DFMEA 기준 + 5 Track) · WEB_STRUCTURE.md · FACT_CHECK_V1_V6.md · 커밋 fee8de1
> 목적: 현 사이트(`src/pages/cases/*` 4개 + 홈)를 **5개 테마 섹션**으로 재배치.
> 상태: **리뷰 대기** — astro 파일 이동/수정은 승인 후.

---

## 1. 재구성 근거 — v3 DFMEA/5 Track 적용

CONTENT_V2 v3는 임팩트 블록을 Track A~E 5개로 분할했다. 그 축이 "고장모드 → 설계로 돌아가는 사고방식(DFMEA)"이다.
현 사이트는 `eop-400w / patent / ss500-state-machine / test-engineering` 4개 케이스 페이지로 구성돼 있고, 홈은 ThemeHeatmap + CaseCard 나열 구조다.
**문제**: 케이스 4개가 "프로젝트 단위"로 묶여 있어서 "이 사람의 엔지니어링 관점"이 드러나지 않는다. EOP/SS500이라는 프로젝트 이름만 남고, 사고방식이 섹션 경계를 못 넘는다.
**해결**: 5 Track의 "접근 방식"(DFMEA → 시험 증명 → 시스템 설계 → 양산 체계 → 기술 뿌리)을 테마 축으로 올리고, 프로젝트(SS500/EOP/Research)는 각 테마의 **근거**로 내려보낸다. 이렇게 하면 Track A~E + 역량 뿌리가 서사 흐름으로 이어진다.

---

## 2. 5개 테마 섹션 정의

### T-1. 현장에서 돌아오는 설계 — DFMEA
**핵심 메시지**: 현상을 의심하지 않고 원인을 추적한다. 고장모드를 먼저 상상하고 Boundary Diagram까지 돌려놓는다.
**포함 케이스**:
- Track A 4건: MCB 전해부식(#204) / LCD·RC·ADT 상태머신(#79) / 펌프 동파 오링 / GND 바운스 P-15
- 기존 `cases/ss500-state-machine`은 Track A-2의 심화 원고로 편입
**타깃 독자**: 양산·품질·신뢰성 담당자. DFMEA를 문서가 아닌 사고방식으로 다루는 엔지니어를 찾는 팀.
**공통 프레임**: 고장모드 → 근본원인 → 설계 변경 → 재현 검증 (4줄 고정)

### T-2. 기획에서 양산까지 — 시험으로 증명
**핵심 메시지**: 문서에서 끝나는 성능이 아니라 고객 손에 들어가는 성능. 장비가 없으면 만든다.
**포함 케이스**:
- Track B 3건: 팬 +57%(7.9→12.4 m/s) / 분사 트레이드오프(명판 허위 검증) / 범퍼 정지거리 0.082m
- 시험 4단계 프로세스 (기획·설계·증명·분석)
- 기존 `cases/test-engineering`은 T-2의 뿌리 케이스로 편입 (다이나모/팬/펌프/범퍼 벤치 직접 구축)
**타깃 독자**: 제품개발·신뢰성 검증 조직. "벤치 있어요?" 물었을 때 "만들었습니다"라고 답할 엔지니어를 찾는 팀.
**공통 프레임**: 기획 → 개발·분석 → 시험 증명 → 양산 반영 (4줄 고정)

### T-3. 시스템 아키텍처 — CAN과 차세대 설계
**핵심 메시지**: 통신이 깨지면 제품이 죽는다. 현 제품의 데이터가 다음 제품의 요구사항이 된다.
**포함 케이스**:
- Track C: CAN 5노드 분산 제어 · DBC 4종 · BusLoad 분석 · DBC 버전 비교로 BREAKING CHANGE 4건 사전 검출
- Track E: SS500 → SS1000 성능 로드맵 · 2-layer 장애물 감지 · 팬 POC Option A
**타깃 독자**: 시스템 설계·아키텍처 리더. 단일 노드가 아닌 분산 시스템을 끌어본 경험을 찾는 팀.
**비고**: Track C와 E를 한 테마로 묶는 이유는 "현재 시스템 설계 → 다음 시스템 설계"가 같은 근육이기 때문. Lifecycle Heatmap의 개발·기획·설계 셀을 관통.

### T-4. 양산 체계 — APQP로 제품을 완성한다
**핵심 메시지**: 양산은 문서로 굴러간다. DFMEA가 없으면 엔지니어의 직감이 사라졌을 때 품질이 무너진다.
**포함 케이스**:
- Track D 8건: APQP Phase 2~3 / DFMEA Assembly 재편 + Boundary Diagram / DFMEA #201/#210 Step 1~7(AP=H 5건) / BOM 132 / IQC 가이드 / 양산 ROM 체크리스트 / 혁신제품 실사 / D-13 즉시 조치
- 주니어 PM 역할 근거 (APQP/WBS/BOM 관리)
**타깃 독자**: 품질·PM·양산 준비 담당 리더. AIAG-VDA 정석 구조를 이해하고 운영한 사람을 찾는 팀.
**비고**: 기존 PREPARED 2-3(GT-SS500 PM 경험)이 이 섹션의 원고 소스.

### T-5. 엔지니어의 뿌리 — EOP · 연구 · 특허 · AI-Native
**핵심 메시지**: 현재의 역량은 "모델 → 시뮬레이션 → 실험 검증" 체질에서 왔다. AI 도구는 그 체질의 연장선.
**포함 케이스**:
- EOP 400W (2023~2024): SVPWM 절환 · CAN Sleep · -40°C 기동 · 다이나모 토크제어 비선형성 0.008%
- Patents 2건 (정직 기재): PN231067KR 초기위치 검출(공동 발명) / 저온 기동(개발 기여)
- Research (석사): IPMSM PHM · 저널 1 · 학회 4 · PHM 2021 우수포스터 · 신뢰성 2022 최우수발표
- AI-Native × 공학 철학: 3계층 LLM 라우팅 / PM 오케스트레이터 / hih-skills / Obsidian 297노트
- 기존 `cases/eop-400w`와 `cases/patent` 페이지는 T-5 하위 하드 링크로 유지
**타깃 독자**: 기술 깊이와 학습 이력을 읽어내는 리드 엔지니어. "이 사람이 뭘 훈련해서 여기까지 왔나"를 보려는 면접관.
**비고**: 4개 서브 블록이지만 테마는 하나 — **훈련된 체질**. 상단 인트로 한 단락으로 묶고 하위 카드 4장으로 분기.

---

## 3. 기존 페이지 → 테마 매핑표

| 현 경로 | 현 역할 | 재배치 대상 | 조치 |
|---|---|---|---|
| `src/pages/index.astro` | 홈 (Hero + ThemeHeatmap + CaseCard 4장) | 5 테마 섹션 컨테이너 | 섹션 구성 재작성. Hero + Lifecycle Heatmap + T-1~T-5 + About |
| `src/pages/cases/ss500-state-machine/index.astro` | SS500 제어권 상태머신 상세 | **T-1** (DFMEA A-2 심화) | 유지 + T-1 카드에서 딥링크 |
| `src/pages/cases/test-engineering/index.astro` | 시험 공학 케이스 | **T-2** (시험 4단계 뿌리 케이스) | 유지 + T-2 카드에서 딥링크 |
| `src/pages/cases/eop-400w/index.astro` | EOP 400W 상세 | **T-5** (EOP 서브 블록) | 유지 + T-5 EOP 카드에서 딥링크 |
| `src/pages/cases/patent/index.astro` | 특허 2건 상세 | **T-5** (Patents 서브 블록) | 유지 + T-5 Patents 카드에서 딥링크 |
| `src/components/Hero.astro` | Hero | 재사용 | CONTENT_V2 §2 카피로 교체 (별도 태스크) |
| `src/components/ThemeHeatmap.astro` | 테마 × 프로젝트 히트맵 | **Lifecycle Heatmap으로 교체** | 7단계 × 3프로젝트 매트릭스로 재작성 (별도 태스크) |
| `src/components/CaseCard.astro` | 범용 카드 | T-1/T-2/T-3/T-4 공통 카드 | 4줄 프레임(고장모드/기획) 대응 variant 추가 필요 |
| `src/components/StateMachine.astro` | 상태머신 HTML 컴포넌트 | T-1 (A-2 시각화) | 유지 |
| `src/components/SystemArchitecture.astro` | 아키텍처 HTML | T-3 (CAN 5노드 시각화) | 유지 · CAN 5노드 버전 검토 |
| `src/components/Timeline.astro` | 타임라인 | About 블록 | 최근순 재배치 (별도 태스크) |

### 신규 필요 컴포넌트 (승인 후 생성)
| 이름 | 용도 | 대응 테마 |
|---|---|---|
| `DFMEAField.astro` | 4줄 프레임 카드 4장 | T-1 |
| `PerformanceFlow.astro` | 기획→양산 4줄 카드 3장 | T-2 |
| `TestProcess.astro` | 시험 4단계 (기획/설계/증명/분석) | T-2 하단 |
| `CANDesign.astro` | CAN 5노드 분산 설계 | T-3 |
| `NextGen.astro` | SS1000 차세대 3건 | T-3 |
| `APQPSystem.astro` | 양산 체계 테이블 | T-4 |
| `Research.astro` | 석사 연구 블록 | T-5 |
| `Patents.astro` | 특허 2건 카드 (정직 기재) | T-5 |
| `AINative.astro` | AI-Native × 공학 철학 | T-5 |

---

## 4. 삭제/통합 후보

| 대상 | 판단 | 사유 |
|---|---|---|
| `ThemeHeatmap.astro` (현재 테마×프로젝트) | **교체** | v3 축이 "테마 × 프로젝트"가 아니라 "Lifecycle 7단계 × 3프로젝트". 새 `LifecycleHeatmap.astro`로 교체 후 기존 파일 삭제. |
| SCU / ADT / WIA 관련 잔존 콘텐츠 | **삭제** | CONTENT_V2 §11 Removal List 확정. 본인 주도 아님. |
| `/contact` 별도 페이지 계획 | **Footer로 축약** | WEB_STRUCTURE에는 있었으나 CONTENT_V2 §11에서 Footer 축약 확정. |
| "시험 9개" / "시험 7종" 개수 강조 | **표현 전환** | "기획·설계·증명·분석" 프로세스 강조로 교체. 개수 나열 제거. |
| 배터리 BMS SOC 162% 에피소드 | **제외 유지** | CONTENT_V2 §11 확정. 이미 현 사이트에도 없음. |
| `CaseCard.astro` 현 4장 그리드 | **재사용·리포지션** | 컴포넌트는 유지하고 index.astro에서의 역할만 5 테마 섹션으로 교체. |

---

## 5. 섹션 최종 순서 (index.astro 기준)

```
1. Hero
2. Lifecycle Heatmap (7단계 × 3프로젝트)

━━ 5 테마 섹션 ━━
3. T-1 현장에서 돌아오는 설계 (DFMEA) ─ Track A 4건
4. T-2 기획에서 양산까지 (시험 증명) ─ Track B 3건 + 시험 4단계
5. T-3 시스템 아키텍처 (CAN · 차세대) ─ Track C + E
6. T-4 양산 체계 (APQP) ─ Track D 8건
7. T-5 엔지니어의 뿌리 ─ EOP + Patents + Research + AI-Native

━━ 본인 소개 ━━
8. Timeline (최근순)
9. About + 기술 스택
10. Footer (연락처)
```

**서사 흐름**: "지금 푸는 문제(T-1/T-2) → 지금 설계하는 시스템(T-3/T-4) → 여기까지 온 훈련(T-5) → 사람 소개". CONTENT_V2 §12의 3블록 구조를 유지하되, 임팩트 5개와 역량 5개를 하나의 5 테마로 통합해서 섹션 수를 10→5로 압축.

---

## 6. CONTENT_V2 매핑 추적

| V3 테마 | CONTENT_V2 §번호 | Track | 비고 |
|:-:|---|:-:|---|
| T-1 | §6 | A | DFMEA 4건 그대로 |
| T-2 | §7 + §7 시험 4단계 | B + 시험 | §7이 중복 번호(7.x와 7.x)라 컴포넌트 레벨에서 TestProcess로 분리 |
| T-3 | §7A + §7C | C + E | CAN 설계 + 차세대 기획 통합 |
| T-4 | §7B | D | APQP 그대로 |
| T-5 | §4.2 + §4.3 + §5 + §8 | — | EOP + Research + Patents + AI를 "뿌리" 테마로 통합 (Track 외 역량 블록) |

**중복 번호 이슈**: CONTENT_V2에 §7이 두 번 나옴(§7 Track B, §7 시험 4단계). 구현 시점에 파일 분리 필요. 현 문서에서는 테마 레벨로 T-2 하위 두 컴포넌트(PerformanceFlow + TestProcess)로 해결.

---

## 7. 리뷰 체크리스트 (승인 전 확인)

- [ ] 5 테마 이름/경계가 사용자의 의도와 맞는가?
- [ ] T-3에 Track C(CAN)와 E(차세대)를 묶는 게 자연스러운가, 분리가 나은가?
- [ ] T-5 "뿌리"에 AI-Native까지 넣는 게 맞는가, 별도 섹션으로 뺄 것인가?
- [ ] `/contact` Footer 축약 방침 유지?
- [ ] `ThemeHeatmap.astro` 삭제·교체 합의 가능?
- [ ] 기존 4개 case 페이지(`eop-400w`, `patent`, `ss500-state-machine`, `test-engineering`)를 유지하고 홈에서 딥링크만 거는 방식 OK?

**승인 후 다음 단계**:
1. `src/data/theme-map.json` → Lifecycle Heatmap용으로 교체
2. `src/data/cases.json` → 5 테마 카드로 교체 (CONTENT_V2 §13.2 6카드 기반, T 매핑 추가)
3. 신규 컴포넌트 9종 생성 (§3 표)
4. `index.astro` 섹션 순서 재배치
5. `ThemeHeatmap.astro` 삭제 + `LifecycleHeatmap.astro` 신규
