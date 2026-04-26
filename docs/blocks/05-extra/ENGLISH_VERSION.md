# B5-03 영문 버전 가이드 — ENGLISH_VERSION

> 최종 수정: 2026-04-26 (B5-03 신규 작성)
> 위치: `docs/blocks/05-extra/ENGLISH_VERSION.md`
> 입력 SSOT:
> - `docs/포트폴리오/EXPERT_REVIEW_20260426.md` — 영문 어휘 권장 (Sim2Real / Co-simulation / Robotics Systems Integration / Physical AI / 0→1 Builder 등)
> - `docs/blocks/02-usage/USAGE_STRATEGY.md` — 메시지 후보 8개 (MC-A ~ MC-H)
> - `docs/포트폴리오/CONTENT_V2.md` §4 — 한국어 사실 SSOT
> - `docs/포트폴리오/PAPERS.md` — 논문 영문 제목 (이미 확정)
> - `src/components/Hero.astro`, `Timeline.astro`, `src/pages/cases/*/index.astro` — 한국어 헤드라인
> 운영 원칙:
> - 가이드 본문은 한국어, 어휘집은 한/영 양면, 영문 예시(Summary/Headline)는 영문 그대로
> - **ATS(Applicant Tracking System) 친화** — 약어는 full name 병기 (예: `PHM (Prognostics and Health Management)`)
> - 영문은 한국어 SSOT의 사실을 1:1로 반영하되, 도메인 어휘는 EXPERT_REVIEW 권장에 맞춰 리프레임
> - 본 문서는 **번역 결정**만 담는다. 사실 변경은 CONTENT_V2/PAPERS에서만.

---

## §0. 본 문서의 역할

영문 포트폴리오 사이트 / 영문 CV / GitHub 영문 README / 영문 LinkedIn 프로필을 작성할 때의 **표준 어휘집 + 구조 가이드**. 한국어 SSOT를 영문으로 변환할 때 표현이 케이스마다 달라지는 문제를 막는다.

흐름: 한국어 SSOT (CONTENT_V2/PAPERS) → §1 어휘 매핑 → §2 헤더 / §3 Summary / §4 케이스 톤 → 영문 사이트/CV/LinkedIn/GitHub.

**작성 원칙** (본 문서를 쓰는 방법):
1. §1 어휘집은 SSOT. 다른 채널에서 영문 표기가 흔들리면 §1로 돌아와 수정.
2. §3 Summary는 4종 모두 유지. 회사 JD에 따라 1개 선택해 미세 조정. **합치지 않는다.**
3. §4 케이스 영문 헤드라인은 한국어 h1이 SSOT. 한국어가 바뀌면 함께 수정.
4. §5 인용은 PAPERS.md가 SSOT. 본 §5에서 직접 수정하지 말 것.
5. **영문에서 새 수치를 만들지 않는다** (CONTENT_V2 §4에 없는 숫자는 영문에도 없다).
6. 약어 첫 등장 시 full name 병기 (ATS 자동 필터 누락 방지).

---

## §1. 영문 표기 표준 (Term Glossary)

> 한국어 → 영문 1:1 매핑. 한 번 쓴 영문 표기는 다른 채널에서도 동일하게 쓴다.

### 1.1 모터·전력 제어 (Motor & Power Control)

| 한국어 | 영문 표준 (1차) | 영문 동의어/약어 | 비고 |
|---|---|---|---|
| 모터 제어 | Motor Control | — | 일반어 |
| 인버터 | Inverter | — | EV 도메인 핵심 |
| 영구자석 동기 전동기 (IPMSM) | Interior Permanent Magnet Synchronous Motor (IPMSM) | IPMSM | 첫 등장 시 full name 병기 |
| 표면부착형 동기 전동기 | Surface-Mounted PMSM (SPMSM) | SPMSM | — |
| 센서리스 BLDC | Sensorless BLDC | Sensorless Brushless DC Motor | — |
| BLDC 초기 위치 검출 | Sensorless BLDC Initial Rotor Position Detection | Initial Position Estimation | 특허 #1 정본 영문 |
| 극저온 기동 | Cryogenic Cold Start | Low-Temperature Startup, Sub-Zero Startup | 특허 #2 정본 영문 |
| 다이나모미터 토크 제어 | Dynamometer Torque Control | Dyno Torque Control | 사내 세미나 발표 |
| FOC (자속기준제어) | Field-Oriented Control (FOC) | Vector Control | — |
| SVPWM | Space-Vector PWM (SVPWM) | — | 절환은 SVPWM/DPWM Modulation Switching |
| DPWM | Discontinuous PWM (DPWM) | — | — |
| EEMF/BEMF 옵저버 | Extended/Back-EMF Observer | — | 센서리스 추정기 |
| 전동 오일펌프 | Electric Oil Pump (EOP) | — | EOP 케이스 정본 |
| 전력제어 개발자 | Power Control Engineer | Motor Control Engineer | 직무 표기 |

### 1.2 시스템 통합·임베디드 (Systems Integration & Embedded)

| 한국어 | 영문 표준 (1차) | 영문 동의어/약어 | 비고 |
|---|---|---|---|
| 분산 임베디드 시스템 통합 | Distributed Embedded Systems Integration | — | EXPERT_REVIEW 권장어 |
| CAN 5노드 분산 제어 | 5-Node CAN-Bus Distributed Control | — | 핵심 시스템 표기 |
| VCU (차량 제어 장치) | Vehicle Control Unit (VCU) | — | — |
| BMS (배터리 관리 시스템) | Battery Management System (BMS) | — | — |
| OTA (무선 업데이트) | Over-the-Air (OTA) Update | — | AWS OTA로 표기 시 "AWS-Based OTA Pipeline" |
| 상태머신 | State Machine | Finite State Machine (FSM) | 첫 등장 시 FSM 병기 |
| RC/LCD/ADT 3모드 제어권 | 3-Mode Operator Authority FSM (RC / LCD / Autonomous) | — | SS500 케이스 정본 |
| 페일세이프 핸드셰이크 | Fail-Safe Handshake | — | 자율주행 PC 협업 |
| 실외 자율 모빌리티 플랫폼 | Outdoor Autonomous Mobility Platform | Outdoor Autonomous Vehicle | "농업용 Speed Sprayer"의 시스템 통합 리프레임 |
| 자율주행 방제기 | Autonomous Speed Sprayer | — | 도메인 명시가 필요할 때 |

### 1.3 시뮬레이션·연구 (Simulation & Research)

| 한국어 | 영문 표준 (1차) | 영문 동의어/약어 | 비고 |
|---|---|---|---|
| 디지털 트윈 | Digital Twin | Physics-Informed Digital Twin | EXPERT_REVIEW 권장어 |
| 시뮬-실험 루프 | Sim-to-Real (Sim2Real) Loop | Sim2Real Pipeline | EXPERT_REVIEW 권장어 |
| Co-simulation | Co-Simulation | — | 표준어, 한국어 그대로도 통용 |
| 전자기 해석 (FEM) | Electromagnetic Finite Element Analysis (FEA) | Ansys Maxwell FEA | T-01 학위논문 |
| MATLAB/Simulink 모델링 | MATLAB/Simulink Modeling | — | — |
| 모터 파라미터 LUT | Motor Parameter Look-Up Table (LUT) | — | T-01 핵심 산출물 |
| 시스템 수준 시뮬레이션 | System-Level Simulation | — | P-03 핵심어 |
| HIL 벤치 | Hardware-in-the-Loop (HIL) Bench | HIL Test Bench | 다이나모를 HIL로 재포지셔닝 |
| MIL/SIL/HIL | Model-in-the-Loop / Software-in-the-Loop / Hardware-in-the-Loop | — | 검증 단계 표준어 |

### 1.4 신뢰성·진단 (Reliability & PHM)

| 한국어 | 영문 표준 (1차) | 영문 동의어/약어 | 비고 |
|---|---|---|---|
| PHM (예지 보전·건전성 관리) | Prognostics and Health Management (PHM) | — | 첫 등장 시 full name |
| 고장 진단 | Fault Diagnosis | Anomaly Detection | T-01/P-01/P-03 |
| 가속수명시험 | Accelerated Life Test (ALT) | — | P-04/P-05 |
| 본드와이어 결함 | Bond-Wire Fault | Bond-Wire Lift-Off | P-01 IEEE TIM 정본 |
| 다중 센서 PHM | Multi-Sensor PHM | Multi-Signal PHM Architecture | P-05 |
| 신뢰성 기반 설계 최적화 | Reliability-Based Design Optimization (RBDO) | — | RBDO Lab 영문 표기 |

### 1.5 양산·품질 시스템 (Productization & Quality System)

| 한국어 | 영문 표준 (1차) | 영문 동의어/약어 | 비고 |
|---|---|---|---|
| APQP (선행 제품 품질 계획) | Advanced Product Quality Planning (APQP) | — | AIAG 표준 |
| DFMEA | Design Failure Mode and Effects Analysis (DFMEA) | — | AIAG-VDA |
| PFMEA | Process Failure Mode and Effects Analysis (PFMEA) | — | — |
| Boundary Diagram | Boundary Diagram | System Boundary Diagram | DFMEA 산출물 |
| BOM (자재명세서) | Bill of Materials (BOM) | — | — |
| IQC / OQC | Incoming / Outgoing Quality Control (IQC/OQC) | — | — |
| NCR (부적합 보고서) | Non-Conformance Report (NCR) | — | 현장 이슈 분류 정본 |
| Concession (특채) | Concession | Deviation Permit | 양산 임시 승인 |
| 설계 변경 지시 | Engineering Change Order (ECO) | Engineering Change Notice (ECN) | — |
| 풀사이클 양산 | End-to-End Productization | Full-Cycle Productization, Concept-to-Production | EXPERT_REVIEW 권장어 |
| 양산 출하 | Mass Production Release | Series Production Launch | — |
| 품질 게이트 | Quality Gate | Phase Gate | APQP Phase별 게이트 |

### 1.6 프로젝트 관리·프로세스 (Project Management & Process)

| 한국어 | 영문 표준 (1차) | 영문 동의어/약어 | 비고 |
|---|---|---|---|
| 기획→설계→증명→분석 | Plan → Design → Prove → Analyze | Specify → Design → Verify → Analyze | 시험 4단계 정본 |
| 시험 기획 | Test Plan / Test Engineering | Test Specification | — |
| 시험체계 | Test Engineering Framework | In-House Test Infrastructure | "장비가 없으면 만든다" |
| 현장 이슈 | Field Issues | Field Findings | 37건+ 정본 |
| 근본원인 분석 (RCA) | Root Cause Analysis (RCA) | — | — |
| Cross-functional 협업 | Cross-Functional Collaboration | — | 6개팀 협업 |
| 주니어 PM | Junior Project Manager | Associate PM | (스타트업에서는 사용 비권장) |

### 1.7 헤더용 키워드 (Headline Keywords)

> EXPERT_REVIEW 권장어. 도메인별 헤드라인 §2에서 사용.

`Physical AI` · `Sim-to-Real (Sim2Real)` · `Robotics Systems Integration` · `0→1 Builder` · `Full-Stack Hardware Engineer` · `AI-Augmented Engineer` · `Field-Hardened Engineer` · `Concept-to-Production Engineer`

### 1.8 약어 풀세트 (ATS 친화 — 첫 등장 시 full name 병기)

```
APQP (Advanced Product Quality Planning)
ASIL (Automotive Safety Integrity Level)
BLDC (Brushless DC Motor)
BMS (Battery Management System)
BOM (Bill of Materials)
CAN (Controller Area Network)
DFMEA (Design Failure Mode and Effects Analysis)
ECO (Engineering Change Order)
EOP (Electric Oil Pump)
FEA (Finite Element Analysis)
FOC (Field-Oriented Control)
FSM (Finite State Machine)
HIL (Hardware-in-the-Loop)
IPMSM (Interior Permanent Magnet Synchronous Motor)
NCR (Non-Conformance Report)
OTA (Over-the-Air)
PFMEA (Process Failure Mode and Effects Analysis)
PHM (Prognostics and Health Management)
PMSM (Permanent Magnet Synchronous Motor)
RBDO (Reliability-Based Design Optimization)
RCA (Root Cause Analysis)
RTK GNSS (Real-Time Kinematic Global Navigation Satellite System)
SVPWM (Space-Vector Pulse-Width Modulation)
VCU (Vehicle Control Unit)
```

---

## §2. 영문 헤더·슬로건 후보

> Hero 영문 헤드라인 / 영문 CV Headline / 영문 LinkedIn Headline 공통.
> 도메인별 1순위 후보를 두고, B2 §2.2 메시지 확정에 맞춰 1개 선택.

### 2.1 도메인 무관 — 일반 후보

| # | 영문 헤드라인 | 한국어 매칭 | 비고 |
|---|---|---|---|
| H-1 | **Solving Physical-World Problems with Data** | "분야를 막론하고 — 문제가 있으면 해결한다" | 현재 사이트 어조 그대로 영문화 |
| H-2 | **From Motor Control to End-to-End Productization** | "모터제어부터 양산 출하까지" | 풀사이클 강조 |
| H-3 | **Plan · Design · Prove · Analyze — End-to-End** | "기획·설계·증명·분석을 끝까지" | 프로세스 강조 |

### 2.2 Physical AI / 로보틱스 도메인 후보

| # | 영문 헤드라인 | 비고 |
|---|---|---|
| H-4 | **Sim-to-Real Engineer for Physical Systems** | EXPERT_REVIEW 1순위 권장 |
| H-5 | **From Motor Control to Robotics Systems Integration** | EXPERT_REVIEW 권장어 그대로 |
| H-6 | **Physical AI Builder — Co-Simulation, Multi-Sensor PHM, Distributed Embedded** | 자산 3건 동시 호출 |
| H-7 | **Outdoor Autonomous Mobility Engineer (RTK GNSS · CAN · Sim2Real)** | SS500을 자율 모빌리티로 리프레임 |

### 2.3 제품 개발 PM 도메인 후보

| # | 영문 헤드라인 | 비고 |
|---|---|---|
| H-8 | **End-to-End Product Engineer — APQP / DFMEA / Concept-to-Production** | 대기업 PM 트랙 |
| H-9 | **Concept-to-Production PM with Hands-On Power Control Background** | PM 일색 회피, HW 깊이 보전 |
| H-10 | **Mass-Production-Hardened Engineering Lead** | 양산 검증 강조 |

### 2.4 스타트업 / 0→1 도메인 후보

| # | 영문 헤드라인 | 비고 |
|---|---|---|
| H-11 | **Full-Stack Hardware · 0→1 Builder · AI-Augmented** | EXPERT_REVIEW 권장어 정본 |
| H-12 | **Single-Person Hardware Stack — Power Control to Mass Production** | 단독 주도 강조 |
| H-13 | **Hardware Founder-Engineer — Build, Test, Ship** | 창업가 톤 |

> 권장 순서: B2에서 도메인이 정해지면 위 그룹에서 1개 → 한 번 정한 헤드라인은 사이트/CV/LinkedIn 모두 동일하게 사용.

---

## §3. 영문 이력서 마스터 — Summary 4옵션

> 영문 CV 최상단 Summary 섹션 (5~7줄). 도메인별 4종 마스터를 두고 회사 JD에 맞춰 1개 선택 후 미세 조정.
> **수치는 한국어 SSOT(CONTENT_V2 §4)와 1:1 일치**. 영문에서 새 수치를 만들지 않는다.

### 3.1 옵션 A — 모터 제어 / 임베디드 R&D 트랙 (대기업 EV·인버터 메이커)

```
Power-Control Engineer with end-to-end experience from algorithm research to mass-
production release of a 48 V autonomous outdoor mobility platform (GT-SS500). Co-
authored an IEEE Transactions on Instrumentation and Measurement paper on bond-wire
fault diagnosis for IGBT inverters (DOI 10.1109/TIM.2024.3472910). Designed an SVPWM/
DPWM modulation-switching scheme on NXP MC9S12ZVMC for a 12 V / 400 W EOP, validated
across 2,932 operating points with 1–6 °C FET temperature reduction and 1.0–3.8 %
input-power savings. Built an in-house dynamometer torque-control system (0.008 %
non-linearity) and validated -40 °C cold start (300 s → 100 s). Co-inventor on one
Korean patent for sensorless BLDC initial-rotor-position detection.
```

### 3.2 옵션 B — 제품 개발 PM 트랙 (대기업 PM 트랙)

```
Concept-to-production engineer with hands-on power-control depth and full-cycle
project leadership of a 48 V autonomous Speed Sprayer (GT-SS500) — from algorithm
through APQP Phase 2–3, DFMEA #201/#210 Step 1–7 (5 high-AP findings), boundary
diagram and assembly redesign, BOM management of 132 line items, to mass-production
release of 16 + 4 units. Resolved 37+ field issues (14 owned directly), including
root-cause analysis of MCB electrolytic corrosion and re-design of solenoid O-ring
specifications. Coordinated 6 cross-functional teams and authored 7 in-house test
specifications (pump, fan, nozzle, spray, PID/PWM, track endurance, cold start).
```

### 3.3 옵션 C — Physical AI / Robotics 트랙

```
Physical-AI engineer trained in physics-informed motor digital twins (Ansys Maxwell
FEA + MATLAB/Simulink Co-Simulation) and multi-sensor PHM (phase current, temperature,
shaft displacement, vibration). M.S. thesis at Konkuk University RBDO Lab on IPMSM
fault diagnosis simulation. Integrated a distributed-embedded outdoor mobility
platform with 5-node CAN-bus, RTK GNSS, IMU and camera, plus a 3-mode operator-
authority FSM (RC / LCD / Autonomous) with fail-safe handshake to an external
autonomous-driving PC. Co-authored 5 peer-reviewed papers (IEEE TIM 2024, Solar
Energy 2024, J. Power Electron. 2024, PCIM Asia 2022, PHM Asia-Pacific 2023). Two
national-conference best-paper / best-poster awards.
```

### 3.4 옵션 D — Startup / 0→1 Builder 트랙

```
Full-stack hardware builder, 0 → 1 to mass production, AI-augmented. Solo-led the
power-control stack of GT-SS500: STM32-based VCU, 5-node CAN distributed control,
LiFePO4 BMS integration, AWS-based OTA, and integration with an external autonomous-
driving PC. Built every test bench from scratch (dynamometer 0.008 % non-linearity,
fan +57 % air-speed gain, pump linearity benchmark, bumper safety stop at 0.082 m
from 308 A peak). Designed an internal AI workflow: 13 modular skills, 3-tier LLM
routing (Opus / GLM / Ollama), an unattended overnight cron pipeline, and a unified
project-manager orchestrator across 8 active projects. Co-author on IEEE TIM 2024.
```

> **공통 ATS 친화 패턴**: 첫 등장 약어는 full name 병기, 수치는 단위 포함, 회사 JD 키워드(예: ASIL, ISO 26262, ROS2)가 있으면 본인 자산과 매칭되는 것만 추가.

### 3.5 모든 옵션 공통 — 헤드라인 한 줄 (Summary 위 1줄)

| 트랙 | 한 줄 헤드라인 (CV 최상단) |
|---|---|
| A | `Power-Control Engineer · IPMSM / BLDC / SVPWM · IEEE TIM Co-Author` |
| B | `Concept-to-Production PM · APQP · DFMEA · Hands-On Power Control` |
| C | `Sim-to-Real Engineer · Co-Simulation · Multi-Sensor PHM · Distributed Embedded` |
| D | `Full-Stack Hardware · 0 → 1 Builder · AI-Augmented` |

---

## §4. 케이스 페이지 영문 톤 가이드

> 4개 케이스 각각의 영문 헤드라인 + 1줄 설명. `src/pages/cases/*/index.astro`의 한국어 헤드라인을 1:1 영문화.

### 4.1 EOP 400W (`cases/eop-400w/`)

| 항목 | 한국어 (현재) | 영문 권장 |
|---|---|---|
| h1 헤드라인 | EOP 12V 400W — 모터제어 개발 | **EOP 12 V / 400 W — Motor Control Development** |
| 1줄 설명 | NXP MC9S12ZVMC 기반 자동차용 BLDC 모터 제어 | Automotive BLDC motor control on NXP MC9S12ZVMC: SVPWM/DPWM modulation switching, CAN sleep/wake-up, cryogenic cold start. |
| 섹션 1 | SVPWM 효율 최적화 | SVPWM Efficiency Optimization |
| 섹션 2 | CAN Sleep/Wakeup 구현 | CAN Sleep / Wake-Up Implementation |
| 섹션 3 | 극저온 기동 검증 (-40°C) | Cryogenic Cold-Start Validation (-40 °C) |
| 섹션 4 | 모터 초기위치 검출 — 직무발명 특허 | Sensorless BLDC Initial Rotor Position Detection — Employee Invention Patent |
| 섹션 5 | 다이나모미터 시스템 — 자체 구축 | In-House Dynamometer Torque-Control System (0.008 % non-linearity) |

### 4.2 SS500 State Machine (`cases/ss500-state-machine/`)

| 항목 | 한국어 (현재) | 영문 권장 |
|---|---|---|
| h1 헤드라인 | 48V 전동 자율주행 방제기 — 전력제어 개발 | **48 V Autonomous Outdoor Mobility Platform — Power Control & Systems Integration** |
| 부제 1줄 | (없음) | Distributed embedded systems integration: STM32 VCU, 5-node CAN, RTK GNSS / IMU / camera, AWS-based OTA, integration with an external autonomous-driving PC. |
| 섹션 0 | VCU 운전 상태머신 | VCU Operation Finite State Machine |
| 섹션 1 | 전력제어 핵심 알고리즘 | Power-Control Core Algorithms |
| 섹션 2 | 현장 이슈 해결 | Field Issue Resolution |
| 섹션 3 | 센서 구동 · 페리퍼럴 설정 · 물리값 스케일링 | Sensor Drivers, Peripheral Configuration, Physical-Value Scaling |
| 섹션 4 | 제품 테스트 → 이슈 발견 → 해결 → 협업 | Product Test → Issue Discovery → Resolution → Cross-Functional Coordination |
| 섹션 5 | 시험 기획 · 실시 · 결과 정리 | Test Planning, Execution, and Reporting |
| 섹션 6 | APQP 양산 체계 · 주니어 PM | APQP Productization System (Junior PM) |

### 4.3 Patent (`cases/patent/`)

| 항목 | 한국어 (현재) | 영문 권장 |
|---|---|---|
| h1 헤드라인 | 문제를 풀면 특허가 된다 | **From Solved Problems to Filed Patents** |
| 카드 #1 | 모터 초기 위치 검출 알고리즘 | Sensorless BLDC Initial Rotor Position Detection (Co-Inventor) |
| 카드 #2 | 극저온 기동 알고리즘 | Cryogenic Cold-Start Algorithm (Development Contribution) |
| Honest 메모 | 발명자 명단이 전부는 아니다 | "Inventorship is not the full story — what matters is who solved the problem." |

### 4.4 Test Engineering (`cases/test-engineering/`)

| 항목 | 한국어 (현재) | 영문 권장 |
|---|---|---|
| h1 헤드라인 | 확인하고 싶으면 장비를 만들어서라도 본다 | **If a Bench Doesn't Exist, Build It** |
| 부제 1줄 | (없음) | Plan → Design → Prove → Analyze. Seven in-house test rigs designed, built, and operated end-to-end. |
| 패턴 | 패턴 — 3년간의 진화 | Pattern — Three-Year Evolution from EOP Dynamometer to GT-SS500 Test Suite |

### 4.5 현장 이슈 분류 영문 표기 (홈 임팩트 섹션 / Track A)

> "현장 이슈 37건+" → 영문 분류는 양산 품질 표준어를 따른다.

| 한국어 | 영문 표준 |
|---|---|
| 현장 이슈 (총괄) | Field Issues / Field Findings |
| 부적합 (NCR) | Non-Conformance Report (NCR) |
| 특채 (Concession) | Concession / Deviation Permit |
| 설계 변경 (ECO) | Engineering Change Order (ECO) / Engineering Change Notice (ECN) |
| 양산 라인 정지 사례 | Line Stop / Line-Down Incident |
| Lessons Learned | Lessons Learned (PFMEA Knowledge Base) |

---

## §5. 논문·학회·특허 영문 표기

> PAPERS.md (영문 제목 SSOT) 그대로 인용. 본 §5는 인용 형식만 표준화한다.

### 5.1 학위논문 (M.S. Thesis)

```
Inhyeok Hwang. "Fault Diagnosis Simulation of Interior Permanent Magnet Synchronous
Motor using Electromagnetic Analysis." M.S. Thesis, Department of Mechanical Design
and Production Engineering, Konkuk University, Seoul, Korea, 2023.
Advisor: Prof. Namsu Kim (RBDO Lab).
```

> CV / LinkedIn Education 항목 권장 1줄: `M.S., Mechanical Design and Production Engineering, Konkuk University (2023). Advisor: Prof. Namsu Kim, RBDO Lab.`

### 5.2 저널 (Peer-Reviewed Journals) — IEEE 스타일

```
[J1] J. Oh, I. Kim, I. Hwang, B. Choi, and N. Kim, "Programmable Online Bond-Wire
     Fault Detection and Location Method for Insulated Gate Bipolar Transistor
     Using Inverter Output Parameters," IEEE Transactions on Instrumentation and
     Measurement, vol. 73, pp. 1–8, Art. no. 10726721, Oct. 2024.
     DOI: 10.1109/TIM.2024.3472910

[J2] S. Choi, W. Kwon, J. Oh, I. Hwang, J. Lee, J. Lee, G. Hong, J. Kim, D. Shim,
     and N. Kim, "Lifetime Prediction of Polymeric Materials in PV Module under
     Continuously Varying Environments Based on Damage Summation Approach,"
     Solar Energy, vol. 276, Art. no. 112645, Jul. 2024.
     DOI: 10.1016/j.solener.2024.112645

[J3] S. Choi, J. Oh, J. Lee, W. Kwon, J. Lee, I. Hwang, J. Park, and N. Kim,
     "Identification of Failure Modes in Interior Permanent Magnet Synchronous
     Motor under Accelerated Life Test Based on Dual Sensor Architecture,"
     Journal of Power Electronics, vol. 24, no. 5, pp. 822–831, May 2024.
     DOI: 10.1007/s43236-024-00810-8
```

### 5.3 학회 (Conference Proceedings)

```
[C1] J. Oh, I. Hwang, et al., "The Effect of Quasi-DC Power Cycling on Insulated
     Gate Bipolar Transistor Dual-In-Line Package Intelligent Power Module," in
     Proc. PCIM Asia 2022, Shanghai, China, Oct. 2022.

[C2] W. Kwon, J. Oh, I. Hwang, and N. Kim, "System-Level Simulation of 120 kW
     Interior Permanent Magnet Synchronous Motor Drive for Electric Vehicle
     Usage Under Various Types of Faults for Fault Diagnosis," in Proc. PHM
     Society Asia-Pacific Conference, vol. 4, no. 1, 2023.
     DOI: 10.36001/phmap.2023.v4i1.3780
```

### 5.4 한국 학회 (Korean Conferences) — 영문 인용

```
[K1] I. Hwang, "Fault Diagnosis of IGBT Open-Circuit Faults in a Motor Drive
     System Using System-Level Measurements," presented at the Annual Conference
     of the Korean Society of Prognostics and Health Management (PHM Korea),
     2021. Best Poster Award.

[K2] I. Hwang, "Development of Efficient Predictive-Maintenance Technology for
     Electrified-Vehicle Drive Systems," presented at the Spring Conference of
     the Korean Reliability Society, 2022. Best Presentation Award.

[K3] I. Hwang, "Modeling Analysis for Precise Simulation of an Interior
     Permanent Magnet Synchronous Motor for Electric Vehicles," presented at
     the Annual Conference of PHM Korea, 2022.
```

### 5.5 특허 (Patents)

```
[P1] I. Hwang et al., "Method for Detecting Initial Rotor Position of a Sensor-
     less BLDC Motor," Korean Patent Application PN231067KR, filed 2023.
     Co-inventor.

[P2] (Inventor list does not include applicant.) "Cryogenic Cold-Start Method
     for Brushless DC Motor." Development contribution: experimental validation
     in a sub-zero environmental chamber demonstrating start-up time reduction
     from 300 s to 100 s at -40 °C.
```

> P2의 "Inventorship is not the full story" 메모는 영문 CV의 Patents 섹션 하단에 1줄로 병기 권장.

---

## §6. 사이트 i18n 구현 옵션

> 영문 사이트를 어떻게 만들지 — 3가지 옵션 비교. B5-03 본 문서는 결정만 정리, 실제 구현은 별도 태스크.

### 6.1 3개 옵션 비교

| 옵션 | 방식 | 장점 | 단점 | 권장 |
|---|---|---|---|---|
| **A. 영문 페이지 신규** (`src/pages/en/...`) | 별도 영문 페이지 + KO/EN 토글 | Astro 정적 빌드와 잘 맞음 / 카피 자유도 / 의존성 0 | 카피 동기화 책임 사용자 / 페이지 수 2배 | **1순위** |
| **B. astro-i18n 라이브러리** | 모든 텍스트를 키-값 JSON 분리 | 동기화 명시적 / 다국어 확장성 | 마이그레이션 비용 큼 / **패키지 의존성 추가 → 사용자 승인 필요** (overnight.md) | 3개 언어 이상일 때만 |
| **C. 영문 CV PDF 다운로드만** | 사이트는 한국어 유지, About에 PDF 버튼 | 구현 비용 0 | 사이트 콘텐츠는 한국어 그대로 / GitHub README 별도 필요 | 임시 브리지 |

### 6.2 권장 단계 (B2 결과에 따라 조정)

| 단계 | 옵션 | 비고 |
|---|---|---|
| 1단계 (즉시) | C — 영문 CV PDF + 영문 GitHub README | 어차피 필요한 자산. 1~2일 |
| 2단계 (4주 내) | A — `src/pages/en/index.astro` + 영문 Hero + 영문 About | Hero/About만 영문화 → MVP |
| 3단계 (필요 시) | A 확장 — 영문 케이스 4개 | 옵션 A를 옵션 B로 갈아엎지 않는다 (의존성 추가는 마지막) |

---

## §7. 영문 LinkedIn 프로필 가이드

> LinkedIn은 ATS와 채용담당자 검색의 1차 진입점. 영문 헤드라인/About은 §2 권장 + §3 Summary와 1:1 매칭.

### 7.1 5개 섹션 매핑

| LinkedIn 섹션 | 본 문서 매칭 | 길이 가이드 |
|---|---|---|
| Headline | §2 헤드라인 1개 (선택한 도메인) | 220자 이내 |
| About | §3 Summary 4옵션 중 1개 (트랙 일치) | 600~1,000자 |
| Experience | §4 케이스 페이지 영문 톤 가이드 + 한국어 SSOT의 사실 | 회사별 3~5 bullet |
| Skills | §1 어휘집의 영문 표준어 | 30~50개 (ATS 검색 키워드) |
| Publications / Honors | §5 논문·학회·특허 영문 표기 | 그대로 인용 |

### 7.2 Headline 권장 패턴

```
{H-#} | {핵심 자산 1} | {핵심 자산 2} | {도메인 키워드}
```

예시 (Physical AI 트랙):
```
Sim-to-Real Engineer for Physical Systems | IPMSM Co-Simulation | Multi-Sensor
PHM | IEEE TIM Co-Author
```

예시 (스타트업 트랙):
```
Full-Stack Hardware · 0 → 1 Builder · AI-Augmented | STM32 VCU + 5-Node CAN
+ AWS OTA | Concept-to-Production
```

### 7.3 Skills 섹션 — ATS 검색 키워드 추천 (30개)

> §1 어휘집에서 도메인별로 추출. 모든 항목 영문 표준어로.

`Motor Control` · `FOC` · `SVPWM` · `Sensorless BLDC` · `IPMSM` · `Inverter Design` · `Power Electronics` · `Embedded C` · `NXP MC9S12` · `STM32` · `CAN-Bus` · `DBC` · `OTA Update` · `BMS` · `Distributed Embedded Systems` · `VCU` · `State Machine` · `APQP` · `DFMEA` · `PFMEA` · `BOM Management` · `Mass Production` · `Co-Simulation` · `Ansys Maxwell` · `MATLAB / Simulink` · `PHM` · `Multi-Sensor Fault Diagnosis` · `Sim-to-Real` · `Test Engineering` · `Cross-Functional Collaboration`

### 7.4 Experience 섹션 — Bullet 패턴

> 회사별 3~5 bullet. §3 Summary와 동일한 사실을 bullet 형태로 분해 (CONTENT_V2 §4 SSOT). 추가 작성 예시는 §3.1~3.4 Summary를 분해해 사용.

---

## §8. 우선 작업 순서 + 완료 게이트

### 8.1 P1 — 즉시 (1주 내)

| # | 작업 | 입력 |
|---|---|---|
| 1 | §3 Summary 4옵션 중 1개 확정 후 영문 CV 1p 최상단 배치 | B2 §2.2 M1 메시지와 매칭되는 트랙 (A/B/C/D) |
| 2 | §5 논문·특허 영문 인용 블록을 영문 CV에 그대로 복붙 | PAPERS.md 정본 |
| 3 | GitHub 영문 README 작성 (`~/.github/profile/README.md` 또는 메인 레포) | §3 Summary + §1.8 약어 + §5 논문 |
| 4 | 영문 LinkedIn Headline + About 1차 작성 | §7.2 + §3 Summary |

### 8.2 P2 — 4주 내

| # | 작업 | 입력 |
|---|---|---|
| 5 | §6 옵션 A 1단계 — `src/pages/en/index.astro` Hero + About 영문화 (MVP) | §2 헤드라인 + §3 Summary |
| 6 | `src/pages/en/cases/*` 4개 페이지 헤드라인 + 1줄 설명 우선 영문화 | §4 케이스 톤 가이드 |
| 7 | LinkedIn Skills 섹션 등록 | §7.3 |

### 8.3 P3 — 회사 지원이 시작되면

| # | 작업 |
|---|---|
| 8 | JD별 Summary 미세 조정 (§3 4옵션 베이스 + JD 키워드 매칭) |
| 9 | §4 케이스 페이지 본문을 한국어 SSOT 기반으로 풀 영문화 |
| 10 | §6 3단계 — 영문 케이스 4개 모두 풀 영문 본문 완료 |

### 8.4 완료 게이트 체크리스트

영문 자료 산출 전 확인:

- [ ] §1 어휘집을 한 번 통독, 한국어 → 영문 매핑 인지
- [ ] §2 헤드라인 후보 13개 중 도메인 그룹 1개 선택
- [ ] §3 Summary 4옵션 중 1개 확정 (트랙 일치)
- [ ] §4 케이스 4개의 영문 헤드라인 1줄씩 확정
- [ ] §5 논문·특허 인용 형식이 IEEE 스타일과 일치
- [ ] §6 i18n 옵션을 P1/P2/P3 단계와 매칭
- [ ] §7 LinkedIn 5개 섹션 매핑 표를 따라 Headline부터 작성

게이트 통과 후 → 실제 영문 자료(CV PDF / GitHub README / LinkedIn) 산출.
