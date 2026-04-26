# 논문 / 학회 발표 SSOT

> 최종 수정: 2026-04-26
> 위치: `docs/포트폴리오/PAPERS.md` (SSOT)
> 참조: CONTENT_V2.md §4.3, FACT_CHECK_V1_V6.md
> 적용 페이지: `src/pages/cases/patent/index.astro` 하단 "관련 연구 — 핵심 논문" 섹션

---

## 1. 확정 — 공식 출처 확인 완료

### P-01. PHM Society Asia-Pacific Conference 2023 (공저, 황인혁 3저자)
- **제목**: System-Level Simulation of 120 kW Interior Permanent Magnet Synchronous Motor Drive for Electric Vehicle Usage Under Various Types of Faults for Fault Diagnosis
- **저자 (순서)**: Woyeong Kwon, **Jaewook Oh (오재욱)**, **Inhyeok Hwang (황인혁)**, Namsu Kim
- **발표지**: PHM Society Asia-Pacific Conference, Vol. 4 No. 1 (2023)
- **DOI**: https://doi.org/10.36001/phmap.2023.v4i1.3780
- **링크**: https://papers.phmsociety.org/index.php/phmap/article/view/3780
- **소속**: 건국대학교 (Konkuk University)
- **내용**: 120 kW 8극 36슬롯 IPMSM 구동 시스템에 다양한 고장 모드(영구자석 감자, 권선 단락 등) 주입 → 상전류 데이터 → SVM 분류. 200 kW 다이나모/ NI-9215 DAQ 실험 검증.
- **사이트 표기 권장**: 본 논문이 `오재욱 공저` 핵심 후보. patent 페이지 P-1 카드에 출처 + DOI 링크 적용.

---

## 2. CONTENT_V2 §4.3 인용 — 학회 4편 + 저널 1편

> CONTENT_V2.md §4.3에 SSOT로 등록된 한국 학회/저널 항목. 각 발표 PDF/링크는 추후 확보.

### J-01. 주저자 저널 (1편)
- **제목**: *Co-simulation for Fault Diagnosis of 120kW Interior Permanent Magnet Synchronous Machine and Experimental Validation*
- **상태**: 게재지/연도/링크 [확인필요] — RISS·DBPia·KCI 검색 시 직접 매칭 미발견 (2026-04-26)
- **추정**: P-01(PHM Asia-Pacific 2023)의 저널 확장본일 가능성 / 한국 학술지(전기학회 등) 단독 게재본일 가능성
- **사이트 표기**: 현재 patent 페이지 P-1 카드에 이 제목 사용 중. 정확한 출처 확정되면 교체.

### C-01. 한국PHM학회 2021 정기학술대회 (우수포스터상)
- **제목**: 시스템 수준 측정값을 이용한 모터 구동 시스템 내 IGBT 개방 고장 진단 기법
- **수상**: 우수포스터상
- **링크**: [확인필요]
- **비고**: IGBT 고장 진단 — patent 페이지 P-2 카드의 또 다른 후보

### C-02. 한국신뢰성학회 2022 춘계학술대회 (최우수발표 논문상)
- **제목**: 전동화 차량 구동시스템의 효율적인 예방정비 기술 개발
- **수상**: 최우수발표 논문상
- **링크**: [확인필요]

### C-03. 한국PHM학회 2022 정기학술대회
- **제목**: 전기자동차용 매입형 영구자석 동기전동기의 정밀한 시뮬레이션을 위한 모델링 분석
- **링크**: [확인필요]

### C-04. PCIM Asia 2022
- **제목 (CONTENT_V2)**: IGBT Power Cycling
- **정확한 제목**: [확인필요] — PCIM Asia 2022 proceedings(VDE Verlag)에 황인혁/오재욱 등재 확인됨, 단 정확한 발표 제목 미확보
- **링크 후보**: https://www.vde-verlag.de/books/565911/pcim-asia-2022.html

---

## 3. 학위논문 (석사 졸업논문)

- **저자**: 황인혁 (Inhyeok Hwang)
- **소속**: 건국대학교 대학원
- **연도**: 2023 졸업 (학위수여 2023-03-22 — `archive/personal/91)기타/2024/황인혁-국문-학위수여증명서-202303221543.pdf`)
- **제목**: [확인필요] — RISS·KCI에서 직접 매칭 결과 미발견 (2026-04-26)
- **추정 분야**: IPMSM 모델링·고장진단·PHM (CONTENT_V2 §1.3)
- **체크 방법**: dcollection.konkuk.ac.kr 또는 RISS에서 "황인혁" + 학과/학번 검색

---

## 4. patent 페이지 적용 권장안

> 현재 `src/pages/cases/patent/index.astro` line 95~123 "관련 연구 — 핵심 논문" 2개 카드 적용 중.
> [확인필요] 주석을 다음과 같이 정리:

### 카드 1 (P-1) — 졸업논문/저널
- 제목: *Co-simulation for Fault Diagnosis of 120kW IPMSM and Experimental Validation*
- 출처: 건국대학교 석사 (2023) — **저널 게재 정보는 추후 확정**
- 표기: "석사 졸업논문 · 저널" 배지 + "건국대학교 · 2023"

### 카드 2 (P-2) — 오재욱 공저 (인버터 IGBT 고장)
- **권장**: P-01 PHM Asia-Pacific 2023 논문으로 확정 (DOI 명시 가능)
- 제목: *System-Level Simulation of 120 kW IPMSM Drive for EV Usage Under Various Types of Faults for Fault Diagnosis*
- 저자: Kwon, **Oh**, **Hwang**, Kim (Konkuk University)
- 발표: PHM Society Asia-Pacific Conference, 2023
- DOI: 10.36001/phmap.2023.v4i1.3780
- 표기: "학회 발표 · 공동" + "PHM Asia-Pacific 2023 · 공저자 오재욱" + DOI 링크

> 단, 사용자가 "오재욱 공저 inverter bondwire fault"라고 명시했으므로,
> **bondwire 고장 진단 자체를 다룬 별도 논문**(PCIM Asia 2022 또는 한국PHM 2021)을 우선하길 원할 수 있음.
> 현재 자료로는 PHM Asia-Pacific 2023이 가장 명확한 공저 출처 → 우선 적용 후 사용자 검토.

---

## 5. 미해결 / 후속 작업

| 항목 | 작업 |
|---|---|
| 학위논문 정확한 제목 | dcollection.konkuk.ac.kr 또는 RISS 직접 접속 검색 |
| J-01 저널 게재 정보 | KCI/Web of Science 검색 |
| C-04 PCIM Asia 2022 정확한 발표 제목 | VDE proceedings 구매 또는 사용자 메모/원본 자료 |
| C-01~03 한국 학회 발표 PDF | 학회 홈페이지 또는 ResearchGate |
