# Resume — Inhyeok Hwang

> Target: xAI · Mechanical Engineering Tutor (Remote, Part-time)
> Version: 2026-05-04 v2 (xAI tailored — researcher + writer tone; fact-check pass)
> Source SSOT: RESUME.md master (`docs/blocks/05-extra/RESUME.md`)
> Note: All experience claims reflect RESUME.md SSOT directly. No standard-name post-mapping.

---

## INHYEOK HWANG

**Senior Researcher** · Electrical Control & Product Development
**Email**: dlsgur5560@gmail.com
**GitHub**: github.com/hwanginhyeok
**Portfolio**: hwanginhyeok.github.io/portfolio

---

## SUMMARY

Mechanical engineering researcher with an M.S. from Konkuk University's Reliability-Based Design Optimization (RBDO) Lab, 4 peer-reviewed publications (IEEE TIM · Solar Energy · Journal of Power Electronics, 2024; PHM Asia-Pacific, 2023), and 2 patents. My research spans IPMSM fault diagnosis, accelerated life testing, PHM/RUL estimation, and lifetime prediction under varying stress environments — across three distinct material systems (semiconductor, polymer, motor drivetrain).

At GINT Corp., I have applied this academic foundation across three years of industrial product development: from motor control firmware through full APQP lifecycle management to first-article production plan. The bridge between academic rigor and production reality is where I operate.

Beyond domain depth, I bring a demonstrable record of autonomous learning and technical writing. When tasked with a knowledge gap in optical and camera reliability, I conducted a self-directed one-week study — the kind of cross-domain acquisition that AI training data curation demands.

**Core identity**: ME researcher with publication depth · autonomous learner · technical writer · industrial practitioner.

---

## PUBLICATIONS & PATENTS

### Peer-Reviewed Journals (3, co-authored)

| Year | Journal | Title (abbreviated) | Role |
|------|---------|--------------------|----|
| 2024 | **IEEE Transactions on Instrumentation and Measurement**, Vol. 73 | Bond-wire fault detection in IGBT via inverter output parameters | **3rd author** |
| 2024 | **Solar Energy** (Elsevier), Vol. 276, Art. 112645 | Lifetime prediction of PV polymers under varying environments via damage summation (Miner's Rule) | **4th author** |
| 2024 | **Journal of Power Electronics**, Vol. 24(5), pp. 822–831 | Failure mode identification in IPMSM under ALT via dual sensor architecture | **6th author** |

### Conference Presentations (4)

| Year | Conference | Topic | Award |
|------|-----------|-------|-------|
| 2023 | PHM Society Asia-Pacific | 120 kW IPMSM system-level fault diagnosis | — |
| 2022 | PCIM Asia | IGBT IPM quasi-DC power cycling | — |
| 2022 | Korean Society for Reliability (KSR) | Predictive maintenance for EV drivetrain | **Best Paper Award** |
| 2021 | Korean PHM Society | IGBT open-fault diagnosis via system-level measurements | **Best Poster Award** |

### Patents (2)

- **Patent #1** — Motor initial position detection · Co-inventor · KR App. PN231067KR (2023) · Detection time reduced: 1.0 s → **0.56 s**
- **Patent #2** — *Method for preventing step-out of rotor of motor in low temperature and apparatus thereof* · KR App. **10-2023-0175484** (filed 2023-12-06) · Reg. **10-2654562** (granted 2024-04-01) · Applicant: GINT Inc. · IPC H02P 29/032 · Development contributor (experimental validation; not on inventor list) · −40°C cold-start time: 300 s → **100 s**

---

## EDUCATION

### Konkuk University — M.S. in Mechanical Design (RBDO Lab)
**Mar 2021 – Feb 2023** · 27 major credits · Major GPA 3.77/4.5 · Advisor: Prof. Namsu Kim

**Thesis**: *Fault Diagnosis Simulation of Interior Permanent Magnet Synchronous Motor using Electromagnetic Analysis* (49 pp., RISS: f678963f23f2e418ffe0bdc3ef48d419)

- Constructed an IPMSM digital twin integrating Ansys Maxwell FEM with MATLAB/Simulink inverter Co-simulation; validated across multiple operating conditions (Sim2Real precursor methodology)
- Participated in government-funded PHM SoC development project (MOTIE, Apr 2021 – Oct 2022): RUL estimation for IPMSM drivetrain fault diagnosis using multi-sensor signal fusion
- Observed full ALT design-test-redesign cycle for IPMSM eccentricity fault characterization — load factor application, FTA, dual-sensor architecture operation (P-05, J. Power Electron. 2024, 6th author)
- Research experience: 2.5 years total (6 months undergrad research assistant + 2 years M.S.)

### Konkuk University — B.S. in Mechanical Design
**Mar 2015 – Feb 2021** · 79 major credits · Major GPA 3.24/4.5

---

## EXPERIENCE

### GINT Corp. — Electrical Control R&D + Product Development (Junior PM, concurrent)
**Senior Researcher** · Jan 2025 – Present

**GT-SS500: 48V Electric Autonomous Speed Sprayer — Full Lifecycle from R&D to Mass Production**

- Managed full product lifecycle from algorithm research through first-article production plan of 16 units plus 2 transport carts and 2 spares (APQP Phase 2–3), coordinating across 6 cross-functional teams (design / manufacturing / sourcing / quality / safety / sales)
- Authored 5 Design FMEAs covering Step 1–7; identified 5 high-priority action items (AP=H), all resolved before production ramp
- Led 4 root-cause analyses to closure — MCB electrolytic corrosion, control-mode state machine fault, pump freeze O-ring failure, GND bounce noise
- Designed and built 4 custom test rigs in-house (dynamometer, fan bench, pump bench, bumper safety rig)
- Operated 27-item NCR closed-loop corrective action process; defined IQC/OQC criteria for supplier qualification
- Designed 5-node CAN distributed control architecture (VCU ↔ dual drive MC ↔ fan ESC ↔ pump DRV ↔ BMS); authored 4 DBC files; standardized 3-pass consistency validation protocol

---

### GINT Corp. — Electrical Control R&D
**Junior Researcher** · Feb 2023 – Dec 2024

**EOP 400W: Automotive BLDC Motor Control (Government R&D Project)**

- Conducted Power Cycling Tests on IGBT modules; identified bond-wire lift-off as primary failure mode (P-01, IEEE TIM 2024, 3rd author, DOI 10.1109/TIM.2024.3472910)
- Developed SVPWM/DPWM switching strategy — reduced FET temperature 1–6°C, input power 1–3.8% (validated on 2,932 data points)
- Demonstrated cold-start improvement at −40°C: 300 s → 100 s (subject of Patent #2; experimental validation conducted independently)
- Built dynamometer torque-control system achieving 0.008% nonlinearity; presented at internal engineering seminar
- 2 patent filings (see Patents section above)

---

## SKILLS

### Mechanical Engineering Domains
- Motor design & control: IPMSM, BLDC, sensorless FOC, SVPWM/DPWM, CAN distributed control
- Reliability engineering: ALT (participated in full cycle as observer), PCT (directly conducted), DFMEA (Step 1–7), root-cause analysis, PHM/RUL estimation
- Simulation & modeling: FEM (Ansys Maxwell), Co-simulation (MATLAB/Simulink), digital twin, Sim2Real validation
- Test infrastructure: dynamometer, custom test rigs built in-house, CAN / CANoe
- Lifetime analysis: Damage Summation (Miner's Rule), Weibull estimation (concept), multi-environment stress mapping

### Research & Communication
- Peer-reviewed journal publications: IEEE TIM (Vol. 73, 3rd author), Solar Energy (Vol. 276, 4th author), J. Power Electronics (Vol. 24, 6th author)
- Conference presentations with awards: KSR Best Paper Award (2022), Korean PHM Society Best Poster Award (2021)
- Technical writing: journal manuscripts, patent specifications, design documentation, 1,900+ lines of portfolio materials
- Autonomous learning: self-directed cross-domain knowledge acquisition — self-study notes on camera/optical reliability produced in one week
- Bilingual: Korean (native) · English (professional reading & writing)

### Tools & Platforms
- Programming: Python, MATLAB/Simulink, C (embedded — STM32, NXP MC9S12ZVMC)
- Signal processing & ML familiarity: multi-sensor PHM, prognostics models, classical anomaly detection
- Documentation: Markdown, LaTeX, Git workflow
- Instrumentation: CANoe, Vector VN1600, NI DAQ (NI-9215), oscilloscope, SPICE

---

## SELECTED RESEARCH HIGHLIGHTS

- **IGBT bond-wire fault detection via inverter output parameters** — Power Cycling Test directly conducted; failure mechanism characterized at system level without in-circuit instrumentation (IEEE TIM 2024, 3rd author)
- **PV polymer lifetime prediction under continuously varying environments** — Damage Summation (Miner's Rule) applied to multi-environment stress histories; demonstrates ability to structure complex multi-variable ME problems rigorously (Solar Energy 2024, 4th author)
- **Failure mode identification in IPMSM under ALT via dual-sensor architecture** — Observed full design-test-redesign cycle; methodology illustrates ALT principles applicable to AI training explanation (J. Power Electronics 2024, 6th author)
- **120 kW IPMSM system-level fault diagnosis** — Multi-sensor signal fusion for drivetrain RUL estimation (PHM Society Asia-Pacific 2023)
- **IPMSM digital twin thesis** — Co-simulation (FEM + control model) validated against experimental data; Sim2Real precursor methodology (Konkuk University, 2023)
