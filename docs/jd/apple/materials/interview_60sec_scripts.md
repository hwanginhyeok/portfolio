# 인터뷰 60초 답변 스크립트 — Cheat Sheet

> 작성: 2026-05-04 | 갱신: 2026-05-04 v2 (fact-check pass — RESUME.md SSOT 직접 인용)
> Apple Reliability Engineer 면접 준비
> 목적: Day 1~7 핵심을 60초 영문 답변으로 압축한 최종 cheat sheet
> 기준: 60~120 단어, 자연스러운 회화 톤, 경험 기반 구체성
> fact-check 원칙: 본인이 직접 수행한 사실만 단언. 표준명 사후 매핑 제거.

---

## Script 1 — "How do you determine the reliability of a part?"

> "Both strength and stress are distributions — not fixed values — and reliability
> is the probability that strength exceeds stress at all times.
> That Stress-Strength Interference framework is the theoretical core of my master's
> lab, which was literally named the Reliability-Based Design Optimization Lab.
> In practice, we fit failure time data to a Weibull distribution.
> The shape parameter β tells us where we are on the bathtub curve —
> below 1 is infant mortality, around 1 is random failure, above 1 is wear-out.
> From β and the scale parameter η we compute B10: the time at which
> 10% of the population fails. That's the number we defend against acceptance criteria
> in accelerated life testing."

단어 수: 105 / 발화: ~60초

---

## Script 2 — "Tell me about your semiconductor reliability experience"

> "My most direct semiconductor reliability work is Power Cycling Testing on IGBT
> modules — I personally ran the test cycles, monitoring Vce-sat to detect bond-wire
> lift-off as the dominant failure mode. The aluminum bond wire fatigues and
> delaminates from the chip pad under repeated ΔTj cycling.
> That work was co-authored for publication in IEEE Transactions on Instrumentation
> and Measurement, 2024 — I was the third author.
> To extrapolate PCT cycle life to field conditions, the Coffin-Manson model
> applies: field life scales with test ΔT over field ΔT, raised to the n-th power —
> n is typically 5 to 7 for aluminum bond wires."

단어 수: 110 / 발화: ~62초

*Note (fact-check): 표준 규격명(JESD47/JEP122)은 일반 학습 지식으로는 언급 가능하나 "per JESD47/JEP122 직접 수행" 표현은 제거. "I ran PCT" 사실은 RESUME §4/§5에 직접 명시되어 있음.*

---

## Script 3 — "How do you select test standards for a new product?"

> "Standard selection depends on the product's market and the failure modes we're
> screening. For consumer electronics, IEC 60068-2 covers vibration, shock, thermal
> cycling, and humidity — the international standard for component and product level.
> MIL-STD-810 addresses the same categories at system level with more severe profiles.
> At GINT I designed and built four test rigs in-house covering vibration, impact,
> flow measurement, and bumper safety — the test categories overlap with
> environmental methods like those in MIL-STD-810 and IEC 60068-2, though
> those weren't always the explicit reference document.
> The key is mapping each failure mode to a stress category and setting
> pass criteria against field operating conditions."

단어 수: 112 / 발화: ~63초

*Note (fact-check): "aligned with MIL-STD-810 / IEC 60068-2" → 시험 카테고리 중복 인정으로 약화. "sealed CAN connectors to IEC 60529 IP67" 완전 제거 — RESUME에 직접 명시 없음.*

---

## Script 4 — "Walk me through one of your RCAs"

> "The clearest example is the MCB contact carbonization issue on GT-SS500.
> The symptom was visible charring on the 48V power terminal after field cycling.
> Step one: we defined the failure mode precisely — contact resistance rising
> until thermal runaway. Step two: we traced back to the root cause —
> the MCB was rated below the required specification for that current level,
> making electrolytic corrosion under DC current unavoidable.
> Step three: redesigned to a spec-compliant breaker. Step four: reproduced the
> original failure in the lab to confirm the mechanism, then confirmed zero
> recurrence with the new part. That closed as part of our NCR closed-loop —
> the corrective action documented, and the fix flowed into the production BOM."

단어 수: 119 / 발화: ~67초

*Note (fact-check): "5 Why + Ishikawa" 명시 제거. "FRACAS loop" → "NCR closed-loop"로 변경. 사실 자체(MCB 탄화·전해부식·IEC 60947-2 등급 교체)는 RESUME §4 직접 명시 확인.*

---

## Script 5 — "What's your biggest knowledge gap and how are you closing it?"

> "Camera optics and VCM-specific reliability is where my background is thinnest —
> my domain has been electric motors and power electronics, not optical modules.
> That said, the methods are the same: ALT, DFMEA, power cycling for thermal fatigue,
> Weibull lifetime analysis. I've spent this past week mapping those methods
> explicitly to camera VCM failure modes — coil open, spring fatigue, Hall sensor
> drift — and studying how reliability test approaches apply to imaging components.
> My honest view is that the reliability methodology transfers directly;
> the learning curve is the physics of the specific components, which I'm actively
> closing through self-study before this role."

단어 수: 106 / 발화: ~60초

*Note (fact-check): "Weibull lifetime estimation" 어필 약화 → "Weibull lifetime analysis"(일반 학습 언급) 유지. "JEDEC JESD47 test categories as they apply to imaging components" 제거 — 직접 사용 아닌 학습 중. VCM 고장모드 5종은 자가학습 자료 근거로 언급 가능하나 "인터뷰 직전 자가학습 수준"임을 인식할 것.*

---

## Script 6 — "Walk me through how you operated NCR / FRACAS"

> "A corrective action closed loop has five stages: Failure Reporting, Analysis,
> Corrective Action, Verification, and System Update.
> At GINT I ran this loop on 27 NCRs for the GT-SS500 program.
> Each NCR started with a standard form — date, product ID, observed symptom,
> who found it. We ran root-cause analysis; I personally led four — including an
> MCB carbonization case traced to electrolytic corrosion via current rating mismatch.
> The corrective action was verified by reproducing the original failure,
> then confirmed zero recurrence. Then we updated the DFMEA, inspection guide, and
> BOM. We called it NCR tracking, but the structure maps directly to a FRACAS loop —
> I'm formalizing that framing now."

단어 수: 116 / 발화: ~65초

*Note (fact-check): "27 NCRs as FRACAS" → "NCR closed-loop; maps to FRACAS which I'm formalizing"로 정직 표현.*

---

## Script 7 — "How do you handle small-sample reliability?"

> "When sample sizes are small — say fewer than twenty units in an ALT —
> frequentist MLE gives wide confidence intervals on B10, sometimes too wide for
> useful decision-making. Bayesian reliability addresses this by incorporating a
> prior: historical data from a predecessor component, or a Jeffreys non-informative
> prior if nothing better is available. The posterior on Weibull parameters is
> narrower, and you can extract a credible interval on B10 directly.
> I haven't applied Bayesian reliability in production yet, but it's a natural
> extension of the RBDO framework from my graduate lab, where we used prior
> distributions to model strength uncertainty before test data arrived."

단어 수: 110 / 발화: ~62초

---

## Script 8 — "What is Cpk and how does it relate to IQC/OQC?"

> "Cpk is the process capability index — the minimum of USL minus mean over
> three sigma and mean minus LSL over three sigma — accounting for both spread
> and centering. A Cpk of 1.33 is the standard production baseline: the mean
> sits at least four sigma from the nearer spec limit.
> At GINT I defined IQC and OQC inspection criteria for GT-SS500 — pass/fail
> thresholds and re-sample rules — at first-article scale (16 units plus
> spares). We didn't yet operate a formal Cpk/Ppk dashboard since sample
> volume was small, but that's the layer I'd add as production scales —
> Cpk for spread and centering on each measurement, Ppk for long-term drift
> across batches."

단어 수: 113 / 발화: ~63초

*Note (fact-check): 사용자가 IQC/OQC 정의는 직접 수행(RESUME §5.1 "IQC 검사 가이드"), Cpk/Ppk 대시보드 운영은 RESUME에 없음 — 답변에서 "We didn't yet operate a formal Cpk/Ppk dashboard since sample volume was small"로 직접 수행 X를 명시 분리. "first-article scale (16 units plus spares)" RESUME §4 직접 매핑. 면접관 후속 질문 "Did you run Cpk?" → "No, sample volume was first-article scale, not full production"로 자연스럽게 답변 가능.*

---

## Script 9 — "How would you approach Apple's VCM reliability test plan?"

> "I'd start with DFMEA — coil open, spring fatigue, Hall sensor drift,
> demagnetization, and contamination are the five primary failure modes.
> Then map each to an ALT stress: high-temperature operation for coating delamination
> and magnet degradation, temperature cycling for FPC fatigue, drop test for spring
> failure, humidity exposure for coil corrosion. From ALT data I'd fit Weibull,
> compute B10, and require B10 to exceed the field life target with an appropriate
> safety factor. For production I'd define incoming inspection criteria on coil
> resistance and stroke length. Any field NCR feeds back into a closed-loop —
> DFMEA update, inspection guide revision, horizontal deployment to similar parts."

단어 수: 114 / 발화: ~64초

*Note (fact-check): "incoming Cpk monitoring" 제거 → "define incoming inspection criteria". "FRACAS closed loop" → "closed-loop". 전반적으로 "I would" 가정형 유지 — VCM 직접 경험 없음 명시.*

---

## Script 10 — "What's a corrective action that didn't work the first time?"

> "On the GT-SS500, we had a ground-bounce noise issue that caused intermittent
> control instability. The first corrective action was a localized grounding strap —
> it reduced noise amplitude but didn't eliminate it. On retesting, the symptom
> recurred under high-load conditions. We re-ran the root-cause analysis and discovered
> the root cause was deeper: the power and signal ground planes were sharing a single
> return path that became a noise antenna under motor braking current. We redesigned
> the PCB grounding topology — separate return planes with a single tie point — and
> added differential treatment on the signal lines. Recurrence zero on re-verification.
> The lesson: if the symptom reduced but didn't disappear, the root cause analysis
> wasn't deep enough."

단어 수: 121 / 발화: ~68초

*Note (fact-check): GND 노이즈 RCA 사실 — RESUME §4 "GND 노이즈" 직접 명시. "shielding/grounding countermeasure" 구체화 표현 일부 약화 → "differential treatment on signal lines" 수준 유지.*

---

## Script 11 — "Tell me about your APQP experience"

> "I led APQP Phase 2 and 3 for the GT-SS500, a 48V autonomous agricultural sprayer.
> In Phase 2, I built four custom test rigs in-house and authored five DFMEAs
> covering Step 1 through 7 — all five AP=H action points resolved before gate.
> In Phase 3, I defined IQC and OQC inspection criteria and managed a 132-item BOM.
> I ran weekly Gate Reviews across six cross-functional teams, tracked 27 NCRs
> through closure, and took the product to a first-article production plan of
> 16 units, plus 2 transport carts and 2 spares."

단어 수: 96 / 발화: ~55초

*Note (fact-check): "aligned with MIL-STD-810 and IEC 60068-2" 제거. "AIAG-VDA 2019" 제거 → "Step 1–7"만. "Six Sigma DMAIC gating logic" 제거. "first-article shipment of 16 units" → "first-article production plan of 16 units plus 2 transport carts and 2 spares".*

---

## 빠른 참조 — 숫자 + 공식 카드 (Day 1~7 통합)

### Day 1~3 (기존)

| 항목 | 값 / 공식 |
|------|---------|
| Weibull CDF | F(t) = 1 − exp[−(t/η)^β] |
| B10 공식 | B10 = η·(−ln 0.9)^(1/β) = η·(0.10536)^(1/β) |
| B10 예시 | η=10,000h, β=2 → B10 = 3,247h |
| MTTF 공식 | η·Γ(1+1/β) |
| β 해석 | <1 초기불량 / =1 우발 / >1 마모 |
| S-S Reliability Index | β_HL = (μ_S−μ_L)/√(σ_S²+σ_L²) |
| Coffin-Manson | Nf = C·(ΔT)^(−n) |
| n (Al 본드와이어) | 5~7 |
| n (Sn-Pb 솔더) | 1.9~2.5 |
| CM 외삽 | Nf_field = Nf_test × (ΔT_test/ΔT_field)^n |
| HTOL 조건 | 125°C, bias, 1000h |
| HTSL 조건 | 150°C, no bias, 1000h |
| THB 조건 | 85°C / 85%RH, 1000h |
| HAST 조건 | 130°C / 85%RH (가압), ~96h |
| HBM ESD | 100pF + 1.5kΩ, 피크 ~1.33A |

### Day 4~6 (신규 추가)

| 항목 | 값 / 공식 |
|------|---------|
| FRACAS 5단계 (학습 지식) | Failure Reporting → Analysis → Corrective Action → Verification → System Update |
| Duane growth rate α | 0.3~0.5 = 양호한 신뢰도 성장 |
| AMSAA intensity | λ(t) = λ·β·t^(β-1), β<1이면 신뢰도 성장 중 |
| Cpk 공식 (학습 지식) | min[(USL-μ)/3σ, (μ-LSL)/3σ] |
| Cpk 기준 | 1.33 = 양산 baseline (4σ / 63 DPMO), 1.67 = 고신뢰성 (5σ) |
| Ppk vs Cpk | Cpk: 단기 within-σ / Ppk: 장기 overall-σ |
| Bayesian | posterior ∝ likelihood × prior |
| Jeffreys prior | π(η) ∝ 1/η — 비정보적, 변환 불변 |
| Miner's Rule | D = Σ(ni/Ni), D≥1 → 수명 만료 |
| VCM B10 예시 | η=500k cycles, β=2.5 → B10 ≈ 201,100 cycles |
| 안전계수 기준 | B10 ≥ 필드 수명 × 1.5 |
| VCM 5 고장 모드 | 코일 단선 / 스프링 피로 / 홀센서 드리프트 / 자석 감자 / 이물 침입 |

### STAR 5종 핵심 수치 빠른 암기

| STAR | 핵심 수치 |
|------|---------|
| #1 MCB RCA | 48V·30A, 200 cycles 검증, NCR #204, 16 units 생산계획 |
| #2 IGBT PCT | ΔTj, Vce-sat 20% 기준, IEEE TIM 2024 (3rd author), bond-wire lift-off |
| #3 DFMEA | Step 1–7, 5 DFMEAs, AP=H 5건, 잔여 위험 0 |
| #4 APQP | 132-item BOM, 27 NCRs, 6팀, 초도 16 units 생산계획 |
| #5 Damage Sum | Miner's Rule, Σ(ni/Ni), Solar Energy 2024 (4th author) |
