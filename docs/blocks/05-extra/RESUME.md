# 이력서 마스터 (RESUME)

> 최종 수정: 2026-04-26 (B5-01 신규 작성)
> 위치: `docs/blocks/05-extra/RESUME.md`
> 형식: 한국어 마스터. 추후 PDF / 영문(B5-03) 변환 가능한 마크다운.
> 입력 SSOT:
> - `docs/포트폴리오/CONTENT_V2.md` — 사실 원본
> - `docs/포트폴리오/PAPERS.md` — 학위논문 1 + 공저 5 + 수상 2
> - `docs/포트폴리오/EXPERT_REVIEW_20260426.md` — 4개 도메인 갭 분석
> - `docs/blocks/02-usage/USAGE_STRATEGY.md` — 메시지 후보 8개 (MC-A ~ MC-H)
> - `docs/blocks/03-layout/LAYOUT.md` — 헤드라인 후보 H-A/H-B/H-C
> 운영 원칙:
> - 사실 자체는 SSOT(CONTENT_V2/PAPERS)에서만 수정. 본 문서는 이력서 형태로 **재배치**만 한다.
> - 사용자 입력 영역은 `[TODO: 사용자 입력]` 표시. 제출 직전 채움.
> - 도메인별 분기 모듈은 §11~§14에 별도 섹션으로 보관. 출력 시 §2 Summary와 §5/§7 강조 순서를 도메인 모듈로 교체.

---

# Part 1 — 마스터 이력서

## §1 인적사항

| 항목 | 내용 |
|------|------|
| **이름** | 황인혁 (Inhyeok Hwang) |
| **현재 소속** | GINT(긴트) · 전력제어개발팀 (선임연구원) + 제품개발팀 (주니어 PM 겸임) |
| **이메일** | `[TODO: 사용자 입력 — 공개 이메일]` |
| **연락처** | `[TODO: 사용자 입력 — 휴대폰]` |
| **GitHub** | `[TODO: 사용자 입력 — github.com/<id>]` |
| **포트폴리오 사이트** | `[TODO: 사용자 입력 — 도메인 확정 후]` |
| **거주지** | `[TODO: 사용자 입력]` |

---

## §2 요약 (Summary) — 4가지 톤 옵션

> 본 마스터는 4개 톤을 모두 적재. 제출 시 타겟 도메인 1개를 골라 §2를 단일화한다.
> 도메인별 강조 영역은 §11 ~ §14 모듈을 동시에 참고.

### 2.A 모터제어/임베디드 R&D 톤 (현대차/모비스/LG마그나/삼성SDI 등)

> BLDC/PMSM 모터제어 깊이 — SVPWM/DPWM 절환, 센서리스 초기위치 추정, 극저온 기동.
> 학위논문(IPMSM 시뮬레이션) → IEEE TIM 2024 공저 → EOP 400W 국책과제 → GT-SS500 양산까지,
> "모델 → 시뮬레이션 → 실험 → 양산"으로 이어진 8년 일관 트랙.

### 2.B 풀사이클 PM 톤 (대기업 제품 PM 트랙)

> APQP 5 Phase 풀사이클 PM. GT-SS500 농업 자율주행 제품에서 알고리즘 → 시험체계 → DFMEA →
> 양산 BOM(132 항목) → 대외 인증(혁신제품 실사) → 양산 출하까지 7단계 Lifecycle을 끝까지 수행.
> 6개팀 Cross-functional facilitation, 이슈 37건+ 트래킹, NCR 27건, DFMEA AP=H 5건 도출.

### 2.C Physical AI / 로보틱스 시스템 통합 톤

> Physics-informed motor digital twin (Ansys Maxwell + MATLAB/Simulink Co-simulation) +
> multi-sensor PHM(IEEE TIM 2024) + CAN 5노드 분산 제어 + 실외 자율 모빌리티 플랫폼(GT-SS500).
> Sim2Real precursor 체질 — 시뮬레이션에서 시작해 다이나모(비선형성 0.008%)로 실증하고
> ADT PC와 페일세이프 핸드셰이크까지 끌고 가는 시스템 통합 엔지니어.

### 2.D 스타트업 풀스택 빌더 톤

> Full-stack Hardware · 0→1 Builder · AI-Augmented.
> STM32 VCU + 5노드 CAN + LiFePO4 BMS + AWS OTA + 자율주행 연동을 단독 주도.
> 시험 장비 자가 구축(다이나모 0.008% / 팬 +57% / 범퍼 0.082m) — "장비가 없으면 만든다".
> 3계층 LLM 라우팅(Opus/GLM/Ollama) + PM 오케스트레이터 + 자동화 스킬 13개로 1인=N인 효과.

---

## §3 학력

### 건국대학교 대학원 · 기계설계학과 · 석사 (2021.03 ~ 2023.02)

- **학위수여**: 2023-03-22 (학위수여증명서 보관: `archive/personal/91)기타/2024/황인혁-국문-학위수여증명서-202303221543.pdf`)
- **연구실**: 신뢰성 기반 설계 최적화(RBDO) Lab — 지도교수 **김남수** (Namsu Kim)
- **세부전공**: 매입형 영구자석 동기전동기(IPMSM)의 모델링 및 고장 진단 (PHM)
- **학위논문 (T-01)**:
  - 국문: *전자기 해석을 이용한 매입형 영구자석 동기 전동기의 고장 진단 시뮬레이션에 관한 연구*
  - 영문: *Fault Diagnosis Simulation of Interior Permanent Magnet Synchronous Motor using Electromagnetic Analysis*
  - 49p · RISS control_no: `f678963f23f2e418ffe0bdc3ef48d419`
  - 핵심 기여: flux-state variable model + FEA로 IPMSM 자기포화 효과 포함 시뮬레이션 → 인버터 제어와 Co-simulation → 다양한 운전 조건 실험 검증.
- **연구 경력**: 2년 6개월 (학부연구생 6개월 + 석사 2년)

### 건국대학교 · 기계공학부 기계설계학과 · 학사 (2015 ~ 2021)

- 학사학위 취득. (세부 — `[TODO: 사용자 입력 — GPA / 우등 여부 등]`)

---

## §4 경력

### GINT (긴트) — 전력제어개발팀 + 제품개발팀(주니어 PM 겸임)
**선임연구원** · 2025.01 ~ 현재

- **GT-SS500 풀사이클 주도** — 알고리즘부터 양산까지. APQP Phase 2~3, DFMEA #201/#210 Step 1~7, BOM 132 항목, 혁신제품 실사 4/9 대응, 양산 초도 16pcs+대차 2+Spare 2 생산계획.
- **CAN 5노드 분산 제어 설계** — VCU ↔ 구동×2 ↔ 팬 ↔ 펌프 ↔ BMS. DBC 4종 직접 작성/관리. BREAKING CHANGE 4건 사전 검출.
- **시험체계 단독 구축** — 다이나모미터 / 펌프 벤치 / 팬 벤치 / 범퍼 시험대 직접 설계.
- **DFMEA 현장 RCA 4건** — MCB 전해부식(#204) / LCD 상태머신(#79) / 펌프 동파 오링 / GND 노이즈.
- **이슈 트래킹** — 37건+ 중 전력제어 직접 담당 14건, NCR 27건.

### GINT (긴트) — 전력제어개발팀
**주임연구원** · 2023.02 ~ 2024.12

- **EOP 400W 국책과제 완료** — 12V 400W 전동오일펌프 BLDC 모터제어. MC9S12ZVMC.
- **SVPWM/DPWM 절환 기법** — FET 온도 1~6°C 저감, 입력전력 1~3.8% 감소 (2,932 데이터 포인트 검증).
- **CAN Sleep/Wakeup 구현** — 암전류 요구 충족, 5차례 rev 개선.
- **극저온 기동 실험** — -40°C 환경 300초 → 100초로 기동시간 단축 실증.
- **다이나모미터 토크제어 시스템** 직접 구축 — 비선형성 0.008% (사내 세미나 발표).
- **특허 출원 2건** — §6 참조.

---

## §5 핵심 프로젝트

### 5.1 GT-SS500 — 48V 전동 자율주행 Speed Sprayer (2025.01 ~ 2026.양산)

> 농업용 Physical AI 제품. STM32 기반 VCU + 5노드 CAN 분산 제어 + RC/LCD/자율주행 3모드 상태머신 + LiFePO4 BMS + AWS OTA. 전력제어 개발자(본업) + 주니어 PM(겸임)으로 풀사이클 수행.

| 영역 | 정량 성과 |
|------|----------|
| 양산 준비 | APQP Phase 2~3, DFMEA Step 1~7 (AP=H 5건), Boundary Diagram + Assembly 재편 |
| BOM 관리 | 132 항목 관리 · 재고 미확보 23건 사전 식별 |
| 시험체계 | 다이나모/펌프/팬/범퍼 시험대 직접 설계, CAN 정합성 체크리스트 3차 반복 |
| 안전 검증 | 범퍼 정지거리 0.082m · 피크 308A · 정착시간 467ms (3km/h 주행) |
| 성능 개선 | 팬 풍속 7.9 → 12.4 m/s (+57%) · 펌프 3시료 선형관계 규명 |
| CAN 통신 | DBC 4종 직접 작성 · BREAKING CHANGE 4건 사전 검출 |
| 현장 이슈 | 37건+ 트래킹, 직접 담당 14건, NCR 27건 |
| 대외 대응 | 혁신제품 실사 4/9 대응(#205), 농진원 대응 |

### 5.2 EOP 400W — 12V 자동차용 전동오일펌프 (2023~2024 국책과제)

> 자동차용 BLDC 모터 제어. MC9S12ZVMC. SVPWM/DPWM 절환 · CAN Sleep/Wakeup · 극저온 기동.

| 영역 | 정량 성과 |
|------|----------|
| SVPWM/DPWM 절환 | FET 온도 1~6°C ↓, 입력전력 1~3.8% ↓ (2,932 데이터 포인트) |
| 극저온 기동 | -40°C 300초 → 100초 단축 실증 |
| 저전력 통신 | CAN Sleep/Wakeup 5차 rev, 암전류 요구 충족 |
| 시험 인프라 | 다이나모미터 토크제어 시스템 비선형성 0.008% (사내 세미나 발표) |
| 특허 | 출원 2건 (§6) |

### 5.3 시험 기획 7종 — "장비가 없으면 만든다"

| # | 시험 | 정량 결과 |
|---|------|----------|
| 1 | 다이나모미터 토크제어 (EOP) | 비선형성 **0.008%** |
| 2 | 팬 벤치 (SS500) | 풍속 7.9 → **12.4 m/s** (+57%) |
| 3 | 펌프 벤치 (SS500) | 3시료 선형관계 규명, 명판 허위 검증 |
| 4 | 범퍼 시험대 (SS500) | 정지거리 **0.082m**, 피크 **308A**, 정착시간 467ms |
| 5 | CAN 정합성 체크리스트 | 3차 반복 검증 프로토콜 표준화 |
| 6 | -40°C 극저온 챔버 (EOP 특허 #2) | 300초 → 100초 |
| 7 | PWM 온도/효율 비교 (EOP) | 2,932 데이터 포인트 |

---

## §6 논문 / 학회 / 특허

### 6.1 학위논문 (1편)

- **T-01** (2023) · *전자기 해석을 이용한 매입형 영구자석 동기 전동기의 고장 진단 시뮬레이션에 관한 연구* · 건국대학교 대학원 기계설계학과 · 49p · 지도교수 김남수.

### 6.2 공저 저널 (3편 — IEEE TIM / Solar Energy / J. Power Electronics)

- **P-01** (2024) · IEEE Transactions on Instrumentation and Measurement, Vol. 73, Art. 10726721. · *Programmable Online Bond-Wire Fault Detection and Location Method for IGBT Using Inverter Output Parameters*. · DOI 10.1109/TIM.2024.3472910 · Oh, Kim, **Hwang**, Choi, Kim.
- **P-04** (2024) · Solar Energy (Elsevier), Vol. 276, Art. 112645. · *Lifetime prediction of polymeric materials in PV module under continuously varying environments based on damage summation approach*. · DOI 10.1016/j.solener.2024.112645 · Choi, Kwon, Oh, **Hwang**(4저자) 외 6명.
- **P-05** (2024) · Journal of Power Electronics, Vol. 24 Issue 5, pp. 822-831. · *Identification of failure modes in IPMSM under accelerated life test based on dual sensor architecture*. · DOI 10.1007/s43236-024-00810-8 · Choi, Oh, Lee, Kwon, Lee, **Hwang**(6저자) 외 2명.

### 6.3 학회 발표 (4편)

- **C-01** (2021) · 한국PHM학회 2021 정기학술대회 · *시스템 수준 측정값을 이용한 모터 구동 시스템 내 IGBT 개방 고장 진단 기법*. **우수포스터상**.
- **C-02** (2022) · 한국신뢰성학회 2022 춘계학술대회 · *전동화 차량 구동시스템의 효율적인 예방정비 기술 개발*. **최우수발표 논문상**.
- **C-03** (2022) · 한국PHM학회 2022 정기학술대회 · *전기자동차용 매입형 영구자석 동기전동기의 정밀한 시뮬레이션을 위한 모델링 분석*.
- **P-02 / P-03** (2022~2023) · PCIM Asia 2022 (IGBT Power Cycling, IPM 본드와이어/솔더 열화) · PHM Society Asia-Pacific Conference 2023 (120kW IPMSM 시스템 수준 고장진단, DOI 10.36001/phmap.2023.v4i1.3780).

### 6.4 수상

- **한국PHM학회 2021 우수포스터상**.
- **한국신뢰성학회 2022 최우수발표 논문상**.

### 6.5 특허 (2건 — 정직 기재)

- **특허 #1 — 모터 초기 위치 검출 (공동 발명자)**.
  출원번호 PN231067KR (2023) · 특허법인 더웨이브 경유 출원 · 요구 1.0초 → **0.56초** 검출 시간 달성 · 사전조사 논문 1건 + 특허 10건.
- **특허 #2 — 저온 기동 기법 (개발 기여, 명세서 발명자 명단 미포함)**.
  실험적 검증 담당 — 극저온 챔버 기동 특성 측정 · -40°C 환경 **300초 → 100초** 단축 실증 · 사전조사 논문 3건. 출원번호 `[TODO: 사용자 확인]`.

> 정직 기재 메모: 두 건 중 한 건은 발명자 명단에 올라가지 않았다. 저온 기동 건은 실험 설계와 데이터 검증을 본인이 담당했고, 그 데이터가 없었다면 출원 자체가 성립하지 않았다.

---

## §7 보유 기술 (Skills)

### 7.1 모터제어 / 전력 전자

- BLDC · IPMSM · PMSM 제어 · FOC · SVPWM / DPWM 절환 · 센서리스 초기위치 추정 · BEMF observer · 극저온 기동.
- 인버터 게이트 신호 진단 · 본드와이어 lift-off 검출 (IEEE TIM 2024).

### 7.2 임베디드 / FW

- STM32 · NXP MC9S12ZVMC · Infineon TC23x · RTOS · 상태머신 (RC/LCD/ADT 3모드) · 모터 컨트롤러 FW 코드리뷰.

### 7.3 통신 / 시스템 설계

- CAN · CAN-FD · CAN Sleep/Wakeup · DBC 작성/관리 (4종) · CAN BusLoad 분석 · 5노드 분산 제어 토폴로지.
- (자동차) ISO 13849 reading · Functional Safety 매핑 학습 단계.

### 7.4 시뮬레이션 / 해석

- Ansys Maxwell (FEM, Transient) · MATLAB/Simulink · **Co-simulation (Sim2Real precursor)** · MIL/SIL/HIL 개념 적용.

### 7.5 시험 / 분석

- 다이나모미터 토크제어 · 팬/펌프/범퍼 벤치 자가 설계 · CANoe · Vector VN1600 · SPICE · Oscilloscope · DAQ (NI-9215 등).

### 7.6 PHM / 신호처리

- Multi-sensor PHM · Anomaly Detection · phase current / 온도 / shaft displacement / vibration 다중 신호 융합.

### 7.7 품질 / PM 산출물

- APQP Phase 1~5 · DFMEA / PFMEA · DRBFM · Boundary Diagram · BOM 관리 · IQC/OQC 검사 가이드 · WBS · NCR 처리.

### 7.8 SW / AI 워크플로우

- Python · C / C++ · Git · Linux.
- **3계층 LLM 라우팅** (의사결정 Opus / 실무 GLM / 배치 Ollama) · Claude Code · MCP · Obsidian + Dataview.
- **PM 오케스트레이터** (8개 프로젝트 통합 모니터링) · 자동화 스킬 13개 (`hih-skills` 모듈화) · cron 야간 무인 실행.
- PyTorch · LangChain · Docker — 학습 / 활용 단계.

### 7.9 로보틱스 (사이드 / 학습 단계)

- ROS2 · Gazebo · nav2 · turtlebot3 · EKF — 사이드 프로젝트 학습 단계 (정직 기재).

---

## §8 수상

- **2022** · 한국신뢰성학회 2022 춘계학술대회 **최우수발표 논문상** (전동화 차량 구동시스템의 효율적인 예방정비 기술 개발).
- **2021** · 한국PHM학회 2021 정기학술대회 **우수포스터상** (시스템 수준 측정값 IGBT 개방 고장 진단).
- 사내 — EOP 다이나모미터 토크제어 시스템(비선형성 0.008%) 사내 세미나 발표.

---

## §9 어학 / 자격

| 항목 | 내용 |
|------|------|
| 영어 | `[TODO: 사용자 입력 — TOEIC / OPIc / TEPS 등급 + 점수]` |
| 기타 어학 | `[TODO: 사용자 입력 — 해당 시]` |
| 자격증 | `[TODO: 사용자 입력 — 기사/산업기사/PMP/식스시그마 등 해당 시]` |
| 보안 | `[TODO: 사용자 입력 — 병역 / 보안 등급 등]` |

---

## §10 추가 정보

### 10.1 사이드 프로젝트 / OSS

- `hih-skills` — 자동화 스킬 13개 모듈화 레포 (개인).
- `[TODO: 사용자 입력 — demo URL 1~2건 (스타트업 트랙)]`.

### 10.2 학회 / 협회

- 한국PHM학회 · 한국신뢰성학회 (학회 발표 이력).

### 10.3 추천인

- `[TODO: 사용자 입력 — 요청 시 제공]`.

---

# Part 2 — 도메인별 분기 모듈

> 각 모듈은 §2 Summary 교체 + §5/§7 강조 순서 변경 가이드. 마스터 사실은 그대로 두고, 출력 시 모듈을 적용한다.

---

## §11 모듈 A — 모터제어 R&D (대기업 R&D / 자동차 전장 / 가전 모터)

**§2 Summary 교체**: §2.A 사용.

**§5 강조 순서**: 5.2 EOP 400W → 5.1 GT-SS500 (모터제어 측면) → 5.3 시험 기획.

**§5 추가 1줄 카피**: "BLDC/PMSM 모터제어 깊이 — SVPWM 절환·-40°C 기동·다이나모 0.008%."

**§6 강조 순서**: 학위논문 T-01 → P-01 IEEE TIM 2024 → 특허 #1 (PN231067KR) → 특허 #2 → P-05 J. Power Electron. → 학회 4편.

**§7 강조 순서**: 7.1 모터제어 → 7.4 시뮬레이션(Co-simulation) → 7.2 임베디드 → 7.5 시험 → 7.6 PHM → 7.3 통신 → 나머지.

**키워드 매칭**: BLDC · PMSM · IPMSM · FOC · SVPWM · DPWM · 센서리스 · BEMF · 인버터 · IGBT · 본드와이어 · 극저온 · 다이나모 · CAN · IEEE TIM · 학위논문.

**컷 항목**: §7.8 AI 워크플로우 1줄로 축약 · §7.9 로보틱스 컷 · 사이드 프로젝트 컷.

---

## §12 모듈 B — 제품 개발 PM (대기업 PM 트랙 / 풀사이클 양산)

**§2 Summary 교체**: §2.B 사용.

**§5 강조 순서**: 5.1 GT-SS500 (PM 측면 강조) → 5.3 시험 기획 → 5.2 EOP 400W (국책과제 완료보고서).

**§5 추가 1줄 카피**: "APQP 5 Phase 풀사이클 PM — DFMEA AP=H 5건 · NCR 27건 · BOM 132 · 6팀 협업."

**§6 강조 순서**: 학위논문 T-01 → 특허 2건 → 공저 저널 3편 → 학회 4편.

**§7 강조 순서**: 7.7 품질/PM → 7.5 시험 → 7.3 통신 → 7.1 모터제어 → 7.2 임베디드 → 7.4 시뮬레이션 → 7.8 AI 워크플로우 → 7.6 PHM.

**보강 권장 (EXPERT_REVIEW §3)**:
- APQP Phase 1~5 × 본인 RACI 매트릭스 1장 첨부 (별첨 또는 사이트 `cases/apqp-rmci/` 링크).
- DFMEA RPN before/after 1건 정량화 — MCB #204 또는 LCD #79 중 1건.
- WBS 게이트차트 1장 (알파 → 파일럿 → 양산).
- QCD KPI: 이슈 평균 Closure 일수, NCR 재발률.

**§4 표기 톤**: "주니어 PM" 표현 **유지** (대기업 PM 트랙은 직급 명확성을 선호).

**키워드 매칭**: APQP · DFMEA · PFMEA · DRBFM · BOM · NCR · IQC · OQC · Boundary Diagram · WBS · Cross-functional · 양산 · 풀사이클 · 인증 · 혁신제품.

**컷 항목**: §7.9 로보틱스 컷 · §10.1 OSS 1줄로 축약.

---

## §13 모듈 C — 로보틱스 / Physical AI (시스템 통합)

**§2 Summary 교체**: §2.C 사용.

**§5 강조 순서**: 5.1 GT-SS500 (시스템 통합 측면) → 5.2 EOP 400W (분산 임베디드 깊이) → 5.3 시험 기획 (HIL 벤치).

**§5 추가 1줄 카피**: "Co-simulation에서 ADT까지 — 분산 임베디드 시스템 통합 + multi-sensor PHM."

**§5 어휘 리프레임 (EXPERT_REVIEW §1·§2)**:
- "농업용 Speed Sprayer" → "**실외 자율 모빌리티 플랫폼** (RTK GNSS+IMU+카메라+CAN 분산제어)".
- "모터 모델링/고장진단" → "**physics-informed motor digital twin · multi-sensor PHM**".
- 학위논문 부제: "**Sim2Real precursor: IPMSM digital twin + Co-simulation**".
- 다이나모미터 → "**HIL 벤치** (다이나모 0.008%)".

**§6 강조 순서**: T-01 학위논문(디지털트윈) → P-01 IEEE TIM(다중신호 PHM) → P-03 PHM Asia 2023(시스템 수준 고장진단) → P-05 dual sensor → 특허 → 학회.

**§7 강조 순서**: 7.4 시뮬레이션(Co-simulation/Sim2Real) → 7.6 PHM → 7.3 통신/시스템 설계 → 7.1 모터제어 → 7.9 로보틱스(ROS2/Gazebo/nav2) → 7.2 임베디드 → 7.5 시험(HIL) → 7.8 AI 워크플로우.

**보강 권장 (EXPERT_REVIEW §1·§2)**:
- 사이드 프로젝트 1건 추가 — turtlebot3 + Gazebo + nav2 + EKF (GT-SS500 차동조향 시뮬).
- ADT PC 협업 깊이 1단락 — 좌표계, 메시지 주기, 페일세이프 핸드셰이크.
- About 헤더: "**Robotics Systems Integration**" 추가 (모터제어 6 : 시스템 통합 4).

**키워드 매칭**: ROS2 · Gazebo · nav2 · SLAM · EKF · Sensor Fusion · RTK GNSS · IMU · Co-simulation · Sim2Real · Digital Twin · PHM · Anomaly Detection · ADT · CAN · ISO 13849 · HIL · MIL/SIL.

---

## §14 모듈 D — 스타트업 풀스택 빌더 (0→1 / AI-Augmented)

**§2 Summary 교체**: §2.D 사용.

**§4 표기 톤**: "주니어 PM" 표현 **컷** → "**Full-stack Hardware · 0→1 Builder · AI-Augmented**" (EXPERT_REVIEW §4 권장).

**§5 강조 순서**: 5.1 GT-SS500 (단독 풀사이클 강조) → 5.3 시험 기획 (자가 구축) → 5.2 EOP 400W → §10.1 OSS / 사이드.

**§5 추가 1줄 카피**: "STM32 VCU + 5노드 CAN + BMS + AWS OTA + 자율주행 단독 주도 — 장비가 없으면 만든다."

**§6 강조 순서**: 특허 2건 → 학위논문 T-01 → P-01 IEEE TIM → 학회 수상 2건 (간결하게).

**§7 강조 순서**: 7.8 AI 워크플로우 → 7.1 모터제어 → 7.5 시험 → 7.7 품질/PM → 7.3 통신 → 7.2 임베디드 → 7.4 시뮬레이션 → 7.6 PHM → 7.9 로보틱스.

**보강 권장 (EXPERT_REVIEW §4)**:
- **사업 임팩트 정량화 (가장 큰 갭)**: "GT-SS500 양산 출하 K억 기여 / 출하대수 N대 / 단가절감 X%" — 공개 가능 범위에서 1줄. `[TODO: 사용자 입력]`.
- **속도 증거**: "혼자 X일 만에 PoC", "AI 워크플로우로 주 N시간 → 연 환산 M개월" — `[TODO: 사용자 입력]`.
- **GitHub 활동 위젯** 임베드 (이력서 본문 또는 사이트 `/impact`).
- 사이드 프로젝트 1건 demo URL + 스크린샷 + "혼자 X일" 라벨.

**키워드 매칭**: Full-stack · 0→1 · 단독 주도 · AI-Augmented · LLM 라우팅 · MCP · 자동화 · cron · OTA · BMS · 풀사이클 · PoC · 자본 효율성 · 1인=N인.

**컷 항목**: §7.7 품질/PM 산출물 1~2줄로 축약 (스타트업은 풀사이클 + 속도가 우선).

---

# Part 3 — 운영 메모

## §15 출력 시 체크리스트

이력서 PDF/제출본 생성 전:

- [ ] §1 인적사항 `[TODO]` 4항목 채움 (이메일·연락처·GitHub·사이트).
- [ ] §3 학력 학부 `[TODO]` 채움.
- [ ] §6.5 특허 #2 출원번호 `[TODO]` 채움.
- [ ] §9 어학·자격 `[TODO]` 채움.
- [ ] 타겟 도메인 1개 결정 → §11~§14 중 1개 모듈 적용 → §2 Summary 단일화.
- [ ] 모듈에 따른 §5 / §7 강조 순서 재배치.
- [ ] 모듈 D 적용 시 §4 직급 표현 "Full-stack Builder"로 교체.
- [ ] 도메인별 어휘 리프레임 적용 (모듈 C의 "Sim2Real precursor" / "HIL 벤치" 등).
- [ ] 사실 변경 사항 발생 시 SSOT(CONTENT_V2 / PAPERS) 먼저 수정 → 본 문서 동기화.
- [ ] 제출 전 한 번 더 정직 기재 점검 (특허 #2 발명자 미기재 / 로보틱스 학습 단계 표기).

## §16 후속 작업 (B5 시리즈)

- **B5-02**: GitHub 활동 위젯 임베드 / `/impact` 페이지 구성.
- **B5-03**: 본 마스터 영문 변환 (Physical AI / 로보틱스 어휘 우선).
- **B5-04**: 도메인별 1페이지 경량 이력서 (PDF 출력) 4종 생성.

---

> 본 문서는 "사실의 마스터 + 도메인 분기 가이드"이다. 사실은 SSOT에서, 톤·강조는 모듈에서, 제출본은 출력 단계에서 결정한다.
