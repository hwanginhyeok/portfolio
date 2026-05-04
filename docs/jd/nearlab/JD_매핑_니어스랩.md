# 니어스랩(Nearthlab) JD 매핑 — 황인혁

> 작성일: 2026-05-04
> JD 출처: nearlab-interview-prep.md §3 기술 스택 (채용공고 기준) + §8 면접 포인트 (잠정 base)
> **실제 JD URL/텍스트 확보 시 §1 교체 필요** — 문서 말미 확인 요청 참조

---

## §1. 니어스랩 JD 요건 정리 (잠정)

> 대상 직군: **임베디드 엔지니어 / 전장 개발** (추정)
> 근거: 채용공고 기준 기술 스택 + 기술 면접 질문 패턴 역산

### 필수 (Must-have)

| # | 요건 | 핵심 키워드 |
|---|------|-----------|
| R1 | C/C++ 임베디드 개발 — ARM Cortex 계열 | MCU FW, 드라이버 |
| R2 | RTOS 기반 실시간 제어 | FreeRTOS / NuttX, ISR, 인터럽트 |
| R3 | 분산 통신 프로토콜 설계·구현 | CAN / MAVLink / DroneCAN |
| R4 | 상태머신 설계 + 안전 로직 (Failsafe) | Arming/Disarming, 비정상 전환 처리 |
| R5 | 멀티센서 통합 + 실시간 데이터 처리 | IMU, GPS, 전류/온도 센서 |
| R6 | 모터 드라이버 / ESC 제어 | BLDC, FOC, PWM |
| R7 | 임베디드 Linux + ARM 플랫폼 | Embedded Linux, 드라이버 작성 |

### 우대 (Nice-to-have)

| # | 요건 | 핵심 키워드 |
|---|------|-----------|
| P1 | ROS / ROS2 개발 경험 | uORB, 노드, 토픽, 실시간성 |
| P2 | PX4 / ArduPilot 소스코드 이해 | commander 상태머신, ekf2 |
| P3 | 자세 제어 이론 (Cascaded PID) | mc_att_control, mc_rate_control |
| P4 | 엣지 AI / 온디바이스 추론 | TensorRT, ONNX, Jetson |
| P5 | 전력 시스템 / BMS 인터페이스 | SOC 추정, 보호 로직, 셀 불균형 |
| P6 | APQP / 양산 프로세스 경험 | DFMEA, BOM, 초도품 검사 |
| P7 | PHM / 고장 진단 알고리즘 | 이상 탐지, 센서 퓨전 기반 진단 |

---

## §2. 자산 매트릭스 — JD 요건 × 황인혁 케이스

> ⭐ 핵심 증거 (수치 + 산출물 있음) | ✓ 보조 증거 | — 해당 없음

| JD 요건 | 매핑 케이스 | 핵심 수치 | 산출물 위치 |
|---------|-----------|---------|-----------|
| **R1** C/C++ ARM | EOP-400W SVPWM, STM32 RTOS 루프 | 2,932 data points 검증 | `src/pages/cases/eop-400w/` |
| **R1** | SS500 VCU FW (STM32, NXP MC9S12ZVMC) | 3모드 상태머신 + 5절 CAN 루프 | `src/pages/cases/ss500-state-machine/` |
| **R2** RTOS | ⭐ STM32 1ms ISR 기반 제어 루프 | PID 제어 레이트 1kHz | `cases/D3_state_machine_case.md` |
| **R2** | FreeRTOS 태스크 구조 (VCU: 제어/통신/진단 분리) | — | `src/pages/cases/ss500-state-machine/` |
| **R3** CAN | ⭐ CAN 5노드 분산 제어 설계 (VCU↔MC×2↔팬ESC↔펌프DRV↔BMS) | DBC 4개, 브레이킹 체인지 4건 사전 탐지 | `src/pages/cases/ss500-state-machine/` |
| **R3** | MAVLink 비교 학습 — DroneCAN과 1:1 구조 대응 이해 | — | `nearlab-interview-prep.md §14` |
| **R4** 상태머신 | ⭐ SS500 상태머신 안전 버그 발굴 + 수정 | CTRL=NONE 상태 삭제, Init 강제 삽입. 실차 6개 전환 검증 | `cases/D3_state_machine_case.md` |
| **R4** | PX4 commander 구조 독학 비교 분석 | arming_state / navigation_state 전환 패턴 매핑 | `nearlab-interview-prep.md §12` |
| **R5** 멀티센서 | ⭐ BMS 정합성 검증 — 셀별 전압 CAN 로그 추출 vs 기대값 비교 | SOC 162.4% 오버플로우 발굴, 3차 ROM 업데이트 감시 | `cases/D2_battery_compatibility_case.md` |
| **R5** | 다이나모미터 NI-DAQ 기반 토크·속도·전류 실시간 계측 | 비선형성 0.008% 달성 | `src/pages/cases/test-engineering/` |
| **R6** 모터 | ⭐ SVPWM/DPWM 절환 알고리즘 — FET 온도↓, 효율↑ | FET 온도 1~6°C↓, 입력전력 1~3.8%↓ | `src/pages/cases/eop-400w/` |
| **R6** | FOC sensorless BLDC — BEMF 관측기 + 초기위치 특허 | -40°C 기동 300s→100s, 초기위치 1.0s→0.56s | `src/pages/cases/patent/` |
| **R7** Embedded Linux | ROS2 SLAM 자율주행 사이드 프로젝트 | — | (진행 중, 사이트 미노출) |
| **P1** ROS/ROS2 | ✓ 자율주행 사이드 (ROS2 nav2, STM32 CAN 브릿지) | PX4 SITL 독학 검증 | `nearlab-interview-prep.md §11` |
| **P2** PX4 | ✓ PX4 아키텍처 독학 — uORB/commander/ekf2/mc_att_control 분석 | SS500 VCU와 모듈 1:1 대응 | `nearlab-interview-prep.md §12` |
| **P3** 자세제어 | ✓ Cascaded PID 이론 학습 — Roll/Pitch/Yaw 능동 제어 vs 지상 차량 | SS500 PID(속도·전류) Outer/Inner 구조와 동일 패턴 | `nearlab-interview-prep.md §13` |
| **P4** Edge AI | — | Claude Code 기반 AI 워크플로우 경험 있으나 추론 최적화(TRT/ONNX)는 미경험 | 갭 §4 참조 |
| **P5** BMS | ⭐ BMS 업체 ROM 3차 검증 + 보호 로직 강제 유발 테스트 | SOC 오버플로우 발굴 | `cases/D2_battery_compatibility_case.md` |
| **P6** APQP | ⭐ APQP Phase 2~3 주니어 PM 수행 | 16units 초도 출하, BOM 132개, NCR 27건 | `cases/E01_pm_experience.md` |
| **P6** DFMEA | DFMEA #201/#210 Step 1~7, AP=H 5건 도출 | — | `resume_en.md` |
| **P7** PHM | ⭐ 대학원 IPMSM 고장 진단 시뮬레이션 (Ansys Maxwell + MATLAB) | IEEE TIM 2024, J.Power Electronics 2024 공저 | `resume_en.md` §PUBLICATIONS |

### 요건별 커버리지 요약

| 구분 | ⭐ 핵심 | ✓ 보조 | — 갭 |
|------|:------:|:-----:|:---:|
| 필수 R1~R7 | 5 | 2 | 0 |
| 우대 P1~P7 | 3 | 3 | 1 (P4) |

---

## §3. 핵심 메시지 3개

> B2-01 USAGE_STRATEGY.md §2와 정합: 니어스랩 특화 버전

### M-N1 (필수 역량 직전이) — 드론 비행 컨트롤러 = SS500 VCU의 3D 버전

"SS500은 STM32 VCU + CAN 5노드 + 3모드 상태머신 + 48V 전력 시스템으로 구성된 Physical AI 플랫폼입니다. 니어스랩의 드론 FCU는 같은 서브시스템을 3D 공간으로 확장한 것 — 구조가 동일합니다. 지상에서 양산까지 증명한 아키텍처를 공중에서 재현합니다."

**증거**: C/C++ STM32, CAN 5노드, 상태머신 안전 버그 수정, RTOS 1ms ISR 루프

### M-N2 (차별화) — 데이터 없으면 안 넘어가는 엔지니어

"BMS 업체가 '완료'라고 했을 때도 CAN 로그에서 셀별 전압을 직접 추출해서 SOC 162.4% 오버플로우를 잡았습니다. SVPWM 개선 효과도 2,932 포인트를 직접 수집해서 검증했습니다. 드론에서 비행 데이터가 말하는 것만 믿겠습니다."

**증거**: BMS 로그 검증(C02), SVPWM 2,932 data points(N01/N02), 다이나모 0.008%(I-E04)

### M-N3 (양산 경험) — 드론 스타트업에서 드문 조합: APQP × 임베디드

"SS500 APQP Phase 2~3, DFMEA #201/#210, BOM 132개 관리를 주니어 PM으로 직접 수행했습니다. 니어스랩이 IPO를 앞두고 방산 납품 양산화를 구축하는 지금, 임베디드 개발과 양산 프로세스를 동시에 이해하는 사람은 희귀합니다."

**증거**: E01 PM 경험(APQP), resume_en.md §EXPERIENCE (16units, 132 BOM, 27 NCR)

---

## §4. 갭 분석

| JD 요건 | 갭 | 보완 계획 |
|---------|---|---------|
| **P4** 엣지 AI — TensorRT/ONNX | 추론 최적화 실경험 없음. AI 워크플로우(Claude Code)와 분야가 다름 | 입사 전: NVIDIA Jetson 오픈소스 예제 실행 + YOLOv8 TensorRT 변환 1회 수행. 면접에서 솔직히 밝히고 학습 로드맵 제시 |
| **R7** Embedded Linux 드라이버 | ROS2 레벨 경험, 커널 레벨 드라이버 작성 미경험 | Linux Device Driver 3rd Ed. + i2c_dev 드라이버 예제. 면접에서 "ROS2 노드 레벨까지는 경험, 드라이버는 배우는 중" |
| **P2** PX4 소스코드 기여 | 독학 분석 수준, 실기여 없음 | SITL에서 commander 상태 전환 로그 직접 추출 → 포트폴리오 체크리스트 항목 (면접 전 완료 목표) |
| **R3** MAVLink 실구현 | 이론 이해 수준 | DroneCAN 구조 비교로 전환 비용이 낮음을 면접에서 논리적으로 설명 |

### 면접 갭 대응 전략

- **솔직 + 구체적 학습 계획**: "없습니다, 하지만 ___로 접근하겠습니다" 패턴
- **이전 도메인 전이 논리**: "SS500에서 ___ 했고, 드론에서 이것이 ___로 매핑된다"
- **입사 후 기여 가능 시점 명시**: "1개월 내 PX4 SITL, 3개월 내 실기체 적용"

---

## §5. 면접 답변 템플릿

### 자기소개 (2분) — 니어스랩 JD 직접 매핑 버전

> §9 기존 답변 기반 재작성. JD R1~R7 + M-N1~N3 연결.

"저는 GINT에서 3년간 임베디드 전력제어 엔지니어로 일하면서, STM32 기반 RTOS 시스템부터 CAN 분산 제어, FOC 모터 알고리즘까지 직접 설계하고 양산까지 끌고 갔습니다.

대표 제품 GT-SS500은 48V 460Ah LiFePO4 배터리로 구동되는 농업용 전동 자율주행 방제 로봇입니다. CAN 5노드 분산 제어, STM32 VCU, 3모드 상태머신, RTK-GPS 자율주행 — 니어스랩 드론 FCU의 서브시스템을 지상에서 구현한 제품입니다.

구체적으로는 — CAN DBC 4개를 직접 작성해서 통합 전 4개의 브레이킹 체인지를 사전 탐지했고, 상태머신 안전 버그를 발굴해서 CTRL=NONE 상태를 삭제하고 모든 전환에 Init을 강제 삽입했습니다. SVPWM 절환 효과를 2,932 데이터 포인트로 검증했고, BMS 업체가 완료라고 해도 CAN 로그를 직접 파서 SOC 오버플로우를 잡았습니다.

대학원에서는 IPMSM 고장 진단 — Ansys Maxwell FEM + MATLAB 코-시뮬레이션으로 센서 퓨전 기반 PHM을 연구해서 IEEE TIM 2024를 포함한 3편에 공저했습니다.

니어스랩에서 하고 싶은 건 이 역량의 공중 버전입니다. STM32 CAN 상태머신 → PX4 commander, 분산 제어 → DroneCAN, BMS 검증 원칙 → 드론 전력 시스템. 도메인은 바뀌지만 구조는 같습니다."

---

### "왜 니어스랩인가" (60초)

"드론 스타트업 중 실제 물건이 격추되고 있는 곳은 많지 않습니다. KAiDEN이 통신 차단 환경에서 비전만으로 150km/h 표적을 격추한다는 게 — 비전 AI 성능이 무기 수준으로 검증됐다는 의미입니다.

저는 지상에서 Physical AI 제품을 양산까지 만들어봤는데, 그 경험을 가장 극한 조건에서 검증할 수 있는 곳이 여기라고 생각했습니다.

그리고 IPO를 앞두고 방산 납품 양산화를 구축해야 하는 지금, APQP와 임베디드를 동시에 이해하는 사람이 필요한 타이밍이라고 봅니다. 제가 그 교차점에 있습니다."

---

## 미해결 질문 (PM 보고)

1. **실제 JD 텍스트 보유 여부** — 현 문서는 채용공고 기준 기술 스택(§3)과 면접 질문 패턴(§8) 역산으로 작성. 실제 JD URL 또는 원문이 있으면 §1 교체하면 정밀도 대폭 향상됨. 특히 "우대" 항목 순서가 바뀔 수 있음.
2. **지원 직군 확정** — 임베디드 엔지니어 / 전장 엔지니어 / AI 엔지니어 중 실제 지원 포지션에 따라 §2 매트릭스 가중치가 달라짐. AI 직군이면 P4(엣지 AI) 갭이 필수 항목이 됨.
3. **PX4 SITL 실행 여부** — 면접 체크리스트 §10 항목. SITL 스크린샷이 있으면 §5 자기소개에 "이미 시작했습니다" 한 줄 추가로 드론 경험 갭을 공격적으로 닫을 수 있음.

---

> USAGE_STRATEGY.md §2 정합 상태: M-N1 = "역량 직전이" / M-N2 = "검증 문화" / M-N3 = "양산 임베디드"
> → B2-01 메시지 확정 시 우선순위 동기화 필요
