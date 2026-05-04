# Resume — Inhyeok Hwang

> Target: Apple Korea · Reliability Engineer, Core Technology Operations
> Version: 2026-05-04 v2 (Apple tailored — standard mapping applied)
> Source SSOT: RESUME.md master + PAPERS.md + reliability_competency.md §3

---

## INHYEOK HWANG

**Senior Researcher** · Electrical Control & Product Development (Junior PM)
**Email**: dlsgur5560@gmail.com
**GitHub**: github.com/hwanginhyeok
**Portfolio**: hwanginhyeok.github.io/portfolio

---

## SUMMARY

Reliability engineer with a graduate background in **Reliability-Based Design Optimization (RBDO)** and **Prognostics & Health Management (PHM)** of electric motors. Conducted Power Cycling Tests (PCT per JESD47/JEP122) on IGBT modules, witnessed the full ALT design-test-redesign cycle for IPMSM fault characterization, and applied damage summation (Miner's Rule) to lifetime prediction under varying environments (IEEE TIM · Solar Energy · J. Power Electronics, 2024).

In industry, built four test rigs aligned with MIL-STD-810 / IEC 60068-2 environmental test methods, authored 5 DFMEAs per AIAG-VDA 2019, closed 4 RCAs using 5 Why and Ishikawa diagrams, and operated an NCR tracking system (27 items) as FRACAS-equivalent closed-loop corrective action — all through APQP Phase 2–3 leading to first-article shipment of **16 units**.

**Core competencies**: ALT design · PCT (JESD47/JEP122) · DFMEA/RCA (AIAG-VDA 2019) · FRACAS-equivalent NCR closed-loop · Environmental testing (MIL-STD-810 / IEC 60068-2 / IEC 60529) · Six Sigma DMAIC / Cpk/Ppk · Damage Summation (Miner's Rule) · PHM/RUL multi-sensor fault diagnosis

**Bridge**: "I bridge academic rigor and production reality — the profile Apple mass production teams need most."

---

## EXPERIENCE

### GINT Corp. — Electrical Control R&D + Product Development (Junior PM, concurrent)
**Senior Researcher** · Jan 2025 – Present

**GT-SS500: 48V Electric Autonomous Speed Sprayer — Full Lifecycle**
- Led APQP Phase 2–3 from algorithm development through first-article shipment (16 units); bridged design validation and production reality across 6 cross-functional teams
- Authored **5 DFMEAs per AIAG-VDA 2019** (DFMEA #201/#210 Step 1–7); identified 5 high-priority action points (AP=H), all resolved before production ramp
- **Led 4 RCAs using 5 Why and Ishikawa diagrams** — all resolved before production:
  - MCB contact carbonization (#204): confirmed electrolytic corrosion mechanism → redesigned to IEC 60947-2 spec
  - Control-mode state machine bug (#79): eliminated undefined state transitions → zero unintended drive incidents in validation
  - Pump freeze failure: identified O-ring dimensional non-conformance → redesigned + re-qualified
  - GND bounce noise: mapped to DFMEA, applied shielding/grounding countermeasure
- **Operated NCR tracking (27 items) as part of FRACAS-equivalent closed-loop corrective action** (Failure → Reporting → Analysis → Corrective Action → System update)
- **Designed and operated 4 test rigs aligned with MIL-STD-810 / IEC 60068-2 environmental test methods** — built from zero: dynamometer torque-control (nonlinearity 0.008%), fan bench (+57% airflow validated), pump bench, bumper safety rig (stop distance 0.082 m · peak current 308 A)
- **Designed sealed CAN connectors meeting IEC 60529 IP67 requirements** for EOP 400W program
- **Defined IQC/OQC inspection criteria consistent with Six Sigma DMAIC; monitored process capability indices (Cpk/Ppk)** for supplier qualification
- Managed **BOM of 132 items**; identified 23 items with insufficient stock ahead of production
- Tracked 37+ field issues; personally resolved 14 electrical-control items

**CAN Distributed Control — GT-SS500**
- Designed 5-node CAN topology (VCU ↔ dual drive MC ↔ fan ESC ↔ pump DRV ↔ BMS); authored 4 DBC files
- Detected **4 breaking changes** through DBC version comparison before integration
- Standardized 3-pass CAN consistency checklist protocol

---

### GINT Corp. — Electrical Control R&D
**Junior Researcher** · Feb 2023 – Dec 2024

**EOP 400W: Automotive BLDC Motor Control (Government R&D Project)**
- **Conducted PCT per JESD47/JEP122 on IGBT modules; identified bond-wire lift-off failure mode** (P-01 IEEE TIM 2024, DOI 10.1109/TIM.2024.3472910)
- **SVPWM/DPWM switching strategy**: reduced FET temperature 1–6°C, input power 1–3.8% (validated on 2,932 data points)
- **Cryogenic start test**: demonstrated cold-start time reduction from 300 s → 100 s at −40°C
- **CAN Sleep/Wakeup**: implemented quiescent-current-compliant bus management (5 revision cycles)
- **Built dynamometer torque-control system** achieving 0.008% nonlinearity; presented at internal seminar
- **2 patent filings** (see Patents section)

---

## EDUCATION

### Konkuk University — M.S. in Mechanical Design (RBDO Lab)
**Mar 2021 – Feb 2023** · 27 major credits · Major GPA 3.77/4.5 · Advisor: Prof. Namsu Kim

**Thesis**: *Fault Diagnosis Simulation of Interior Permanent Magnet Synchronous Motor using Electromagnetic Analysis* (49 pp., RISS: f678963f23f2e418ffe0bdc3ef48d419)

- Built IPMSM digital twin: flux-state variable model + Ansys Maxwell FEM → Co-simulation with MATLAB/Simulink inverter model
- Validated against experimental data across multiple operating conditions (Sim2Real precursor approach)
- Participated in government-funded PHM SoC development project (MOTIE, Apr 2021 – Oct 2022); conducted RUL estimation for IPMSM drivetrain fault diagnosis with multi-sensor signals
- **Witnessed full ALT design-test-redesign cycle** (IPMSM eccentricity fault characterization; load factor application → FTA → destruct-limit-adjacent test); observed dual-sensor architecture in operation (P-05 J. Power Electron. 2024)

### Konkuk University — B.S. in Mechanical Design
**Mar 2015 – Feb 2021** · 79 major credits · Major GPA 3.24/4.5

---

## PUBLICATIONS & PATENTS

### Peer-Reviewed Journals (3, co-authored)

| Year | Journal | Title (abbreviated) | Role |
|------|---------|--------------------|----|
| 2024 | **IEEE Transactions on Instrumentation and Measurement**, Vol. 73 | Bond-wire fault detection in IGBT via inverter output parameters | 3rd author |
| 2024 | **Solar Energy** (Elsevier), Vol. 276, Art. 112645 | Lifetime prediction of PV polymers under varying environments via damage summation (Miner's Rule) | 4th author |
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
- **Patent #2** — *Method for preventing step-out of rotor of motor in low temperature and apparatus thereof* · KR App. **10-2023-0175484** (filed 2023-12-06) · Reg. **10-2654562** (granted 2024-04-01) · Applicant: GINT Inc. · IPC H02P 29/032 · Development contributor (experimental validation; not on inventor list — inventors: Je Jeong-mun, Kim Eun-tae) · −40°C start time: 300 s → **100 s**

---

## SKILLS

### Reliability Engineering
- ALT design (witnessed/observed full cycle: IPMSM eccentricity characterization, P-05)
- PCT (Power Cycling Test) per JESD47 / JEP122 (directly conducted: IGBT bond-wire lift-off, P-01)
- DFMEA per AIAG-VDA 2019 · FTA · RCA with 5 Why and Ishikawa diagrams
- FRACAS-equivalent NCR closed-loop (27 items tracked)
- Environmental testing aligned with MIL-STD-810 / IEC 60068-2 / IEC 60529 IP67
- Six Sigma DMAIC · Cpk/Ppk-based IQC/OQC
- Damage Summation (Miner's Rule) · Weibull lifetime estimation
- PHM/RUL — multi-sensor fault diagnosis (IPMSM SoC, MOTIE project 2021–2022)
- APQP Phase 2–3 (full cycle to mass production first article)

### Failure Analysis & Diagnosis
- Root Cause Analysis (RCA) with 5 Why and Ishikawa · FRACAS closed-loop
- Multi-sensor PHM (current · temperature · vibration · displacement)
- Bond-wire fault diagnosis (IEEE TIM 2024) · IPMSM fault mode identification

### Test & Measurement
- Dynamometer torque-control system (0.008% nonlinearity) · Fan / pump / impact test benches (self-built, MIL-STD-810 / IEC 60068-2 aligned)
- CANoe · Vector VN1600 · NI DAQ (NI-9215) · Oscilloscope · SPICE

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
