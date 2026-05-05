# Day 2 — JESD47 7종 시험 + PCT / Coffin-Manson (학습 가이드)

> 작성: 2026-05-05 | Apple Reliability Engineer 면접 준비 자가학습
> 베이스: `learning_day1to3.md` §2, `reliability_competency.md` Block 4
> **자가학습 SSOT**: 본 문서는 학습용 자가 정리 자료다. 외부 제출 자료에 직접 인용 금지.

---

## 🎯 학습 목표

이 D2를 끝내면 영어로 60초 안에 다음 3가지를 설명할 수 있다.

1. **JESD47 7종 시험** — 각 시험의 목적·가속 조건·주요 고장 모드를 1줄로
2. **Coffin-Manson** — 가속 인자(AF) 계산과 수명 외삽 방법
3. **PCT ≠ Coffin-Manson** — 시험 프로토콜 vs 수명 모델 혼용 금지

> IGBT Power Cycling Test (PCT) 직접 기여 경험이 있으므로 이 주제는 100% 질문 들어온다.

---

## 1. JESD47 7종 시험 매트릭스

### 1.1 한 줄 정의

> "JESD47 defines a minimum set of stress tests a semiconductor must pass to demonstrate
> long-term reliability — it specifies the stress conditions, durations, and sample sizes,
> but NOT how to model lifetime from the results. That's what Coffin-Manson and Arrhenius do."

### 1.2 7종 시험 요약표 (★★★ 암기)

| 시험 | 약자 | 스트레스 | 표준 조건 | 주요 고장 모드 |
|------|------|---------|----------|-------------|
| High Temp Operating Life | HTOL | 고온 + 동작 전압 | 125°C, 1000h | Hot carrier, NBTI, EM |
| Temperature Humidity Bias | THB | 고온·고습 + 바이어스 | 85°C/85%RH, 1000h | 부식, 이온 이동 |
| Temperature Cycling | TC | 공기 온도 변화 (수동) | -55°C ↔ +125°C, 1000 cycles | 솔더·와이어 피로 (Coffin-Manson) |
| Power Cycling | PC | 접합 온도 변화 (능동) | ΔTj 제어, 수천 cycles | 본드와이어 lift-off, die-attach |
| ESD — Human Body Model | HBM | 정전기 방전 | 100pF / 1.5kΩ, ±2kV | Gate 절연 파괴 |
| ESD — Charged Device Model | CDM | 디바이스 자체 충전 | ±500V | 얇은 게이트 산화막 파괴 |
| Electromigration | EM | DC 전류밀도 | 고온 + J_max | 금속선 보이드·힐록 |

**TC vs PC 핵심 차이**:

| 항목 | TC (Temperature Cycling) | PC (Power Cycling) |
|------|--------------------------|-------------------|
| 온도 제어 | 외부 챔버 공기 온도 | 내부 접합 온도 Tj (전류로 직접 가열) |
| 사이클 시간 | 수 분 | 수 초~수십 초 |
| 주 고장부위 | 솔더 범프·FPC·패키지 | 본드와이어·die-attach |
| 적용 대상 | 패키지 솔더 | 파워 반도체 (IGBT, MOSFET) |

---

## 2. Coffin-Manson + 가속 인자

### 2.1 Coffin-Manson 산식

```
기본형 (응력 기반):
    Nf = C · (Δεp)^(-c)

    Nf  : 고장까지 사이클 수
    Δεp : 소성 변형 범위 (plastic strain range)
    C, c : 재료 상수

온도 기반 단순화형 (솔더 피로에 주로 사용):
    Nf = A · (ΔT)^(-n)

    ΔT  : 온도 스윙 (°C)
    n   : 재료 지수 (SAC305 솔더 ≈ 2, Al 와이어 ≈ 3~5)
```

### 2.2 가속 인자 (AF)

```
AF = (ΔT_test / ΔT_field)^n

예시:
    필드 ΔT = 20°C, 시험 ΔT = 100°C, n = 2

    AF = (100/20)^2 = 5^2 = 25

    → 시험 1,000 cycles = 필드 25,000 cycles
    → 필드 3년 = 109,500 cycles 대응 시험 = 4,380 cycles
```

### 2.3 Arrhenius (HTOL용 가속 인자)

```
AF = exp[ (Ea/k) · (1/T_use - 1/T_test) ]

    Ea  : 활성화 에너지 (eV) — NBTI ≈ 0.4~0.6eV, EM ≈ 0.7~1.0eV
    k   : Boltzmann = 8.617×10⁻⁵ eV/K
    T   : 절대 온도 (K)
```

### 2.4 PCT ≠ Coffin-Manson (★ 혼용 금지)

```
PCT  = 시험 프로토콜 (어떻게 테스트하는가)
       → JESD47 Power Cycling 조건 정의

Coffin-Manson = 수명 외삽 모델 (데이터로 수명을 어떻게 계산하는가)
       → PCT 결과 데이터를 입력으로 써서 필드 수명 계산

PCT를 수행 → 데이터 수집 → Coffin-Manson으로 외삽 = 올바른 순서
"PCT로 수명 계산했다" = 의미 혼용 오류
```

### 🖼️ 참고 figure URL

- **Coffin-Manson 소성 변형 vs 수명 (log-log 직선)**:
  https://en.wikipedia.org/wiki/Coffin%E2%80%93Manson_relation
  → Wikipedia 페이지에 Δεp vs Nf log-log 그래프 + 식 정의.

- **Temperature Cycling Failure Mode (솔더 크랙)**:
  https://en.wikipedia.org/wiki/Solder_fatigue
  → 솔더 피로 메커니즘 + 크랙 단면 사진. Coffin-Manson 연결.

- **JESD47 개요 (JEDEC 공식)**:
  https://www.jedec.org/standards-documents/docs/jesd47
  → JEDEC 공식 문서 목록. 실제 PDF는 계정 필요할 수 있으나 개요는 무료 열람.

- **Electromigration 메커니즘 (Wikipedia)**:
  https://en.wikipedia.org/wiki/Electromigration
  → EM void + hillock 형성 그림. HTOL/EM 시험 원리 이해용.

- **Accelerated Life Testing 개요 (ReliaWiki)**:
  검색어: site:reliawiki.org "Accelerated Life Testing"
  → ReliaWiki ALT 개요 페이지. Arrhenius/Coffin-Manson 모델 figure 포함.

---

## 3. 황인혁 경험 ↔ 개념 연결

| 개념 | 내 경험 | 인터뷰 한 줄 |
|------|--------|------------|
| Power Cycling Test | IGBT PCT 기여 (P-01 IEEE TIM 2024, 3저자) | "I contributed to PCT work on IGBT modules — the bond-wire lift-off was confirmed as β>1, a wear-out mode, which is exactly what Coffin-Manson models." |
| Coffin-Manson 외삽 | 개념 적용 (학습) — Solar Energy P-04는 Miner's Rule 기반 유사 방법론 | "I applied Miner's Rule for variable-environment lifetime prediction — the same damage-accumulation philosophy as Coffin-Manson, generalized to mixed-stress histories." |
| JESD47 TC/PC | PCT 프로토콜 준수 (ΔTj 제어) | "In the IGBT PCT, we followed the JESD47 Power Cycling protocol — junction temperature swing was controlled, not ambient." |
| HTOL / THB | 개념 학습 (직접 수행 X) | "HTOL and THB target different mechanisms — HTOL for hot carrier and NBTI, THB for moisture-driven corrosion. I've studied both but haven't run them directly." |

---

## 4. 인터뷰 60초 답변 (영문 — 외워야 함)

> Q: "Walk me through how you'd select a JESD47 test for a new power module."

> A: "I'd start with the failure mechanism. For a power module with bond-wire
> interconnects, the dominant degradation is thermal fatigue — so Power Cycling
> per JESD47 is the primary test. Power Cycling controls junction temperature
> directly, unlike Temperature Cycling which controls ambient. The PCT data
> gives you Vce-sat rise and thermal resistance rise over cycles. To translate
> that to field life, you apply Coffin-Manson: N_f equals A times delta-T to
> the power of negative n. The acceleration factor is the ratio of test delta-T
> to field delta-T, raised to n — typically 2 for solder. The key distinction is
> PCT is the test protocol, Coffin-Manson is the life model — confusing the two
> leads to wrong extrapolations. I ran PCT on IGBT modules at the lab, and the
> bond-wire lift-off we observed had a Weibull beta greater than one — classic
> wear-out, which validates Coffin-Manson applicability."

— 약 58초. PCT/Coffin-Manson 구분 명시, IGBT 경험 연결, β>1 언급.

---

## 5. 예상 Follow-up 5개

1. **"What's the difference between TC and PC?"**
   → TC = 챔버 공기 온도 제어. PC = 전류 인가로 접합 직접 가열. TC는 솔더/패키지, PC는 본드와이어/die-attach 타겟.

2. **"Why is n=2 for SAC305 solder?"**
   → 실험적 관찰 기반 경험식. 소성 변형 지수. Al 와이어는 n≈3~5 (더 가파름). 재료마다 보정 필요.

3. **"How do you determine activation energy Ea for Arrhenius?"**
   → 복수 온도에서 HTOL 시험 → ln(MTTF) vs 1/T 직선 기울기 = Ea/k. 문헌값 참조도 일반적.

4. **"What if your field delta-T is not constant?"**
   → Miner's Rule (Damage Summation): D = Σ(n_i/N_i). 각 사이클 온도 구간별 Coffin-Manson Nf 계산 후 합산.

5. **"How do you validate the Coffin-Manson fit?"**
   → 복수 ΔT 조건에서 PCT 데이터 → log-log 직선 fitting → R² 확인 + 필드 반환품 데이터 교차 검증.

---

## 6. 학습 체크리스트

- [ ] JESD47 7종 이름·조건·고장모드 표 손으로 한 번 써보기 (TC/PC 차이 중심)
- [ ] Coffin-Manson 산식으로 AF = 25 예제 직접 계산 (ΔT 20→100, n=2)
- [ ] "PCT ≠ Coffin-Manson" 설명을 비전공자에게 1분 안에 설명 연습
- [ ] IGBT PCT 경험을 STAR 형식으로 말해보기 (D7 Script #2 참조)
- [ ] Arrhenius AF 예제 1회 계산 (Ea=0.7eV, T_use=70°C → T_test=125°C)

---

## 7. 다음 학습 (D3 예고)

**MIL-STD-810 / IEC 60068-2 / IEC 60529 (IP 코드)**
- 미군·민간 환경 시험 표준 비교 매핑
- IP67/IP68 즉답 — iPhone 방수 기준 직접 연결
- GT-SS500 농업 자율주행 환경 시험 연결
