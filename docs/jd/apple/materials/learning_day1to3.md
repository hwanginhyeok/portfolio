# Reliability 학습 코스 — Day 1~3

> 작성: 2026-05-04 | Apple Reliability Engineer 면접 준비
> 목표: ★★★ 우선순위 3종 + 연계 ★★ 항목 집중 학습
> 기준: "이 개념을 영문으로 60초 안에 설명할 수 있는가"
> 참조: reliability_competency.md §5 학습 우선순위

---

# Day 1 — Stress-Strength Interference + Weibull / B10

---

## 1.1 핵심 개념 정의

### Stress-Strength Interference (S-S)

**한 줄 정의**: 부품 강도(Strength)와 가해지는 부하(Stress)가 모두 분포를 가지며,
그 분포가 겹치는 영역(interference)이 바로 고장 확률이다.

**영문 한 줄**:
> "Reliability is the probability that a component's strength exceeds the applied
> stress at every moment of operation — both are distributions, not fixed values."

### 안전계수(Safety Factor) vs 신뢰도 패러다임

| 구분 | 안전계수 (SF) | Stress-Strength 신뢰도 |
|------|-------------|----------------------|
| 접근 | SF = μ_S / μ_L (평균값 비율) | R = P(S > L) = 면적 계산 |
| 정보 | 평균만 사용 | 분포 전체 (μ, σ) 사용 |
| 출력 | 단일 숫자 (예: 1.5) | 고장 확률 (예: 10⁻⁶) |
| 한계 | "SF=1.5이면 안전하다"는 정성적 주장 | 정량적 신뢰도 — 인터뷰 어필 핵심 |

**핵심 주장** (인터뷰 때 쓸 수 있는 한 줄):
> "A safety factor of 1.5 tells you the ratio of means — it does NOT tell you
> the probability of failure. Stress-Strength overlap gives you that number."

---

## 1.2 산식 / 메커니즘

### S-S Interference 수식

설 Strength 분포: f_S(s) (부품 강도 PDF)
설 Stress 분포: g_L(l) (부하 PDF, L for Load)

```
R = P(S > L) = ∫_{-∞}^{∞} f_S(s) · G_L(s) ds

G_L(s) = P(L ≤ s) = ∫_{-∞}^{s} g_L(l) dl   (CDF of Load)

고장 확률 Pf = 1 - R = ∫_{-∞}^{∞} g_L(l) · F_S(l) dl

F_S(l) = P(S ≤ l) = CDF of Strength
```

**직관적 그래프 설명**:

```
확률밀도
   |        f_S(s)           ← 강도 분포 (오른쪽)
   |       /  \
   |      /    \
   |  g_L(l)    \
   |  /  \ ← 이 겹침 영역 = Pf
   | /    \  \
   |/      \  \
   +---------+--------→ s, l
              ↑
          interference 영역
```

- f_S가 왼쪽으로 이동하거나 (강도 감소) g_L이 오른쪽으로 이동하면 (부하 증가) Pf 상승
- 두 분포 사이 간격(reliability index β_HL)을 넓히는 것이 설계 목표

### 정규분포 가정 시 간편 공식

강도 S ~ N(μ_S, σ_S²), 부하 L ~ N(μ_L, σ_L²) 이면:

```
Z = S - L ~ N(μ_S - μ_L, σ_S² + σ_L²)

R = P(Z > 0) = Φ((μ_S - μ_L) / √(σ_S² + σ_L²))

β_HL = (μ_S - μ_L) / √(σ_S² + σ_L²)   ← Hasofer-Lind reliability index
```

예시: μ_S = 100 MPa, σ_S = 10 MPa, μ_L = 70 MPa, σ_L = 8 MPa
```
β_HL = (100 - 70) / √(10² + 8²) = 30 / 12.81 = 2.34
R = Φ(2.34) = 0.9904   → Pf = 0.0096 ≈ 1%
```

### RBDO 연결

**RBDO (Reliability-Based Design Optimization)**:
S-S를 제약조건으로 걸고 설계 변수를 최적화한다.

```
Minimize:    f(x)        ← 목적함수 (무게, 비용 등)
Subject to:  R_i(x) ≥ R_target    ← S-S 신뢰도 제약 (예: R ≥ 0.999)
             g_j(x) ≤ 0           ← 결정론적 제약
```

**결정론적 최적화 vs RBDO**:
- 결정론적: "최소 무게, SF ≥ 1.5" → 분산 무시
- RBDO: "최소 무게, P(고장) ≤ 10⁻³" → 분산 고려 → 더 정확한 신뢰도

---

## 1.3 황인혁 경험과의 연결

### RBDO Lab 석사 (★ 핵심 어필)

건국대 RBDO Lab은 이름 자체에 "Reliability-Based Design Optimization"이 들어간다.
S-S Interference는 RBDO의 핵심 개념이므로 인터뷰에서 100% 질문이 온다.

**연결 방법**: "저의 석사 연구실 자체가 Reliability-Based Design Optimization Lab입니다.
RBDO에서 신뢰도 제약조건이란 곧 S-S Interference의 수식화입니다."

### IPMSM Co-simulation 학위논문 (T-01)

직접 S-S 분석을 수행하지는 않았으나, 개념적으로 연결된다:
- 시뮬레이션 모델(Ansys Maxwell + MATLAB)과 실험 데이터를 비교하는 작업
- → 모델 예측 분포와 실험 측정 분포가 얼마나 겹치는지 = 간접적 S-S 검증
- "Sim2Real 정합성 검증 = 모델 강도 분포가 실험 부하 분포를 커버하는가"로 재해석 가능

**인터뷰 답변 톤**: "could be interpreted as a distribution-matching exercise
similar to S-S analysis" — 직접 수행 주장은 하지 않는다.

### PV 폴리머 수명 예측 (P-04)

- 변동 환경 하 수명 추정 = 확률론적 수명 분포 구축
- 수명 분포가 "요구 수명" 분포와 어떻게 관계 맺는지 → S-S 구조와 동일
- Miner's Rule 자체는 결정론적이지만, 입력 스트레스 이력의 불확실성을 분포로 처리하면 S-S 프레임에 들어맞음

---

## 1.4 인터뷰 60초 답변 스크립트

### Script 1-A: "How do you quantify reliability?"

> "Reliability is the probability that a component's strength exceeds the applied
> stress at all times. Both strength and stress are distributions — not single values.
> The overlap area between those two distributions is the failure probability.
> This Stress-Strength Interference framework is the foundation of
> Reliability-Based Design Optimization, which was the core methodology of
> my master's lab at Konkuk University.
> Where a safety factor of 1.5 only compares mean values,
> S-S interference gives you an actual failure probability — for example,
> a Hasofer-Lind reliability index of 2.34 maps to roughly 1% failure probability.
> That quantitative output is what drives acceptance criteria in ALT."

단어 수: 약 100단어 / 실제 발화 약 55~60초 (원어민 속도 기준)

### Script 1-B: "What is B10 life?"

> "B10 life is the time at which 10% of a population is expected to have failed —
> equivalently, the 10th percentile of the failure time distribution.
> We compute it from Weibull parameters: B10 equals eta times
> the quantity negative natural-log of 0.9, all raised to the power of one over beta.
> For example, with eta of 10,000 hours and beta of 2,
> B10 works out to about 3,247 hours.
> B10 is the standard acceptance criterion in accelerated life testing
> because it captures the early-tail behavior that matters most
> for a product in the field."

단어 수: 약 95단어 / 실제 발화 약 55초

---

## 1.5 예상 Follow-up 질문 5개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "How do you fit Weibull from censored data?" | MLE (Maximum Likelihood Estimation) — 중단 데이터(suspended/censored) 처리 가능. 대안: Median Rank Regression. MLE가 대표본에서 더 정확. |
| 2 | "What does β=2 physically mean?" | 선형 증가 고장률 (h(t) = (β/η)(t/η)^(β-1)). β=2이면 h(t) ∝ t. 피로(fatigue), 마모(wear) 고장 메커니즘과 연결. |
| 3 | "Difference between B10 and MTTF?" | B10 = 10th percentile (10% 고장 시점). MTTF = η·Γ(1+1/β) = 평균 수명. Weibull에서는 B10 ≠ MTTF (지수분포만 β=1일 때 단순 MTTF 기준 가능). 제품 신뢰성에서는 B10이 더 보수적이고 실용적. |
| 4 | "How do you handle confidence intervals on B10?" | Fisher Information Matrix → CI (parametric). 대안: Bootstrap (비모수). 소표본이면 Bayesian prior 활용. 보통 90% single-sided CI 사용. |
| 5 | "When does Weibull NOT fit well?" | Multi-modal failure population (두 개 이상의 고장 메커니즘이 섞임). → Weibull Mixture Model 또는 competing risk 모델 사용. 예: 초기불량 + 마모 동시 존재 → 2-parameter Weibull 1개로 설명 불가. |

---

## 1.6 Weibull 분포 핵심 정리

### 누적분포 함수 (CDF)

```
F(t) = 1 - exp[-(t/η)^β]

F(t): t 시점까지의 고장 확률
η: 척도 모수 (characteristic life) — F(η) = 1 - e^(-1) ≈ 63.2%
β: 형상 모수 (shape parameter) — 고장률 형태 결정
```

### β 해석표 (Bathtub Curve 매핑)

| β 범위 | 고장률 추세 | Bathtub 구간 | 물리적 의미 | 대표 원인 |
|--------|-----------|-------------|-----------|---------|
| β < 1 | 감소 (DFR) | 초기불량 (Infant Mortality) | 초기에 약한 개체가 먼저 고장 | 제조 결함, 재료 불균일 |
| β = 1 | 일정 (CFR) | 우발고장 (Random Failure) | 지수분포와 동일, 기억 없음 | 외부 충격, 무작위 스트레스 |
| β > 1 | 증가 (IFR) | 마모고장 (Wear-out) | 사용할수록 고장 가능성 증가 | 피로, 마모, 산화, 열화 |

### 주요 산식

```
생존함수:   R(t) = exp[-(t/η)^β]

고장률:     h(t) = (β/η)(t/η)^(β-1)

MTTF:       E[T] = η · Γ(1 + 1/β)        [Γ: 감마함수]

B10 산식:   B10 = η · (-ln 0.9)^(1/β)
                = η · (0.10536)^(1/β)
```

### B10 계산 예시

조건: η = 10,000 h, β = 2

```
B10 = 10,000 × (0.10536)^(1/2)
    = 10,000 × 0.3247
    = 3,247 h

검증: F(3247) = 1 - exp(-(3247/10000)²)
             = 1 - exp(-0.1055)
             = 1 - 0.8999 ≈ 10% ✓
```

MTTF (동일 조건):
```
MTTF = 10,000 × Γ(1 + 1/2)
     = 10,000 × Γ(1.5)
     = 10,000 × 0.8862
     = 8,862 h

∴ B10 (3,247 h) ≪ MTTF (8,862 h) — 항상 B10 < MTTF (β>1)
```

### Weibull Plot (직선화)

```
F(t) = 1 - exp[-(t/η)^β]
1 - F(t) = exp[-(t/η)^β]
ln(1-F) = -(t/η)^β
-ln(1-F) = (t/η)^β
ln(-ln(1-F)) = β·ln(t) - β·ln(η)

→ y = ln(-ln(1-F)), x = ln(t) 로 치환하면
  y = β·x - β·ln(η)   ← 직선!

기울기 = β, x절편 = ln(η)
```

**실용**: Weibull 확률지 (Weibull probability paper)에 실험 데이터를 찍으면
직선으로 정렬되는지 확인 가능 → β, η 추정.

---

## 1.7 학습 자료 / 출처

| 자료 | 상세 | 용도 |
|------|------|------|
| ReliaSoft Reliability HotWire | reliawiki.org/index.php/Life_Data_Analysis_Reference | Weibull 산식 + B10 계산 레퍼런스 |
| Kapur & Pecht, *Reliability Engineering* (Wiley) | Ch.3 (Stress-Strength), Ch.5 (Weibull) | 교과서 수준 S-S 유도 |
| Haldar & Mahadevan, *Probability, Reliability and Statistical Methods in Engineering Design* | Ch.6 RBDO 연결 | RBDO Lab 배경과 연결 |
| Nelson, *Accelerated Testing: Statistical Models, Test Plans, and Data Analysis* | Weibull MLE + 신뢰구간 | 실전 ALT 분석 |
| NIST/SEMATECH e-Handbook, §8.1.6 | https://www.itl.nist.gov/div898/handbook/ | 무료, Weibull 플롯 실습 |

---

---

# Day 2 — JESD47 핵심 시험 7종 + Coffin-Manson 외삽

---

## 2.1 핵심 개념 정의

### JESD47 개요

**한 줄 정의**: JEDEC이 제정한 반도체 신뢰성 자격(qualification) 표준 — IC·모듈이
시장 출하 전 통과해야 하는 가속수명시험 항목과 조건을 규정한다.

**영문 한 줄**:
> "JESD47 is the JEDEC standard that defines the minimum reliability qualification
> test suite for integrated circuits — covering stress tests from HTOL to ESD and
> power cycling, each targeting a specific failure mechanism."

### JEP122 연결

JEP122 = JEDEC에서 발행한 "Failure Mechanisms and Models for Semiconductor Devices"
— JESD47의 각 시험이 어떤 고장 메커니즘을 검출하는지 물리적 근거 제공.

황인혁 직접 경험: "Conducted PCT per **JESD47/JEP122** on IGBT modules"
(resume_en.md §EXPERIENCE · P-01 IEEE TIM 2024)

---

## 2.2 JESD47 핵심 시험 7종

| # | 시험 약어 | 정식 명칭 | 대표 조건 | 검출 고장 메커니즘 | Apple 연관성 |
|---|----------|---------|---------|-----------------|------------|
| 1 | **HTOL** | High Temperature Operating Life | 125°C, bias 인가, 1000h | Electromigration, TDDB (gate oxide breakdown), hot carrier injection | IC 칩 장기 신뢰성 |
| 2 | **HTSL** | High Temperature Storage Life | 150°C, no bias, 1000h | 이종 금속 확산(interdiffusion), 산화, 접착제 열화 | 패키지 저장 수명 |
| 3 | **THB** | Temperature Humidity Bias | 85°C / 85%RH, bias 인가, 1000h | 부식(corrosion), 금속 이온 이동(CAF), 절연 열화 | FPC·커넥터·칩 방습 |
| 3' | **HAST** | Highly Accelerated Stress Test | 130°C / 85%RH (가압), bias, ~96h | 동일 (THB 가속 버전) | 단기 자격 시험 |
| 4 | **TC** | Temperature Cycling | −65°C ↔ +150°C, N cycles (보통 1000) | 솔더 fatigue, die-attach 박리, 와이어 루프 균열 | 스마트폰 온도 사이클 |
| 5 | **PCT** | Power Cycling Test | 전력 ON/OFF로 ΔTj 자체 발생, N cycles | Bond-wire lift-off, 솔더 fatigue, die-attach 피로 | 파워 모듈, 배터리 관리 IC |
| 6 | **ESD** | Electrostatic Discharge (HBM / CDM) | HBM: ±2kV / CDM: ±500V | 게이트 산화막 파괴, metal spike, 접합 용융 | 모든 IC — 정전기 내성 |
| 7 | **EM** | Electromigration | 고온 + 고전류 밀도 (가속) | Metal void 형성 → 배선 개방 / 힐록 → 단락 | 고성능 SoC 배선 |

### THB vs HAST 차이

| 항목 | THB | HAST |
|------|-----|------|
| 온도 | 85°C | 130°C (가압 환경) |
| 시간 | ~1000h | ~96h |
| 가속 이유 | 표준 조건 | 압력으로 수증기 침투 가속 |
| 용도 | 정밀 자격 | 빠른 스크리닝 |

→ HAST가 THB보다 "더 가혹한(harsher)" 이유: 고온·고압력이 수분 침투를 10배 이상 가속.

### ESD HBM 2kV 물리적 의미

```
HBM (Human Body Model):
- 인체(100pF 커패시터) + 1.5kΩ 직렬 저항이 방전하는 모델
- 2kV = 인체에 축적된 전압 → 피크 전류 ≈ 2000/1500 ≈ 1.33 A
- 방전 시간: ~100 ns
- 이 피크 전류가 μm 단위 게이트 산화막을 순식간에 파괴

CDM (Charged Device Model):
- IC 자체가 대전 → 핀에 접촉 시 방전
- 전류 피크 더 크고 시간 더 짧음 → 더 위험
```

---

## 2.3 PCT ↔ Coffin-Manson 페어링

### Power Cycling Test (PCT) — 황인혁 직접 경험

**PCT 메커니즘**:
```
전력 ON → 접합부(Junction) 가열 → ΔTj 발생
전력 OFF → 냉각
반복 → 열팽창/수축 반복 → 계면 피로
```

**주요 고장 모드 (P-01 IEEE TIM 2024 기반)**:
- **Bond-wire lift-off**: 알루미늄 본드와이어와 칩 패드 계면 피로 박리 → 가장 지배적
- Die-attach solder fatigue: 칩과 기판 사이 솔더 균열
- (관찰된 다른 고장 메커니즘: P-01 논문에서 확인 — 인터뷰 시 "추가 고장 모드 동시 관찰"로 언급)

**PCT vs TC 차이**:

| 항목 | TC (Temperature Cycling) | PCT (Power Cycling) |
|------|--------------------------|---------------------|
| 열원 | 외부 오븐 | 디바이스 자체 전력 |
| 온도 분포 | 균일 (기판+칩 동시) | 불균일 (칩 내부 먼저 가열) |
| 고장 주도 부위 | 전체 패키지 | 칩-와이어 계면 (본드와이어) |
| 현실 반영 | 저장·수송 환경 | 실제 파워 사이클링 필드 조건 |

### Coffin-Manson 모델

**정의**: 열피로 사이클 수명을 온도 진폭(ΔT)의 함수로 표현하는 경험식

```
Nf = C · (ΔT)^(-n)

Nf: 고장까지의 사이클 수
ΔT: 온도 사이클 진폭 (K 또는 °C)
C:  재료 상수
n:  피로 지수 (재료·메커니즘에 따라 다름)
```

### n 값 대표 예시

| 재료 / 고장모드 | 피로 지수 n | 비고 |
|----------------|-----------|------|
| Sn-Pb 공정 솔더 | 1.9 ~ 2.5 | TC 환경 |
| SAC305 솔더 (무연) | 2.5 ~ 3.5 | TC 환경 |
| Al 본드와이어 | 5 ~ 7 | PCT 환경 — 황인혁 직접 관련 |
| IGBT die-attach | 4 ~ 6 | PCT 환경 |

n이 클수록 ΔT에 민감: ΔT 2배 → 수명 2^n 배 감소.
Al 본드와이어 n=6이면: ΔT 2배 → 수명 64배 감소.

### 외삽 계산 예시

**문제**: 시험 ΔT=100K에서 Nf=10,000 사이클 측정.
필드 조건 ΔT=40K일 때 예상 수명은?

```
Coffin-Manson 외삽:

Nf_field = Nf_test × (ΔT_test / ΔT_field)^n

n = 5 (Al 본드와이어, 보수적 하한):
Nf_field = 10,000 × (100/40)^5
         = 10,000 × 2.5^5
         = 10,000 × 97.66
         ≈ 976,600 사이클

n = 6 (중간값):
Nf_field = 10,000 × 2.5^6
         = 10,000 × 244.1
         ≈ 2,441,000 사이클
```

→ 필드 조건이 시험 조건의 절반 미만 ΔT라면 수명이 수십~수백 배 늘어난다.

**페어링 정리**:
```
PCT → ΔTj 측정 (실험 데이터)
         ↓
Coffin-Manson → 필드 ΔT 조건으로 수명 외삽
         ↓
B10 목표 달성 여부 판정
```

---

## 2.4 황인혁 경험과의 연결

### PCT 직접 수행 (★ 핵심 어필)

- P-01 IEEE TIM 2024 (DOI 10.1109/TIM.2024.3472910)
- IGBT 모듈 PCT 직접 수행 → bond-wire lift-off 확인 + 추가 고장 모드 동시 관찰
- JESD47 Power Cycling 항목 + JEP122 IGBT 고장 메커니즘 가이드라인과 정확히 매핑
- **표준명 인식 없이 수행 → 이제 표준명으로 어필 가능**

### Coffin-Manson 외삽 경험 여부

P-01 논문에서 Coffin-Manson 모델을 명시적으로 사용했는지는 논문 원문 확인 필요.
→ 인터뷰에서는 "PCT 실험 데이터 기반으로 Coffin-Manson 모델을 통한
필드 수명 외삽이 가능하다는 것을 이해하고 있다"로 표현.
직접 계산 수행을 주장하지는 않는다. (정직한 기재 원칙)

### Miner's Rule vs Coffin-Manson 비교

| 항목 | Miner's Rule (P-04 직접 경험) | Coffin-Manson |
|------|------------------------------|--------------|
| 종류 | 누적 손상 합산 | 등온 사이클 수명 경험식 |
| 입력 | 변동 스트레스 이력 + 각 스트레스에서의 파손 기준 | 온도 진폭 ΔT, n값 |
| 출력 | 누적 손상 D (D≥1이면 파손) | 고장까지의 사이클 수 Nf |
| 차이 | 여러 스트레스 레벨 혼합 처리 | 단일 ΔT 기준 수명 예측 |
| 실제 관계 | Coffin-Manson Nf가 Miner's Rule의 Ni 입력으로 사용 가능 | Miner와 함께 사용 가능 |

---

## 2.5 인터뷰 60초 답변 스크립트

### Script 2-A: "Tell me about your semiconductor reliability experience"

> "My most direct semiconductor reliability experience is Power Cycling Testing
> on IGBT modules, which falls under JESD47 and is guided by JEP122 for failure
> mechanisms. I ran PCT on our 400W BLDC motor controller IGBT modules and
> identified bond-wire lift-off as the dominant failure mode — the aluminum
> bond wire fatigues at the chip-pad interface due to repeated thermal expansion
> from power cycling. This work was published in IEEE Transactions on
> Instrumentation and Measurement in 2024. For extrapolating that cycle life
> to field conditions, the standard approach is the Coffin-Manson model:
> field life equals test life times the ratio of test ΔT to field ΔT,
> all raised to the power n — typically 5 to 7 for aluminum bond wires."

단어 수: 약 120단어 / 실제 발화 약 65~70초 (조금 빠르게 하면 60초)

### Script 2-B: "What tests are in JESD47?"

> "JESD47 covers the core semiconductor qualification suite: HTOL at 125°C with
> bias for electromigration and oxide breakdown, HTSL at 150°C no-bias for
> diffusion and oxidation, THB or HAST for corrosion and moisture reliability,
> Temperature Cycling for solder and die-attach fatigue, Power Cycling for
> bond-wire and thermal interface fatigue, ESD in both HBM and CDM modes,
> and Electromigration for metal interconnect reliability.
> Each test targets a specific failure mechanism — that mechanistic linkage is
> why JESD47 pairs with JEP122."

단어 수: 약 90단어 / 실제 발화 약 50초

---

## 2.6 예상 Follow-up 질문 5개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "What's the typical n value for solder vs bond-wire?" | 솔더(Sn-Pb/SAC): n ≈ 2~3.5. Al 본드와이어: n ≈ 5~7. n이 클수록 ΔT 민감도 높음. |
| 2 | "How do you separate bond-wire fatigue from die-attach degradation in PCT?" | 전기적 모니터링: Vce(sat) 증가 → bond-wire 저항 증가. 열저항(Rth) 증가 → die-attach 열화. 두 신호의 독립 모니터링으로 분리. P-01에서 이 다중 신호 분석 수행. |
| 3 | "Why is HAST harsher than THB?" | 130°C + 가압(1기압 이상) → 수증기 분압 증가 → 흡습 속도 ↑. 동일 ΔRH에서 온도 10°C 상승 = 가속 인자 2배 (Arrhenius). 96시간 HAST ≈ 1000시간 THB (근사). |
| 4 | "What does ESD HBM 2kV mean physically?" | 인체(100pF) + 1.5kΩ → 2kV → 피크 전류 1.33A, 100ns 방전. μm 단위 게이트 산화막이 이 순간 파괴됨. |
| 5 | "When do you stop a TC test?" | 목표 사이클 도달 (예: 1000 cycles) + 중간 전기 특성 검사 주기 (예: 100 cycles마다). 또는 고장 기준(합격선) 위반 시 즉시 중단. |

---

## 2.7 학습 자료 / 출처

| 자료 | 상세 | 용도 |
|------|------|------|
| JESD47 원문 | jedec.org (무료 다운로드) | 시험 조건 공식 확인 |
| JEP122 원문 | jedec.org | 고장 메커니즘 물리 근거 |
| Ciappa, "Selected failure mechanisms of modern power modules" | Microelectronics Reliability, 2002 | bond-wire + solder fatigue 메커니즘 |
| Coffin (1954) + Manson (1953) 원논문 | 피로 사이클 수명 모델 기원 | 역사적 맥락 |
| IPC-9701 | Solder Joint Reliability Test 표준 | TC 솔더 피로 — 보완 표준 |

---

---

# Day 3 — 환경시험 표준 매핑 (MIL-STD-810 / IEC 60068-2 / IEC 60529)

---

## 3.1 핵심 개념 정의

### 세 표준의 위상

**한 줄 정의**:
- MIL-STD-810: 미 국방부 환경공학 + 시험 표준 (시스템 레벨, 군용)
- IEC 60068-2: 전기·전자 부품의 환경 내성 기본 시험 절차 (국제, 산업·소비재)
- IEC 60529: 외함(enclosure)의 방진·방수 등급 (IP 등급) 표준 (국제, 전 산업)

**영문 한 줄**:
> "MIL-STD-810 sets system-level environmental test methods for military applications;
> IEC 60068-2 is the international equivalent for component and product-level
> environmental testing; IEC 60529 defines the IP rating system for dust and
> water ingress protection."

---

## 3.2 MIL-STD-810 — 핵심 Method 매핑

| Method | 제목 | 주요 시험 조건 | 검출 내용 |
|--------|------|--------------|---------|
| **510** | High Temperature | +71°C (최대 시나리오에 따라 상이) | 열화, 크리프, 절연 열화 |
| **511** | Low Temperature | −51°C (지상 기본) | 기계적 취성, 윤활 실패, 재료 경화 |
| **514** | Vibration | 협대역 정현파 or 광대역 랜덤 PSD | 공진 주파수 → 피로 파손, 접합부 불량 |
| **516** | Shock | 반정현파(half-sine) 충격 | 구조 파괴, 납땜 크랙, 커넥터 분리 |
| **516.7** | Drop Test | 1.2m ~ 규정 높이, 6면 or 8면 | 낙하 충격 시뮬레이션 |
| **518** | Acoustic Noise | 음압 레벨 dB, 협대역 or 광대역 | 항공/군용 음향 피로 |
| **520** | Temperature, Humidity, Vibration, and Altitude | 복합 시험 | 실제 운용 복합 환경 |

**주의**: MIL-STD-810은 소비재(consumer electronics)에서는 직접 인용보다
"equivalent to MIL-STD-810 method" 표현이 현실적. Apple은 자사 시험 스펙으로 재정의하지만 방법론은 동일.

---

## 3.3 IEC 60068-2 — MIL-STD-810 매핑 + 핵심 Part

| IEC 60068-2 Part | 제목 | 동일 MIL 카테고리 | 주요 조건 예시 |
|-----------------|------|-----------------|--------------|
| **-1** | Cold (저온) | MIL 511 | −40°C, 2h 노출 |
| **-2** | Dry Heat (건열 고온) | MIL 510 | +70°C, 16h |
| **-6** | Sinusoidal Vibration | MIL 514 (정현파) | 10~2000 Hz, 로그 스윕, 1oct/min |
| **-14** | Thermal Shock | MIL 503 | −40°C ↔ +85°C, 급격 전환 |
| **-27** | Shock | MIL 516 | 11 ms, 반정현파, 50 gn 예시 |
| **-29** | Cyclic Damp Heat | — | 55°C ↔ 25°C, 85%RH 사이클 |
| **-30** | Damp Heat Cyclic | — | 55°C, 85%RH — THB 유사 |

### 정현파 vs 랜덤 진동 선택 기준

| 구분 | 정현파 (Sinusoidal) | 랜덤 (Random PSD) |
|------|--------------------|--------------------|
| 용도 | 공진 주파수 탐색, 구조 취약부 탐지 | 실제 운용 환경 모사 (차량·항공) |
| 조건 표현 | 주파수 + 가속도 진폭 | 파워 스펙트럼 밀도 (g²/Hz) |
| Apple 사용 | DVT 초기 공진 스캔 | 최종 내구성 검증 |

---

## 3.4 IEC 60529 — IP 등급 체계

### IP 등급 구조

```
IP  [X1]  [Y2]  [추가문자]

X1 = 방진 등급 (0~6)
Y2 = 방수 등급 (0~9K)
추가문자 = 특수 (예: 고전압 등)
```

### 방진 등급 (X1)

| 등급 | 의미 |
|------|------|
| 0 | 보호 없음 |
| 1 | 50mm 이상 고체 차단 |
| 4 | 1mm 이상 와이어 차단 |
| 5 | 방진 — 완전 차단은 아니나 먼지 침입 최소화 |
| 6 | **완전 방진** — 먼지 침입 없음 |

### 방수 등급 (Y2)

| 등급 | 의미 | 조건 |
|------|------|------|
| 0 | 보호 없음 | — |
| 4 | 사방 물 분사 방호 | — |
| 5 | 직접 분사 방호 | — |
| 6 | 강한 물 분사 방호 | — |
| **7** | **1m 침수, 30분 방호** | 1m 수심, 30분 |
| **8** | **제조사 지정 조건 침수 방호** | 예: iPhone 6m, 30분 |
| **9K** | 고온 고압 분사 방호 | 자동차·산업용 |

### Apple 제품 IP 등급 예시

| 제품 | IP 등급 | 실제 조건 |
|------|---------|---------|
| iPhone 16 series | **IP68** | 6m, 30분 (제조사 정의) |
| Apple Watch Series 9 | **IP6X** + WR50 | 완전 방진 + 50m 수심 방수 |
| AirPods Pro 2 | **IPX4** | 방진 없음, 4방향 물 분사 방호 |

---

## 3.5 황인혁 경험과의 연결

### 표준 매핑 전체 표

| 황인혁 경험 | 표준 매핑 | Method / Part | 비고 |
|-----------|---------|---------------|------|
| GT-SS500 동력계(다이나모) + 진동 시험 | MIL-STD-810 Method 514 / IEC 60068-2-6 | 진동 내성 | 직접 시험대 구축 |
| GT-SS500 범퍼 충격 시험 (정지거리 0.082m, 피크 308A) | MIL-STD-810 Method 516 / IEC 60068-2-27 | 충격 내성 | 충격 시험 리그 직접 설계 |
| EOP CAN 커넥터 방수 설계 | IEC 60529 IP67 | 방진6 + 1m/30min 방수 | 설계 요건 + 검증 직접 수행 |
| 극저온 기동 시험 −40°C | MIL-STD-810 Method 511 / IEC 60068-2-1 | 저온 환경 | EOP 400W 기동 실험 |
| 팬 벤치 + 펌프 벤치 | IEC 60068-2-6 (진동) / MIL 514 유사 | 부품 레벨 환경 내성 | 직접 구축 |

**핵심 메시지**: "표준명을 몰랐을 뿐, 실제 시험 절차와 합격 기준은 동일 카테고리에 해당한다."

---

## 3.6 인터뷰 60초 답변 스크립트

### Script 3-A: "How do you select test standards for a new product?"

> "Standard selection depends on three things: the product's market (consumer vs
> automotive vs military), the applicable regulatory requirements, and the specific
> failure modes we're trying to screen.
> For consumer electronics like Apple's products, IEC 60068-2 is the primary
> reference for environmental testing — vibration, shock, thermal cycling, humidity.
> MIL-STD-810 covers the same categories but targets system-level military
> applications, so the profiles are harsher.
> For water and dust protection, IEC 60529 defines the IP rating.
> At GINT, I built four test rigs covering vibration, shock, thermal, and torque —
> the profiles were equivalent to MIL-STD-810 Method 514 and 516,
> and our EOP sealed connectors were designed to IP67 per IEC 60529."

단어 수: 약 120단어 / 발화 약 65~70초

### Script 3-B: "What is IP68 and how is it tested?"

> "IP68 is an IEC 60529 rating meaning the device is fully dust-tight — IP6X —
> and water-protected under manufacturer-specified conditions beyond 1 meter depth.
> For iPhone, Apple specifies 6 meters for 30 minutes.
> Testing involves submerging the device at the specified depth and verifying
> no water ingress after the full duration — typically checking electrical
> function, display, and ports post-immersion.
> The design implication is that every cable entry, button gap, and speaker mesh
> must be sealed to that level — which I applied to CAN connector design
> for our EOP 400W program, targeting IP67."

단어 수: 약 105단어 / 발화 약 60초

---

## 3.7 예상 Follow-up 질문 5개 + 답변 키워드

| # | 질문 | 답변 키워드 |
|---|------|-----------|
| 1 | "Difference between IP67 and IP68?" | IP67 = 1m / 30min (고정). IP68 = 제조사 정의 (더 가혹, 예: 6m/30min). 두 등급 모두 방진 6(완전 방진). IP68이 IP67보다 높은 등급 — 그러나 IP68을 받았더라도 IP67도 충족해야 함 (표준상 IP68 ⊃ IP67). |
| 2 | "Why IEC not MIL-STD for consumer products?" | MIL-STD-810 = 군용 시스템 레벨, 가혹 조건, 미국 방산. IEC = 국제 표준, 민간·산업 전반 인용. Apple은 글로벌 제품이므로 국제 표준 IEC 우선. 또한 IEC 컴포넌트 레벨 시험에 더 적합. |
| 3 | "How long is a typical IEC 60068-2-6 vibration profile?" | 최소 10분/축 × 3축 = 30분 (단순 스위프). 내구성 시험은 수 시간~수십 시간. 주파수 범위: 10~2000 Hz. 실제 제품 스펙에 따라 Apple 내부 기준으로 연장 가능. |
| 4 | "How do you select between random and sinusoidal vibration?" | 정현파: 공진 탐색, 특정 주파수 취약점 검출. 랜덤: 실제 운용 환경(도로, 진동기계) 모사, 광대역 스트레스. 일반적: 먼저 정현파 스윕으로 공진 확인 → 랜덤으로 내구성 검증. |
| 5 | "Difference between thermal cycling and thermal shock?" | Thermal Cycling (IEC 60068-2-14 Na): 완만한 온도 전환 (자연 대류). 솔더 피로, 재료 팽창 반복 검출. Thermal Shock (IEC 60068-2-14 Nb): 급격한 전환 (액체조 or 고속 공기). 계면 응력 + 취성 파괴 검출. Shock이 더 가혹, Cycling이 더 현실적. |

---

## 3.8 학습 자료 / 출처

| 자료 | 상세 | 용도 |
|------|------|------|
| MIL-STD-810H (2019) | everyspec.com 무료 | Method별 조건 상세 |
| IEC 60068-2 Part 별 원문 | iec.ch (유료, 요약은 무료) | 국제 표준 조건 |
| IEC 60529 원문 | iec.ch | IP 등급 표 + 시험 방법 |
| Apple Device Specifications | apple.com | 실제 IP 등급 + 스펙 참조 |
| Steinberg, *Vibration Analysis for Electronic Equipment* | 전자기기 진동 해석 교과서 | PSD, 공진 개념 |

---

## 총정리 — Day 1~3 학습 핵심 요약

| Day | 핵심 공식 | 핵심 숫자 | 황인혁 직접 경험 | 황인혁 간접/이해 |
|-----|---------|---------|--------------|--------------|
| 1 | R = Φ(β_HL), B10 = η·(-ln0.9)^(1/β) | β_HL=2.34→R=99%, B10(η=10k, β=2)=3247h | RBDO Lab 석사, PV 폴리머 수명 추정 | S-S 공식 학습 |
| 2 | Nf = C·(ΔT)^(-n) | n(Al bond wire)=5~7, 예시 Nf_field≈976k | PCT IGBT (IEEE TIM 2024) | Coffin-Manson 외삽 계산 이해 |
| 3 | IP XX (방진·방수), MIL↔IEC 매핑 | IP67=1m/30min, IP68=6m/30min(Apple) | 진동/충격 시험대 구축, EOP IP67 커넥터 설계 | 표준명 매핑 |
