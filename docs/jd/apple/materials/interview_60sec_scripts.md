# 인터뷰 60초 답변 스크립트 — Cheat Sheet

> 작성: 2026-05-04 | Apple Reliability Engineer 면접 준비
> 목적: Day 1~3 핵심을 60초 영문 답변 5개로 압축한 최종 cheat sheet
> 기준: 60~90 단어, 자연스러운 회화 톤, 경험 기반 구체성

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

## 빠른 참조 — 숫자 + 공식 카드

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
