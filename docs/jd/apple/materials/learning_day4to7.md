# Reliability 학습 코스 — Day 4~7

> 작성: 2026-05-04 | Apple Reliability Engineer 면접 준비
> 전편: learning_day1to3.md (Weibull·B10 / JESD47·Coffin-Manson / 환경시험 표준)
> 목표: FRACAS·Reliability Growth / Bayesian·Cpk / VCM 통합 / STAR 5종 영문 풀스크립트
> 기준: "이 개념을 영문으로 60초 안에 설명할 수 있는가"

---

# Day 4 — FRACAS 5단계 + Reliability Growth (Duane / AMSAA)

---

## 4.1 핵심 개념 정의

### FRACAS (Failure Reporting, Analysis, and Corrective Action System)

**한 줄 정의**: 필드·시험 불량을 폐루프로 추적·분석·시정·검증·표준화하는 체계적
불량 관리 시스템 (DoD MIL-HDBK-2155 / IEC 60300-3-2 표준).

**영문 한 줄**:
> "FRACAS is a closed-loop system that ensures every failure — whether in test or
> field — is reported, root-caused, corrected, verified, and fed back into the
> design and process standard."

### Reliability Growth — Duane / AMSAA

**한 줄 정의**: NPI(신규 제품 도입) 또는 개발 단계에서 시정조치가 누적될수록
고장률이 낮아지는 추세를 추적·예측하는 모델 군.

**영문 한 줄**:
> "Reliability Growth models — Duane Plot and AMSAA Crow — quantify how failure
> rate decreases as design fixes accumulate during development, allowing prediction
> of when the product will hit the reliability target."

---

## 4.2 산식 / 메커니즘 / 프로세스

### FRACAS 5단계 폐루프 (★★★ 암기)

```
┌─────────────────────────────────────────────────────────────┐
│  FRACAS 폐루프                                               │
│                                                             │
│  ① Failure Reporting ──► ② Analysis ──► ③ Corrective Action│
│        ↑                                          │        │
│        │                                          ▼        │
│  ⑤ System Update ◄────────────── ④ Verification           │
└─────────────────────────────────────────────────────────────┘
```

| 단계 | 내용 | 산출물 |
|------|------|--------|
| **① Failure Reporting** | 발견 즉시 표준 양식 기록: 날짜·제품 ID·관찰 현상·발견자 | NCR / Defect Report |
| **② Analysis** | RCA (5 Why / Fishbone / DoE) — 근본원인 규명 | Root Cause Statement |
| **③ Corrective Action** | 설계 변경 / 공정 변경 / SOP 변경 | ECN / PCN / SOP Rev |
| **④ Verification** | 시정조치 효과 확인 — 재현 시험 또는 통계적 유의성 검증 | Re-test Report |
| **⑤ System Update** | DFMEA·검사 가이드·SOP 업데이트 + 동종 제품 horizontal deployment | 개정 문서 배포 |

**FRACAS 실무 도구**: Jira / SAP QM / Windchill / 자체 NCR DB

**FRACAS vs CAPA 차이**:

| 항목 | FRACAS | CAPA (QSR Part 820) |
|------|--------|---------------------|
| 출처 표준 | MIL-HDBK-2155 | FDA 21 CFR 820 |
| 적용 분야 | 항공·국방·반도체·소비재 | 의료기기·의약품 |
| 구조 | 5단계 폐루프 | Corrective + Preventive 2트랙 |
| 근본 차이 | 필드/시험 불량 중심 | 규제 준수 기록 중심 |

---

### Reliability Growth — Duane Plot

**Duane 관찰 (1962)**:
- 개발 시험 중 누적 고장 수를 추적하면, **log(누적 MTBF) vs log(누적 시험 시간)**이
  직선으로 나타난다.

```
Duane Plot:

log(θ_c) = log(K) + α · log(T)

θ_c : 누적 MTBF (= T / 누적 고장 수)
T   : 누적 시험 시간
K   : 상수
α   : Duane growth rate (기울기)

좋은 신뢰도 성장: α = 0.3 ~ 0.5
```

**직관적 의미**:
- α = 0.4이면 시험 시간이 10배 증가할 때 누적 MTBF가 10^0.4 ≈ 2.5배 증가.
- 시정조치가 효과적일수록 α가 크다.

```
log(θ_c)
   |             ●
   |          ●
   |       ●                   ← 기울기 = α (growth rate)
   |    ●
   | ●
   +─────────────────→ log(T)
```

---

### Reliability Growth — AMSAA Crow Model

**NHPP (Non-Homogeneous Poisson Process) 기반**:

```
λ(t) = λ · β · t^(β-1)

λ(t): 순간 고장 강도 (intensity function)
λ:    스케일 파라미터
β:    형상 파라미터

β < 1 → 고장률 감소 = 신뢰도 향상 중
β = 1 → 일정 고장률 (HPP, 지수분포)
β > 1 → 고장률 증가 (마모)
```

**신뢰도 성장 확인**: 개발 시험 중 β < 1이어야 한다.
β값이 0.5에 가까울수록 공격적인 성장 추세.

**AMSAA vs Duane 차이**:

| 항목 | Duane | AMSAA Crow |
|------|-------|-----------|
| 기반 | 경험적 직선 관계 | 통계 모델 (NHPP) |
| 추정 방법 | 그래프적 | MLE / Bayesian |
| 신뢰구간 | 없음 (그래픽) | 산출 가능 |
| 사용 시기 | 빠른 시각화 | 정밀 분석·예측 |

---

## 4.3 황인혁 경험과의 연결

### NCR 27건 = FRACAS 폐루프 (★★★ 핵심 어필)

황인혁의 GT-SS500 NCR 운영은 명칭만 다를 뿐 FRACAS 5단계와 1:1 매핑된다.

| FRACAS 단계 | 황인혁 NCR 실제 운영 |
|------------|---------------------|
| ① Failure Reporting | NCR 발행 — 날짜·제품 ID·현상·발행자 기록 |
| ② Analysis | RCA 수행 (MCB #204, LCD #79, 오링, GND 노이즈 4건) |
| ③ Corrective Action | 설계 변경(MCB 등급 교체)·공정 변경·검사 기준 갱신 |
| ④ Verification | 재현 시험·IQC/OQC 재합격 확인 |
| ⑤ System Update | DFMEA 갱신·검사 가이드 개정·BOM 반영 |

**인터뷰 핵심 멘트**: "The label was NCR, but the structure is FRACAS."

### Reliability Growth — DFMEA AP=H 5건 → 전부 해소

- DFMEA 5건 작성 → AP=H 5건 도출 → 전부 시정조치 → 잔여 위험 제로로 양산 진입.
- Reliability Growth 개념으로 재해석하면: "개발 단계 5개 고위험 항목을 순차 제거
  → β < 1 추세로 수렴 → 양산 기준 통과."
- AMSAA 수치는 계산하지 않았으나, 구조는 동일. 인터뷰에서는
  "functionally equivalent to Reliability Growth tracking" 표현 사용.

---

## 4.4 인터뷰 60초 답변 스크립트

### Script 4-A: "How do you operate a FRACAS system?"

> "FRACAS is a five-step closed loop: Failure Reporting, Analysis, Corrective
> Action, Verification, and System Update. At GINT I ran this loop on 27 NCRs
> for the GT-SS500 program. Each NCR started with a standard form — date,
> product ID, observed symptom, who found it. We then ran RCA: I personally
> led four of them, including an MCB carbonization case traced to electrolytic
> corrosion. The corrective action — upgrading to an IEC 60947-2 compliant
> breaker — was verified by reproducing the original failure mode and confirming
> zero recurrence. Then we updated the DFMEA, inspection guide, and BOM so
> the same failure couldn't slip through in production. The label was NCR,
> but the structure is textbook FRACAS."

단어 수: 120 / 발화: 약 65~70초 (조금 빠르게 하면 60초)

### Script 4-B: "What is Reliability Growth?"

> "Reliability Growth tracks the improvement in reliability as design fixes
> accumulate during development. The Duane model shows that log of cumulative
> MTBF grows linearly with log of cumulative test time — the slope, called alpha,
> is the growth rate. Alpha between 0.3 and 0.5 is considered healthy.
> The AMSAA Crow model is the statistical version — it uses a non-homogeneous
> Poisson process where the intensity function lambda times beta times t to the
> power beta minus one. If beta is less than one, the failure rate is decreasing,
> meaning reliability is growing.
> In my GT-SS500 program, we resolved all five high-priority DFMEA action points
> before production ramp — functionally equivalent to driving a Reliability Growth
> curve to target before release."

단어 수: 118 / 발화: 약 65초

---

## 4.5 예상 Follow-up 5개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "How do you decide when to close an NCR?" | 재현 시험 통과 확인 + DFMEA·SOP 업데이트 완료 확인 + 동종 제품 horizontal deployment 완료 후 |
| 2 | "What's the hardest part of FRACAS?" | ④ Verification — 시정조치가 새로운 문제를 만들지 않았는지 확인. 2차 효과(side effect) 검증이 RCA 자체보다 어렵다 |
| 3 | "Difference between FRACAS and CAPA?" | CAPA = FDA QSR Part 820, 의료기기 규제 준수 중심. FRACAS = MIL-HDBK-2155, 항공·반도체·소비재. 구조는 유사하나 규정 목적이 다름 |
| 4 | "How do you prioritize multiple open NCRs?" | Severity × Occurrence 점수 + 양산 일정 영향도. S=9~10 (Safety)은 무조건 1순위. 양산 gate 블로킹 여부 두 번째 기준 |
| 5 | "Tell me about a corrective action that didn't work" | 정직 답변: 1차 시정조치가 재발로 이어진 경우 → 근본원인이 충분히 깊게 파지 않았기 때문. 예: GND 노이즈 — 첫 번째 접지 보강 후 재현 → 추가 쉴딩으로 해소 |

---

## 4.6 학습 자료 / 출처

| 자료 | 상세 | 용도 |
|------|------|------|
| MIL-HDBK-2155 | everyspec.com | FRACAS 표준 원문 |
| IEC 60300-3-2 | iec.ch | 민간 FRACAS 표준 |
| Crow, "Reliability Analysis for Complex Repairable Systems" | AMSAA Technical Report (1975) | AMSAA 모델 원전 |
| ReliaSoft AMSAA 가이드 | reliawiki.org | Duane/AMSAA 플롯 실습 |
| Crow-AMSAA 계산기 | ReliaSoft Weibull++ | 실전 도구 |

---

---

# Day 5 — Bayesian Reliability + Six Sigma Cpk/Ppk

---

## 5.1 핵심 개념 정의

### Bayesian Reliability

**한 줄 정의**: 사전 정보(prior: 과거 ALT 데이터·전문가 의견)를 새 시험 데이터
(likelihood)와 결합해 사후 신뢰도 분포(posterior)를 도출하는 통계 프레임워크.

**영문 한 줄**:
> "Bayesian reliability combines a prior distribution — from historical ALT data
> or expert judgment — with observed test data via Bayes' theorem to produce
> a posterior that is narrower and more accurate than frequentist MLE alone,
> especially when sample sizes are small."

### Six Sigma / Cpk / Ppk

**한 줄 정의**: 공정 산포(σ)가 규격(USL·LSL) 대비 얼마나 여유를 갖는지 정량화하는
공정 능력 지수. Cpk ≥ 1.33이 양산 기본 기준.

**영문 한 줄**:
> "Cpk is the process capability index that accounts for both spread and centering —
> it equals the minimum of (USL minus mean) over three sigma and (mean minus LSL)
> over three sigma. Cpk of 1.33 corresponds to the typical production baseline
> of 4-sigma distance from mean to the nearer spec limit."

---

## 5.2 산식 / 메커니즘

### Bayesian Reliability — 핵심 수식

```
Bayes' Theorem:
P(θ | data) ∝ P(data | θ) × P(θ)

posterior ∝ likelihood × prior

θ: 신뢰성 파라미터 (예: Weibull β, η)
```

**Frequentist vs Bayesian 비교**:

| 항목 | Frequentist (MLE) | Bayesian |
|------|------------------|---------|
| 추정 기반 | 데이터만 | prior + 데이터 |
| 소표본 시 | 신뢰구간 폭 큼 | prior로 좁힐 수 있음 |
| 결과 | 점추정 + 신뢰구간 | 사후 분포 전체 |
| 해석 | "이 데이터가 나올 확률" | "파라미터의 확률" |
| 계산 도구 | Excel, Minitab | MCMC (Stan, PyMC3) |

**Jeffreys Prior** (비정보적 사전분포, non-informative):
- 데이터 변환에 불변(parameterization-invariant)하는 사전분포
- Weibull η에 대한 Jeffreys prior: π(η) ∝ 1/η (log-uniform)
- 사전 정보가 없을 때 기본 선택 — 반도체 신뢰성에서 종종 사용

**B10 Bayesian 추정 흐름**:
```
1. Prior 정의: β, η에 대한 사전 분포 (과거 ALT 결과 또는 Jeffreys)
2. Likelihood: 현재 시험 데이터 (고장 시간 + 중단 데이터)
3. Posterior 계산: MCMC 또는 conjugate 해석해
4. B10 사후 분포: 10th percentile of posterior predictive distribution
5. 90% 신뢰구간 도출 → 합격 기준 비교
```

**사용 시기**:
- 표본 수가 적어 Frequentist MLE가 불안정할 때
- 반도체 ALT (수십 개 이하 시험 유닛)
- 우주·항공 고신뢰성 부품 (시험 샘플 극소)

---

### Six Sigma — Cpk / Ppk 산식 (★★★ 암기)

```
Cp  = (USL - LSL) / 6σ_within
Cpk = min[ (USL - μ) / 3σ_within,  (μ - LSL) / 3σ_within ]

Pp  = (USL - LSL) / 6σ_overall
Ppk = min[ (USL - μ) / 3σ_overall,  (μ - LSL) / 3σ_overall ]

σ_within  : 단기 공정 내 σ (서브그룹 내 변동 → 공정 능력)
σ_overall : 장기 전체 σ (모든 변동 포함 → 공정 성과)
```

**Cpk vs Ppk 차이**:

| 항목 | Cpk | Ppk |
|------|-----|-----|
| σ 산출 | within-subgroup (단기) | 전체 데이터 (장기) |
| 반영 변동 | 기계 자체 정밀도 | 드리프트·시프트·배치 간 변동 포함 |
| 목적 | 공정 자체 능력 | 실제 공정 성과 |
| Cpk > Ppk | 공정 드리프트 존재 | Cpk = Ppk이면 안정된 공정 |

**Cpk 기준 해석표**:

| Cpk 값 | 해석 | 비고 |
|--------|------|------|
| < 1.0 | 불량 발생 중 | 즉시 개선 필요 |
| 1.00 | 3σ — 2700 DPMO | 최소 수준 |
| **1.33** | **4σ — 63 DPMO** | **양산 기본 기준 (통상 목표)** |
| **1.67** | **5σ — 0.57 DPMO** | **고신뢰성 부품 기준** |
| 2.00 | 6σ — 0.002 DPMO | 인체 이식형·항공 수준 |

**6σ의 의미 정리**:
```
단기 (±6σ 폭): DPMO = 0.002 (100만 회 중 0.002건)
장기 (1.5σ 드리프트 가정): DPMO = 3.4
→ "식스 시그마 = 3.4 DPMO"는 장기 성과 기준
```

**Cp가 높은데 Cpk가 낮은 경우 — centering 문제**:
```
예: USL=105, LSL=95, μ=102, σ=1

Cp = (105-95)/(6×1) = 1.67  ← 공정 폭은 충분
Cpk = min[(105-102)/3, (102-95)/3]
    = min[1.00, 2.33]
    = 1.00               ← 중심 치우침으로 Upper 쪽 여유 좁음
```
→ 공정을 μ=100으로 이동하면 Cpk = 1.67로 개선.

---

### DMAIC 5단계 (Six Sigma 방법론)

```
D — Define   : 문제 정의. CTQ(Critical to Quality) 식별. Project Charter
M — Measure  : 현재 공정 측정. Cpk/Ppk 기준선 수립. Gauge R&R
A — Analyze  : 근본원인 분석. Regression / DOE / Fishbone
I — Improve  : 최적 공정 조건 도출. Pilot run
C — Control  : 관리도(SPC) 설정. 표준화. 인수인계
```

---

## 5.3 황인혁 경험과의 연결

### Bayesian Reliability

**직접 사용 경험 없음. 정직한 기재.**

- RBDO Lab 출신 → 사전 분포(prior)로 강도 모델링하는 개념과 연결 가능.
- RBDO에서 강도 분포의 불확실성을 prior로 정의하고 후속 데이터로 업데이트하는
  구조가 Bayesian 프레임과 동일.
- 인터뷰 표현: "I haven't applied Bayesian reliability directly, but it's a natural
  extension of the RBDO framework I trained in — using prior distributions to model
  strength uncertainty before data is collected."

### Six Sigma / Cpk

**GT-SS500 IQC/OQC 운영 — 간접 적용**:
- IQC·OQC 검사 기준 정의 = DMAIC Define·Measure 단계와 동일 구조.
- 합격/불합격 기준 설정이 사실상 Cpk 목표값 기반.
- Cpk 보고서 공식 작성·검토 경험은 부수적 수준 — 인터뷰에서 과장 금지.
- 인터뷰 표현: "The gating logic was consistent with Cpk-based acceptance, though
  the full Six Sigma dashboard wasn't always our daily artifact."

---

## 5.4 인터뷰 60초 답변 스크립트

### Script 5-A: "How do you handle small-sample reliability?"

> "When sample sizes are small — say fewer than twenty units in an ALT — frequentist
> MLE gives wide confidence intervals on B10, sometimes too wide to be useful for
> decision-making. Bayesian reliability addresses this by incorporating a prior:
> historical data from a predecessor component, or a Jeffreys non-informative prior
> if nothing better is available. The posterior distribution of the Weibull parameters
> is then narrower than MLE alone, and you can extract a credible interval on B10
> directly. I haven't applied Bayesian reliability in production yet, but it's a
> natural extension of the RBDO framework from my graduate lab, where we used
> prior distributions to model strength uncertainty before test data arrived."

단어 수: 113 / 발화: 약 63초

### Script 5-B: "What is Cpk and how does it relate to IQC/OQC?"

> "Cpk is the process capability index that accounts for both spread and centering.
> It's the minimum of USL minus mean over three sigma, and mean minus LSL over three
> sigma. A Cpk of 1.33 is the standard production baseline — it means the mean is
> at least four sigma away from the nearer spec limit. For high-reliability parts
> you'd target 1.67 or above. At GINT I defined IQC and OQC inspection criteria
> for GT-SS500 production. The acceptance thresholds were set consistent with Six
> Sigma DMAIC principles, monitoring process capability for supplier qualification.
> Cpk and Ppk together tell you whether an underperforming supplier has a precision
> problem — Cpk low — or a drift problem — Ppk lower than Cpk."

단어 수: 118 / 발화: 약 65초

---

## 5.5 예상 Follow-up 5개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "Cpk vs Ppk — when does the gap matter?" | Cpk > Ppk이면 공정 드리프트 존재. 설비 교체·배치 간 원자재 변동 의심. Cpk = Ppk이면 공정 안정적 |
| 2 | "Why is 1.33 the baseline, not 1.0?" | Cpk 1.0 = 3σ = 2700 DPMO. 공정 변동·드리프트 여유 부족. 1.33 = 4σ = 63 DPMO. 1.5σ 장기 드리프트 허용 후에도 안전 |
| 3 | "How do you handle non-normal distributions in Cpk?" | 비정규: Box-Cox 변환 후 정규화 또는 비모수 Cpk (백분위수 기반). 또는 Cpk 자체를 포기하고 p-value 기반 합격률로 대체 |
| 4 | "What prior would you use for a brand-new component?" | 비정보 Jeffreys prior 또는 유사 기술 계열(예: 전 세대 IGBT) 데이터 기반 weakly informative prior. "No free lunch" — 사전 정보 없으면 데이터가 더 필요 |
| 5 | "Walk me through DMAIC on a real case" | GT-SS500 GND 노이즈 사례: D=노이즈 유발 제어 불안정 / M=Scope 파형·전압 레벨 기록 / A=DFMEA + 5 Why → EMI 경로 / I=쉴딩·접지 보강 / C=IQC 항목 추가·DFMEA 갱신 |

---

## 5.6 학습 자료 / 출처

| 자료 | 상세 | 용도 |
|------|------|------|
| Gelman et al., *Bayesian Data Analysis* (3rd ed.) | Ch.2 (prior·posterior), Ch.13 (Weibull) | Bayesian 기초 |
| Hamada et al., *Bayesian Reliability* (Springer) | 신뢰성 특화 Bayesian 교과서 | 실전 적용 |
| Minitab 공식 문서 | minitab.com | Cpk/Ppk 계산·해석 |
| Montgomery, *Introduction to Statistical Quality Control* (8th ed.) | Ch.8 (Cpk/Ppk) | SQC 교과서 |
| PyMC3 / Stan 공식 문서 | pymc.io / mc-stan.org | MCMC 실습 |

---

---

# Day 6 — Camera/VCM 복습 + Day 1~5 수식 교차연결

---

## 6.1 camera_vcm_reliability.md 핵심 8포인트 요약

> 원본 참조: camera_vcm_reliability.md (전체 학습 완료 필요)

**포인트 1. VCM 5대 고장 모드**

| 고장 모드 | 물리 메커니즘 | 황인혁 경험 연결 |
|-----------|--------------|----------------|
| 코일 단선/층간 단락 | 과전류·굴곡 피로 | IGBT 본드와이어 lift-off (동일: 전기 연결 열화) |
| 스프링 피로 파괴 | 반복 사이클·낙하 | 기계 피로 ALT 개념 (P-05) |
| 홀센서 드리프트 | 온도 의존성 | 멀티센서 PHM 경험 |
| 자석 감자 | 고온·역자기장 | IPMSM 영구자석 감자 (T-01, P-03) |
| 이물 침입 (먼지/수분) | 밀봉 불량 | EOP CAN 커넥터 IP67 설계 |

**포인트 2. ALT 스트레스 인자 → 고장 모드 매핑**

| 스트레스 | 가속 조건 | 주요 고장 모드 |
|---------|----------|--------------|
| 고온 | HTOL 85°C, 1000h | 코팅 박리·렌즈 크리프·자석 감자 |
| 온도 사이클 | −40°C ↔ +85°C | FPC 피로·접착제 박리 |
| 진동 | MIL-STD-810 Method 514 | 스프링 피로·접점 불량 |
| 낙하 충격 | 1.2m × 다방향 | 스프링 파괴·렌즈 파손 |
| 습도 | THB 85°C/85%RH | 코일 부식·코팅 박리 |

**포인트 3. VCM DFMEA 예시 (인터뷰 시연용)**

| 기능 | 고장 모드 | S | O | D | RPN | AP |
|------|----------|---|---|---|-----|----|
| AF 구동 | 코일 단선 | 8 | 4 | 4 | 128 | H |
| 위치 유지 | 스프링 파손 | 7 | 3 | 5 | 105 | M |
| AF 정확도 | 홀센서 드리프트 | 6 | 5 | 4 | 120 | H |

**포인트 4. PHM 신호 (실시간 열화 감지)**

| 센서 | 측정값 | 진단 대상 |
|------|--------|----------|
| 전류 | VCM 구동 전류 | 코일 저항 변화 → 열화 |
| 홀 센서 | 렌즈 위치 | 스트로크 감소 → 스프링 피로 |
| 온도 | 모듈 온도 | 열화 가속 모니터링 |
| 자이로 | 진동/각속도 | OIS 성능 저하 |

**포인트 5. Damage Summation VCM 적용**
```
스마트폰 하루 100회 AF 구동 → 3년 = 109,500회
ALT: 50°C 조건 500,000회 무고장 → Coffin-Manson 외삽으로 필드 수명 계산
```

**포인트 6. VCM 전용 B10 계산 참조** → §6.3 상세

**포인트 7. FA 5단계 (MCB → VCM 동일 적용)**
1. 현상 관찰 → 2. 고장 모드 정의 → 3. RCA → 4. 설계 변경 → 5. 재현 검증

**포인트 8. 광학 갭 현황 (정직한 자기 평가)**
- VCM 드라이버 회로 (Rohm/TI) — 추가 학습 필요
- 이미지 품질 평가 (ISO 12233 MTF) — 기초 이해 수준
- OIS 제어 알고리즘 — 개념 파악, 세부 구현 미달

---

## 6.2 Day 1~5 수식 → VCM 교차연결

### 연결 1: VCM 코일 단선 → JESD47 EM + Coffin-Manson

Day 2 Coffin-Manson 복습:
```
Nf = C · (ΔT)^(-n)
```

VCM 코일 구동 시 줄열(Joule heating) → 온도 사이클 발생 → 코일-단자 계면 피로.

```
VCM 코일 ΔT 추정:
- 구동 전류: 100 mA, 코일 저항: 20 Ω → P = I²R = 0.2 W
- 열저항(코일→환경) ≈ 30°C/W → ΔT ≈ 6°C per 1회 AF
- n(소형 코선) ≈ 3~5 (Al 와이어보다 작음, 솔더 범위)
- Nf = C · (6)^(-4) = C / 1296
→ 필드 109,500회 대비 ALT에서 ΔT를 50°C로 올리면:
  가속 인자 = (50/6)^4 ≈ 5,000배 → ALT ~22회만으로 3년 필드 커버
```

### 연결 2: VCM 스프링 피로 → Miner's Rule (Day 1) + Weibull β>1 마모

Day 1 Weibull 복습: β>1 → 마모 고장, 고장률 증가.

스프링 피로 메커니즘:
- β = 2.5~3.5 (기계 피로 마모 범위)
- Miner's Rule: 낙하 충격 + 일상 AF 사이클 + 온도 변동 → 복합 누적 손상

```
D_total = n_drop/N_drop + n_AF/N_AF + n_TC/N_TC

n_drop = 100회 (3년 추정), N_drop = 3,000 (ALT 낙하 수명)
n_AF   = 109,500회, N_AF = 1,000,000 (ALT AF 수명)
n_TC   = 1,095회 (1/day × 3yr), N_TC = 50,000 (ALT TC 수명)

D = 100/3,000 + 109,500/1,000,000 + 1,095/50,000
  = 0.033 + 0.110 + 0.022
  = 0.165   < 1.0 → 수명 OK (설계 마진 있음)
```

### 연결 3: 카메라 NCR → FRACAS 5단계 (Day 4) — Apple 공장 시나리오

```
시나리오: iPhone 카메라 생산 중 AF 불량 NCR 발행

① Failure Reporting: 생산 라인에서 AF 응답속도 규격 초과 → 즉시 NCR 발행
② Analysis: FA → 코일 저항 +15% 상승 → 재료 추적 → 납품 로트 특정 배치 이상
③ Corrective Action: 해당 배치 격리·재검사 + 납품업체 공정 감사
④ Verification: 신규 배치 100% IQC 전수 검사 → 저항 분포 정상 범위 확인
⑤ System Update: IQC에 코일 저항 Cpk ≥ 1.33 항목 추가 + DFMEA 원인 항목 추가
```

### 연결 4: VCM Cpk — 코일 저항 산포 (Day 5)

```
가정: 코일 저항 목표 = 20 Ω, 공정 σ = 0.5 Ω
     규격: USL = 22 Ω, LSL = 18 Ω

Cpk = min[(22-20)/(3×0.5), (20-18)/(3×0.5)]
    = min[2/1.5, 2/1.5]
    = min[1.33, 1.33]
    = 1.33   ← 기준 딱 충족

공정 중심 이동 μ = 20.5 Ω 로 드리프트 시:
Cpk = min[(22-20.5)/1.5, (20.5-18)/1.5]
    = min[1.00, 1.67]
    = 1.00   ← 기준 미달 → 납품 보류
```

### 연결 5: VCM ALT 합격 기준 → B10 + 안전계수 (Day 1)

B10 ≥ 필드 수명 × 안전계수 1.5 적용 시 필요 샘플 수 도출:

```
가정: η = 50,000 AF cycles, β = 2.5 (mechanical wear)

B10 = η · (-ln 0.9)^(1/β)
    = 50,000 × (0.10536)^(1/2.5)
    = 50,000 × (0.10536)^0.4
    = 50,000 × 0.4022
    ≈ 20,110 cycles

필드 요구 수명: 100 cycles/day × 365 × 3 = 109,500 cycles
안전계수 적용 합격 기준: 109,500 × 1.5 = 164,250 cycles

B10 (20,110) < 164,250 → 불합격 → η 또는 β 개선 필요
개선 목표: η ≥ 408,000 cycles 이상 (B10 ≈ 164,250 달성)
```

---

## 6.3 VCM 전용 B10 계산 예시 (인터뷰 시연용)

**시나리오**: VCM 스프링 피로 ALT 데이터에서 Weibull 피팅.

```
가정:
  η = 500,000 AF cycles (개선 후)
  β = 2.5 (기계적 마모)

B10 = 500,000 × (0.10536)^(1/2.5)
    = 500,000 × 0.4022
    ≈ 201,100 cycles

필드 수명 요구: 109,500 cycles
안전계수 1.5 기준: 164,250 cycles

B10 (201,100) > 164,250 → 합격 ✓
여유율: (201,100 - 164,250) / 164,250 × 100% = 22.4% margin
```

---

## 6.4 인터뷰 통합 답변 60초 — "Apple VCM 신뢰성을 어떻게 접근하시겠습니까"

> "I'd start with DFMEA — coil open, spring fatigue, Hall sensor drift,
> demagnetization, and contamination are the five primary VCM failure modes.
> Then I'd map each to an ALT stress: HTOL at 85°C for coating delamination
> and magnet degradation, temperature cycling for FPC and adhesive fatigue,
> drop test for spring failure, and THB for coil corrosion. From the ALT data
> I'd fit Weibull, compute B10, and require B10 to exceed the field life target
> times a safety factor of 1.5 — that calculation determines whether we pass
> or need to iterate on the design. For production I'd run incoming Cpk monitoring
> on coil resistance and stroke length. Any field NCR feeds back into a FRACAS
> closed loop — DFMEA update, inspection guide revision, horizontal deployment
> to similar part numbers."

단어 수: 128 / 발화: 약 70초 (빠르게 하면 60초)

---

## 6.5 예상 Follow-up 3개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "How do you set the ALT sample size for VCM qualification?" | 목표 B10 기준 + 신뢰수준(90%) + Weibull β 가정 → ReliaSoft 샘플 플래너 또는 χ² 기반 공식. 비용·일정 제약 시 Bayesian prior로 보완 |
| 2 | "What's the biggest failure risk for iPhone camera in the field?" | 낙하 충격 → 스프링 파괴 최우선. 스마트폰 필드에서 낙하 사고가 가장 빈번. 그 다음 장기 사용에 의한 VCM 코일 열화 (고온 환경, 셀피 동영상 장시간 사용) |
| 3 | "How does PHM apply to a VCM in a shipped iPhone?" | 구동 전류 서명 모니터링: 코일 저항 증가 → 구동 전류 변화 → 진단 알고리즘 → 사용자에게 서비스 권고. Apple Diagnostics 같은 내장 SW가 RUL 추정 역할 가능 |

---

---

# Day 7 — STAR 영문 답변 5종 풀스크립트

---

## 7.0 STAR 프레임워크 복습

**Apple 행동면접 표준**:

| 파트 | 권장 길이 | 핵심 |
|------|----------|------|
| Situation | 60~80단어 | 컨텍스트·제품·시점 명확히 |
| Task | 30~50단어 | 본인 역할과 목표 |
| Action | 80~120단어 | 본인이 취한 구체적 행동 (I, not we) |
| Result | 50~70단어 | **정량 수치 1~2개 필수** |
| 총 답변 | 2~3분 | 5~7분 절대 금지 |

**공통 주의사항**:
- "we did" → "I led / I identified / I decided"
- 정량 수치: 27건, 5건, 16 units, −40°C, 308A, 0.082m 등
- 질문이 "most challenging" / "biggest failure" 유형이면 정직한 어려움 포함
- 시제: 과거형 일관 (Simple Past)

---

## 7.1 STAR #1 — MCB Carbonization RCA (electrolytic corrosion)

### Situation (영문, 60단어)

> "During GT-SS500 pre-production validation in early 2025, I discovered visible
> charring on the 48V main circuit breaker terminals after repeated power cycling
> in the field simulation rig. The product was two months from planned production
> ramp, and an unresolved power fault at this voltage posed both a schedule risk
> and a potential field safety issue."

단어 수: 57

### Task

> "I was responsible for leading the root cause analysis, implementing a corrective
> action, verifying the fix, and ensuring the resolution was reflected in the DFMEA,
> inspection guide, and production BOM before first-article shipment."

단어 수: 40

### Action

> "I ran a five-step RCA. First, I precisely defined the failure mode: contact
> resistance rising under sustained DC current until thermal runaway.
> Second, I used 5 Why to trace back through the evidence: the charring was worst
> at the high-current terminal, arcing marks were asymmetric, and the MCB data
> sheet showed a continuous current rating below our 48V, 30A operating condition.
> Third, I identified the root cause as electrolytic corrosion — the MCB was running
> beyond its IEC 60947-2 specification, making galvanic degradation under DC bias
> unavoidable. Fourth, I redesigned to an IEC 60947-2 compliant breaker with
> adequate continuous current rating. Fifth, I reproduced the original failure
> mechanism in the lab with the old MCB, then ran 200 power cycles with the new
> MCB and confirmed zero recurrence. I logged this as NCR #204 in our tracking
> system and updated the DFMEA, IQC inspection item list, and BOM."

단어 수: 161

### Result

> "NCR #204 was closed before production ramp. The corrective action was
> horizontally deployed — the same IEC 60947-2 check was added to the inspection
> guide for all future programs. The first production batch of 16 units shipped
> with zero recurrence of the MCB fault. This RCA is now cited internally as a
> reference case for electrical component specification verification."

단어 수: 65

---

### 풀스크립트 (면접용, 자연스러운 연결)

> "During GT-SS500 pre-production validation in early 2025, I discovered visible
> charring on the 48V main circuit breaker terminals after repeated power cycling.
> The product was two months from planned production ramp, and an unresolved power
> fault posed both schedule risk and a potential field safety issue.
>
> My task was to lead RCA, implement a fix, verify it, and get it into the DFMEA
> and BOM before first-article shipment.
>
> I ran a five-step RCA. I defined the failure mode precisely: contact resistance
> rising under sustained DC until thermal runaway. Using 5 Why, I traced back:
> charring was worst at the high-current terminal, arcing was asymmetric, and the
> MCB data sheet showed a continuous current rating below our 48V, 30A operating
> condition. Root cause: electrolytic corrosion — the MCB was running beyond its
> IEC 60947-2 spec. I redesigned to a compliant breaker, reproduced the original
> failure in the lab to confirm the mechanism, then ran 200 power cycles with the
> new part and confirmed zero recurrence. I updated the DFMEA, IQC list, and BOM.
>
> NCR #204 closed before ramp. The fix was horizontally deployed to the inspection
> guide for all future programs. The first production batch of 16 units shipped
> with zero MCB faults. This case is now a reference example internally for
> electrical component specification checks."

총 단어 수: 220

### 후속 질문 3개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "How did you reproduce the failure in the lab?" | 동일 MCB + 48V / 30A 지속 전류 인가 + 수 시간 사이클 → 동일 탄화 패턴 재현. 재현 가능성 = 근본원인 신뢰도의 증거 |
| 2 | "What would you have done differently?" | NCR 발행 전 IQC에 IEC 등급 체크 항목이 있었다면 조달 단계에서 걸렸을 것. 앞으로는 DFMEA 시 전기 부품 규격 등급 항목을 설계 단계에서 검증 |
| 3 | "Was there schedule impact?" | 2주 지연 (재현 시험 + 신규 MCB 조달). 양산 일정에 흡수 가능한 버퍼 내. Critical Path에 영향 없었음 |

---

## 7.2 STAR #2 — IGBT PCT — Bond-Wire Lift-Off Identification (P-01)

### Situation (영문)

> "At Konkuk University RBDO Lab in 2022, our team was investigating health
> monitoring methods for IGBT power modules used in electric vehicle drivetrains.
> The question was: can we detect internal failure modes — specifically bond-wire
> degradation — from inverter output signals alone, without disassembly, during
> active operation of the motor drive system?"

단어 수: 61

### Task

> "I conducted Power Cycling Tests on IGBT modules following the JESD47 power
> cycling protocol, and my specific role was to identify the dominant failure mode,
> monitor electrical output signatures during degradation, and validate that
> bond-wire lift-off could be detected non-invasively."

단어 수: 50

### Action

> "I set up the PCT bench: the IGBT module was cycled between power-on and
> power-off states, generating a controlled junction temperature swing, delta-Tj,
> at the chip interface. I monitored three output parameters throughout the test:
> Vce saturation voltage, which rises as bond-wire resistance increases; collector
> current harmonics; and thermal resistance, which indicates die-attach degradation.
> After several thousand cycles, I observed a step increase in Vce-sat that was
> not accompanied by a rise in thermal resistance — this asymmetry confirmed that
> bond-wire lift-off, not die-attach solder fatigue, was the primary failure mode.
> I correlated the electrical signature pattern with physical inspection via
> cross-sectional microscopy after test. This work was conducted per JESD47
> and guided by JEP122 failure mechanism models."

단어 수: 141

### Result

> "The bond-wire lift-off failure was identified as the dominant degradation mode,
> and the non-invasive electrical signature detection was validated. This work
> was published in IEEE Transactions on Instrumentation and Measurement in 2024.
> DOI 10.1109/TIM.2024.3472910. The approach demonstrates that IGBT health can
> be monitored from system-level output parameters — no disassembly required."

단어 수: 65

---

### 풀스크립트

> "In 2022 at Konkuk University, our RBDO Lab team was investigating non-invasive
> health monitoring for IGBT power modules in EV drivetrains. The key question
> was whether we could detect internal failure modes from inverter output signals
> alone — without opening the module.
>
> My role was to run Power Cycling Tests per the JESD47 protocol on IGBT modules,
> identify the dominant failure mode, and validate electrical signature detection.
>
> I set up the PCT bench, cycling the module to generate a controlled delta-Tj at
> the chip interface. I monitored three parameters: Vce saturation voltage, collector
> current harmonics, and thermal resistance. After several thousand cycles, I saw
> a step increase in Vce-sat with no corresponding rise in thermal resistance.
> That asymmetry was the diagnostic key — it isolated bond-wire lift-off from
> die-attach solder fatigue. I confirmed with cross-sectional microscopy post-test.
> The test protocol followed JESD47; failure mode attribution was guided by JEP122.
>
> The work demonstrated that IGBT bond-wire lift-off is detectable from system-level
> output signals, and was published in IEEE Transactions on Instrumentation and
> Measurement in 2024. The core finding: Vce-sat rise without Rth rise equals
> bond-wire degradation — a signature that requires no disassembly to detect."

총 단어 수: 205

### 후속 질문 3개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "What was the test stopping criterion?" | 고장 기준: Vce-sat 20% 이상 증가 또는 Rth 20% 이상 증가. 어느 쪽이든 먼저 도달 시 중단. JESD47 정의 준수 |
| 2 | "How did you separate thermal resistance from electrical resistance?" | Vce-sat: 전기적 (bond-wire 저항) 변화. Rth: 열적 (die-attach 계면) 변화. 두 신호를 독립 모니터링 → 교차 분석으로 분리 가능 |
| 3 | "Can this apply to VCM coil degradation?" | VCM 코일도 저항 증가 → 구동 전류 변화 → 서명 기반 진단 가능. 원리 동일. PHM 경험을 카메라 모듈에 확장하는 스토리로 연결 |

---

## 7.3 STAR #3 — DFMEA #204 — AP=H 5건 도출 → 시정조치

### Situation (영문)

> "In late 2024 and early 2025, leading up to GT-SS500 production ramp, I was
> responsible for authoring Design Failure Mode and Effects Analysis for the
> 48V electrical architecture of the machine. The GT-SS500 is an autonomous
> agricultural speed sprayer operating in harsh outdoor environments — vibration,
> humidity, chemical exposure, temperature extremes — so the DFMEA scope covered
> all safety-critical and operationally critical electrical systems."

단어 수: 73

### Task

> "Using the AIAG-VDA 2019 DFMEA methodology, I needed to identify, quantify, and
> resolve all high-priority action points — AP=H items — across five DFMEAs before
> the production gate review."

단어 수: 42

### Action

> "I applied the seven-step AIAG-VDA 2019 process: planning and preparation;
> structure analysis; function analysis; failure analysis; risk analysis using
> Severity, Occurrence, and Detection ratings plus the Action Priority matrix;
> optimization; and results documentation.
> I authored five DFMEAs covering the MCB power circuit, the LCD control state
> machine, the hydraulic pump system, the CAN communication bus, and grounding
> and EMI. Across these five, I identified five items with Action Priority High —
> meaning the combination of severity and detectability required corrective action
> regardless of occurrence rating.
> For each AP=H item, I assigned ownership, defined the corrective action,
> set a target completion date, and tracked closure through NCR updates. The MCB
> item led to the RCA described earlier. The state-machine item required eliminating
> undefined state transitions that could cause unintended drive activation. The
> O-ring item required a dimensional redesign verified by pressure cycling. The
> GND noise item required shielding and revised grounding topology. The fifth item
> required a revised connector specification."

단어 수: 163

### Result

> "All five AP=H items were resolved and verified before the production gate review.
> Residual risk dropped to zero high-priority items at production entry. The updated
> DFMEAs were incorporated into the inspection guide and BOM, ensuring the corrective
> actions were production-proof. First-article shipment of 16 units produced with
> zero safety-critical defects."

단어 수: 62

---

### 풀스크립트

> "Ahead of GT-SS500 production ramp in early 2025, I authored five DFMEAs covering
> the 48V power circuit, LCD state machine, hydraulic pump, CAN bus, and EMI
> grounding. The GT-SS500 is an autonomous agricultural sprayer operating in harsh
> conditions — vibration, humidity, chemicals, temperature extremes — so the
> electrical DFMEA scope was broad and safety-relevant.
>
> My task: apply AIAG-VDA 2019 seven-step methodology, identify all AP=H items, and
> close them before the production gate review.
>
> I worked through all seven steps: structure analysis, function analysis, failure
> analysis, risk rating with Severity-Occurrence-Detection plus Action Priority
> matrix, and optimization. Across five DFMEAs I identified five AP=H items — each
> requiring corrective action regardless of occurrence rate due to high severity or
> low detectability. I owned tracking: assigned owners, set dates, linked each AP=H
> to an NCR, and followed through to verified closure. The MCB item became the RCA
> I described. The state-machine item required eliminating undefined states that
> could cause unintended drive activation. The O-ring required dimensional redesign
> and pressure-cycle re-qualification.
>
> All five AP=H items closed before the gate review. Residual risk at production
> entry: zero high-priority items. First-article batch of 16 units shipped with
> zero safety-critical defects. The DFMEAs are now living documents — updated with
> each NCR close."

총 단어 수: 218

### 후속 질문 3개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "How is AIAG-VDA 2019 different from the old AIAG FMEA?" | 2019: Action Priority (AP) matrix 도입 — RPN 단독 사용 대신 S × D 우선 + O 보조. 7단계 명시. "Failure Chain" 개념으로 Cause → Failure Mode → Effect 분리 강화 |
| 2 | "How do you set Detection rating?" | 현행 설계 관리 방법의 검출 능력 평가. D=1: 거의 확실히 검출. D=10: 검출 방법 없음. IQC 항목이 있으면 D 낮아짐. 시험으로 재현 가능하면 D 낮아짐 |
| 3 | "What happens if AP=H is not resolved at gate?" | Gate 통과 불가 원칙. 설계 동결 전 반드시 해소. 긴급 시: 임시 조치(interim control) 정의 + 해소 일정 확약 + 리스크 수용 승인 (Sign-off) 필요 |

---

## 7.4 STAR #4 — APQP Phase 2~3 + Gate Review + 양산 16pcs Ramp

### Situation (영문)

> "In 2025, GINT was ramping the GT-SS500 autonomous agricultural sprayer
> from engineering validation to production. This was a 48V electric platform
> with a distributed CAN control architecture and a BOM of 132 items. Six
> cross-functional teams — electrical control, mechanical, software, procurement,
> quality, and field service — needed to converge on a production-ready design
> and process simultaneously, and I was the engineer responsible for both the
> technical work and cross-team coordination as Junior PM."

단어 수: 82

### Task

> "Lead APQP Phase 2 (Product Design and Development) and Phase 3 (Process Design
> and Development) through Gate Review to first-article shipment, while tracking
> 27 NCRs, maintaining a 132-item BOM, and ensuring all DFMEA AP=H items closed."

단어 수: 48

### Action

> "In Phase 2, I built and operated four test rigs from scratch — dynamometer,
> fan bench, pump bench, and bumper safety rig — using profiles aligned with
> MIL-STD-810 and IEC 60068-2. I ran design verification tests, documented results,
> and fed findings directly into DFMEA updates and NCR issuance.
> For Phase 3, I defined IQC inspection criteria for drive motors and nozzle assemblies,
> aligned with Six Sigma DMAIC gating logic. I created a production readiness checklist
> of 45 items across BOM, IQC, OQC, tooling, and documentation.
> I ran weekly Gate Review status meetings with representatives from all six teams,
> using an NCR-based health dashboard: any open AP=H item or critical-path NCR
> was escalated immediately. I personally tracked 14 of the 27 NCRs — the electrical
> control items — from issuance to verified closure.
> Three weeks before planned shipment, procurement flagged 23 BOM items with
> insufficient stock. I reprioritized the NCR backlog, accelerated 8 critical-path
> NCRs, and negotiated with procurement on substitution approvals for 5 components."

단어 수: 186

### Result

> "Gate Review passed on schedule. First-article batch of 16 units plus 2 demo
> units and 2 spares shipped on plan. All 27 NCRs closed before ramp.
> Five AP=H DFMEA items resolved with zero residual safety risk at production entry.
> The production readiness checklist and NCR dashboard were retained as templates
> for the next program at GINT."

단어 수: 63

---

### 풀스크립트

> "In 2025 I led APQP Phase 2 and 3 for the GT-SS500, a 48V autonomous agricultural
> sprayer. The platform had a distributed CAN control architecture, a 132-item BOM,
> and six cross-functional teams that all needed to converge on a production-ready
> design simultaneously. I was both the electrical control engineer and the Junior PM
> for this ramp.
>
> My task: take the product from engineering validation through Gate Review to
> first-article shipment, tracking 27 NCRs, managing the DFMEA AP=H closure, and
> maintaining BOM alignment across procurement, quality, and design.
>
> In Phase 2 I built four test rigs from scratch — dynamometer, fan bench, pump
> bench, and bumper rig — all aligned with MIL-STD-810 and IEC 60068-2 profiles.
> Test results fed directly into DFMEA updates and NCR issuance. In Phase 3 I
> defined IQC criteria for key assemblies using Six Sigma gating logic, and built
> a 45-item production readiness checklist. I ran weekly Gate Reviews with health
> dashboards showing NCR status and AP=H closure progress. Three weeks out,
> procurement flagged 23 BOM items with insufficient stock — I reprioritized the
> NCR backlog, accelerated 8 critical-path items, and worked with procurement on
> 5 component substitutions.
>
> Gate Review passed on schedule. Sixteen units shipped on plan. All 27 NCRs
> closed, five AP=H items resolved with zero residual safety risk at production
> entry. The NCR dashboard and readiness checklist are now templates for the
> next program."

총 단어 수: 241

### 후속 질문 3개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "What was the biggest Gate Review blocker?" | BOM 23개 재고 부족 + MCB #204 NCR (전해 부식 미해소 시점). 동시에 터진 두 이슈를 Critical Path 분석으로 우선순위화 |
| 2 | "How did you manage six teams with no formal authority?" | 주간 Gate Review에서 NCR 공개 대시보드 → 투명성으로 압력 대신 책임감 유도. 블로킹 항목은 팀장 에스컬레이션, 기술 항목은 직접 해결 |
| 3 | "What would you do differently in the next APQP?" | Phase 1 (Plan & Define)에서 IQC 기준 초안을 더 일찍 잡을 것. Phase 3에서 Cpk 목표값을 공급사 계약에 명시할 것. NCR 발행 기준을 더 명확히 SOP화할 것 |

---

## 7.5 STAR #5 — Damage Summation (P-04) — 변동환경 PV 폴리머 수명 외삽

### Situation (영문)

> "In 2023 as an undergraduate researcher at Konkuk University, I contributed
> to a project on photovoltaic module lifetime prediction. PV modules installed
> in the field experience continuously varying temperature and humidity — not
> constant stress like a standard ALT assumes. The challenge was to accurately
> predict polymer encapsulant lifetime under this variable real-world stress
> history, which prior single-stress models significantly overestimated."

단어 수: 73

### Task

> "My contribution was to apply a damage summation approach — Miner's Rule —
> to integrate variable stress histories into a unified lifetime prediction,
> and to quantify the improvement in accuracy over existing single-stress
> constant-condition models."

단어 수: 42

### Action

> "I processed long-term temperature and humidity measurement data from field-deployed
> PV sites. The stress history was discretized into bins — each bin representing
> a temperature-humidity combination with a measured duration. For each bin, I
> applied the single-stress model to compute the failure cycle count N_i at that
> specific condition. Then I summed the damage fractions: D = Σ(n_i / N_i),
> where n_i is the actual time spent at condition i and N_i is the life at that
> condition.
> When D reaches 1.0, the polymer is predicted to have reached end-of-life.
> I compared this damage summation prediction against the field-observed degradation
> data and against predictions from a constant worst-case stress assumption.
> The single-stress worst-case model predicted failure far earlier than observed —
> overly conservative. The damage summation model aligned much more closely with
> field data, reducing the prediction error."

단어 수: 153

### Result

> "The damage summation model demonstrated significantly improved accuracy over
> the single worst-case stress assumption. This work was published in Solar Energy,
> Elsevier, Volume 276, Article 112645, 2024. DOI 10.1016/j.solener.2024.112645.
> The approach is directly applicable to any variable-environment reliability
> prediction — including consumer electronics exposed to daily use temperature
> and humidity cycles."

단어 수: 65

---

### 풀스크립트

> "In 2023 as an undergraduate researcher, I contributed to a PV module lifetime
> prediction project. PV encapsulant polymers degrade under temperature and humidity,
> but real field conditions are continuously variable — not the constant stress
> that standard ALT models assume. Single-stress models applied at worst-case
> conditions significantly overestimated degradation rate — too conservative.
>
> My contribution was to apply Miner's Rule damage summation to integrate the
> variable stress history into a unified lifetime prediction.
>
> I processed long-term field measurement data: temperature and humidity time
> series from deployed PV sites. I discretized the history into stress-condition
> bins. For each bin, I computed N_i — the life at that condition from the
> single-stress model — then accumulated the damage fraction n_i over N_i.
> When the sum of all fractions reached 1.0, that was the predicted end-of-life.
> I compared this against field-observed degradation and against the worst-case
> constant-stress prediction. The damage summation model aligned much more closely
> with field reality, substantially reducing prediction error without sacrificing
> conservatism.
>
> This was published in Solar Energy, Elsevier, 2024 — DOI 10.1016/j.solener.2024.112645.
> The method is directly applicable to any product with variable-environment stress
> histories: smartphones cycling through outdoor and indoor temperatures, or camera
> modules exposed to daily humidity variation."

총 단어 수: 214

### 후속 질문 3개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "What is Miner's Rule's main limitation?" | 순서 효과(sequence effect) 무시 — 높은 스트레스 먼저 vs 나중에 따라 실제 수명이 달라지나 Miner's Rule은 순서를 무시. 또한 D=1.0이 항상 고장이 아님 (D=0.7~1.5 범위에서 고장 발생). 비선형 손상 모델(Corten-Dolan)로 보완 가능 |
| 2 | "How do you get N_i for each stress condition?" | 단일 스트레스 ALT 데이터에서 Arrhenius 또는 Eyring 모델로 스트레스-수명 관계 구축 → 각 조건 외삽. PV 폴리머는 온도+습도 복합 모델 사용 |
| 3 | "How would you apply this to an iPhone camera?" | 하루 온도 프로파일 수집 (저장 → 주머니 → 야외 직사광) → 각 구간 Coffin-Manson N_i 계산 → Miner's D 적산 → 3년 후 스프링·FPC 수명 예측. 기존 단일 ΔT 가정보다 정확 |

---

## 7.6 녹음·연습 가이드

### 녹음 체크리스트

| 항목 | 기준 |
|------|------|
| 속도 | 원어민 대화 속도 기준 → 자기 녹음 60~80%로 재생해 어색함 확인 |
| 정량 수치 강조 | "27 NCRs", "16 units", "five AP=H", "Cpk 1.33" — 모두 강세로 |
| "I" 시작 빈도 | 답변 1개에 5회 이하. "We" 필요 시 "I led our team to..." 구조 |
| 길이 | 타이머로 2~3분 체크. 넘으면 Action 파트 단축 |
| 기술 용어 발음 | Coffin-Manson, JESD47, AIAG-VDA, Cpk, FRACAS — 미리 여러 번 발음 연습 |

### 연습 순서 (권장)

```
1회차: Script를 읽으면서 녹음
2회차: 80% 재생 속도로 듣고 어색한 파트 표시
3회차: 정량 수치와 기술 용어 강조 연습
4회차: Script 없이 키워드만 보고 자연스럽게 말하기
5회차: 실제 면접처럼 착석 후 첫 문장부터 끝까지
```

### 핵심 수치 빠른 암기 카드

| STAR | 핵심 수치 |
|------|----------|
| #1 MCB RCA | 48V, 30A, 200 cycles 검증, NCR #204, 16 units 출하 |
| #2 IGBT PCT | ΔTj, Vce-sat 20% 기준, IEEE TIM 2024, bond-wire lift-off |
| #3 DFMEA | AIAG-VDA 2019, 5 DFMEAs, AP=H 5건, 잔여 위험 0 |
| #4 APQP | 132-item BOM, 27 NCRs, 6팀, 16+2+2 units, 45항목 체크리스트 |
| #5 Damage Sum | Miner's Rule, Σ(ni/Ni), Solar Energy 2024, D=1.0 |

---

## 총정리 — Day 4~7 학습 핵심 요약

| Day | 핵심 공식/구조 | 핵심 숫자 | 황인혁 직접 경험 | 황인혁 학습(간접) |
|-----|---------------|-----------|----------------|----------------|
| 4 | FRACAS 5단계 폐루프, AMSAA λ(t)=λβt^(β-1) | α=0.3~0.5 (Duane 좋은 범위), β<1 신뢰도 향상 중 | NCR 27건 (FRACAS 동일 구조), DFMEA AP=H 5건 해소 | Duane/AMSAA 수치 계산 (학습) |
| 5 | Cpk = min[(USL-μ)/3σ, (μ-LSL)/3σ], Bayesian: posterior ∝ likelihood × prior | Cpk 1.33 baseline, 1.67 고신뢰성 | IQC/OQC 기준 정의 (Six Sigma 동일 구조) | Bayesian 적용 경험 없음 — 정직 기재 |
| 6 | B10 = η·(-ln 0.9)^(1/β) VCM 예시, Miner's D 교차 계산 | B10(η=500k, β=2.5)=201k cycles > 164k 기준 | VCM 5 고장 모드 이해, DFMEA 시연 | 광학 세부 (드라이버 회로, MTF) 추가 학습 필요 |
| 7 | STAR S/T/A/R 구조 | MCB 48V/NCR#204, IGBT IEEE TIM 2024, 5 AP=H, 132 BOM/16 units, Solar Energy 2024 | 5종 모두 직접 경험 기반 | — |
