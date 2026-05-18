# Apple Reliability Engineer JD ↔ 황인혁 팩트 매칭 (v1 초안)

> 작성: 2026-05-18 | 목적: 사용자 직접 어필 메시지 결정용 | 모든 팩트는 RESUME.md SSOT 직접 인용

---

## 0. 종합 스코어

| 영역 | O | △ | ✗ |
|------|:-:|:-:|:-:|
| Minimum Qualifications (4) | 2 | 2 | 0 |
| Preferred Qualifications (6) | 3 | 2 | 1 |
| Responsibilities (4) | 4 | 0 | 0 |
| **합계 (14)** | **9** | **4** | **1** |

---

## 1. Minimum Qualifications (4개) — 필수

### MQ-1. Mechanical / Electrical Engineering / Image Science 학위 — **O**

| Apple 요구 | 내 팩트 (RESUME §3) |
|---|---|
| BS+ in ME/EE/Image Science | 건국대 기계공학부 학사 2021.02 (GPA 3.24/4.5) |
| MS 우대 | 건국대 대학원 기계설계학과 석사 2023.02 (GPA 3.77/4.5) |
| 신뢰성 도메인 | **RBDO Lab** (Reliability-Based Design Optimization, 지도교수 김남수) |

**어필 메시지**: "Reliability was the focus of my master's research, not a side topic — RBDO Lab is named after Reliability-Based Design Optimization."

---

### MQ-2. 모듈 신뢰성 시험 실무 (camera, VCM, lens, semiconductor, vibrator, etc.) — **△**

| Apple 컴포넌트 | 내 직접 경험 | 매칭 | 근거 |
|---|---|:--:|---|
| Semiconductor | **IGBT PCT** (Power Cycling Test) 직접 수행, bond-wire lift-off 검증 | O | P-01 IEEE TIM 2024 3저자, DOI 10.1109/TIM.2024.3472910 |
| Vibrator (진동/모터) | IPMSM ALT 관찰 참여, dual sensor architecture (phase current/온도/shaft displacement/vibration) | △ | P-05 J. Power Electron. 2024 6저자, DOI 10.1007/s43236-024-00810-8 |
| Camera / VCM / Lens | 직접 경험 **없음** | ✗ | camera_vcm_reliability.md 자가학습 진행 중 |

**플러스**: 시험체계 4종 자력 구축 (RESUME §5.3) — 다이나모 0.008% / 팬 7.9→12.4 m/s / 펌프 / 범퍼 0.082m
**갭**: 광학 모듈 직접 경험 ✗. JD 표현 "etc."로 열거형 — 반도체/진동기만이라도 인정 가능 여부가 키
**리스크**: 광학을 "the real gap"으로 솔직 인정 → 방법론(ALT/PCT/multi-sensor) 이식 가능성으로 전환

---

### MQ-3. Consuming product FA 경험 — **△**

| Apple 요구 | 내 팩트 (RESUME §5.1) |
|---|---|
| 소비자 제품 기반 기술·불량 분석 | GT-SS500 RCA 4건: MCB 전해부식(#204) / LCD 상태머신(#79) / 펌프 동파 오링 / GND 노이즈 |
| 폐루프 corrective action | **NCR 27건 closed-loop** (Failure→Reporting→Analysis→CA→System) |
| 교차기능 조율 | 6팀 cross-functional, GT-SS500 PM 겸임 |

**갭**: GT-SS500은 농업용 산업기계. "consuming product"(iPhone/iPad 등 소비자 가전)와 도메인 차이
**어필**: FA 5단계 방법론과 closed-loop NCR 구조는 동일. **컴포넌트 도메인 차이만**

---

### MQ-4. 데이터 분석·해석 — **O**

| Apple 요구 | 내 팩트 |
|---|---|
| 시험 데이터 통계 분석 | SVPWM/DPWM 검증 **2,932 데이터 포인트** (RESUME §5.2) |
| 모델-실험 정합성 | Co-simulation (Ansys Maxwell FEM + MATLAB/Simulink) 다양 운전조건 실험 검증 (T-01 학위논문) |
| 다중센서 분석 | IPMSM ALT 4중 센서 융합 (P-05) |
| 환경변동 수명추정 | **Damage Summation (Miner's Rule)** — PV 폴리머 (P-04 Solar Energy 2024 4저자) |
| AI 진단 | **PHM SoC** (산자부 과제 2021-2022) — SVM fault classification |

**어필 메시지**: physics-informed + statistical 양쪽

---

## 2. Preferred Qualifications (6개) — 우대

### PQ-1. CRE certification — **✗**

| Apple 요구 | 내 상태 |
|---|---|
| ASQ Certified Reliability Engineer | 미취득 |

**솔직 답변**: "Currently studying ASQ CRE Body of Knowledge — Weibull, MTBF, Stress-Strength Interference, FRACAS. 1-year acquisition target."

---

### PQ-2. SPC + quality control — **△**

| Apple 요구 | 내 팩트 |
|---|---|
| SPC (Statistical Process Control) | 명시적 SPC 차트(X-bar/R, p, c) 운영 자료 없음 |
| Quality control | IQC/OQC 검사 가이드 직접 정의, **Cpk ≥ 1.33 acceptance criteria** (resume_en L40) |
| 폐루프 품질 | NCR 27건 closed-loop |
| 산출물 | APQP Phase 1-5, DFMEA/PFMEA, DRBFM, Boundary Diagram |

**어필**: Cpk 기준 적용 + IQC/OQC 직접 정의
**갭**: SPC 차트 도구(Minitab/JMP) 직접 운영 자료 없음. Six Sigma 인증도 없음

---

### PQ-3. Business level EN + KR — **O (조건부)**

| Apple 요구 | 내 팩트 (RESUME §9) |
|---|---|
| 한국어 | 원어민 |
| 영어 | TOEIC 920 (2021-2022 응시, **유효기간 만료**) / TOEIC Speaking IH 140 Lv.6 (만료) |
| **영문 실증** | **IEEE TIM 2024 · Solar Energy 2024 · J. Power Electron. 2024** 공저 3편 + 학회 영문 발표 4편 (PCIM Asia, PHM Asia-Pacific) |

**어필**: 점수보다 **영문 저널 공저 3편 + 학회 4편**이 실증력 강함
**갭**: 점수 재응시 예정 (B5-04 PREPARED)

---

### PQ-4. Communications + Leadership — **O**

| Apple 요구 | 내 팩트 |
|---|---|
| 리더십 | GT-SS500 PM 겸임, 6팀 cross-functional 조율 |
| 멘토링 | 주니어 엔지니어 멘토링 (CAN, 상태머신, DFMEA) |
| 공급사 조율 | BMS 공급사 quality review 6 agenda 주도 |
| 발표 | 사내 세미나 (다이나모 0.008%) |

---

### PQ-5. AI or ML experience — **O (강함)**

| Apple 요구 | 내 팩트 |
|---|---|
| 학술 AI/ML | **PHM SoC** (산자부 2021-2022) — SVM fault classification on phase-current signatures (IPMSM demagnetization/winding-fault) |
| 응용 LLM | 3계층 LLM 라우팅 (Opus/GLM/Ollama), Claude Code · MCP · 8개 프로젝트 자동화 |
| 학습 | PyTorch · LangChain · Docker |

**어필 메시지**: physics-informed ML — digital twin(Ansys FEM)으로 고장 메커니즘 이해 → SVM으로 실측 신호 deviation 추적. **field usage model**(JD R-2 원문)에 직접 매핑

---

### PQ-6. Gumi 근무 가능 — **사용자 결정**

확인 필요: 거주지·통근 조건. 면접 단계 명시.

---

## 3. Responsibilities (4개) — 업무

### R-1. ORT in development and sustaining stage — **O**

| Apple 업무 | 내 매핑 |
|---|---|
| 개발 단계 신뢰성 시험 | EOP 400W 다이나모 토크제어 비선형성 **0.008%** 직접 구축 |
| 양산 직전 검증 | GT-SS500 APQP Phase 2-3 primary, 시험체계 4종 자력 구축 |
| 양산 sustaining | APQP Phase 4(PPAP)/Phase 5(60+ field issue) supporting |

---

### R-2. Component/module reliability + field product usage model — **O**

| Apple 업무 | 내 매핑 |
|---|---|
| 컴포넌트 신뢰성 | **P-01 IGBT PCT** (IEEE TIM 2024 3저자) |
| 모듈 신뢰성 | **P-05 IPMSM ALT** dual sensor architecture (J. Power Electron. 2024 6저자) |
| **field usage model** ← JD 원문 | **P-04 Damage Summation** for PV polymer under continuously varying environments (Solar Energy 2024 4저자) |

**어필 메시지**: "P-04 directly addresses 'continuously varying environments → lifetime prediction via damage summation' — which is the field-usage-model methodology Apple's JD calls out."

---

### R-3. ORT 이슈 식별 + 우선순위화 — **O**

| Apple 업무 | 내 매핑 |
|---|---|
| 이슈 식별 | **DFMEA #201/#210 Step 1-7** |
| 우선순위화 | **AP=H 5건** (Action Priority High) 도출 → 양산 전 종결, RPN(S×O×D) |
| 시스템 분석 | 60+ field-issue database → 6 failure chains 식별 |

---

### R-4. Deep FA + cross-functional corrective action — **O**

| Apple 업무 | 내 매핑 |
|---|---|
| Deep FA | RCA 4건: MCB → IEC 60947-2 등급 교체 / 상태머신 → 재설계 / 펌프 오링 → 저온 재설계 / GND 노이즈 → DFMEA 반영 |
| 교차기능 조율 | 6팀 + BMS 공급사 quality review 6 agenda 주도 |
| Closed-loop | **NCR 27건** Failure→Reporting→Analysis→CA→System |

---

## 4. 핵심 어필 메시지 후보 (사용자 선택)

| # | 메시지 | 근거 강도 |
|---|--------|:--------:|
| M1 | "Reliability was the focus of my master's research, not a side topic" — RBDO Lab + IEEE TIM 2024 + 학회 수상 2건 | ★★★ |
| M2 | "Bridge between academic rigor and production reality" — RBDO 연구 + GT-SS500 APQP 풀사이클 | ★★★ |
| M3 | "Physics-informed ML for reliability" — Co-simulation digital twin + SVM fault classifier (PHM SoC) | ★★★ |
| M4 | "I build the infrastructure when it doesn't exist" — 시험체계 4종 자가 구축 | ★★ |
| M5 | "Closed-loop FA at scale" — NCR 27건 + RCA 4건 + DFMEA AP=H 5건 | ★★ |
| M6 | "Field usage model is a methodology I've already published" — Damage Summation (P-04 Solar Energy 2024) | ★★★ |

---

## 5. 솔직히 인정할 갭

1. **광학 도메인 (camera/VCM/lens) 직접 경험 ✗** — 자가학습으로 보완 중. 방법론 이식 가능성으로 전환.
2. **소비자 가전 FA 직접 경험 ✗** — 산업기계 RCA 4건의 방법론 동일.
3. **CRE 자격증 ✗** — 학습 시작, 1년 내 응시.
4. **SPC 차트 도구 (Minitab/JMP) 명시 자료 부족** — Cpk/IQC-OQC로 우회.
5. **TOEIC 점수 만료** — 영문 저널 공저 3편으로 실증.
