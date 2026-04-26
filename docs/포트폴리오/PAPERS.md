# 논문 / 학회 발표 SSOT

> 최종 수정: 2026-04-26
> 위치: `docs/포트폴리오/PAPERS.md` (SSOT)
> 적용 페이지: `src/pages/cases/patent/index.astro` 하단 "관련 연구 — 핵심 논문" 섹션
> 소속: 건국대학교 김남수 (Namsu Kim) 교수 연구실 (PHM·신뢰성 기반 설계 최적화)
> 검증: Google Scholar · DBLP · IEEE Xplore · Springer · RISS (2026-04-26)

---

## 0. 학위논문 (석사) — RISS 확정

### T-01. 석사 학위논문 (2023)
- **국문 제목**: 전자기 해석을 이용한 매입형 영구자석 동기 전동기의 고장 진단 시뮬레이션에 관한 연구
- **영문 제목**: Fault Diagnosis Simulation of Interior Permanent Magnet Synchronous Motor using Electromagnetic Analysis
- **저자**: 황인혁 (Inhyeok Hwang)
- **소속**: 건국대학교 대학원 **기계설계학과** (국내석사)
- **연도**: 2023 (학위수여 2023-03-22)
- **지도교수**: 김남수 (Namsu Kim) — RBDO Lab
- **페이지 수**: 49p
- **RISS control_no**: `f678963f23f2e418ffe0bdc3ef48d419`
- **RISS 링크**: https://www.riss.kr/search/detail/DetailView.do?p_mat_type=be54d9b8bc7cdb09&control_no=f678963f23f2e418ffe0bdc3ef48d419
- **핵심 기여**: flux-state variable model + FEA로 IPMSM의 자기포화 효과 포함 시뮬레이션. 모터 구동 시스템 + 인버터 제어와 Co-simulation. 다양한 운전 조건 실험 검증.
- **출처**: RISS 학위논문 DB (2026-04-26 검증)
- **비고**: J-01 ("Co-simulation for Fault Diagnosis of 120kW IPMSM and Experimental Validation")의 한국어 학위논문 정본. 사이트의 P-1 카드 정본.

---

## 1. 황인혁 공저 논문 5편 (2022 ~ 2024)

### P-01. IEEE TIM 2024 ⭐ (인버터 본드와이어 고장 진단) — 정본
- **제목**: Programmable Online Bond-Wire Fault Detection and Location Method for Insulated Gate Bipolar Transistor Using Inverter Output Parameters
- **저자 (순서)**: Jaewook Oh, Inhwan Kim, **Inhyeok Hwang**, Bowook Choi, Namsu Kim
- **저널**: IEEE Transactions on Instrumentation and Measurement, **Vol. 73, pp. 1-8** (2024)
- **Article No / Document ID**: 10726721
- **출판일**: 2024-10-21 (online)
- **DOI**: https://doi.org/10.1109/TIM.2024.3472910
- **링크**: https://ieeexplore.ieee.org/document/10726721/
- **핵심 기여**: IGBT 본드와이어 lift-off 결함을 게이트 신호/콜렉터 단자 접근 없이 인버터 출력 파라미터(3상 전동기 단자 전압)만으로 검출 + 위치 식별. EV 인버터 신뢰성 진단의 핵심 기여.
- **사이트 표기**: patent 페이지 **P-2 카드 정본**.

### P-02. PCIM Asia 2022 (IGBT IPM 전원사이클 시험)
- **제목**: The effect of quasi-DC power cycling on insulated gate bipolar transistor dual-in-line package intelligent power module
- **저자**: Jaewook Oh, **Inhyeok Hwang**, Namsu Kim, et al.
- **발표지**: PCIM Asia 2022 Conference Proceedings (VDE Verlag), 2022-10-26~27, Shanghai
- **링크**: https://ieeexplore.ieee.org/abstract/document/10072319/
- **핵심 기여**: IGBT IPM에 준-DC 전원사이클 시험을 가해 본드와이어/솔더 열화 모드 분석. P-01 IEEE TIM 2024의 기초.

### P-03. PHM Asia-Pacific 2023 (IPMSM 시스템 수준 고장 진단)
- **제목**: System-Level Simulation of 120 kW Interior Permanent Magnet Synchronous Motor Drive for Electric Vehicle Usage Under Various Types of Faults for Fault Diagnosis
- **저자 (순서)**: Woyeong Kwon, Jaewook Oh, **Inhyeok Hwang**, Namsu Kim
- **발표지**: PHM Society Asia-Pacific Conference, Vol. 4 No. 1 (2023)
- **DOI**: https://doi.org/10.36001/phmap.2023.v4i1.3780
- **링크**: https://papers.phmsociety.org/index.php/phmap/article/view/3780
- **핵심 기여**: 120 kW 8극 36슬롯 IPMSM 구동 시스템에 다양한 고장 모드(영구자석 감자·권선 단락 등) 주입 → 상전류 데이터 → SVM 분류. 200 kW 다이나모/NI-9215 DAQ 실험 검증. T-01 학위논문 기반 학회 발표.

### P-04. Solar Energy 2024 (PV 폴리머 수명 예측)
- **제목**: Lifetime prediction of polymeric materials in PV module under continuously varying environments based on damage summation approach
- **저자 (순서, 10명)**: Sikgyeong Choi, Woyeong Kwon, Jaewook Oh, **Inhyeok Hwang** (4번째), Junho Lee, Jeonghae Lee, Gil Hong, Jaewan Kim, Dabo Shim, Namsu Kim (교신)
- **저널**: Solar Energy, Elsevier, **Vol. 276, Article 112645** (2024)
- **DOI**: https://doi.org/10.1016/j.solener.2024.112645
- **출판일**: 2024-06-08 (online) / 2024-07 (print)
- **링크**: https://www.sciencedirect.com/science/article/pii/S0038092X24003402
- **핵심 기여**: 백시트 등 폴리머의 가속수명시험 기반 경험식 수명모델 도출 → 실제 운영조건과 ALT 조건 양쪽에서 누적 damage 계산 → damage summation으로 변동 환경하 수명 추정.

### P-05. Journal of Power Electronics 2024 (IPMSM 가속수명시험)
- **제목**: Identification of failure modes in interior permanent magnet synchronous motor under accelerated life test based on dual sensor architecture
- **저자 (순서, 8명)**: Sikgyeong Choi, Jaewook Oh, Juho Lee, Woyeong Kwon, Jeonghae Lee, **Inhyeok Hwang** (6번째), Jongbum Park, Namsu Kim (교신)
- **저널**: Journal of Power Electronics, **Vol. 24, Issue 5, pp. 822-831** (2024)
- **DOI**: https://doi.org/10.1007/s43236-024-00810-8
- **출판일**: 2024-04-12 (online) / 2024-05 (print)
- **링크**: https://link.springer.com/article/10.1007/s43236-024-00810-8
- **핵심 기여**: PMSM 샤프트에 radial load → 가속수명시험. phase current·온도·shaft displacement·진동 모니터링 → 베어링/샤프트가 가장 취약. 전류와 진동 신호로 failure mode 분류 가능.

---

## 2. CONTENT_V2 §4.3 인용 — 한국 학회 발표 + J-01 검증 결과

> 영문 저널/학회와 별도로 CONTENT_V2.md §4.3에 한국 학회 발표 4건이 SSOT로 등록됨. 일부는 위 §1과 매칭 가능.

### J-01. CONTENT_V2 "주저자 저널 1편" — ⚠ 외부 DB 미확인 (2026-04-26 B1-17b 검증)
- **제목 (CONTENT_V2 §4.3 인용)**: *Co-simulation for Fault Diagnosis of 120kW Interior Permanent Magnet Synchronous Machine and Experimental Validation*
- **검증 결과**: Google Scholar / KCI / Springer / PHM Society / ADS 모두 **일치 항목 0건**.
- **결론**: "주저자 저널" 표현은 근거 부재 가능성 높음. 가장 가까운 출판물은 P-03 (PHM Asia-Pacific 2023, 황인혁 3저자 컨퍼런스) — "주저자 저널"은 아님. 학위논문(T-01) 영문 인용일 가능성도 있음.
- **권장 처리** (사용자 결정 영역):
  - (a) **단일화**: CONTENT_V2 §4.3에서 "주저자 저널 1편" 표현 삭제 → "학위논문 + 공저 저널 3편"로 재정렬
  - (b) **재정의**: J-01 → P-03 (공저 PHM Asia-Pacific 2023)으로 명시
- **사이트 영향**: patent 페이지 P-1 카드는 학위논문(T-01)으로 이미 교체 완료(e4f4c4a). J-01 표현은 사이트에서 사용 안 함. CONTENT_V2 §4.3 텍스트만 잔존.

### C-01. 한국PHM학회 2021 정기학술대회 (우수포스터상)
- **제목**: 시스템 수준 측정값을 이용한 모터 구동 시스템 내 IGBT 개방 고장 진단 기법
- **수상**: 우수포스터상

### C-02. 한국신뢰성학회 2022 춘계학술대회 (최우수발표 논문상)
- **제목**: 전동화 차량 구동시스템의 효율적인 예방정비 기술 개발
- **수상**: 최우수발표 논문상

### C-03. 한국PHM학회 2022 정기학술대회
- **제목**: 전기자동차용 매입형 영구자석 동기전동기의 정밀한 시뮬레이션을 위한 모델링 분석

### C-04. PCIM Asia 2022 → P-02와 동일 논문
- CONTENT_V2 §4.3에 "IGBT Power Cycling"으로 약식 등재되었던 것이 §1 P-02 정본임.

---

## 3. 종합 통계 — 사이트 표기 권장

| 분류 | 건수 | 표기 |
|---|:---:|---|
| 석사 학위논문 | 1 | **건국대 2023, IPMSM 고장진단 시뮬레이션** |
| 영문 저널 (주저자급 공저) | 3 | IEEE TIM · Solar Energy · J. Power Electron. (2024) |
| 영문 학회 발표 | 2 | PCIM Asia 2022 · PHM Asia-Pacific 2023 |
| 한국 학회 발표 | 3~4 | PHM 2021 우수포스터 · 신뢰성 2022 최우수발표 · PHM 2022 등 |
| **수상** | 2 | 한국PHM 2021 우수포스터상 · 한국신뢰성 2022 최우수발표 논문상 |

> Hero/Timeline 카운트 권장:
> - "**저널 3편 · 학회 4편 (수상 2건)**" — 영문 저널 3 + 한국 학회 4
> - 또는 보수적으로 "**저널 1편 · 학회 4편**" (CONTENT_V2 §4.3 기준 그대로)
> - 사용자 결정 영역.

---

## 4. patent 페이지 적용안 (확정)

> `src/pages/cases/patent/index.astro` line 95~ "관련 연구 — 핵심 논문" 카드.

### P-1 카드 — 석사 학위논문 (T-01) ⭐
- 국문 제목: 전자기 해석을 이용한 매입형 영구자석 동기 전동기의 고장 진단 시뮬레이션에 관한 연구
- 영문 부제: Fault Diagnosis Simulation of IPMSM using Electromagnetic Analysis
- 저자: 황인혁 (지도교수 김남수)
- 표기: "석사 학위논문" 배지 + "건국대학교 · 2023"
- RISS 링크 [TODO 추후 control_no 확정 시 추가]

### P-2 카드 — IEEE TIM 2024 (P-01) ⭐
- 제목: Programmable Online Bond-Wire Fault Detection and Location Method for IGBT Using Inverter Output Parameters
- 저자: Oh, Kim, **Hwang**, Choi, Kim (건국대)
- 저널: IEEE TIM, Vol. 73 (2024)
- DOI: 10.1109/TIM.2024.3472910

> 카드 추가 검토 (선택): P-05 J. Power Electron. 2024 (IPMSM dual sensor) — patent 페이지 본문이 IPMSM 고장 진단과 직결되어있어 자연스러운 추가 후보.

---

## 5. 미해결

| 항목 | 작업 |
|---|---|
| ~~T-01 학위논문 RISS control_no~~ | ✅ 2026-04-26 확보 (`f678963f23f2e418ffe0bdc3ef48d419`) |
| ~~P-04 Solar Energy 정확한 권/페이지/DOI~~ | ✅ 2026-04-26 확보 (Vol 276, Art 112645, DOI 10.1016/j.solener.2024.112645) |
| ~~P-05 J. Power Electronics 페이지/Issue~~ | ✅ 2026-04-26 확보 (Vol 24 Issue 5, pp 822-831) |
| ~~P-01 IEEE TIM 출판일/Article No~~ | ✅ 2026-04-26 확보 (Art. 10726721, 2024-10-21 online) |
| P-02 PCIM Asia 2022 정확한 페이지 | VDE proceedings 또는 IEEE 직접 — 잔여 |
| C-01~C-03 한국 학회 발표 PDF | 학회 홈페이지/ResearchGate — 잔여 |
| dcollection.konkuk 직접 링크 | 외부 검색엔진 인덱싱 막힘 — RISS "원문보기" 경유 권장 |
| 2025/2026 신규 논문 | Google Scholar 미발견 (모니터링). IEEE Access 2025 (Noh/Lee/Oh/Kang/Kim)는 황인혁 미포함 확인 |
