# 인터뷰 60초 답변 스크립트 — Cheat Sheet

> 작성: 2026-05-04 | 갱신: 2026-05-04 (Day 4~7 스크립트 6개 추가, 총 11개)
> Apple Reliability Engineer 면접 준비
> 목적: Day 1~7 핵심을 60초 영문 답변으로 압축한 최종 cheat sheet
> 기준: 60~120 단어, 자연스러운 회화 톤, 경험 기반 구체성

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
> modules — conducted per JESD47 and guided by JEP122 for failure mechanisms.
> We ran repeated power ON/OFF cycles on a 400W BLDC controller IGBT module,
> which caused repeated ΔTj at the chip interface. Bond-wire lift-off was the
> dominant failure mode — the aluminum wire fatigues and delaminates from the chip pad.
> That work was published in IEEE Transactions on Instrumentation and Measurement,
> 2024. To extrapolate PCT cycle life to field conditions, the Coffin-Manson model
> applies: field life scales with test ΔT over field ΔT, raised to the n-th power —
> n is typically 5 to 7 for aluminum bond wires."

단어 수: 116 / 발화: ~65초 (약간 빠르게)

---

## Script 3 — "How do you select test standards for a new product?"

> "Standard selection depends on the product's market and the failure modes we're
> screening. For consumer electronics, IEC 60068-2 covers vibration, shock, thermal
> cycling, and humidity — the international standard for component and product level.
> MIL-STD-810 addresses the same categories at system level for military applications
> with more severe profiles. For water and dust protection, IEC 60529 defines the
> IP rating. At GINT I designed and built four test rigs covering vibration and
> impact — equivalent to MIL-STD-810 Methods 514 and 516 — and designed sealed
> CAN connectors to IEC 60529 IP67 for our EOP 400W program. The standards
> weren't always the explicit reference, but the test profiles and pass criteria
> matched those categories."

단어 수: 118 / 발화: ~65초

---

## Script 4 — "Walk me through one of your RCAs"

> "The clearest example is the MCB contact carbonization issue on GT-SS500.
> The symptom was visible charring on the 48V power terminal after field cycling.
> Step one: we defined the failure mode precisely — contact resistance rising
> until thermal runaway. Step two: we used 5 Why to trace back to the root cause —
> the MCB was rated below the IEC 60947-2 specification for that current level,
> making electrolytic corrosion under DC current unavoidable.
> Step three: redesigned to a spec-compliant breaker. Step four: reproduced the
> original failure in the lab to confirm the mechanism, then confirmed zero
> recurrence with the new part. That RCA closed as part of the FRACAS loop —
> the NCR was verified, corrective action documented, and the fix flowed into
> production BOM."

단어 수: 121 / 발화: ~68초

---

## Script 5 — "What's your biggest knowledge gap and how are you closing it?"

> "Camera optics and VCM-specific reliability is where my background is thinnest —
> my domain has been electric motors and power electronics, not optical modules.
> That said, the methods are the same: ALT, DFMEA, PCT for thermal fatigue,
> Weibull lifetime estimation. I've spent this past week mapping those methods
> explicitly to camera VCM failure modes — coil open, spring fatigue, Hall sensor
> drift — and studying JEDEC JESD47 test categories as they apply to imaging
> components. My honest view is that the reliability methodology transfers directly;
> the learning curve is the physics of the specific components, which I'm actively
> closing through self-study before this role."

단어 수: 107 / 발화: ~60초

---

---

## Script 6 — "Walk me through how you operated NCR / FRACAS"

> "FRACAS is a five-step closed loop: Failure Reporting, Analysis, Corrective
> Action, Verification, and System Update. At GINT I ran this loop on 27 NCRs
> for the GT-SS500 program. Each NCR started with a standard form — date, product ID,
> observed symptom, who found it. We ran RCA, I personally led four — including an
> MCB carbonization case traced to electrolytic corrosion via IEC 60947-2 spec
> mismatch. The corrective action was verified by reproducing the original failure,
> then confirmed zero recurrence. Then we updated the DFMEA, inspection guide, and
> BOM. The label was NCR, but the structure is textbook FRACAS."

단어 수: 112 / 발화: ~62초

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

> "Cpk is the process capability index that accounts for both spread and centering —
> the minimum of USL minus mean over three sigma, and mean minus LSL over three sigma.
> A Cpk of 1.33 is the standard production baseline: the mean is at least four sigma
> away from the nearer spec limit. For high-reliability parts you'd target 1.67 or
> above. At GINT I defined IQC and OQC inspection criteria for GT-SS500 production,
> consistent with Six Sigma DMAIC gating logic and process capability monitoring
> for supplier qualification. Cpk and Ppk together diagnose whether an underperforming
> supplier has a precision problem — Cpk low — or a drift problem — Ppk lower than Cpk."

단어 수: 118 / 발화: ~65초

---

## Script 9 — "How would you approach Apple's VCM reliability test plan?"

> "I'd start with DFMEA — coil open, spring fatigue, Hall sensor drift,
> demagnetization, and contamination are the five primary failure modes.
> Then map each to an ALT stress: HTOL at 85°C for coating delamination and magnet
> degradation, temperature cycling for FPC fatigue, drop test for spring failure,
> THB for coil corrosion. From ALT data I'd fit Weibull, compute B10, and require
> B10 to exceed the field life target times a safety factor of 1.5. For production
> I'd run incoming Cpk monitoring on coil resistance and stroke length. Any field
> NCR feeds back into a FRACAS closed loop — DFMEA update, inspection guide
> revision, horizontal deployment to similar part numbers."

단어 수: 118 / 발화: ~65초

---

## Script 10 — "What's a corrective action that didn't work the first time?"

> "On the GT-SS500, we had a ground-bounce noise issue that caused intermittent
> control instability. The first corrective action was a localized grounding strap
> — it reduced noise amplitude but didn't eliminate it. On retesting, the symptom
> recurred under high-load conditions. We re-ran the RCA and discovered the root
> cause was deeper: the power and signal ground planes were sharing a single return
> path that became a noise antenna under motor braking current. We redesigned the
> PCB grounding topology — separate return planes with a single tie point — and
> added differential shielding on the signal lines. Recurrence zero on re-verification.
> The lesson: if the symptom reduced but didn't disappear, the root cause analysis
> wasn't deep enough."

단어 수: 122 / 발화: ~68초

---

## Script 11 — "Tell me about your APQP experience"

> "I led APQP Phase 2 and 3 for the GT-SS500, a 48V autonomous agricultural sprayer.
> In Phase 2, I built four test rigs aligned with MIL-STD-810 and IEC 60068-2 and
> authored five DFMEAs per AIAG-VDA 2019 — all five AP=H action points resolved
> before gate. In Phase 3, I defined IQC and OQC criteria using Six Sigma DMAIC
> gating logic and managed a 132-item BOM. I ran weekly Gate Reviews across six
> cross-functional teams, tracked 27 NCRs through closure, and took the product
> to first-article shipment of 16 units on schedule."

단어 수: 98 / 발화: ~55초

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
| IP67 | 완전방진 + 1m/30min 침수 |
| IP68 (Apple) | 완전방진 + 6m/30min 침수 |
| HTOL 조건 | 125°C, bias, 1000h |
| HTSL 조건 | 150°C, no bias, 1000h |
| THB 조건 | 85°C / 85%RH, 1000h |
| HAST 조건 | 130°C / 85%RH (가압), ~96h |
| HBM ESD | 100pF + 1.5kΩ, 피크 ~1.33A |

### Day 4~6 (신규 추가)

| 항목 | 값 / 공식 |
|------|---------|
| FRACAS 5단계 | Failure Reporting → Analysis → Corrective Action → Verification → System Update |
| Duane growth rate α | 0.3~0.5 = 양호한 신뢰도 성장 |
| AMSAA intensity | λ(t) = λ·β·t^(β-1), β<1이면 신뢰도 성장 중 |
| Cpk 공식 | min[(USL-μ)/3σ, (μ-LSL)/3σ] |
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
| #1 MCB RCA | 48V·30A, 200 cycles 검증, NCR #204, 16 units 출하 |
| #2 IGBT PCT | ΔTj, Vce-sat 20% 기준, IEEE TIM 2024, bond-wire lift-off |
| #3 DFMEA | AIAG-VDA 2019, 5 DFMEAs, AP=H 5건, 잔여 위험 0 |
| #4 APQP | 132-item BOM, 27 NCRs, 6팀, 16 units 출하, 45항목 체크리스트 |
| #5 Damage Sum | Miner's Rule, Σ(ni/Ni), Solar Energy 2024 |
