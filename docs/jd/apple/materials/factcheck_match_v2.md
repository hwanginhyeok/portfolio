# Apple Reliability Engineer JD ↔ 황인혁 팩트 매칭 (v2)

> 작성: 2026-05-18 | Round 1 컨센서스 10개 반영 | 모든 팩트는 RESUME.md SSOT 직접 인용
> v1 → v2 변경: MQ-2 vibrator 삭제 / IGBT PCT "직접 수행"→"3저자 기여" / R-1 O→△ / R-2 매핑 약화 / SVM SSOT 정합화 / 표준 갭 신설

---

## 0. 종합 스코어 (v2 재평가)

| 영역 | O | △ | ✗ |
|------|:-:|:-:|:-:|
| Minimum Qualifications (4) | 2 | 2 | 0 |
| Preferred Qualifications (6) | 3 | 2 | 1 |
| Responsibilities (4) | 3 | 1 | 0 |
| **합계 (14)** | **8** | **5** | **1** |

> v1 대비: O 9→8 (R-1 하향), △ 4→5. 정직성 우선.

---

## 1. Minimum Qualifications (4개) — 필수

### MQ-1. ME / EE / Image Science 학위 — **O**

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
| Semiconductor (IGBT) | **3저자로 IGBT Power Cycling Test 연구에 기여** — bond-wire lift-off 검출 알고리즘 참여 | △ | P-01 IEEE TIM 2024 3저자, DOI 10.1109/TIM.2024.3472910 |
| Vibrator (햅틱/리니어 액추에이터) | 직접 경험 **없음** | ✗ | (v1 IPMSM 매핑 삭제 — IPMSM은 전동기이며 vibrator 아님) |
| Camera / VCM / Lens | 직접 경험 **없음** | ✗ | camera_vcm_reliability.md 자가학습 진행 중 |
| etc. (시험체계 일반) | 시험체계 4종 자력 구축 (다이나모 0.008% / 팬 +57% / 펌프 / 범퍼 0.082m) | O | RESUME §5.3 |

**v2 정정**: v1의 "IGBT PCT 직접 수행"은 3저자 위치에서 과대. resume_en.md "Co-authored a programmable online bond-wire fault detection..." 표현이 정합. SSOT(RESUME §6.2)도 "Hwang, 3저자" 외 직접 PCT 설계 기여 명시 없음.

**갭 정직 인정**: Apple JD 리스트 첫 컴포넌트가 camera. Camera/VCM/lens/vibrator 4종 중 직접 경험 0건. 면접 단계에서 방법론 이식 가능성으로 전환.

---

### MQ-3. Consumer product FA 경험 — **△**

> v2 정정: JD 원문 "consuming product"는 거의 확실히 "consumer product"의 비표준 표기.

| Apple 요구 | 내 팩트 |
|---|---|
| 소비자 제품 FA | GT-SS500 RCA 4건: MCB 전해부식(#204) / LCD 상태머신 버그(#79) / 펌프 동파 오링 / GND 노이즈 |
| 폐루프 corrective action | **NCR 27건 closed-loop** (Failure→Reporting→Analysis→CA→System) |
| 교차기능 조율 | 6팀 cross-functional, GT-SS500 PM 겸임 |

**갭**: GT-SS500은 농업용 산업기계. consumer electronics(iPhone 등) 직접 경험 없음.
**어필**: FA 5단계 + closed-loop 방법론 동일. 컴포넌트 도메인 차이만.

---

### MQ-4. 데이터 분석·해석 — **O**

| Apple 요구 | 내 팩트 |
|---|---|
| 시험 데이터 통계 분석 | SVPWM/DPWM 검증 **2,932 데이터 포인트** (RESUME §5.2) |
| 모델-실험 정합성 | Co-simulation (Ansys Maxwell FEM + MATLAB/Simulink) 다양 운전조건 실험 검증 (T-01 학위논문) |
| 다중센서 분석 | IPMSM ALT 4중 센서 융합 — 관찰 참여 (P-05 6저자) |
| 환경변동 수명추정 | **Damage Summation** — PV 폴리머 누적 손상 분석 4저자 기여 (P-04 Solar Energy 2024) |
| AI 진단 | PHM SoC (산자부 2021-2022) — 황인혁 담당 역할: **physics-based 모터 모델링 + 고장 모델링 + Co-simulation**. SVM 분류는 팀 산출물 |

**v2 정정**: PHM SoC SVM "직접 구현" 주장 삭제. RESUME §3.2 SSOT 근거에 따라 황인혁 역할은 모터 모델링·Co-simulation. SVM은 팀 산출물로 명확화.

---

## 2. Preferred Qualifications (6개) — 우대

### PQ-1. CRE certification — **✗**

미취득. 면접 답변: "Currently studying ASQ CRE Body of Knowledge — Weibull, MTBF, Stress-Strength Interference."
> v2 옵션: 매트릭스 어필 메시지에서 "studying" 언급 삭제 (HM 페르소나 권고: 약점 강조 효과)

---

### PQ-2. SPC + quality control — **△**

| Apple 요구 | 내 팩트 |
|---|---|
| Quality control (Cpk) | IQC/OQC 검사 가이드 직접 정의, **Cpk ≥ 1.33 (short-term capability target)** for key characteristics |
| 폐루프 품질 | NCR 27건 closed-loop |
| 산출물 | APQP Phase 1-5, DFMEA/PFMEA, DRBFM, Boundary Diagram |

**갭 정직 인정**: SPC 차트(X-bar/R, p, c) Minitab/JMP 직접 운영 자료 없음. Six Sigma 인증 없음.
**v2 추가**: Cpk 표기에 "short-term capability target" 조건 명시. 측정계 R&R 질문 대비.

---

### PQ-3. Business level EN + KR — **△**

| Apple 요구 | 내 팩트 (RESUME §9) |
|---|---|
| 한국어 | 원어민 |
| 영어 점수 | TOEIC 920 (2021-2022, **expired**) / TOEIC Speaking IH 140 Lv.6 (expired). 재응시 예정 |
| **영문 실증** | **IEEE TIM 2024 · Solar Energy 2024 · J. Power Electron. 2024** 공저 3편 + 학회 영문 발표 4편 |

**v2 정정**: v1 "O (조건부)" → **△**. 만료 점수 명시 + 재응시 명시. resume_en.md도 만료 표기 필요.

---

### PQ-4. Communications + Leadership — **O**

| Apple 요구 | 내 팩트 |
|---|---|
| 리더십 | GT-SS500 PM 겸임, 6팀 cross-functional 조율 |
| 멘토링 | 주니어 엔지니어 멘토링 (CAN, 상태머신, DFMEA) |
| 공급사 조율 | BMS 공급사 quality review 6 agenda 주도 |
| 발표 | 사내 세미나 (다이나모 0.008%) |

---

### PQ-5. AI or ML experience — **O**

| Apple 요구 | 내 팩트 |
|---|---|
| 학술 ML 기여 | **PHM SoC** (산자부 2021-2022) — 팀이 SVM fault classification 개발. 황인혁 담당: physics-based co-simulation + 모터/고장 모델링 → SVM 학습 데이터 생성 기반 |
| LLM 응용 (선택적 어필) | 3계층 LLM 라우팅, Claude Code, MCP, 자동화 13종 — **매트릭스에서 어필 약화** (Apple 신뢰성 무관) |

**v2 정정**: v1 "O (강함)"에서 "강함" 약화. SVM 직접 구현 주장 삭제. resume_en.md Skills에서 LLM 자동화 전량 삭제 권고.
**어필 메시지**: physics-informed ML — digital twin으로 고장 메커니즘 정의 + SVM은 팀 산출물로 협력.

---

### PQ-6. Gumi 근무 가능 — **사용자 결정**

확인 필요: 거주지·통근 조건.

---

## 3. Responsibilities (4개) — 업무

### R-1. ORT in development and sustaining stage — **△**

> v2 정정: v1 "O" → **△**. 사유: APQP Phase 2-3은 DVT/PVT 단계이지 정형 ORT(Ongoing Reliability Testing, 양산 후 지속 모니터링)가 아님.

| Apple 업무 | 내 매핑 (정직) |
|---|---|
| Development stage reliability testing | EOP 400W 다이나모 토크제어 비선형성 **0.008%** 직접 구축 (DV equivalent) |
| Production validation | GT-SS500 APQP Phase 2-3 primary (DVT/PVT equivalent), 시험체계 4종 자력 구축 |
| Sustaining stage (양산 후) | APQP Phase 5 supporting — 60+ field issue database tracking, 6 failure chain 식별 |

**어필 메시지**: "Development and validation-stage reliability testing experience (DVT/PVT equivalent within APQP framework); sustaining-stage field issue analysis through APQP Phase 5. Formal ORT protocol design experience is something I would build at Apple."

---

### R-2. Component/module reliability + field product usage model — **△**

> v2 정정: v1 "O" → **△**. 사유: P-04 4저자 + Miner's Rule이 PV폴리머 누적 손상이지 소비자 제품 mission profile/duty cycle modeling은 아님.

| Apple 업무 | 내 매핑 (정직) |
|---|---|
| 컴포넌트 신뢰성 | P-01 IGBT PCT 3저자 기여 (IEEE TIM 2024) |
| 모듈 신뢰성 | P-05 IPMSM ALT 관찰 참여 (J. Power Electron. 2024 6저자) |
| Field product usage model | **방법론 친숙도**: P-04 4저자로 Damage Summation 적용 논문에 기여. continuously varying environments → lifetime prediction 개념 이해. 단, mission profile/duty cycle 직접 정의 경험 없음 |

**어필 메시지**: "Methodology familiarity with continuously varying-environment damage accumulation (co-authored P-04 Solar Energy 2024). I would expect to learn Apple's specific field product usage model framework on the job."

---

### R-3. ORT 이슈 식별 + 우선순위화 — **O**

| Apple 업무 | 내 매핑 |
|---|---|
| 이슈 식별 | **DFMEA #201/#210 Step 1-7** (AIAG-VDA 2019 기준) |
| 우선순위화 | **AP=H 5건** (Action Priority High) 도출 → 양산 전 종결 |
| 시스템 분석 | 60+ field-issue database → 6 failure chains 식별 |

**v2 추가**: 면접 준비 — AP=H 1건 (예: MCB 전해부식 #204)의 before/after S·O·D 등급 숙지.

---

### R-4. Deep FA + cross-functional corrective action — **O**

| Apple 업무 | 내 매핑 |
|---|---|
| **Deep FA** | RCA 4건 (mechanism analysis → corrective action → DFMEA update loop): MCB → IEC 60947-2 등급 교체 / 상태머신 → 재설계 / 펌프 오링 → 저온 재설계 / GND 노이즈 → DFMEA 반영 |
| 교차기능 조율 | 6팀 + BMS 공급사 quality review 6 agenda 주도 |
| Closed-loop | **NCR 27건** Failure→Reporting→Analysis→CA→System (FRACAS-equivalent) |

**v2 추가**: deep FA 방법론 1개 명시 권고 (5-Why, Fishbone, FTA, 8D 중 실제 사용한 것 1개를 resume에 추가). 현재 RESUME에 명시 없음 — 사용자 확인 후 추가.

---

## 4. 핵심 어필 메시지 Top 3 (HM 페르소나 선정)

| # | 메시지 | 근거 |
|---|--------|------|
| **M5** | **"Closed-loop FA at scale"** — NCR 27건 + RCA 4건 (mechanism→CA→DFMEA loop) + DFMEA AP=H 5건. JD R-4 직접 매칭. 면접 5분 설명 가능 (MCB #204 etc.) | ★★★ |
| **M4** | **"I build the infrastructure when it doesn't exist"** — 시험체계 4종 자력 구축 (다이나모 0.008% 정밀). Apple 구미 부품 신뢰성 인프라 운영 팀에 즉시 매칭 | ★★★ |
| **M1** | **"Reliability was the focus of my master's research"** — RBDO Lab(연구실명에 reliability 명시) + IEEE TIM 2024 3저자 + 한국신뢰성학회 최우수발표상 2022 | ★★★ |

> **제외**: M2 (M1+M4 합집합), M3 (physics-informed ML — PHM SoC SVM 직접 구현 주장 약화로 임팩트 감소), M6 (field usage model — 4저자 기반으로 면접 심화 질문 취약)

---

## 5. 솔직히 인정할 갭 (v2 확장)

| # | 갭 | 심각도 | 대응 |
|---|----|:-----:|------|
| 1 | 광학 도메인 (camera/VCM/lens) 직접 경험 ✗ | 🔴 구조적 | 방법론 이식 가능성으로 전환. 자가학습 1주. **이력서/CL에서 1-2줄 최소화** |
| 2 | Vibrator (햅틱) 직접 경험 ✗ | 🟡 중간 | IPMSM은 vibrator 아님 솔직 인정 |
| 3 | Consumer electronics FA 경험 ✗ | 🟡 중간 | 산업기계 RCA 방법론 동일성 어필 |
| 4 | CRE 자격증 ✗ | 🟢 낮음 | "Studying" 언급 삭제, 없는 것은 없다고 |
| 5 | SPC 차트 도구 직접 운영 ✗ | 🟡 중간 | Cpk + IQC/OQC로 우회 |
| 6 | **JESD47 / AEC-Q100 / IEC 60068 / MIL-STD-810 표준 적용 이력 ✗** ← v2 신설 | 🟡 중간 | IGBT PCT가 JEDEC-style 개념과 유사. Apple 학습 의지 |
| 7 | **TOEIC 점수 만료** | 🟡 중간 | 영문 저널 3편 실증. 재응시 예정 명시 (B5-04) |

---

## 6. Resume / Cover Letter 패치 권고 (v2 → v3 액션)

### A. resume_en.md 키워드 보강 (ATS 페르소나 권고)
- [ ] Summary 첫 줄: "Reliability" 명사로 시작 (현재 RBDO Lab 약어 노출)
- [ ] "ORT" 1회 추가 (DVT/PVT-equivalent 표현으로 정직성 유지)
- [ ] "semiconductor" 1회 (IGBT bullet)
- [ ] "SPC" 1회 ("SPC-based Cpk")
- [ ] "failure analysis" 1회 (RCA bullet 앞)
- [ ] "machine learning" 1회 (PHM 섹션)
- [ ] "field product usage model" 5-word 정확 (현재 "product" 누락)

### B. resume_en.md SSOT 정합화 (SME 페르소나 권고)
- [ ] PHM SoC SVM: "team-developed SVM fault classification; my contribution: physics-based co-simulation and fault modeling"
- [ ] Education P-05 bullet: "FTA-driven test design" 삭제 (SSOT 이탈)
- [ ] Cpk 표기: "short-term capability target for key characteristics"
- [ ] "Patents (2 — honest disclosure)" → "Patents (2)" (헤더 단순화)
- [ ] TOEIC: "(expired; retesting planned)" 명시
- [ ] **LLM 자동화 전량 삭제** (Three-tier LLM routing / Claude Code / MCP / 13-skill automation / PM-orchestrator workflow)

### C. cover_letter.md 구조 (HM + ATS 페르소나 권고)
- [ ] Para 5 광학 갭 단락 1문장으로 압축
- [ ] 마지막 단락 긍정 클로징으로 교체 ("That is exactly where I want to work" → 더 액션 지향)
- [ ] AI/ML 단락(Para 4)에 "machine learning" 단어 1회 (현재 0회)

### D. 사용자 결정 적용 결과 (2026-05-18)
- [x] **deep FA 방법론**: **Fishbone (Ishikawa)** — 사용자 선택. RCA 4건 모두 다요인 분석(4M: 사람·기계·재료·방법) 적합. resume v6 L35에 "applying Fishbone (Ishikawa) cause-and-effect analysis" 명시
- [x] **광학 갭 위치**: Para 5 현행 유지 — 강점 축적 후 솔직 인정 흐름
- [x] **TOEIC 만료**: **"(expired)"** — 사용자 선택. 간결, 재응시 언급 없이 만료 사실만
- [x] **구미 근무**: 이력서/CL 침묵, 면접 단계 명시 — 협상 카드 보존
- [x] **SSOT 불일치 3건 정리** — 전부 정직 정리:
  - AIAG-VDA 2019 표기: 매트릭스/resume에서 미사용 (SSOT 근거 없음)
  - 60+/37+ 불일치: resume L33 "60+ field-issue database" → "37+ field-issue database" (RESUME §5.1 정합)
  - SVM 주체: resume L125-126 "the team built an SVM classifier; my contribution: physics-based co-simulation that generated labeled training data"로 분리
