# Day 5 — Bayesian Reliability + Six Sigma Cpk/Ppk (학습 가이드)

> 작성: 2026-05-05 | Apple Reliability Engineer 면접 준비 자가학습
> 베이스: `learning_day4to7.md` §5
> **자가학습 SSOT**: 본 문서는 학습용 자가 정리 자료다. 외부 제출 자료에 직접 인용 금지.

---

## 🎯 학습 목표

이 D5를 끝내면 영어로 60초 안에 다음 3가지를 설명할 수 있다.

1. **Bayesian Reliability** — Prior + Likelihood → Posterior 흐름과 소표본 강점
2. **Cpk / Ppk 산식** — 단기(within) vs 장기(overall) σ 구분
3. **Cpk = 2.0 = 6σ = 3.4 ppm** — 즉답 (장기 1.5σ 드리프트 가정)

---

## 1. Bayesian Reliability

### 1.1 한 줄 정의

> "Bayesian reliability combines a prior distribution — from historical ALT data
> or expert judgment — with observed test data via Bayes' theorem to produce a
> posterior that is narrower than frequentist MLE alone, especially when
> sample sizes are small."

### 1.2 핵심 수식

```
Bayes' Theorem:
    P(θ | data) ∝ P(data | θ) × P(θ)

    posterior ∝ likelihood × prior

    θ : 신뢰성 파라미터 (예: Weibull β, η)
```

### 1.3 Frequentist vs Bayesian

| 항목 | Frequentist (MLE) | Bayesian |
|------|------------------|---------|
| 추정 기반 | 데이터만 | prior + 데이터 |
| 소표본 시 | 신뢰구간 폭 큼 | prior로 좁힐 수 있음 |
| 결과 | 점추정 + 신뢰구간 | 사후 분포 전체 |
| 해석 | "이 데이터가 나올 확률" | "파라미터의 확률" |
| 계산 도구 | Excel, Minitab | MCMC (Stan, PyMC3) |

**Jeffreys Prior** (비정보적 사전분포):
- 데이터 변환에 불변(parameterization-invariant)
- Weibull η에 대한 Jeffreys prior: π(η) ∝ 1/η (log-uniform)
- 사전 정보가 없을 때 기본 선택

**언제 쓰나**: 반도체 ALT (표본 수십 개 이하), 우주·항공 고신뢰성 부품, Apple Camera 고가 부품 소수 시험.

### 1.4 B10 Bayesian 추정 흐름

```
1. Prior 정의: β, η에 대한 사전 분포 (과거 ALT 데이터 또는 Jeffreys)
2. Likelihood: 현재 시험 데이터 (고장 시간 + 중단 데이터)
3. Posterior: MCMC 또는 conjugate 해석해
4. B10 사후 분포: 10th percentile of posterior predictive distribution
5. 90% 신뢰구간 도출 → 합격 기준 비교
```

### 🖼️ 참고 figure URL

- **Bayesian Inference 개요 (Wikipedia)**:
  https://en.wikipedia.org/wiki/Bayesian_inference
  → Prior/Likelihood/Posterior 다이어그램. "Bayesian updating" 섹션 figure.

- **Beta 분포 (Bayesian Binomial 시험에 사용) (Wikipedia)**:
  https://en.wikipedia.org/wiki/Beta_distribution
  → 다양한 α,β 조합 PDF figure. 신뢰도 시험 합격/불합격 모델에 사용.

- **Bayesian Reliability (ReliaWiki)**:
  검색어: site:reliawiki.org "Bayesian"
  → ReliaWiki Bayesian Reliability 페이지. Prior + Posterior 변화 figure.

---

## 2. Six Sigma — Cpk / Ppk

### 2.1 한 줄 정의

> "Cpk is the process capability index that accounts for both spread and centering
> — it equals the minimum of (USL minus mean) over three sigma and (mean minus LSL)
> over three sigma. Cpk of 1.33 is the standard production baseline, corresponding
> to four sigma clearance from mean to the nearer spec limit."

### 2.2 산식 (★★★ 암기)

```
Cp  = (USL - LSL) / 6σ_within
Cpk = min[ (USL - μ)/3σ_within,  (μ - LSL)/3σ_within ]

Pp  = (USL - LSL) / 6σ_overall
Ppk = min[ (USL - μ)/3σ_overall,  (μ - LSL)/3σ_overall ]

σ_within  = 단기 σ (서브그룹 내 변동)
σ_overall = 장기 σ (모든 변동 포함: 드리프트·배치 간 변동)
```

### 2.3 Cpk vs Ppk 차이

| 항목 | Cpk | Ppk |
|------|-----|-----|
| σ 사용 | σ_within (단기) | σ_overall (장기) |
| 반영 변동 | 기계 자체 정밀도 | 드리프트·시프트·배치 간 변동 포함 |
| 목적 | 공정 자체 능력 | 실제 공정 성과 |
| 관계 | Cpk > Ppk → 공정 드리프트 존재 | Cpk ≈ Ppk → 공정 안정 |

**Cpk는 높은데 Ppk가 낮으면**: 공정 평균이 시간에 따라 이동(drift)하고 있다는 신호.

### 2.4 Cpk 기준표 (★★★ 암기)

| Cpk | 시그마 수준 | DPMO (단기) | 의미 |
|-----|-----------|-----------|------|
| 1.00 | 3σ | 2,700 | 최소 수준 |
| **1.33** | **4σ** | **63** | **양산 기본 기준** |
| **1.67** | **5σ** | **0.57** | **고신뢰성 부품** |
| **2.00** | **6σ** | **0.002** | **인체 이식형·항공·Apple tier** |

**Six Sigma 3.4 ppm 설명**:
```
단기 ±6σ 폭: DPMO = 0.002
장기 1.5σ 드리프트 가정: DPMO = 3.4
→ "6 Sigma = 3.4 DPMO"는 장기 성과 기준
```

### 2.5 Cpk 예제 계산

```
USL=105, LSL=95, μ=102, σ_within=1

Cp  = (105-95) / (6×1) = 1.67   ← 폭은 충분
Cpk = min[(105-102)/3, (102-95)/3]
    = min[1.00, 2.33]
    = 1.00                        ← 중심 치우침으로 Upper 여유 좁음

공정 μ=100으로 이동 시: Cpk = 1.67 ✓
```

### 🖼️ 참고 figure URL

- **공정 능력 지수 (Cpk) — Wikipedia**:
  https://en.wikipedia.org/wiki/Process_capability_index
  → Cp/Cpk 정의 + 시각적 설명 figure. Cp high/Cpk low 케이스 그림 포함.

- **Six Sigma 개요 (Wikipedia)**:
  https://en.wikipedia.org/wiki/Six_Sigma
  → DPMO 표 + DMAIC 다이어그램. Cpk=2.0 해석 근거.

- **Normal Distribution 시그마 영역 (Wikipedia)**:
  https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule
  → 68-95-99.7 rule figure. ±3σ, ±6σ 영역 직관적 이해.

---

## 3. DMAIC 5단계

```
D — Define   : 문제 정의. CTQ 식별. Project Charter
M — Measure  : 현재 공정 측정. Cpk 기준선. Gauge R&R
A — Analyze  : 근본원인 분석. Regression / DOE / Fishbone
I — Improve  : 최적 공정 조건 도출. Pilot run
C — Control  : 관리도(SPC) 설정. 표준화. 인수인계
```

---

## 4. 황인혁 경험 ↔ 개념 연결

| 개념 | 내 경험 | 인터뷰 한 줄 |
|------|--------|------------|
| Bayesian Reliability | 직접 사용 경험 없음 (정직 기재) — RBDO 개념과 연결 가능 | "I haven't applied Bayesian reliability in production, but it's a natural extension of RBDO — using prior strength distributions that you update as test data comes in." |
| Cpk / IQC 기준 | GT-SS500 IQC/OQC 검사 기준 정의 — Six Sigma 구조와 동일 | "The gating logic I designed for GT-SS500 IQC was consistent with Cpk-based acceptance, though the full Six Sigma dashboard wasn't always the daily artifact." |
| DMAIC | GT-SS500 GND 노이즈 RCA: D(노이즈 유발)→M(파형 기록)→A(DFMEA+5Why)→I(쉴딩)→C(IQC 추가) | "Retrospectively, the GND noise NCR I resolved followed the DMAIC structure without explicitly calling it that." |

---

## 5. 인터뷰 60초 답변 (영문 — 외워야 함)

> Q: "How do you handle small-sample reliability testing?"

> A: "When sample sizes are small — say fewer than twenty units in an ALT —
> frequentist MLE gives wide confidence intervals on B10, sometimes too wide to
> drive a decision. Bayesian reliability addresses this by incorporating a prior:
> historical data from a predecessor component, or a Jeffreys non-informative
> prior if nothing better is available. The posterior is narrower than MLE alone,
> and you extract a credible interval on B10 directly. I haven't applied this
> in production yet, but it's a natural extension of the RBDO framework from my
> graduate lab — where we used prior strength distributions before test data arrived.
> On the production side, Cpk quantifies whether the process is centered and capable.
> Cpk of 1.33 is the baseline: four sigma clearance. Ppk adds long-term drift.
> If Cpk exceeds Ppk, your process is drifting — which tells you where to focus
> the process control effort."

— 약 65초. Bayesian → RBDO 연결, Cpk/Ppk 구분, 정직성 유지.

---

## 6. 예상 Follow-up 5개

1. **"Cpk vs Ppk — when does the gap matter?"**
   → Cpk > Ppk → 드리프트 존재. 설비 교체·배치 간 원자재 변동 의심. Cpk ≈ Ppk → 공정 안정.

2. **"Why 1.33 and not 1.0?"**
   → Cpk 1.0 = 3σ = 2700 DPMO. 공정 변동·드리프트 여유 없음. 1.33 = 4σ = 63 DPMO. 1.5σ 장기 드리프트 허용 후 여전히 안전.

3. **"What prior would you use for a brand-new component?"**
   → 비정보 Jeffreys prior 또는 유사 기술 계열 (전 세대 IGBT) 데이터 기반 weakly informative prior.

4. **"Walk me through DMAIC on a real case."**
   → GT-SS500 GND 노이즈: D=노이즈 유발 제어 불안정 / M=Scope 파형·전압 기록 / A=DFMEA+5Why→EMI 경로 / I=쉴딩+접지 보강 / C=IQC 항목 추가·DFMEA 갱신.

5. **"How do you handle non-normal distributions in Cpk?"**
   → Box-Cox 변환 후 정규화 또는 비모수 Cpk (백분위수 기반). 또는 Cpk 포기 후 합격률(p-value 기반)로 대체.

---

## 7. 학습 체크리스트

- [ ] Bayes' Theorem 한 줄 + Prior/Likelihood/Posterior 역할 영어로 설명
- [ ] Cpk/Ppk 산식 종이에 손으로 쓰기
- [ ] Cpk = 1.33 / 1.67 / 2.0 각각 DPMO 즉답 (63 / 0.57 / 0.002)
- [ ] "Cpk가 높은데 Ppk가 낮으면 무슨 의미?" 30초 안에 설명
- [ ] Cpk 예제 (USL=105, LSL=95, μ=102, σ=1) 직접 계산

---

## 8. 다음 학습 (D6 예고)

**Camera/VCM 도메인 + Day 1~5 수식 교차연결**
- VCM 5대 고장 모드를 DFMEA 언어로
- Coffin-Manson + Weibull + FRACAS + Cpk → Apple Camera에 어떻게 연결되는가
- 황인혁 자가학습 1주 결과물 총정리
