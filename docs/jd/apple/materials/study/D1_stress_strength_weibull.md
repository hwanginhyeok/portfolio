# Day 1 — Stress-Strength Interference + Weibull / B10 (학습 가이드)

> 작성: 2026-05-05 | Apple Reliability Engineer 면접 준비 자가학습
> 같이 figure 보면서 공부하기 위한 압축본 + 외부 이미지/그림 URL 모음
> 베이스: `learning_day1to3.md` §1, `reliability_competency.md` Block 2~3

---

## 🎯 학습 목표

이 D1을 끝내면 영어로 60초 안에 다음 3가지를 설명할 수 있다.

1. **Stress-Strength Interference** — "왜 Safety Factor만으론 부족하고 분포가 필요한가"
2. **Weibull β/η/MTTF/B10** — "β=0.7, β=1, β=2.5가 각각 어떤 고장 모드인가"
3. **RBDO 연결고리** — "내가 RBDO Lab 출신이라는 게 이 개념과 어떻게 연결되는가"

> 인터뷰 시 RBDO Lab 출신이면 100% 들어오는 질문군이다.

---

## 1. Stress-Strength Interference (S-S)

### 1.1 한 줄 정의

부품 강도 S와 가해지는 부하 L이 **모두 분포**를 가지며, 두 분포가 겹치는 영역(interference)이 **고장 확률 Pf**가 된다.

> "Reliability is the probability that a component's strength exceeds the applied stress at every moment of operation — both are distributions, not fixed values."

### 1.2 Safety Factor vs S-S

| 구분 | Safety Factor | Stress-Strength |
|------|--------------|----------------|
| 식 | SF = μ_S / μ_L | R = P(S > L) |
| 정보 | 평균만 | 분포 전체 (μ, σ) |
| 출력 | 단일 숫자 (1.5) | 확률 (10⁻⁶) |
| 약점 | 산포 무시 → 같은 SF여도 σ 크면 위험 | 정량적 신뢰도 |

**60초 답변 핵심 문장**:
> "A safety factor of 1.5 tells you the ratio of means — it does NOT tell you the probability of failure. Stress-Strength overlap gives you that number, and that's the foundation of RBDO."

### 1.3 산식

```
R = P(S > L) = ∫ f_S(s) · G_L(s) ds
Pf = 1 - R   (overlap 면적)
```

- f_S: Strength PDF, G_L: Load CDF
- 두 분포 간격 넓힐수록 R↑ → reliability index β_HL 사용

### 1.4 RBDO 연결

RBDO(Reliability-Based Design Optimization)의 출발점이 바로 S-S 모델.
- 결정론적 최적화: g(x) ≤ 0 (제약식)
- RBDO: P[g(x) > 0] ≤ Pf_target (확률 제약)

→ "내 학위 연구 자체가 이 방법론을 IPMSM 고장 진단에 적용한 것이다"로 자연스럽게 연결.

### 🖼️ 참고 figure URL

- **S-S Interference 기본 그래프 (두 분포 overlap)**:
  https://reliawiki.org/index.php/Stress-Strength_Analysis
  → ReliaWiki 페이지 상단의 PDF overlap figure가 표준 교재 그림. 이 figure 하나로 60초 설명 가능.

- **Stress-Strength PDF + Reliability 시각화 (Weibull++)**:
  https://help.reliasoft.com/reference/life_data_analysis/lda/stress_strength_analysis.html
  → ReliaSoft 공식 매뉴얼. Pf 면적이 색칠된 그림.

- **RBDO 개념도 (deterministic vs probabilistic 최적화)**:
  https://en.wikipedia.org/wiki/Reliability-based_design_optimization
  → Wiki에 deterministic vs probabilistic feasible region 비교 figure.

- **신뢰성 지수 β_HL (Hasofer-Lind) 시각화**:
  https://www.sciencedirect.com/topics/engineering/reliability-index
  → ScienceDirect Topic 페이지. β = 원점에서 한계상태면(LSF)까지 최단거리로 설명한 그림.

---

## 2. Weibull 분포

### 2.1 PDF / CDF

```
f(t) = (β/η) · (t/η)^(β-1) · exp[-(t/η)^β]
F(t) = 1 - exp[-(t/η)^β]
R(t) = exp[-(t/η)^β]
```

- **β (shape)**: 고장 모드 결정
- **η (scale)**: 63.2% 고장 시간 (특성 수명)

### 2.2 β 해석 — Bathtub과 1:1 매칭

| β | 의미 | Bathtub 구간 | 대응 전략 |
|---|------|-------------|----------|
| β < 1 | 초기 불량 (h(t)↓) | Infant mortality | Burn-in으로 제거 |
| β = 1 | 우발 고장 (h(t)=const) | Useful life | 지수분포와 동일 |
| β > 1 | 마모 고장 (h(t)↑) | Wear-out | Preventive maintenance |
| β ≈ 3.5 | 정규분포 근사 | — | — |

> 핵심 답변: "β tells me **what** is failing, η tells me **when**. β<1 means screening problem, β>1 means design or material wear."

### 2.3 MTTF / B10 산식

```
MTTF = η · Γ(1 + 1/β)
B10  = η · (-ln 0.9)^(1/β)   ≈ η · (0.1054)^(1/β)
```

- B10: 누적 10% 고장 시간 (베어링·전동기 산업 표준)
- B1: 1% 기준 (항공·의료)

### 2.4 Weibull plot (확률지)

세로축에 ln[ln(1/(1-F))], 가로축에 ln(t)를 그리면 직선이 됨.
- 직선 기울기 = β
- F=63.2% 지점의 가로축 값 = ln(η)

### 🖼️ 참고 figure URL

- **Weibull PDF — β별 형상 변화 (β=0.5/1/2/3.5)**:
  https://en.wikipedia.org/wiki/Weibull_distribution
  → Wiki 우상단의 컬러 PDF/CDF 비교 figure. **이게 표준 그림**. 시험 문제용.

- **Bathtub Curve + Weibull β 매핑**:
  https://www.weibull.com/hotwire/issue14/relbasics14.htm
  → Weibull.com 공식 페이지. β<1/β=1/β>1 영역이 bathtub와 1:1 매칭된 그림.

- **Weibull Probability Plot (확률지)**:
  https://reliawiki.org/index.php/The_Weibull_Distribution
  → ReliaWiki "Weibull Probability Plotting" 섹션. 직선 fitting 예시.

- **β/η 변화에 따른 hazard function h(t) 비교**:
  https://help.reliasoft.com/reference/life_data_analysis/lda/the_weibull_distribution.html
  → ReliaSoft 매뉴얼. h(t) curve가 β별로 그려진 figure.

- **B10 / B1 / Bx life 정의 시각화**:
  https://www.weibull.com/hotwire/issue9/relbasics9.htm
  → CDF 곡선에서 B10 위치를 표시한 그림. 베어링 산업 예시.

---

## 3. 황인혁 경험 ↔ 개념 연결

| 개념 | 내 경험 | 인터뷰 한 줄 |
|------|--------|------------|
| S-S Interference | RBDO Lab 석사 2년 (학위논문 IPMSM Co-simulation) | "Stress-Strength was the foundational concept of my graduate lab — RBDO is just the optimization layer on top of it." |
| Weibull β 해석 | PCT IGBT bond-wire lift-off (P-01 IEEE TIM 2024) | "Bond-wire lift-off in IGBT shows β > 1 — clearly a wear-out mechanism, which is why thermal cycling accelerates it." |
| B10 / MTTF | (학습 후 IPMSM ALT 데이터로 재계산해서 들고 가면 강력) | "I'd report B10 alongside MTTF because for safety-critical components, the early-failure tail matters more than the mean." |

---

## 4. 인터뷰 60초 답변 (영문 — 외워야 함)

> Q: "How would you set a reliability target for a new actuator?"

> A: "I'd start by treating both load and strength as distributions, not single numbers — that's stress-strength interference. The overlap area is the failure probability, and reducing it is the design goal. For lifetime, I'd fit a Weibull to ALT data and report B10 instead of mean — for safety-critical parts, the early failure tail matters more than the average. The shape parameter β also tells me whether I'm dealing with infant mortality, random failures, or wear-out, which determines whether I need burn-in, redundancy, or design margin."

— 약 55초. RBDO 언급 1회, B10/Weibull 언급 1회씩, 실무 결정(burn-in/redundancy) 언급으로 마무리.

---

## 5. 예상 Follow-up 5개

1. **"What's the difference between Pf and 1/MTTF?"**
   → Pf는 누적 확률 (시간 종속), 1/MTTF는 평균 고장률. β=1일 때만 동치.

2. **"Why B10 not B50?"**
   → 산업 표준 (베어링/모터). Safety-critical은 B1이나 B0.1 사용.

3. **"How do you estimate β with censored data?"**
   → MLE (Maximum Likelihood Estimation). Median Rank Regression은 small sample.

4. **"What if your data shows β changing over time?"**
   → Mixture Weibull (2~3 subpopulations) 또는 segmented analysis. Bathtub의 두 구간 동시 fitting.

5. **"How does this relate to RBDO?"**
   → RBDO는 S-S overlap을 Pf 제약식으로 넣고 비용/성능을 최적화. 결정론적 최적화의 확률 일반화.

---

## 6. 학습 체크리스트

- [ ] Wikipedia Weibull PDF figure 보면서 β=0.5/1/2/3.5 PDF 모양 머리에 새기기
- [ ] Weibull.com bathtub 그림 보면서 β와 구간 매칭 외우기
- [ ] ReliaWiki S-S Interference 그림 보면서 overlap = Pf 직관 잡기
- [ ] MTTF / B10 산식 종이에 손으로 도출 (Γ 함수 + ln 변환)
- [ ] 60초 답변 영어로 녹음 → 들어보기
- [ ] (옵션) IPMSM ALT 또는 PCT 데이터로 β/η 추정 손계산 1회

---

## 7. 다음 학습 (D2 예고)

**JESD47 7종 시험 + Coffin-Manson ↔ PCT 페어링**
- HTOL / THB / TC / Power Cycling / ESD HBM·CDM / EM
- PCT(시험 프로토콜) ≠ Coffin-Manson(외삽 모델) — 혼용 금지
- 사용자 PCT 직접 경험 → JESD47 매핑 즉시 강점화
