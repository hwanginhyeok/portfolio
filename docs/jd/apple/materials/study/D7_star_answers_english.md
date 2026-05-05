# Day 7 — STAR 영문 답변 5종 핵심 포인트 카드 (학습 가이드)

> 작성: 2026-05-05 | Apple Reliability Engineer 면접 준비 자가학습
> 베이스: `learning_day4to7.md` §7.1~7.5 — **풀스크립트 원본 그대로 참조**
> **자가학습 SSOT**: 본 문서는 학습용 자가 정리 자료다. 외부 제출 자료에 직접 인용 금지.

---

## 🎯 학습 목표

이 D7을 끝내면:

1. **5가지 STAR 스토리** 각각의 S/T/A/R를 영어로 2~3분 내에 말할 수 있다
2. **핵심 수치 카드** — 각 스토리의 정량 수치를 보지 않고 즉답할 수 있다
3. **Follow-up 3개** — 각 스토리의 예상 심화 질문에 키워드로 답할 수 있다

> 풀스크립트 원본: `learning_day4to7.md` §7.1~7.5 참조 (본 파일은 핵심 압축 카드)

---

## STAR 프레임워크

| 파트 | 권장 길이 | 핵심 |
|------|----------|------|
| Situation | 60~80단어 | 제품·컨텍스트·시점 명확히 |
| Task | 30~50단어 | **본인 역할 + 목표** |
| Action | 80~120단어 | **"I"로 시작 — we 금지** |
| Result | 50~70단어 | **정량 수치 1~2개 필수** |

---

## STAR #1 — MCB Carbonization RCA (전해부식)

### 핵심 포인트 카드

| 포인트 | 내용 |
|--------|------|
| **제품** | GT-SS500 48V 자율주행 Speed Sprayer |
| **현상** | 48V MCB 단자 탄화 — power cycling 중 발견 |
| **근본원인** | IEC 60947-2 규격 미달 MCB → 전해부식 → 열폭주 |
| **시정조치** | IEC 60947-2 준수 MCB 교체 + 200 cycles 재현 검증 |
| **결과** | NCR #204 양산 전 Close · 16 units 출하 무재발 |

### 핵심 수치 (★ 암기)

```
48V / 30A / NCR #204 / 200 power cycles 검증 / 16 units 출하
```

### 외울 1단락 (Action + Result 핵심)

> "I ran a five-step RCA. I defined the failure mode: contact resistance rising
> under sustained DC until thermal runaway. Using 5 Why, I traced back through
> the evidence — charring was worst at the high-current terminal, arcing marks
> were asymmetric, and the MCB data sheet showed a continuous current rating below
> our 48V, 30A operating condition. Root cause: electrolytic corrosion — the MCB
> was running beyond its IEC 60947-2 specification. I redesigned to a compliant
> breaker, reproduced the original failure in the lab, and confirmed zero recurrence
> over 200 power cycles. NCR #204 closed. First-article batch of 16 units shipped
> with zero MCB faults. The fix was horizontally deployed to the inspection guide
> for all future programs."

### Follow-up 3개 + 답변 키워드

| # | 질문 | 키워드 |
|---|------|--------|
| 1 | "How did you reproduce the failure?" | 동일 MCB + 48V/30A 지속 전류 + 수 시간 → 동일 탄화 패턴. 재현 가능성 = 근본원인 신뢰도 |
| 2 | "What would you do differently?" | IQC에 IEC 등급 체크 항목 추가 → 조달 단계 차단. DFMEA 시 전기 부품 등급 검증 항목화 |
| 3 | "Was there schedule impact?" | 2주 지연 (재현 시험 + 신규 조달). Critical Path 영향 없음. 버퍼 내 흡수 |

---

## STAR #2 — IGBT PCT Bond-Wire Lift-Off (P-01 IEEE TIM 2024)

### 핵심 포인트 카드

| 포인트 | 내용 |
|--------|------|
| **장소** | 건국대 RBDO Lab, 2022 |
| **목적** | IGBT 모듈 내부 본드와이어 열화를 분해 없이 전기 파라미터로 감지 |
| **핵심 발견** | Vce-sat 상승 + Rth 변화 없음 = 본드와이어 lift-off (die-attach 아님) |
| **검증** | 단면 현미경 (cross-section microscopy) 사후 확인 |
| **결과** | IEEE TIM 2024 출판 (DOI 10.1109/TIM.2024.3472910) |

### 핵심 수치 (★ 암기)

```
JESD47 PCT 프로토콜 / ΔTj 제어 / Vce-sat 20% 기준 /
bond-wire lift-off / IEEE TIM 2024 (3rd author)
```

### 외울 1단락 (Action + Result 핵심)

> "I set up the PCT bench: the IGBT module was cycled to generate a controlled
> junction temperature swing. I monitored three parameters: Vce saturation voltage,
> collector current harmonics, and thermal resistance. After several thousand cycles,
> I observed a step increase in Vce-sat with no corresponding rise in thermal
> resistance. That asymmetry was the diagnostic key — it isolated bond-wire lift-off
> from die-attach solder fatigue. I confirmed with cross-sectional microscopy
> post-test. The work demonstrated that IGBT bond-wire lift-off is detectable from
> system-level output signals without disassembly. Published in IEEE Transactions on
> Instrumentation and Measurement, 2024."

### Follow-up 3개 + 답변 키워드

| # | 질문 | 키워드 |
|---|------|--------|
| 1 | "What was the test stopping criterion?" | Vce-sat 20%+ 상승 또는 Rth 20%+ 상승 (먼저 도달 시 중단). JESD47 정의 준수 |
| 2 | "How did you separate Rth from Vce-sat changes?" | Vce-sat = 전기적 (bond-wire 저항). Rth = 열적 (die-attach 계면). 독립 모니터링 → 교차 분석 |
| 3 | "Can this apply to VCM coil degradation?" | VCM 코일 저항 증가 → 구동 전류 변화 → 서명 기반 진단. 원리 동일. PHM→Camera 확장 스토리 |

---

## STAR #3 — DFMEA AP=H 5건 도출 → 양산 전 전부 해소

### 핵심 포인트 카드

| 포인트 | 내용 |
|--------|------|
| **제품** | GT-SS500 48V 전장 아키텍처 |
| **방법론** | AIAG-VDA 2019 DFMEA 7단계 |
| **작성 수** | DFMEA 5종 (MCB / LCD 상태머신 / 펌프 / CAN / GND·EMI) |
| **AP=H 항목** | 5건 (Severity 높음 or Detectability 낮음 → 무조건 시정 필요) |
| **결과** | 양산 게이트 전 전부 해소 · 잔여 위험 0 · 16 units 출하 무결함 |

### 핵심 수치 (★ 암기)

```
5 DFMEAs / AP=H 5건 / AIAG-VDA 2019 / 잔여 위험 0 / 16 units
```

### 외울 1단락 (Action + Result 핵심)

> "I applied the AIAG-VDA 2019 seven-step process: structure analysis, function
> analysis, failure analysis, risk rating with Severity-Occurrence-Detection plus
> Action Priority matrix, and optimization. Across five DFMEAs I identified five
> AP=H items — each requiring corrective action regardless of occurrence rate due
> to high severity or low detectability. I owned tracking: assigned owners, set dates,
> linked each to an NCR, and followed through to verified closure. All five AP=H items
> closed before the gate review. Residual risk at production entry: zero high-priority
> items. First-article batch of 16 units shipped with zero safety-critical defects.
> The DFMEAs are now living documents — updated with each NCR close."

### Follow-up 3개 + 답변 키워드

| # | 질문 | 키워드 |
|---|------|--------|
| 1 | "AIAG-VDA 2019 vs old AIAG FMEA?" | 2019: AP(Action Priority) matrix 도입 — S×D 우선, O 보조. RPN 단독 사용 폐기. 7단계 명시. Failure Chain 개념 |
| 2 | "How do you set Detection rating?" | 현행 설계 관리 방법의 검출 능력 평가. D=1: 거의 확실히 검출. IQC 항목 있으면 D 낮아짐 |
| 3 | "What if AP=H is not resolved at gate?" | Gate 통과 불가 원칙. 긴급 시: interim control 정의 + 해소 일정 + Risk 수용 Sign-off |

---

## STAR #4 — APQP Phase 2~3 + Gate Review + 양산 16pcs Ramp

### 핵심 포인트 카드

| 포인트 | 내용 |
|--------|------|
| **제품** | GT-SS500 48V 자율주행 Speed Sprayer |
| **역할** | 전력제어 엔지니어 + 주니어 PM (겸임) |
| **범위** | APQP Phase 2~3, 6팀 Cross-functional, BOM 132항목, NCR 27건 |
| **위기** | 양산 3주 전: BOM 23건 재고 부족 동시 발생 |
| **결과** | Gate Review 계획대로 통과 · 16+2+2 units 출하 · NCR 27건 전부 Close |

### 핵심 수치 (★ 암기)

```
132-item BOM / 27 NCRs / 6팀 / 16+2+2 units /
45항목 체크리스트 / Phase 2~3 / APQP
```

### 외울 1단락 (Action + Result 핵심)

> "In Phase 2 I built four test rigs from scratch — dynamometer, fan bench, pump
> bench, and bumper rig — aligned with MIL-STD-810 and IEC 60068-2 profiles.
> In Phase 3 I defined IQC criteria and built a 45-item production readiness
> checklist. I ran weekly Gate Reviews with NCR health dashboards. Three weeks
> before planned shipment, procurement flagged 23 BOM items with insufficient
> stock — I reprioritized the NCR backlog, accelerated 8 critical-path items,
> and negotiated 5 component substitutions. Gate Review passed on schedule.
> Sixteen units plus two demo units and two spares shipped on plan. All 27 NCRs
> closed, five AP=H items resolved with zero residual safety risk. The checklist
> is now a template for the next program."

### Follow-up 3개 + 답변 키워드

| # | 질문 | 키워드 |
|---|------|--------|
| 1 | "Biggest Gate Review blocker?" | BOM 23개 재고 부족 + MCB #204 미해소 동시. Critical Path 분석으로 우선순위화 |
| 2 | "How to manage 6 teams without formal authority?" | 주간 Gate Review 공개 NCR 대시보드 → 투명성으로 책임감 유도. 블로킹 항목 팀장 에스컬레이션 |
| 3 | "What to do differently next APQP?" | Phase 1에서 IQC 기준 초안 더 일찍. Cpk 목표값을 공급사 계약에 명시. NCR 기준 SOP화 |

---

## STAR #5 — Damage Summation (P-04) PV 폴리머 수명 예측

### 핵심 포인트 카드

| 포인트 | 내용 |
|--------|------|
| **배경** | 건국대 학부 연구원, 2023 (PV 모듈 수명 예측 프로젝트) |
| **문제** | 단일 스트레스 최악 조건 모델 → 과도하게 보수적 (실제 필드보다 수명 과소 예측) |
| **방법** | Miner's Rule (Damage Summation): D = Σ(n_i / N_i) |
| **결과 비교** | 단일 스트레스: 과보수적. Damage Summation: 필드 데이터와 훨씬 정합 |
| **출판** | Solar Energy 2024 (DOI 10.1016/j.solener.2024.112645, 4저자) |

### 핵심 수치 (★ 암기)

```
Miner's Rule / D = Σ(n_i/N_i) / D=1.0 고장 /
Solar Energy 2024 (4th author) / PV 폴리머 수명
```

### 외울 1단락 (Action + Result 핵심)

> "I processed long-term temperature and humidity measurement data from field-deployed
> PV sites. I discretized the stress history into bins — each bin a temperature-humidity
> combination with a measured duration. For each bin, I computed N_i from the single-
> stress model, then accumulated the damage fraction n_i over N_i. When the sum reached
> 1.0, that was the predicted end-of-life. I compared this against field-observed
> degradation and against worst-case constant-stress predictions. The damage summation
> model aligned much more closely with field reality — substantially reducing prediction
> error without sacrificing conservatism. Published in Solar Energy, Elsevier, 2024.
> The method is directly applicable to any variable-environment reliability problem —
> including smartphone camera modules exposed to daily temperature and humidity cycles."

### Follow-up 3개 + 답변 키워드

| # | 질문 | 키워드 |
|---|------|--------|
| 1 | "Miner's Rule main limitation?" | 순서 효과(sequence effect) 무시. D=1.0이 항상 고장 아님 (D≈0.7~1.5 범위). 비선형 Corten-Dolan 모델로 보완 가능 |
| 2 | "How do you get N_i for each stress condition?" | 단일 스트레스 ALT → Arrhenius/Eyring 모델로 스트레스-수명 관계 구축 → 각 조건 외삽 |
| 3 | "Apply this to iPhone camera?" | 하루 온도 프로파일 수집 → 각 구간 Coffin-Manson N_i → Miner's D 적산 → 3년 후 스프링/FPC 수명. 기존 단일 ΔT보다 정확 |

---

## 핵심 수치 빠른 암기 카드 (전체)

| STAR | 핵심 수치 |
|------|----------|
| #1 MCB RCA | 48V · 30A · 200 cycles · NCR #204 · 16 units |
| #2 IGBT PCT | ΔTj · Vce-sat 20% 기준 · IEEE TIM 2024 · bond-wire lift-off |
| #3 DFMEA | AIAG-VDA 2019 · 5 DFMEAs · AP=H 5건 · 잔여 위험 0 |
| #4 APQP | 132 BOM · 27 NCRs · 6팀 · 16+2+2 units · 45항목 |
| #5 Damage Sum | Miner's Rule · Σ(ni/Ni) · Solar Energy 2024 · D=1.0 |

---

## 녹음·연습 가이드

```
1회차: 풀스크립트(learning_day4to7.md §7) 읽으면서 녹음
2회차: 80% 속도로 재생 → 어색한 파트 표시
3회차: 정량 수치·기술 용어 강조 연습
4회차: 이 카드의 핵심 포인트만 보고 자연스럽게 말하기
5회차: 카드도 없이 → 실제 면접 시뮬레이션
```

**기술 용어 발음 연습**:
- Coffin-Manson / AIAG-VDA / FRACAS / Vce-sat / Weibull
- Duane Plot / AMSAA / Cpk / Bayesian / electrolytic
