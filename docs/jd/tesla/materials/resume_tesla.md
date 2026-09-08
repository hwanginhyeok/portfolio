# 이력서 — 황인혁 · Tesla Field Support Engineer 지원용

> 작성: 2026-09-06 (초안)
> 파생 원본: `docs/blocks/05-extra/RESUME.md` (마스터). **사실은 마스터에서만 고친다.**
> 이 문서가 바꾼 것: ① Summary를 진단·현장지원 톤으로 교체 ② §프로젝트를
> EOP(자동차) → 시험기획 → GT-SS500 순으로 재배치 ③ 로보틱스·AI 워크플로우 축소
> ④ 진단/PHM 근거를 앞으로 끌어올림

---

## 1. 인적사항

| 항목 | 내용 |
|------|------|
| 이름 | 황인혁 (Inhyeok Hwang) |
| 현재 소속 | GINT(긴트) · 전력제어개발팀 선임연구원 + 제품개발팀 주니어 PM 겸임 |
| 이메일 | `[TODO: 사용자 채움]` |
| GitHub | github.com/hwanginhyeok |
| 포트폴리오 | hwanginhyeok.github.io/portfolio |

---

## 2. 요약

전동화 파워트레인의 **고장을 데이터로 진단하고, 현장 실패를 설계로 되돌리는** 일을
석사 연구부터 현업까지 이어온 엔지니어.

IPMSM 고장진단 시뮬레이션으로 석사 학위를 받았고, 공저 논문(IEEE TIM 2024)에서 인버터 출력
파라미터만으로 IGBT 본드와이어 열화를 온라인 검출하는 방법을 다뤘다. 현업에서는 12V 자동차용
전동오일펌프(EOP 400W)와 48V 자율주행 플랫폼(GT-SS500)을 개발하며 **CAN 5노드 분산 제어**를
설계하고 DBC 4종을 직접 관리했다. 현장에서 올라온 고장 4건을 근본원인까지 몰고 가 DFMEA에
반영했고, 필요한 계측 환경이 없을 때는 직접 만들었다 — 다이나모미터 토크제어 시스템
비선형성 **0.008%**.

**Keywords**: Fault Diagnosis · PHM · CAN / CAN-FD · Root Cause Analysis · Test Rig Design ·
BLDC / IPMSM Motor Control · Field Issue → Design Feedback

---

## 3. 경력

### GINT(긴트) — 전력제어개발팀 선임연구원 + 제품개발팀 주니어 PM 겸임
**2025.01 ~ 현재**

- **현장 이슈 RCA 4건** — MCB 전해부식(#204) / LCD 상태머신 오동작(#79) / 펌프 동파 오링 /
  GND 노이즈. 증상 재현 → 근본원인 특정 → DFMEA 반영까지 수행
- **이슈 트래킹** — 37건+ 중 전력제어 직접 담당 14건, **NCR 27건** 처리
- **CAN 5노드 분산 제어 설계** — VCU ↔ 구동×2 ↔ 팬 ↔ 펌프 ↔ BMS.
  DBC 4종 직접 작성/관리, **BREAKING CHANGE 4건 사전 검출**
- **시험체계 단독 구축** — 다이나모미터 / 펌프 벤치 / 팬 벤치 / 범퍼 시험대 직접 설계
- **양산 이관** — APQP Phase 2~3, DFMEA #201/#210 Step 1~7(AP=H 5건), BOM 132 항목
  (재고 미확보 23건 사전 식별), 초도 16pcs + 대차 2 + Spare 2 생산계획
- **대외 대응** — 혁신제품 실사 4/9 대응(#205), 농진원 대응

### GINT(긴트) — 전력제어개발팀 주임연구원
**2023.02 ~ 2024.12**

- **EOP 400W 국책과제 완료** — 12V 400W 자동차용 전동오일펌프 BLDC 모터제어 (NXP MC9S12ZVMC)
- **SVPWM/DPWM 절환 기법** — FET 온도 1~6°C 저감, 입력전력 1~3.8% 감소.
  **2,932 데이터 포인트**로 검증
- **CAN Sleep/Wakeup 구현** — 암전류 요구 충족, 5차례 rev 개선
- **극저온 기동 실험** — -40°C 환경에서 기동시간 300초 → **100초** 단축 실증
- **다이나모미터 토크제어 시스템 직접 구축** — 비선형성 **0.008%** (사내 세미나 발표)
- 특허 출원 2건 (§6)

---

## 4. 핵심 프로젝트

### 4.1 EOP 400W — 12V 자동차용 전동오일펌프 (2023~2024, 국책과제)

| 영역 | 정량 성과 |
|------|----------|
| SVPWM/DPWM 절환 | FET 온도 1~6°C ↓, 입력전력 1~3.8% ↓ (2,932 데이터 포인트) |
| 극저온 기동 | -40°C 300초 → 100초 |
| 저전력 통신 | CAN Sleep/Wakeup 5차 rev, 암전류 요구 충족 |
| 시험 인프라 | 다이나모미터 토크제어 비선형성 0.008% |
| 센서리스 | BEMF 관측기 · 초기 위치 추정 (요구 1.0초 → 0.56초, 특허 #1) |

### 4.2 시험 기획 7종 — "장비가 없으면 만든다"

| # | 시험 | 정량 결과 |
|---|------|----------|
| 1 | 다이나모미터 토크제어 (EOP) | 비선형성 **0.008%** |
| 2 | -40°C 극저온 챔버 (EOP) | 기동 300초 → **100초** |
| 3 | PWM 온도/효율 비교 (EOP) | **2,932 데이터 포인트** |
| 4 | 범퍼 시험대 (SS500) | 정지거리 **0.082m** · 피크 **308A** · 정착시간 467ms |
| 5 | 팬 벤치 (SS500) | 풍속 7.9 → **12.4 m/s** (+57%) |
| 6 | 펌프 벤치 (SS500) | 3시료 선형관계 규명 → **명판 스펙 허위 검증** |
| 7 | CAN 정합성 체크리스트 | 3차 반복 검증 프로토콜 표준화 |

### 4.3 GT-SS500 — 48V 전동 자율주행 Speed Sprayer (2025.01 ~ 2026 양산)

STM32 기반 VCU + 5노드 CAN 분산 제어 + RC/LCD/자율주행 3모드 상태머신 + LiFePO4 BMS +
AWS OTA. 알고리즘 → DFMEA → BOM → 양산 출하까지 풀사이클 수행.

| 영역 | 정량 성과 |
|------|----------|
| 안전 검증 | 범퍼 정지거리 0.082m · 피크 308A · 정착시간 467ms (3km/h 주행) |
| CAN 통신 | DBC 4종 직접 작성 · BREAKING CHANGE 4건 사전 검출 |
| 현장 이슈 | 37건+ 트래킹, 직접 담당 14건, NCR 27건 |
| 양산 준비 | APQP Phase 2~3, DFMEA Step 1~7 (AP=H 5건), BOM 132 항목 |

---

## 5. 학력

**건국대학교 대학원 · 기계설계학과 · 석사** (2021.03 ~ 2023.02, 학위수여 2023-03-22)
- 신뢰성 기반 설계 최적화(RBDO) Lab · 지도교수 김남수
- 학위논문: *전자기 해석을 이용한 매입형 영구자석 동기 전동기의 고장 진단 시뮬레이션에 관한 연구* (49p)
- 참여 과제: 전동화 차량 구동 전기모터 상태 진단을 위한 PHM SoC 개발 (산업통상자원부, 2021.04~2022.10)
- 전공 27학점 · 3.77/4.5

**건국대학교 · 기계공학부 기계설계학과 · 학사** (2015 ~ 2021) — 전공 79학점 · 3.24/4.5

---

## 6. 논문 / 특허 / 수상

**저널 (공저 3편)**
- **IEEE Transactions on Instrumentation and Measurement** (2024) Vol.73, Art.10726721 —
  *Programmable Online Bond-Wire Fault Detection and Location Method for IGBT Using Inverter
  Output Parameters* · DOI 10.1109/TIM.2024.3472910
- **Solar Energy** (Elsevier, 2024) Vol.276, Art.112645 — PV 모듈 폴리머 수명 예측 (4저자)
- **Journal of Power Electronics** (2024) 24(5), 822-831 — *Identification of failure modes in
  IPMSM under accelerated life test based on dual sensor architecture*

**학회 / 수상**
- 한국PHM학회 2021 **우수포스터상** — 시스템 수준 측정값을 이용한 IGBT 개방 고장 진단
- 한국신뢰성학회 2022 **최우수발표 논문상** — 전동화 차량 구동시스템 예방정비 기술
- PCIM Asia 2022 · PHM Society Asia-Pacific 2023 (120kW IPMSM 시스템 수준 고장진단)

**특허 2건**
- 모터 초기 위치 검출 (공동 발명자) · 출원 PN231067KR (2023) · 검출 1.0초 → 0.56초
- 저온 모터 회전자 탈조 방지 · 등록 10-2654562 (2024.04.01) · 출원인 ㈜긴트
  — **실험적 검증 담당**(발명자 명단 미포함) · -40°C 300초 → 100초 실증

---

## 7. 보유 기술

| 분류 | 내용 |
|------|------|
| **진단 / PHM** | Multi-sensor PHM · Anomaly Detection · phase current/온도/축변위/진동 융합 · 인버터 게이트 신호 진단 · IGBT 본드와이어 lift-off 검출 |
| **통신 / 시스템** | CAN · CAN-FD · CAN Sleep/Wakeup · **DBC 작성/관리(4종)** · BusLoad 분석 · 5노드 분산 제어 토폴로지 |
| **시험 / 계측** | 다이나모미터 토크제어 · 팬/펌프/범퍼 벤치 자가 설계 · CANoe · Vector VN1600 · SPICE · Oscilloscope · DAQ(NI-9215) |
| **모터제어 / 전력전자** | BLDC · IPMSM · PMSM · FOC · SVPWM/DPWM 절환 · 센서리스 초기위치 추정 · BEMF observer · 극저온 기동 |
| **임베디드** | STM32 · NXP MC9S12ZVMC · Infineon TC23x · RTOS · 상태머신(RC/LCD/ADT 3모드) · FW 코드리뷰 |
| **해석 / 시뮬레이션** | Ansys Maxwell (FEM, Transient) · MATLAB/Simulink · Co-simulation · MIL/SIL/HIL 개념 |
| **품질 / 문서** | APQP Phase 1~5 · DFMEA/PFMEA · DRBFM · Boundary Diagram · BOM 관리 · IQC/OQC 검사 가이드 · WBS · NCR |
| **SW** | Python · C/C++ · Git · Linux |

---

## 8. 어학

| 항목 | 내용 |
|------|------|
| 영어 | 업무 대화 가능 (Working Proficiency) |
| TOEIC | 920점 *(2021~2022 응시 · **유효기간 만료** — 재응시 예정)* |
| TOEIC Speaking | 140점 (Level 6 IH) *(**유효기간 만료** — 재응시 예정)* |

> JD가 영어 유창성을 필수로 요구한다. 제출 전 재응시 여부를 결정할 것 (`../APPLY.md §4`).

---

## 9. 이 이력서가 의도적으로 뺀 것

- **로보틱스(ROS2/Gazebo/nav2)** — 학습 단계라 이 포지션에서는 신호가 약하다
- **AI 워크플로우 / LLM 오케스트레이션** — 강점이지만 이 JD와 축이 다르다.
  면접에서 "동시 다발 업무 관리" 질문이 나오면 그때 꺼낸다
- **UDS · CATIA · OEM 진단장비** — 근거가 없으므로 적지 않는다 (`../JD_매핑 §4`)
