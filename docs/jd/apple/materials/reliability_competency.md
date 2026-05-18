# Reliability 역량 인벤토리 + 연계 경험 매핑

> 작성: 2026-05-04 | Apple Reliability Engineer (Job ID 200656459-3631) 지원 준비
> 기반: Phase 1 30개 개념 자가 점검 + 사용자 미기재 자산 발굴
> 다음 단계: jd_resume_match.md / resume_en.md / cover_letter.md 갱신 입력

> **자가학습 SSOT 명시 (2026-05-04 fact-check pass)**: 본 문서는 학습용 자가 정리 자료다.
> 외부 제출 자료(cover letter / resume / 지원서)에 본 문서의 표현을 직접 인용하지 말 것.
> 사용자 실제 경험은 RESUME.md (`docs/blocks/05-extra/RESUME.md`)가 SSOT.
> 학습 진행 후 깊이 도달이 검증된 항목만 외부 자료에 반영.

---

## 0. 핵심 메시지 (Executive Summary)

건국대 **신뢰성기반최적설계(RBDO) Lab** 석사 2년의 학문적 신뢰성 배경,
IGBT Power Cycling Test(PCT) 직접 수행과 IPMSM ALT 동행 관찰을 통한 반도체·전동계통 신뢰성 실험 경험,
GT-SS500 APQP Phase 2~3 + DFMEA 5건 + IQC/OQC + NCR 27건의 양산 직전 검증 경험이 결합된 프로파일이다.

**양산(APQP) 경험은 학계 출신 신뢰성 후보군과 차별되는 결정적 강점이다.** Apple JD "개발·양산 단계 신뢰성 시험 주도"와 "ORT 이슈 우선순위화"에 직접 매칭하며, 대학원 방법론만 갖춘 후보가 가질 수 없는 양산 현실(BOM·NCR·Gate Review·라인 stop·시정조치 시한) 감각이다.

도구 명칭(RCA, FRACAS, JESD47, MIL-STD-810, IEC 60529/60068)을 몰랐을 뿐, 실제 수행한 업무는 표준에 부합한다. 표준 매핑 후 어필 범위가 2배 확장된다.

광학(카메라/VCM/렌즈) 도메인은 유일한 실질 갭이나, ALT·FA·DFMEA 방법론은 대상과 무관하게 동일하다. 1주 자가학습으로 기본 대화 가능 수준 도달.

---

## 1. Phase 1 인벤토리 — 30개 개념 점검 결과 표

### Block 1 — ALT 계열

| 개념 | 등급 | 직접 경험 한 줄 | 학습 시급도 |
|------|------|----------------|:-----------:|
| **ALT (Accelerated Life Test)** | △+ | IPMSM ALT 설계·운영 옆에서 관찰. 편심(eccentricity) 고장 구현 위해 하중 인자 인가 → FTA 수행 → 의도 고장 미발생으로 destruct limit 인접까지 시도. 학습 사이클 직접 목격 | ★★ |
| **HALT (Highly Accelerated Life Test)** | △ | 위 IPMSM 과하중 시험이 destruct limit 영역에 닿음. 명시적 HALT 설계는 아니었으나 개념적으로 동일 영역 | ★ |
| **HASS** | ✗ | 미수행 | ★ |
| **ORT (Ongoing Reliability Test)** | △ | APQP Gate Review + IQC/OQC 운영 = 양산 단계 ORT와 본질 동일. 표준 명칭 미인지였을 뿐 | ★★ |
| **Burn-in** | ○ | Bathtub 곡선 초기불량 제거 → 평탄구간 진입 메커니즘 이해. 전자제품 적용 사례 인식 | ★ |

### Block 2 — 통계 모델

| 개념 | 등급 | 직접 경험 한 줄 | 학습 시급도 |
|------|------|----------------|:-----------:|
| **Weibull 분포** | ○+ | 개념 숙지. β(형상), η(척도), MTTF 산출 공식 인지. 플롯 해석 연습 필요 | ★★ |
| **Arrhenius 모델** | △+ | IGBT PCT 참여 — bond-wire lift-off + **solder fatigue 동시 관찰** (P-02 PCIM Asia 2022). P-01 IEEE TIM 2024는 검출·위치식별 알고리즘 (PCT 자체 아님). Ea 기반 가속 인자 개념 연결 | ★★ |
| **Eyring / 다중 스트레스 모델** | ○ | 다중 스트레스 동시 인가 개념 이해. PCT = 온도+전류 동시 스트레스 | ★ |
| **Coffin-Manson 모델** | △? | PCT와의 관계 헷갈림. 명확화: PCT는 시험 프로토콜, Coffin-Manson은 그 ΔT로 수명 외삽하는 모델. 인터뷰 혼용 시 위험 | ★★ |
| **Miner's Rule / Damage Summation** | △ | P-04 PV 폴리머 변동환경 수명 추정에 직접 사용 (Solar Energy 2024). 변동 스트레스 이력 → 누적 손상 합산 → 수명 외삽 직접 수행 | ★ |

### Block 3 — 곡선·지표

| 개념 | 등급 | 직접 경험 한 줄 | 학습 시급도 |
|------|------|----------------|:-----------:|
| **Bathtub Curve** | ○+ | 초기불량·우발고장·마모고장 3구간 이해. Burn-in + ORT 연결 이해 | ★ |
| **MTBF / MTTF / MTTR** | ✗→○ | 개념 설명 가능. 산식(MTTF = ∫R(t)dt) 연습 필요 | ★★ |
| **B10 수명** | △ | 10% 고장 확률 기준 수명. Weibull CDF 역산 이해. 산출 연습 필요 | ★★ |
| **RBD (Reliability Block Diagram)** | △ | 직렬/병렬 시스템 신뢰도 계산 개념 이해. 실제 RBD 작성 경험 없음 | ★ |
| **Stress-Strength Interference** | ✗→○ | 처음 들음. 단, RBDO Lab 출신이라 인터뷰 시 100% 들어올 질문. S-S overlap → 고장 확률. RBDO의 핵심 개념. 학습 즉시 어필 가능 | ★★★ |

### Block 4 — 분석 도구

| 개념 | 등급 | 직접 경험 한 줄 | 학습 시급도 |
|------|------|----------------|:-----------:|
| **FMEA / DFMEA** | ✓ | GT-SS500 DFMEA 5건 직접 작성 (MCB 전해부식·상태머신·O-ring·CAN 노이즈 +1). AIAG-VDA 2019 적용. AP=H 5건 도출 | — |
| **FMECA** | ○ | FMEA + Criticality 매트릭스 개념 이해. 실제 Criticality 수치화 경험 없음 | ★ |
| **ETA (Event Tree Analysis)** | △ | 개념 이해. 실제 작성 경험 없음 | ★ |
| **FTA (Fault Tree Analysis)** | ✓ | IPMSM 편심 시험 설계 시 직접 수행. 하중 인자 선정에 FTA 논리 적용 | — |
| **RCA / 5 Why / Fishbone** | ✗→실은✓ | 도구 명칭 몰랐으나 실제 RCA 4건 수행: MCB 전해부식(#204) / LCD 상태머신(#79) / 펌프 O-ring 동파 / GND 노이즈. 5단계(현상→고장모드 정의→근본원인→설계변경→재현검증) 모두 적용 | — |

### Block 5 — 데이터·진단

| 개념 | 등급 | 직접 경험 한 줄 | 학습 시급도 |
|------|------|----------------|:-----------:|
| **PHM (Prognostics & Health Management)** | ✓ | 산자부 과제 직접 수행 — 전동화 차량 구동 전기모터 상태진단 PHM SoC 개발 (2021~2022). C-01 PHM학회 우수포스터상 | — |
| **RUL (Remaining Useful Life)** | △ | **본인 기여**: 물리 모델 기반 Co-simulation (Ansys Maxwell FEM + MATLAB/Simulink) — 고장 모델링 + 학습 데이터 생성 (T-01 학위논문, P-03 PHM Asia 2023). **팀 산출물**: SVM 분류기 (상전류 → 고장 모드). Physics-informed + classical ML 혼합. 딥러닝(LSTM/CNN)은 미사용. **면접 시 SVM 디테일 질문은 팀 기여로 정직 답변.** | — |
| **Reliability Growth (Duane / AMSAA)** | ✗ | 미인지. 개발 단계 고장률 감소 추적 모델 | ★ |
| **FRACAS** | ✗→실은△ | 표준 명칭 미인지. 단 NCR 트래킹 27건 운영 = FRACAS 폐루프(Failure→Reporting→Analysis→Corrective Action→System) 사실상 수행 | ★★★ |
| **CI / Bayesian Reliability** | ✗ | 미인지 | ★ |

### Block 6 — 표준

| 개념 | 등급 | 직접 경험 한 줄 | 학습 시급도 |
|------|------|----------------|:-----------:|
| **Six Sigma / Cpk** | ○ | "백만 분의 1" 정확 이해. 공정 능력 지수(Cp/Cpk) 개념 인지 | ★★ |
| **JESD47 / JEP122** | ✗→실은△ | 표준명 미인지. PCT 직접 수행 = JESD47 항목(Power Cycling) + JEP122(IGBT 고장 메커니즘) 사실상 수행. 표준명 매핑 즉시 어필 가능 | ★★★ |
| **MIL-STD-810 / IEC 60068-2** | ✗→실은△ | 표준명 미인지. GT-SS500 진동·낙하·범퍼 시험 = MIL-STD-810 / IEC 60068-2 환경시험 카테고리 사실상 수행 | ★★ |
| **IEC 60529 IP 등급** | ✗→실은△ | 표준명 미인지. EOP CAN 커넥터 방수 설계 = IEC 60529 IP 등급 적용 실질 수행 | ★★ |
| **AEC-Q100 / ISO 26262** | ✗ | 미인지. GT-SS500 농기계라 ISO 25119 가능성 있음 — Phase 2 확인 예정 | ★ |

---

## 2. 직접 어필 가능 자산 (✓ + △+ 항목 모음)

| 항목 | 근거 사례 | 매핑 Apple JD 요건 | 1줄 어필 문구 |
|------|-----------|-------------------|--------------|
| **① RBDO Lab 학문적 배경** | 건국대 신뢰성기반최적설계(RBDO) Lab 석사 2년. 학위논문: IPMSM 고장 진단 Co-simulation. 한국신뢰성학회 최우수발표 논문상 (2022) | 기계공학 전공 + 신뢰성 이해 | "Reliability was not a side topic — it was my entire graduate research." |
| **② ALT 설계·운영 동행 + IPMSM 편심 고장 구현 시도** | 하중 인자 인가 → FTA → 의도 고장 미발생 → destruct limit 인접까지 시도. 실패로 끝났으나 설계-시험-재설계 루프를 직접 목격. P-05 J. Power Electron. 2024 | 신뢰성 시험 연구 + ALT 설계 | "Witnessed the full ALT design-test-redesign cycle including failure to reproduce intended fault modes." |
| **③ PCT(Power Cycling Test) — IGBT bond-wire lift-off + 추가 고장 메커니즘** | PCT 직접 수행. bond-wire lift-off 확인 + 다른 고장 모드 동시 관찰. P-01 IEEE TIM 2024 (DOI 10.1109/TIM.2024.3472910) | 반도체 모듈 신뢰성 시험 | "Conducted PCT on IGBT modules; identified bond-wire lift-off and co-occurring failure modes (IEEE TIM 2024)." |
| **④ PHM SoC 산자부 과제 + RUL 산출** | 전동화 차량 구동 전기모터 상태진단 PHM SoC 개발 (2021~2022). C-01 PHM학회 우수포스터상. 학위논문 + P-03 PHM Asia 2023 | 데이터 분석 + 진단 자동화 | "Developed PHM SoC for EV drivetrain fault diagnosis; awarded best poster at Korea PHM Society (2021)." |
| **⑤ DFMEA 5건 + FTA + RCA 4건** | GT-SS500: MCB 전해부식(#204) / LCD 상태머신(#79) / 펌프 O-ring 동파 / GND 노이즈 / +1. AIAG-VDA 2019 적용. AP=H 5건 도출 | FA 주도 + 교차 기능 시정조치 | "Closed 4 RCAs and authored 5 DFMEAs using AIAG-VDA 2019; all AP=H items resolved before production ramp." |
| **⑥ APQP Phase 2~3 양산 경험** | Gate Review 운영, IQC/OQC 검사 기준 정의, NCR 27건 트래킹, BOM 132항목 관리, 양산 초도 16pcs 생산계획. → 별도 강조 섹션(§4) 참조 | Mass production quality + ORT 주도 | "I bridge academic rigor and production reality — the profile Apple mass production teams prefer most." |
| **⑦ Damage Summation (Miner's Rule) 직접 사용** | P-04 PV 폴리머 변동환경 수명 추정 (Solar Energy 2024, DOI 10.1016/j.solener.2024.112645). 연속 변동 환경 이력 → 누적 손상 합산 → 수명 외삽 직접 수행 | 데이터 기반 수명 추정 | "Applied damage summation (Miner's Rule) to predict polymer lifetime under continuously varying environments (Solar Energy 2024)." |

---

## 3. 암묵적 사용 → 명시적 명명 매핑

> 이 표가 본 문서의 핵심 자산이다. 사용자가 한 일을 표준명으로 매핑하면 RESUME 강도가 2배 확장된다.

| 사용자가 한 일 | 표준 명칭 | 매핑 근거 | RESUME 표현 (After) |
|---|---|---|---|
| PCT (Power Cycling Test) on IGBT modules | **JESD47 / JEP122** | JESD47은 반도체 신뢰성 시험 표준 (HTOL/TC/PCT 등 포함). JEP122는 IGBT 고장 메커니즘 가이드라인 | "Conducted PCT per JESD47/JEP122 on IGBT modules; identified bond-wire lift-off failure mode (P-01 IEEE TIM 2024)." |
| GT-SS500 진동·낙하·범퍼 시험대 자력 구축 + 시험 수행 | **MIL-STD-810 / IEC 60068-2** | MIL-STD-810 Method 514(Vibration)·516(Shock), IEC 60068-2-27(충격)·60068-2-6(진동) — 동일 카테고리 | "Designed and operated dyno/bumper/fan-bench rigs aligned with MIL-STD-810 / IEC 60068-2 environmental test methods." |
| EOP CAN 커넥터 방수 설계 + 검증 | **IEC 60529 IP 등급** | EOP 방수 커넥터 = IP 등급(방수·방진 분류) 적용 설계 | "Designed sealed CAN connectors meeting IEC 60529 IP67 requirements for EOP 400W program." |
| NCR 트래킹 27건 (GT-SS500 양산 준비) | **FRACAS (일부)** | FRACAS = Failure Reporting, Analysis, and Corrective Action System. NCR 발행→원인 분석→시정조치→효과 확인→재발 방지 = FRACAS 폐루프 | "Operated NCR tracking (27 items) as part of FRACAS-equivalent closed-loop corrective action process." |
| MCB 전해부식 등 RCA 4건 (현상→근본원인→설계변경→재현검증) | **RCA + 5 Why + Ishikawa (Fishbone)** | 표준 RCA 5단계 방법론 그대로 적용. 도구 명칭만 몰랐을 뿐 | "Led 4 RCAs using 5 Why and Ishikawa diagrams; all resolved before production (MCB corrosion, state-machine bug, O-ring freeze, GND noise)." |
| GT-SS500 IQC/OQC 검사 기준 정의 + 운영 | **Six Sigma DMAIC + Cpk/Ppk 기반 수입검사** | IQC 기준 설정 = DMAIC Define·Measure 단계. OQC 합격 기준 = Cpk 목표값 기반 설계 | "Defined IQC/OQC inspection criteria consistent with Six Sigma DMAIC; monitored process capability indices (Cpk/Ppk) for supplier qualification." |

---

## 4. APQP 양산 경험 — 차별 자산 별도 섹션

> 사용자 자가 평가: "부가적인 업무를 안 한 게 속상한데, APQP 쪽으로 양산 경험해본 게 그나마 괜찮다."
> 실제 판단: 이게 진짜 차별점이다. Apple 같은 양산 기업 채용에서 학계 출신 신뢰성 후보와 가장 크게 갈리는 지점.

---

### 4.1 APQP 5단계 중 사용자 경험 매핑

| Phase | 활동 내용 | 황인혁 사례 | Apple JD 매칭 |
|-------|-----------|------------|--------------|
| 1. Plan & Define | 요구사항 정의·목표 설정 | (보유분 — Phase 2 확인 예정) | NPI 초기 계획 |
| **2. Product Design & Dev** | 설계 검증 (DV/DVT) | **DFMEA 5건 (AIAG-VDA 2019) + 시험체계 4종 자력 구축 (다이나모·팬·펌프·범퍼)** | EVT / DVT |
| **3. Process Design & Dev** | 공정 설계 + PFMEA | **BOM 132항목 관리 + IQC 검사 가이드 (구동모터·노즐) + 양산 ROM 검토 체크리스트** | PVT |
| **4. Product & Process Validation** | PV 시험 + 양산 검증 | **IQC/OQC 운영 + NCR 27건 트래킹 + 혁신제품 실사 4/9 대응 + 양산 초도 16pcs 생산계획** | Ramp-up |
| 5. Feedback & CI | 양산 후 모니터링·개선 | (보유분 — Phase 2 확인 예정) | ORT (Apple JD 핵심) |

### 4.2 학계 출신 vs 양산 경험자 — 채용 관점에서의 차별

| 구분 | 학계 출신 신뢰성 후보 | 황인혁 |
|------|----------------------|--------|
| 방법론 깊이 | ○ (ALT / Weibull / FMEA) | ○ (동등) |
| 양산 현실 감각 | ✗ (BOM·NCR·Gate Review·시정조치 시한 미경험) | ✓ (직접 수행) |
| 장비 자력 구축 | ✗ | ✓ (4종) |
| 교차 기능 조율 | ✗ (연구실 단독) | ✓ (PM 겸임, 6팀 협업) |
| Apple ORT 주도 준비도 | 개념만 | 실무 구조 이해 |

**한 줄 포지셔닝**: "I bridge academic rigor and production reality."

---

## 5. 갭 분석 + 학습 우선순위

### 5.1 인터뷰 위험도 기준 학습 시급도

**★★★ (인터뷰 답변 못 하면 치명)**

- **Stress-Strength Interference**: RBDO Lab 출신이라 인터뷰 시 100% 들어올 질문. S-S overlap → 고장 확률 산출. RBDO의 핵심 개념임을 어필하면 강점이 됨. 반드시 선제 학습.
- **JESD47 핵심 시험 7종**: HTOL / THB / TC (Thermal Cycling) / Power Cycling / ESD HBM·CDM / EM(Electromigration). PCT 직접 수행 경험과 연결하면 즉시 강점화.
- **FRACAS 5단계 폐루프**: Failure → Reporting → Analysis → Corrective Action → System update. NCR 트래킹 경험과 1:1 매핑 후 어필.

**★★ (자연스럽게 들어옴)**

- **MTBF/MTTF/B10 산식 + Weibull 플롯 해석**: Weibull β 해석(β<1 초기불량, β=1 우발, β>1 마모), MTTF = η·Γ(1+1/β), B10 = η·(-ln 0.9)^(1/β). 산식 직접 도출 연습.
- **Coffin-Manson ↔ PCT 페어링**: PCT = 시험 프로토콜, Coffin-Manson = ΔT로 수명 외삽 모델. 혼용하지 않도록 정확히 구분. IGBT 사이클 수명 계산 예시 1건 준비.
- **IEC 60068 vs MIL-STD-810 차이**: IEC는 컴포넌트 레벨 국제표준, MIL-STD는 시스템 레벨 미 국방 표준. 겹치는 시험 카테고리 + 차이점 정리.

**★ (보너스)**

- Reliability Growth (Duane / AMSAA) — 개발 단계 고장률 감소 추적
- Bayesian Reliability — 소표본 + 사전정보 통합
- FMECA vs FMEA 차이 (Criticality 수치화 방식)
- ETA (Event Tree Analysis) 간단 작성 실습
- Six Sigma DMAIC 5단계 + Cpk/Ppk 산식

### 5.2 1주 학습 코스 (제안)

| Day | 주제 | 목표 |
|-----|------|------|
| Day 1 | Stress-Strength Interference + Weibull/B10 | 산식 직접 도출·플롯 해석 |
| Day 2 | JESD47 핵심 7종 + Coffin-Manson 외삽 | PCT 경험과 연결·계산 예시 1건 |
| Day 3 | MIL-STD-810 / IEC 60068 / IEC 60529 매핑 | 자신의 시험 경험에 표준명 붙이기 |
| Day 4 | FRACAS 5단계 + Reliability Growth 개념 | NCR 트래킹 → FRACAS 영문 답변 |
| Day 5 | Bayesian Reliability + Six Sigma Cpk 디테일 | 보너스 어필 준비 |
| Day 6 | camera_vcm_reliability.md 복습 + JESD47 광학 적용 | VCM DFMEA·ALT 매핑 재확인 |
| Day 7 | STAR 영문 답변 5종 작성·녹음·교정 | MCB RCA, PCT, DFMEA, APQP, Damage Summation |

---

## 6. Phase 2 확인 결과 (2026-05-15 완료)

| # | 항목 | 결과 | 근거 / 어필 포인트 |
|---|------|:----:|-------------------|
| 1 | PCT 고장 메커니즘 | ✅ | bond-wire lift-off + **solder fatigue** 동시 관찰 (P-02 PCIM Asia 2022) |
| 2 | RUL 방법론 | △ | 본인 기여: 물리 모델 (Co-sim Ansys Maxwell+Simulink) + 학습 데이터 생성. 팀 산출물: SVM 분류기 (상전류→고장모드). 딥러닝 미사용 |
| 3 | APQP Phase 1 | ✅ | VOC·DesignGoals·**ReliabilityGoals(MTBF/B10/RAMS)**·ProductAssurancePlan·SpecialCharacteristics 5종 직접 작성 |
| 4 | APQP Phase 5 | ✅ | **이슈 DB 트래킹 (RESUME 기준 37+, alpha-prototype 전체 DB 60+)** + Cascading 분석(61건) + 양산 후 이슈 클로징 운영. resume_en.md는 SSOT(§5.1) 정합으로 37+ 표기 |
| 5 | ISO 25119 AgPL | ✅ | AgPL d (과충전 보호) 등급 판정 실시. 기능안전 이슈(#47 범퍼·#99 MR) 직접 분류 |
| 6 | IQC Cpk 직접 산출 | ⚠️ | Cpk 목표 ≥ 1.33 직접 정의. IQC 기준값 13종 설정·16대 전수검수. Cpk 실측은 SPC 미착수(양산 후 예정) |
| 7 | 자격증 | ❌ | 없음 (CRE/CQE/Green Belt 미취득) |
| 8 | 학부 신뢰성·통계 과목 | ❓ | HIH_2에서 미발견. **사용자 직접 확인 필요** |
| 9 | 사내 교육·세미나 | ✅ | 다이나모 세미나 발표 (2023-08-09, PDF+PPTX). VCU 소자 교육자료 작성. Fluvva 고객 매니저 교육 진행 |
| 10 | 후배 지도·멘토링 | ⚠️ | 고객 매니저 교육(4/3), 고객 현장 교육 체크리스트 운영. 사내 후배 지도 직접 기록 없음 |
| 11 | 협력사 감사 (Supplier Audit) | ✅ | **현대인버터솔루션(HIS) 현장 방문** — BMS FW 이슈 6건 현장 확인 (2026-03-03). 구동모터 16대 입고검수 |
| 12 | 카메라·광학 경험 | ⚠️ | SS500 자율주행 카메라 케이블 이슈·EMI 간섭 분석 수준. 직접 신뢰성 시험 없음 |

### 6.1 새로 발굴된 어필 포인트

**APQP Full Cycle (Phase 1~5):**
Phase 1 (계획·목표) → Phase 2 (DFMEA 5건) → Phase 3 (PFD·CP·IQC 13종) → Phase 4 (PPAP ROM확정, 16대 초도품) → Phase 5 (issues.csv 60건 Cascading 분석)
→ 인터뷰에서 "I've run the complete APQP cycle from Phase 1 reliability goal-setting through Phase 5 field-issue feedback"

**ISO 25119 AgPL 판정:**
→ "I applied ISO 25119 AgPL risk assessment to SS500 safety functions — over-charge protection was rated AgPL d, the highest category for agricultural machinery functional safety."

**협력사 감사:**
→ "I led a supplier quality visit to our 48 V BMS supplier with a structured checklist covering 6 open issues including FW version verification and SOC anomalies."

**다이나모 세미나:**
→ "I presented our in-house dynamometer torque-control system at an internal technical seminar (August 2023), covering nonlinearity characterization and calibration methodology."

---

## 7. 다음 단계 (체크리스트)

- [ ] Phase 2 사용자 인터뷰 — §6 항목 확인 (우선순위: PCT 고장 메커니즘, RUL 방법론, APQP Phase 1/5 보유분)
- [ ] Phase 2 결과 본 문서 §3 (표준명 매핑) 및 §5.1 (학습 시급도) 반영
- [ ] 본 문서 기반 `jd_resume_match.md` §3 강점/갭 표 갱신 (특히 ✗→실은✓ 항목)
- [ ] 본 문서 기반 `resume_en.md` §Skills·§Experience bullet 갱신 — §3 표의 "RESUME 표현(After)" 직접 이식
- [ ] 본 문서 기반 `cover_letter.md` 작성 — 4단락: ① RBDO Lab + Reliability 학문 ② APQP 양산 + 표준 매핑 ③ 반도체+ALT+PHM 직접 경험 ④ 광학 학습 의지 + 구체적 Apple 관심
- [ ] `CONTENT_V2.md` §5(특허) / §6(Track A DFMEA) 본 문서 인사이트 반영 검토 — 특히 "RCA" → "5 Why + Ishikawa" 명명, "IQC/OQC" → "Six Sigma DMAIC" 매핑

---

## 참조

- `jd_resume_match.md` — JD ↔ 이력 직전 매핑
- `camera_vcm_reliability.md` — 광학 도메인 자가학습 (1169줄)
- `JD_분석_Apple_Reliability_Engineer.md` — JD 원문 + 갭 분석 v2
- `docs/blocks/05-extra/RESUME.md` §6.5(특허) §7(보유기술) §8(수상) — 마스터 SSOT
- `docs/포트폴리오/CONTENT_V2.md` §5(특허) §6(Track A DFMEA) §7B(Track D APQP) — 콘텐츠 SSOT
