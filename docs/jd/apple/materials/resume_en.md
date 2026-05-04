# Resume — Inhyeok Hwang

> Target: Apple Korea · Reliability Engineer, Core Technology Operations
> Version: 2026-05-04 (Apple tailored)
> Source SSOT: RESUME.md master + PAPERS.md

---

## INHYEOK HWANG

**Senior Researcher** · Electrical Control & Product Development (Junior PM)
**Email**: dlsgur5560@gmail.com
**GitHub**: github.com/hwanginhyeok
**Portfolio**: hwanginhyeok.github.io/portfolio

---

## SUMMARY

Reliability engineer with a graduate background in **Reliability-Based Design Optimization (RBDO)** and **Prognostics & Health Management (PHM)** of electric motors. Designed and executed accelerated life tests (ALT), built multi-sensor failure monitoring systems, and published peer-reviewed work on fault diagnosis and lifetime prediction (IEEE TIM · Solar Energy · J. Power Electronics, 2024).

In industry, built four test benches from scratch, led DFMEA-based root cause analysis on production issues, and managed APQP quality gates through first-article shipment of **16 units** of an agricultural autonomous vehicle system.

**Core competencies**: ALT design · DFMEA/RCA · Multi-sensor PHM · Reliability data analysis · Cross-functional FA coordination

---

## EXPERIENCE

### GINT Corp. — Electrical Control R&D + Product Development (Junior PM, concurrent)
**Senior Researcher** · Jan 2025 – Present

**GT-SS500: 48V Electric Autonomous Speed Sprayer — Full Lifecycle**
- Led APQP Phase 2–3 from algorithm development through first-article shipment (16 units)
- Completed **DFMEA #201/#210 Step 1–7** (AIAG-VDA format); identified 5 high-priority action points (AP=H)
- **Root cause analysis — 4 field issues**:
  - MCB contact carbonization (#204): confirmed electrolytic corrosion mechanism → redesigned to IEC 60947-2 spec
  - Control-mode state machine bug (#79): eliminated undefined state transitions → zero unintended drive incidents in validation
  - Pump freeze failure: identified O-ring dimensional non-conformance → redesigned + re-qualified
  - GND bounce noise: mapped to DFMEA, applied shielding/grounding countermeasure
- **Designed and built 4 test systems from zero**: dynamometer torque-control (nonlinearity 0.008%), fan bench (+57% airflow validated), pump bench, bumper safety rig (stop distance 0.082 m · peak current 308 A)
- Managed **BOM of 132 items**; identified 23 items with insufficient stock ahead of production
- Tracked 37+ field issues; personally resolved 14 electrical-control items + 27 NCRs

**CAN Distributed Control — GT-SS500**
- Designed 5-node CAN topology (VCU ↔ dual drive MC ↔ fan ESC ↔ pump DRV ↔ BMS); authored 4 DBC files
- Detected **4 breaking changes** through DBC version comparison before integration
- Standardized 3-pass CAN consistency checklist protocol

---

### GINT Corp. — Electrical Control R&D
**Junior Researcher** · Feb 2023 – Dec 2024

**EOP 400W: Automotive BLDC Motor Control (Government R&D Project)**
- **SVPWM/DPWM switching strategy**: reduced FET temperature 1–6°C, input power 1–3.8% (validated on 2,932 data points)
- **Cryogenic start test**: demonstrated cold-start time reduction from 300 s → 100 s at −40°C
- **CAN Sleep/Wakeup**: implemented quiescent-current-compliant bus management (5 revision cycles)
- **Built dynamometer torque-control system** achieving 0.008% nonlinearity; presented at internal seminar
- **2 patent filings** (see Patents section)

---

## EDUCATION

### Konkuk University — M.S. in Mechanical Design (RBDO Lab)
**Mar 2021 – Feb 2023** · GPA: 3.77/4.5 · Advisor: Prof. Namsu Kim

**Thesis**: *Fault Diagnosis Simulation of Interior Permanent Magnet Synchronous Motor using Electromagnetic Analysis* (49 pp., RISS: f678963f23f2e418ffe0bdc3ef48d419)

- Built IPMSM digital twin: flux-state variable model + Ansys Maxwell FEM → Co-simulation with MATLAB/Simulink inverter model
- Validated against experimental data across multiple operating conditions (Sim2Real precursor approach)
- Participated in government-funded PHM SoC development project (MOTIE, Apr 2021 – Oct 2022)

### Konkuk University — B.S. in Mechanical Design
**Mar 2015 – Feb 2021** · GPA: 3.24/4.5

---

## PUBLICATIONS & PATENTS

### Peer-Reviewed Journals (3, co-authored)

| Year | Journal | Title (abbreviated) | Role |
|------|---------|--------------------|----|
| 2024 | **IEEE Transactions on Instrumentation and Measurement**, Vol. 73 | Bond-wire fault detection in IGBT via inverter output parameters | 3rd author |
| 2024 | **Solar Energy** (Elsevier), Vol. 276, Art. 112645 | Lifetime prediction of PV polymers under varying environments via damage summation | 4th author |
| 2024 | **Journal of Power Electronics**, Vol. 24(5), pp. 822–831 | Failure mode identification in IPMSM under ALT via dual sensor architecture | 6th author |

### Conference Presentations (4)

| Year | Conference | Topic | Award |
|------|-----------|-------|-------|
| 2023 | PHM Society Asia-Pacific | 120 kW IPMSM system-level fault diagnosis | — |
| 2022 | PCIM Asia | IGBT IPM quasi-DC power cycling | — |
| 2022 | Korean Society for Reliability (KSR) | Predictive maintenance for EV drivetrain | **Best Paper Award** |
| 2021 | Korean PHM Society | IGBT open-fault diagnosis via system-level measurements | **Best Poster Award** |

### Patents (2)

- **Patent #1** — Motor initial position detection · Co-inventor · KR App. PN231067KR (2023) · Detection time: 1.0 s → **0.56 s**
- **Patent #2** — Cryogenic motor starting method · Development contributor (experimental validation) · −40°C start time: 300 s → **100 s** · *Application No. [TODO: confirm via KIPRIS — search "저온 기동 황인혁"]*

---

## SKILLS

### Reliability Engineering
- Accelerated Life Testing (ALT) design · Weibull analysis · Damage summation (Miner's Rule) · DFMEA / PFMEA (AIAG-VDA) · FMEA RPN prioritization · IQC/OQC inspection guide · APQP Phase 1–5

### Failure Analysis & Diagnosis
- Root Cause Analysis (RCA) · Multi-sensor PHM (current · temperature · vibration · displacement) · Anomaly detection · Bond-wire fault diagnosis (IEEE TIM 2024) · IPMSM fault mode identification

### Test & Measurement
- Dynamometer torque-control system (0.008% nonlinearity) · Fan / pump / impact test benches (self-built) · CANoe · Vector VN1600 · NI DAQ (NI-9215) · Oscilloscope · SPICE

### Simulation & Modeling
- Ansys Maxwell (FEM / Transient) · MATLAB / Simulink · Co-simulation · HIL (VCU + dynamometer bench)

### Embedded & Motor Control
- STM32 · NXP MC9S12ZVMC · CAN / CAN-FD (5-node topology, DBC authoring) · FOC · SVPWM / DPWM · Sensorless IPMSM (BEMF observer, initial position detection)

### Software
- Python · C / C++ · Git · Linux

### Languages
- Korean: Native
- English: Professional working proficiency

---

## AWARDS

| Year | Award | Issuing Body |
|------|-------|-------------|
| 2022 | **Best Paper Award** | Korean Society for Reliability (KSR) |
| 2021 | **Best Poster Award** | Korean PHM Society |

---

## TODO (fill before submission)

- [ ] Patent #2 application number — 사용자 KIPRIS 확인 완료, 번호 전달 필요
- [x] 포트폴리오 사이트 배포 확인 — hwanginhyeok.github.io/portfolio 접속 확인 (2026-05-04) *단, 현재 구버전. V3 배포 필요*
