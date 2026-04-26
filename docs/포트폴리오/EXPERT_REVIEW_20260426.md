# 전문가 리뷰 — 4개 도메인 갭 분석 (2026-04-26)

> 4개 도메인 시니어 채용 시각으로 포트폴리오 사이트 갭 분석.
> 위치: `docs/포트폴리오/EXPERT_REVIEW_20260426.md`
> 목적: B3 배치 / B4 디자인 / B5 부가 작업의 입력. 메시지·구조 결정의 근거.

---

## 종합 — 4개 도메인 공통 갭 패턴

| 도메인 | 메시지 평가 | 가장 큰 갭 |
|---|:---:|---|
| **Physical AI** | 6/10 | Sim2Real / 디지털트윈 / ROS2 어휘 부재 (Co-simulation 자산을 현대 어휘로 리프레임만 해도 즉효) |
| **로보틱스** | 5/10 | ROS2 + 인지 스택(SLAM/센서퓨전) + Functional Safety 인증 매핑 부재 |
| **제품 개발 PM** | 7/10 | APQP Phase별 RACI 표 + QCD(원가/일정) 정량 부재. PM 직무 언어로 미번역 |
| **스타트업** | 7/10 | 사업 임팩트(매출/출하/시간) 정량 부재. "Junior PM"이 초기멤버 기대와 충돌 |

### 공통 패턴 3가지

1. **표현/어휘 리프레임 (저비용 고효과)**
   - "모델→시뮬레이션→실험" → "Sim2Real precursor / Co-simulation"
   - "농업용 Speed Sprayer" → "실외 자율 모빌리티 (RTK GNSS+IMU+카메라+CAN 분산제어)"
   - "Junior PM" → "Full-stack Hardware · 0→1 Builder · AI-Augmented" (스타트업 향) / "APQP 풀사이클 PM" (대기업 향)

2. **정량 임팩트 추가**
   - **사업**: 매출 기여 / 출하대수 / 단가절감 ROI / 시간 단축
   - **제품**: APQP Phase RACI / QCD KPI / WBS 게이트차트 / DFMEA RPN before-after
   - **속도**: "X일 만에 PoC", "주 N시간 절약" 류 1인=N인 효과

3. **신규 케이스/섹션 권장**
   - **Physical AI**: `cases/autonomy-stack/` — ROS2 노드 그래프, Gazebo 시뮬, ADT PC 인터페이스
   - **로보틱스**: SS500을 "로봇 시스템 통합 케이스"로 리프레임 (인지 스택 협업 깊이 추가)
   - **제품 개발**: APQP Phase × 본인 RACI 매트릭스 1장
   - **스타트업**: GitHub 활동 위젯 / 사이드 프로젝트 demo URL / AI 자동화 절약시간

---

## 1. Physical AI 채용 시각

### 강점 (Physical AI 자산)
- **Co-simulation 체질** — Ansys Maxwell(FEM) → MATLAB/Simulink → 실험 검증 (T-01 학위논문 정본화)
- **다중 신호 PHM** — phase current·온도·shaft displacement·vibration 동시 모니터링 (P-05)
- **분산 임베디드 시스템** — CAN 5노드 + GNSS RTK·카메라·IMU
- **실차 자율주행 노출** — GT-SS500 ADT PC 통합

### 약점/공백
- ROS2 한 줄로만 등장 (사이드 프로젝트). 노드 그래프/tf/rosbag/Nav2 0건
- **"Sim2Real" / "디지털트윈" 단어 사이트·SSOT·THEME_MAP 어디에도 없음** ← 가장 큰 갭
- NVIDIA Isaac/Drive, MuJoCo, Foundation Model, VLA/VLM 키워드 0건
- About 기술 스택에 ROS2/Ansys Maxwell/Co-simulation/Linux/PyTorch 0건

### 보강 권장
- **표현 교체** (코드 변경 최소, ROI 최대):
  - "농업용 Speed Sprayer" → "실외 자율 모빌리티 플랫폼"
  - "모터 모델링/고장진단" → "physics-informed motor digital twin · multi-sensor PHM"
  - 학위논문 부제 → "Sim2Real precursor: IPMSM digital twin + Co-simulation"
- **신규 케이스 페이지**: `cases/autonomy-stack/` — ROS2 + Gazebo + ADT 인터페이스 다이어그램
- **About 기술 스택 보강**: Ansys Maxwell, Co-simulation, ROS2, Linux, RTK GNSS/IMU 융합, PHM/Anomaly Detection

---

## 2. 로보틱스 채용 시각

### 강점 (즉시 인정)
- 임베디드 모터제어 깊이 — SVPWM/DPWM, FOC, EEMF/BEMF observer, 센서리스 초기위치, -40°C 기동
- 분산 임베디드 시스템 통합 — VCU 1대 ↔ CAN 5노드 ↔ ADT PC
- 상태머신 + 안전 설계 — RC/LCD/ADT 3모드, E_Stop 5분 락, 308A 0.082m 정지거리
- 양산 경험 — APQP/PFMEA/IQC-OQC 5단계

### 약점/공백
- **ROS/ROS2 부재** — 1차 ATS 필터에서 탈락 가능
- **인지 스택 0** — SLAM, Path Planning, Sensor Fusion(EKF/UKF) 미언급
- **Functional Safety 인증** — ISO 26262 / ISO 13849 표준 매핑 표기 없음
- 시뮬레이션(Gazebo/Isaac/CARLA, MIL/SIL/HIL) 명시 없음

### 보강 권장
- **가장 큰 갭**: ROS2 + 인지 스택 사이드프로젝트 1건 (GT-SS500 차동조향 → turtlebot3/Gazebo + nav2 + EKF)
- 안전 섹션에 **ISO 13849 Cat.3 PL=d** 매핑 1줄
- 다이나모를 **HIL 벤치**로 재포지셔닝
- ADT PC 협업 깊이 1단락 (좌표계, 메시지 주기, 페일세이프 핸드셰이크)
- 헤더에 **"Robotics Systems Integration"** 추가 — 모터제어 vs 시스템 통합 무게는 6:4 시스템 통합

---

## 3. 제품 개발 PM 채용 시각

### 강점
- 풀사이클 양산 PM (APQP 5단계 + IQC/OQC 5단계 QC + DFMEA/PFMEA 갱신)
- 이슈 트래킹 정량화 — 37건+/직접 14건/NCR 27건 (분류가 PFMEA Lessons Learned 수준)
- 6개팀 Cross-functional facilitation
- 시험 기획 단독 구축 7종 (3년 진화 패턴)
- 국책과제 EOP 완료보고서 핵심 근거

### 약점
- **PMP/CAPM/식스시그마 인증 0건** — 대기업 PM 트랙 ATS 자동필터
- **일정/원가 정량 부재** — QCD 중 Q만 강함. 리드타임/BOM/예산 없음
- **APQP Phase별 RACI 미명시** — Phase 1~5 중 본인 owner 영역 불명
- WBS/Gantt 산출물 0건
- 글로벌/해외 협력사 경험 없음

### 보강 권장 (가장 큰 갭)
> **APQP Phase × 본인 RACI 매트릭스 1장 추가** — 이거 하나로 모터제어 51%/PM 49% → PM 60%로 즉시 전환 가능

추가:
- QCD 정량 추출 (이슈 평균 Closure 일수, NCR 재발률 등)
- WBS 1장 (알파→파일럿→양산 게이트차트)
- DFMEA RPN before/after 1건만이라도 수치화

---

## 4. 스타트업 채용 시각

### 강점
- 풀스택 하드웨어 — STM32 VCU + 5노드 CAN + BMS + AWS OTA + 자율주행 연동 단독 주도
- 시험 장비 자가 구축 — 다이나모 0.008%, 펌프/팬/범퍼 벤치 직접 설계 ("자본 효율성 시그널")
- DFMEA 4건 + 6팀 협업 + APQP 풀사이클
- AI 워크플로우 설계자 — hih-skills 13개, PM 오케스트레이터, 야간 무인 cron

### 약점/공백
- **사업 임팩트 정량 부재** — 매출/출하대수/고객수/단가절감 ROI 0건. CEO 시각 "돈"이 안 보임
- **속도 증거 부족** — "며칠/몇 주 PoC" 류 없음. 모든 케이스 다년 프로젝트
- **고객/사용자 검증 0건** — 농민 인터뷰, 현장 데모 언급 없음
- 팀 빌딩/리더십 경험 부재
- 사이드 프로젝트 demo URL/GitHub 임팩트 없음
- AI 자동화 ROI 미정량 ("주 N시간 절약")

### 보강 권장 (가장 큰 갭)
> **사업 임팩트 정량화** — Hero 수치카드에 매출/출하/시간단축 1건만 추가해도 "훌륭한 시니어 엔지니어" → "초기멤버급 Builder" 톤으로 상승

추가:
- GitHub 활동 위젯 (커밋 히트맵·PR 수)
- 사이드 프로젝트 demo URL + 스크린샷 + "혼자 X일 만에" 라벨
- AI 워크플로우 절약시간 정량화 ("주 N시간 → 연 환산 M개월")
- "GT-SS500 양산으로 회사 매출/계약 K억 기여" (공개 가능 범위)
- 헤더 "Junior PM" → **"Full-stack Hardware · 0→1 Builder · AI-Augmented"**

---

## 종합 결론 — B2~B4 입력으로

### B2 메시지 확정 (USAGE_STRATEGY.md §2)
- 4개 도메인 중 1순위 타겟에 따라 메시지 우선순위 다름
- **공통 강점**: Co-simulation, CAN 분산제어, 양산 경험, AI 워크플로우 — 어느 도메인에도 통함
- **차별화 필요**: 도메인별 어휘 리프레임이 사이드 효과 큼

### B3 배치 (LAYOUT.md)
- 신규 케이스 페이지 후보: `autonomy-stack/` (Physical AI/로보틱스 합산), `apqp-rmci/` (제품 PM)
- Hero 수치카드 1줄 추가 후보: 사업 임팩트
- About 기술 스택 보강

### B4 디자인 (DESIGN_SYSTEM.md)
- 코드 변경보다 **카피/표현 교체가 ROI 최대**
- 도메인별 헤더 분기 가능 여부 검토

### B5 부가 (이력서/GitHub/영문)
- GitHub 위젯 임베드
- 직무별 이력서 분기 (대기업 PM 트랙 vs 스타트업 풀스택)
- 영문 부제는 Physical AI/로보틱스 어휘 우선
