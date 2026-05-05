# Fact-Check — Bond-Wire Lift-Off / IPMSM 학위논문 단언 검증

> 작성: 2026-05-05 | PM 직접 작성 (사용자 명시 지시)
> 트리거: D1 §3 표의 "Bond-wire lift-off in IGBT shows β > 1 — clearly a wear-out mechanism" 단언이 실제 P-01 / T-01 내용과 다르다는 사용자 지적
> 목적: 학습 자료(D1~D7+HTML)에 들어간 사후 매핑·풍부화·추정을 RESUME SSOT + 논문 abstract 기반으로 정정
> 정책: D-007 (외부 제출 자료 fact-check) 학습 자료에도 동일 적용

---

## 0. 결론 (TL;DR)

| 단언 (학습자료) | 실제 근거 | 판정 |
|----------------|----------|:----:|
| "Bond-wire lift-off shows β > 1, wear-out mechanism" (D1 §3) | P-01·T-01·P-02 모두 Weibull β 추정 / 수명 모델 / wear-out 정량화 **없음** | ❌ **사후 매핑** |
| "Conducted PCT; identified bond-wire lift-off and co-occurring failure modes" (D6/reliability_competency) | P-01은 검출·위치식별 방법, P-02는 본드와이어/솔더 열화 **모드 분석** — "identified" 가능, "Weibull fit"은 X | △ 동사 정정 필요 |
| "PCT 직접 수행" (reliability_competency Block 2 Arrhenius 항목) | 사용자 PCT 직접 수행 여부는 RESUME 명시 없음 — 공저 논문 참여 수준 가능성 | △ 사용자 확인 필요 |

→ **D1 §3, D2, D6, index.html에서 β/Weibull/wear-out 단언 제거 + 동사 톤다운 필요.**
→ **P-02에서 사용자가 실제로 PCT 셋업·운영을 했는지 확인 필요** (공저자 역할 명확화).

---

## 1. P-01 IEEE TIM 2024 — 검증 결과

### 1.1 서지 (RESUME §6.2 + IEEE Xplore 검색 결과)

- **저자 순서**: Oh, Kim, **Hwang (3저자)**, Choi, Kim
- **저널**: IEEE Transactions on Instrumentation and Measurement, Vol. 73, Art. 10726721
- **DOI**: https://doi.org/10.1109/TIM.2024.3472910
- **출판**: 2024-10
- **제목 (정확)**: *Programmable Online Bond-Wire Fault Detection and Location Method for Insulated Gate Bipolar Transistor Using Inverter Output Parameters*
- **출처**: IEEE Xplore https://ieeexplore.ieee.org/document/10726721/ (직접 fetch는 anti-bot 차단, WebSearch로 확인)

### 1.2 핵심 기여 (검색 결과 요약 verbatim)

> "Programmable method for detecting and pinpointing the location of bond-wire lift-off in IGBTs without accessing the gate signal or the collector and emitter terminals of the targeted IGBT chip or freewheeling diode."
>
> "Methodology focuses on collecting and processing the collector-emitter voltage data from the three-phase motor phase terminal voltage."
>
> "Addresses prognostics and health monitoring of insulated gate bipolar transistors as a primary concern for inverter system reliability, particularly relevant given the rising popularity of electric vehicles."

### 1.3 본 논문에 **없는 것** (확인됨)

- ❌ Weibull β/η 추정
- ❌ 수명 모델 (Coffin-Manson, Arrhenius, Norris-Landzberg)
- ❌ B10/MTTF 산출
- ❌ wear-out vs random failure 정량화
- ❌ 가속수명시험(ALT) 설계
- ❌ Power Cycling Test (PCT) 자체 수행 (출력 신호 기반 진단이지 PCT 시험 자체가 아님)

→ **본 논문은 검출·위치 식별(detection + location) 알고리즘 논문**. 신뢰성 모델링·수명 분석 논문이 **아님**.

### 1.4 사용자가 한 일 (3저자 통상 역할 + RESUME §6.2 텍스트 기준)

RESUME 문장: "인버터 게이트 신호 진단 · 본드와이어 lift-off 검출 (IEEE TIM 2024)"

- 학습용 자료 인용 시 정직 표현: "Co-authored an IEEE TIM 2024 paper on programmable detection and location of IGBT bond-wire lift-off using inverter output parameters."
- **사용 금지** 표현: "estimated Weibull β / lifetime / wear-out mechanism / Coffin-Manson / B10" (논문 범위 외)

---

## 2. T-01 석사 학위논문 — 검증 결과

### 2.1 서지 (PAPERS.md §0 + RESUME §3 + WebSearch)

- **저자**: 황인혁 (단독, 석사)
- **소속**: 건국대학교 기계항공공학부 → 신뢰성기반최적설계(RBDO) Lab
- **연도**: 2023 (학위수여 2023-03-22)
- **제목 (한글)**: PAPERS.md §0 RISS 등록 정본 — 본 fact-check 시점에 RISS/dcollection 직접 접근 차단으로 정확 한글 제목 미확정 (B1-17b로 등록된 잔존 항목)
- **부제 (RESUME §11)**: "Sim2Real precursor: IPMSM digital twin + Co-simulation"
- **영문 인용 (J-01 표현)**: "Co-simulation for Fault Diagnosis of 120kW IPMSM and Experimental Validation"
- **출처**: RISS 학위논문 DB (PAPERS.md §0 비고 — 2026-04-26 검증)

### 2.2 학위논문 ↔ P-03 PHM Asia 2023의 관계

PAPERS.md §1 P-03 비고: "**T-01 학위논문 기반 학회 발표**"
PAPERS.md §1 P-03 핵심 기여:
> "120 kW 8극 36슬롯 IPMSM 구동 시스템에 다양한 고장 모드(영구자석 감자·권선 단락 등) 주입 → 상전류 데이터 → SVM 분류. 200 kW 다이나모/NI-9215 DAQ 실험 검증."

→ 학위논문 핵심 내용은:
- **대상**: 120 kW 8극 36슬롯 IPMSM 구동 시스템 (모터)
- **고장 주입**: 영구자석 감자(demagnetization) · 권선 단락(winding short) **등** (IGBT 본드와이어 아님)
- **방법**: 상전류 데이터 → SVM 분류
- **검증**: 200 kW 다이나모 + NI-9215 DAQ
- **방법론**: Co-simulation (시뮬레이션 ↔ 실험)

### 2.3 학위논문에 **없는 것** (확인됨)

- ❌ IGBT bond-wire lift-off (별도 논문 P-01에서 다룸 — 다른 트랙)
- ❌ Weibull β 추정 / 수명 모델
- ❌ ALT 설계
- ❌ wear-out mechanism 정량화

### 2.4 학위논문 ↔ S-S Interference / RBDO 연결

- 사용자 소속이 **신뢰성기반최적설계(RBDO) Lab**인 것은 사실 (RESUME §3)
- 단, **학위논문 자체는 RBDO 적용이 아니라 IPMSM 고장 진단 (Co-simulation + SVM)**
- → "RBDO 연구실 출신 + 학위논문은 PHM/Diagnostics 트랙" 분리 표현 필요
- **인터뷰 어필 가능**: "I was trained in RBDO Lab — Stress-Strength interference and reliability index β were the foundational concepts of my graduate environment, even though my thesis focused on co-simulation-based fault diagnosis of a 120 kW IPMSM rather than RBDO optimization itself."

---

## 3. P-02 PCIM Asia 2022 — 검증 결과 (제한적)

### 3.1 서지 (RESUME §6.2)

- **학회**: PCIM Asia 2022
- **주제 (RESUME 표현)**: "IGBT Power Cycling, IPM 본드와이어/솔더 열화"
- **PAPERS.md §1 P-02 핵심 기여**: "IGBT IPM에 준-DC 전원사이클 시험을 가해 본드와이어/솔더 열화 모드 분석. P-01 IEEE TIM 2024의 기초."
- **개방 액세스 미확보** — PCIM Asia proceedings는 유료. 본 fact-check 시점에 abstract 직접 검증 불가.

### 3.2 RESUME 표현 기준 사용자 한 일

- 준-DC 전원사이클 시험 (Quasi-DC Power Cycling Test) 가해서 → 본드와이어/솔더 **열화 모드 분석** (failure mode analysis)
- → **사용자가 PCT를 직접 셋업·운영했는지** vs **공저 논문 참여 수준**인지는 RESUME에 명시 없음
- **확인 필요**: P-02에서 사용자의 정확한 역할 (실험 설계/운영/분석/공저자 검토)

### 3.3 정직 표현 후보

- (확인 후 사용 가능) "Co-authored a PCIM Asia 2022 paper analyzing bond-wire and solder degradation modes in IGBT IPMs under quasi-DC power cycling tests."
- (확인 전 안전 표현) "Participated in a PCIM Asia 2022 paper on quasi-DC power cycling-induced degradation analysis of IGBT IPM bond-wire and solder."

---

## 4. 학습 자료 단언 vs 실제 — Mismatch 표

| 위치 | 학습자료 단언 | 실제 (RESUME + 논문) | 정정안 |
|------|-------------|---------------------|-------|
| D1 §3 표 row 2 | "Bond-wire lift-off in IGBT shows β > 1 — clearly a wear-out mechanism, which is why thermal cycling accelerates it." | P-01 = 검출·위치식별 방법, β 추정 없음. P-02 = 열화 모드 분석, β 추정 명시 없음 | "Co-authored research on IGBT bond-wire fault **detection and location** (P-01 IEEE TIM 2024) and **degradation mode analysis** under power cycling (P-02 PCIM Asia 2022). Lifetime modeling (Weibull/Coffin-Manson) was outside the scope of these papers." |
| D1 §3 표 row 1 | "Stress-Strength was the foundational concept of my graduate lab — RBDO is just the optimization layer on top of it." | 사실 (RBDO Lab 출신 + S-S는 RBDO 기반 개념) | 유지 가능. 단 "내 학위논문 자체는 RBDO 적용이 아니라 IPMSM 고장진단 Co-simulation" 1줄 추가 권장 |
| D2 (Coffin-Manson 페어링) | (확인 필요 — D2 본문 내 Coffin-Manson ↔ PCT 사용자 경험 단언이 있는지 검토 필요) | 사용자 PCT 직접 수행은 P-02 공저자 수준 가능성 | 동사 톤다운 ("conducted" → "co-authored research on" / "participated in") |
| D6 Camera/VCM §6.2 (Day1-5 수식 교차연결) | PCT 데이터로 β 추정 예시 시연 시 사용자 본인 데이터로 묘사된 부분 있으면 | 사용자 본인 β 추정 실적 없음 — 산식 시연용 가상 예시로만 사용 | "예시: 가상 데이터로 β 추정 절차 시연" 명시. 사용자 실데이터 단언 금지 |
| reliability_competency Block 2 Arrhenius | "PCT(Power Cycling Test) **직접 수행** — IGBT bond-wire lift-off 고장 + 추가 고장 메커니즘 동시 관찰 (P-01 IEEE TIM 2024 데이터)" | P-01은 검출 방법 (PCT 자체 수행 X). 사용자 PCT 직접 수행은 P-02 PCIM Asia 2022 가능성 — 역할 명시 없음 | "Co-authored P-01 (IEEE TIM 2024) on bond-wire fault detection method using inverter output parameters; co-authored P-02 (PCIM Asia 2022) on bond-wire/solder degradation modes under quasi-DC power cycling. Direct PCT setup/operation: confirm with user." |
| index.html (D1/D2/D6 섹션) | 위 단언들 동일 반영 가능성 | 동일 정정 필요 | 위 정정안 일괄 적용 |

---

## 5. 권장 정정 톤

### 5.1 인터뷰 60초 답변 (영문) 정정안

**Before (D1 §4 — 현행)**:
> "I'd start by treating both load and strength as distributions, not single numbers — that's stress-strength interference. ... I'd fit a Weibull to ALT data and report B10 instead of mean ..."

→ **유지 가능** (S-S와 Weibull은 일반론 답변, 사용자 본인 fit 단언 아님)

**Before (D1 §3 표 활용 → 답변 시)**:
> "Bond-wire lift-off in IGBT shows β > 1 — clearly a wear-out mechanism."

→ **삭제 필요** (단언 근거 없음)

**After (정직 톤)**:
> "I co-authored two papers in the bond-wire failure space — one on detection and location of IGBT bond-wire lift-off using inverter output parameters (IEEE TIM 2024), and one on degradation mode analysis under quasi-DC power cycling (PCIM Asia 2022). Quantitative lifetime modeling — fitting a Weibull or applying Coffin-Manson — was outside the scope of those papers and is on my self-study list."

### 5.2 Cover letter / Resume 영향

이미 fact-check 통과 (커밋 80a759e, 55431bb, 7c8c5ab) — 외부 제출 자료(resume_en v3, cover_letter)에는 본 단언 없음 확인됨.
→ **학습 자료(D1~D7+HTML)만 정정 대상**.

---

## 6. 사용자 확인 필요 항목 (Phase 2)

학습 자료 정정 전 사용자 답변 받으면 정확도 ↑:

- [ ] **P-02 PCIM Asia 2022에서 본인 역할** — 실험 설계/PCT 셋업/운영/데이터 분석/공저자 검토 중 어디까지?
- [ ] **PCT 시험을 본인이 직접 셋업·운영한 경험이 P-02 외에 있는가?** (예: 연구실 다른 실험, 회사에서)
- [ ] **Weibull β 추정 / Coffin-Manson 외삽 / B10 산출 본인이 직접 한 경험 있는가?** (RESUME에 명시 없으면 학습 자료에서 단언 모두 제거)
- [ ] **학위논문 정확한 한글 제목** (B1-17b 잔존 항목 — RISS/dcollection 직접 검색 결과)
- [ ] **학위논문에서 Co-simulation 외에 신뢰성/Weibull/ALT 관련 챕터 있는가?** (있으면 학습 자료에 활용 가능)

---

## 7. 정정 작업 우선순위 (다음 단계)

1. **즉시 정정 (★★★)**: D1 §3 표 row 2 ("β > 1 wear-out" 단언) + index.html 동일 부분 → "검출·위치식별 + 열화 모드 분석" 톤
2. **즉시 정정 (★★★)**: reliability_competency Block 2 Arrhenius row "PCT 직접 수행" → "co-authored research" 톤다운
3. **사용자 확인 후 정정 (★★)**: D2 / D6 / interview_60sec_scripts에 PCT/β/Weibull 사용자 본인 경험 단언 있으면 일괄 톤다운
4. **확정 후 정정 (★★)**: T-01 한글 제목 PAPERS.md / RESUME §6.1 갱신
5. **DIFFICULTY 추가 검토**: D-007 (외부 제출) 외에 학습 자료에도 동일 패턴 발생 → D-008 별도 또는 D-007 확장으로 기록

---

## 8. 출처 / 참조

- IEEE Xplore P-01: https://ieeexplore.ieee.org/document/10726721/
- DOI: https://doi.org/10.1109/TIM.2024.3472910
- PAPERS.md: `docs/포트폴리오/PAPERS.md` §0 (T-01) §1 (P-01·P-02·P-03)
- RESUME.md: `docs/blocks/05-extra/RESUME.md` §3 (소속) §6.1 (학위논문) §6.2 (공저 저널) §11 (포지셔닝)
- 산업 일반 문헌 (사용자 단언 아님, 참고용):
  - Nature Sci Reports 2021 — Effect of load sequence interaction on bond-wire lifetime due to power cycling
  - ScienceDirect — State-of-the-art of the bond wire failure mechanism and power cycling lifetime in power electronics
  - MDPI Electronics 2022 — A Fault Detection Method of IGBT Bond Wire Fatigue Based on Heatsink Thermal Resistance

→ 산업 일반 문헌은 "bond-wire lift-off는 wear-out mechanism이며 Coffin-Manson/Norris-Landzberg 모델로 외삽 가능"을 지지함. 단, **사용자 본인이 그 분석을 수행한 적은 없음** — 일반론으로만 답변 가능 (인터뷰 시 "I'm aware of the literature... my own work was on detection methods...").

---

## 9. 누락된 1차 자료 — 사용자 제공 요청

PM이 직접 접근 불가능한 자료:

- [ ] **P-01 IEEE TIM 2024 풀텍스트 PDF** — IEEE Xplore 유료, anti-bot 차단. 사용자 IEEE 회원 또는 학교 라이브러리 통해 PDF 확보 후 PM에 경로 알려주기
- [ ] **P-02 PCIM Asia 2022 풀텍스트 PDF** — 학회 proceedings 유료
- [ ] **T-01 석사 학위논문 풀텍스트 PDF** — RISS/dcollection.konkuk 직접 접근 차단 (서버 ECONNREFUSED). 사용자 보유분 또는 dCollection 로그인 필요
- [ ] **(있으면) P-02 발표 슬라이드** — 본인 역할 / PCT 셋업 사진 / 측정 데이터 그림

→ 위 자료 1~2개라도 받으면 §6 Phase 2 항목 즉시 답 가능 + 학습 자료 풍부화 가능 (단, 사후 매핑이 아닌 1차 근거 기반).
