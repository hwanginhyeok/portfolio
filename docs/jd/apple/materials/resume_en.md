# Resume — Inhyeok Hwang

> Target: Apple Korea · Reliability Engineer, Core Technology Operations
> Version: 2026-05-15 v5 (팩트 리스크 3개 수정 + APQP bullet 분리 + Skills APQP 정렬 + TOEIC 표기 개선)
> Source SSOT: `docs/blocks/05-extra/RESUME.md`

---

## INHYEOK HWANG

**Senior Researcher** · Electrical Control & Product Development (Junior PM, concurrent)
**Email**: dlsgur5560@gmail.com
**GitHub**: github.com/hwanginhyeok
**Portfolio**: hwanginhyeok.github.io/portfolio

---

## SUMMARY

Mechanical-design M.S. from Konkuk University's Reliability-Based Design Optimization (RBDO) Lab, with thesis research on IPMSM digital-twin fault diagnosis (Co-simulation of Ansys Maxwell FEM and a MATLAB/Simulink inverter model). Three peer-reviewed journal publications as co-author (IEEE Transactions on Instrumentation and Measurement · Solar Energy · Journal of Power Electronics, all 2024) and two Korean patents.

Three years of industrial product development at GINT Corp., leading the GT-SS500 48 V autonomous speed sprayer through APQP Phase 2–3 (primary) with Phase 1/4/5 supporting scope across the full program lifecycle. Authored DFMEA #201/#210 Step 1–7 with five high-priority risks closed before ramp, applied ISO 25119 AgPL d assessment to safety functions, closed four root-cause analyses on real field issues, and tracked 27 NCRs through closure. Built four custom test rigs in-house (dynamometer, fan bench, pump bench, bumper safety rig) and coordinated a structured 48 V BMS supplier quality review.

---

## EXPERIENCE

### GINT Corp. — Electrical Control R&D + Product Development (Junior PM, concurrent)
**Senior Researcher** · Jan 2025 – Present

**GT-SS500: 48 V Electric Autonomous Speed Sprayer — Full Lifecycle**
- Led **APQP Phase 2–3** (primary scope: design validation, DFMEA, IQC/OQC criteria, NCR closed-loop) for GT-SS500, coordinating six cross-functional teams from algorithm development to a first-article production plan of **16 units + 2 transport carts + 2 spares**
- Supporting scope across the full program lifecycle: **Phase 1** (MTBF/B10 reliability goals, VOC, special-characteristics identification), **Phase 4** (PPAP ROM sign-off), **Phase 5** (60+ field-issue database; cascading-failure analysis identified six failure chains across alpha-prototype issues)
- Authored **DFMEA #201 and #210 (Step 1–7)** and applied **ISO 25119 AgPL** risk assessment — over-charge protection rated **AgPL d** (highest category for agricultural machinery functional safety); five high-priority (AP=H) risks resolved before production ramp
- Closed **four root-cause analyses** on real field issues:
  - **MCB contact carbonization (#204)**: confirmed electrolytic corrosion mechanism; breaker replaced with IEC 60947-2-grade part and re-qualified
  - **LCD-mode state-machine bug (#79)**: undefined transitions removed; verified through validation runs
  - **Pump O-ring freeze failure**: O-ring redesigned and re-qualified for low-temperature operation
  - **Ground-bounce noise on the control bus**: countermeasure mapped back into the DFMEA
- Operated **27 NCRs** through to closure as a closed-loop corrective action process (Failure → Reporting → Analysis → Corrective Action → System update); defined IQC/OQC acceptance criteria with **Cpk ≥ 1.33 targets** for key characteristics
- Managed a structured quality review when our 48 V BMS supplier visited our facility — 6-item agenda covering FW version verification, SOC anomaly root-cause, and relay-behavior confirmation
- Currently mentoring a **junior engineer** in embedded control-system design — CAN protocol architecture, state-machine safety design, and DFMEA methodology
- Built **four custom test rigs** in-house: **dynamometer torque control (nonlinearity 0.008%)**, **fan bench (airflow 7.9 → 12.4 m/s, +57%)**, **pump bench** (three-sample linearity characterization, nameplate-spec falsification), **bumper safety rig** (stop distance 0.082 m, peak current 308 A, settling time 467 ms at 3 km/h)
- Designed a **5-node CAN distributed-control architecture** (VCU ↔ dual drive MC ↔ fan ESC ↔ pump DRV ↔ BMS); authored four DBC files; detected four breaking changes before integration through a three-pass consistency protocol
- **BOM management** across 132 items; 23 items with insufficient stock surfaced ahead of ramp
- Personally resolved **14 field issues** in the electrical-control scope (subset of the Phase 5 database above); represented program at Innovation-Product on-site audit (4 of 9 items handled)

---

### GINT Corp. — Electrical Control R&D
**Junior Researcher** · Feb 2023 – Dec 2024

**EOP 400 W: Automotive BLDC Motor Control (Government R&D Project, NXP MC9S12ZVMC)**
- Co-authored a programmable online bond-wire fault detection and location method for IGBT modules using inverter output parameters — published in *IEEE Transactions on Instrumentation and Measurement* (2024, third author, DOI 10.1109/TIM.2024.3472910)
- **SVPWM/DPWM switching strategy**: FET temperature reduced 1–6 °C, input power reduced 1–3.8 % (validated across 2,932 data points)
- **Cryogenic start test**: cold-start time reduced from 300 s to 100 s at −40 °C
- **CAN Sleep/Wakeup**: quiescent-current-compliant bus management (five revision cycles)
- Built a **dynamometer torque-control system** with nonlinearity 0.008 %; presented at internal seminar
- Two Korean patent contributions (see Patents)

---

## EDUCATION

### Konkuk University — M.S. in Mechanical Design (RBDO Lab)
**Mar 2021 – Feb 2023** · 27 major credits · Major GPA 3.77/4.5 · Advisor: Prof. Namsu Kim

**Thesis**: *Fault Diagnosis Simulation of Interior Permanent Magnet Synchronous Motor using Electromagnetic Analysis* (49 pp., RISS f678963f23f2e418ffe0bdc3ef48d419)

- Built an IPMSM digital twin: flux-state variable model + Ansys Maxwell FEM, co-simulated with a MATLAB/Simulink inverter model and validated against experimental data across multiple operating conditions
- Participated in a government-funded PHM SoC development project (MOTIE, 2021–2022); contributed to multi-sensor fault diagnosis and remaining-useful-life estimation work for the IPMSM drivetrain
- Observed an IPMSM accelerated-life-test program (eccentricity-fault characterization with load-factor stress and FTA-driven test design); the resulting work was later published as *Identification of failure modes in IPMSM under accelerated life test based on dual sensor architecture* (J. Power Electronics, 2024, sixth author)

### Konkuk University — B.S. in Mechanical Design
**Mar 2015 – Feb 2021** · 79 major credits · Major GPA 3.24/4.5

---

## PUBLICATIONS & PATENTS

### Peer-Reviewed Journals (3, co-authored)

| Year | Journal | Title | Author position |
|------|---------|-------|-----------------|
| 2024 | **IEEE Trans. on Instrumentation and Measurement**, Vol. 73, Art. 10726721 | Programmable Online Bond-Wire Fault Detection and Location Method for IGBT Using Inverter Output Parameters (DOI 10.1109/TIM.2024.3472910) | 3rd author |
| 2024 | **Solar Energy** (Elsevier), Vol. 276, Art. 112645 | Lifetime prediction of polymeric materials in PV module under continuously varying environments based on damage summation approach (DOI 10.1016/j.solener.2024.112645) | 4th author |
| 2024 | **Journal of Power Electronics**, Vol. 24(5), pp. 822–831 | Identification of failure modes in IPMSM under accelerated life test based on dual sensor architecture (DOI 10.1007/s43236-024-00810-8) | 6th author |

### Conference Presentations (4)

| Year | Conference | Topic | Award |
|------|------------|-------|-------|
| 2023 | PHM Society Asia-Pacific Conference (DOI 10.36001/phmap.2023.v4i1.3780) | 120 kW IPMSM system-level fault diagnosis | — |
| 2022 | PCIM Asia | IGBT IPM power cycling — bond-wire / solder degradation | — |
| 2022 | Korean Society for Reliability — Spring Conference | Predictive maintenance for EV drivetrain | **Best Paper Award** |
| 2021 | Korean PHM Society Annual Conference | IGBT open-fault diagnosis via system-level measurements | **Best Poster Award** |

### Patents (2 — honest disclosure)

- **Patent #1** — Motor initial position detection (co-inventor) · KR App. PN231067KR (2023, filed via The Wave IP) · detection time 1.0 s → **0.56 s** · prior-art screen of 1 paper and 10 patents
- **Patent #2** — *Method for preventing step-out of rotor of motor in low temperature and apparatus thereof* · KR App. **10-2023-0175484** (filed 2023-12-06) · Reg. **10-2654562** (granted 2024-04-01) · Applicant: GINT Inc. · IPC H02P 29/032 · **Development contributor** (experimental validation of −40 °C cold start, 300 s → 100 s; not on the inventor list — inventors of record: Je Jeong-mun, Kim Eun-tae)

---

## SKILLS

### Motor Control & Power Electronics
- BLDC · IPMSM · PMSM control · FOC · SVPWM/DPWM switching · sensorless initial-position estimation · BEMF observer · cryogenic start
- Inverter gate-signal diagnosis · IGBT bond-wire lift-off detection (IEEE TIM 2024)

### Embedded & Firmware
- STM32 · NXP MC9S12ZVMC · Infineon TC23x · RTOS · multi-mode state machines (RC / LCD / autonomous) · motor-controller firmware code review

### Communication & System Design
- CAN · CAN-FD · CAN Sleep/Wakeup · DBC authoring (4 files) · CAN BusLoad analysis · 5-node distributed control topology
- Reading-level familiarity with ISO 13849 and functional-safety mapping

### Simulation & Analysis
- Ansys Maxwell (FEM, transient) · MATLAB/Simulink · Co-simulation (Sim2Real precursor) · MIL/SIL/HIL concepts

### Test & Measurement
- Dynamometer torque control · self-built fan / pump / bumper benches · CANoe · Vector VN1600 · SPICE · oscilloscope · NI DAQ (NI-9215)

### PHM & Signal Processing
- **Government-funded PHM SoC development** (MOTIE, 2021–2022): physics-based co-simulation (Ansys Maxwell FEM + MATLAB/Simulink) + **SVM fault classification** on phase-current signatures — demagnetization & winding-fault diagnosis for 120 kW IPMSM
- Multi-sensor fusion (phase current · temperature · shaft displacement · vibration) · anomaly detection · field usage model → ALT stress-factor mapping

### Quality & PM Artifacts
- APQP Phase 2–3 (primary) + Phase 1/4/5 supporting · DFMEA / PFMEA · DRBFM · boundary diagram · BOM management · IQC/OQC inspection guides with **Cpk ≥ 1.33 acceptance criteria** · WBS · NCR closed-loop handling (FRACAS-equivalent)

### Software & AI Workflow
- Python · C/C++ · Git · Linux
- Three-tier LLM routing (Opus / GLM / Ollama) · Claude Code · MCP · Obsidian + Dataview
- PM-orchestrator workflow across 8 internal projects · 13-skill automation library (`hih-skills`) · cron-driven overnight execution
- Learning / applying: PyTorch · LangChain · Docker

### Languages
- Korean: native
- English: professional working proficiency
- TOEIC 920 / TOEIC Speaking Lv. 6 (IH 140)

---

## AWARDS

| Year | Award | Issuing Body |
|------|-------|--------------|
| 2022 | **Best Paper Award** (Spring Conference) — Predictive maintenance for EV drivetrain | Korean Society for Reliability (KSR) |
| 2021 | **Best Poster Award** — IGBT open-fault diagnosis via system-level measurements | Korean PHM Society |

## INTERNAL PRESENTATIONS

- EOP 400 W dynamometer torque-control system (nonlinearity 0.008 %) — GINT Corp. internal seminar
