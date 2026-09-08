# NVIDIA Senior Automotive Software Program Manager JD 매핑 — 황인혁

> 작성: 2026-09-06 (초안)
> 출처: Workday cxs JSON 공고 원문 (`JD_원문_Senior_Automotive_Software_Program_Manager.md`, 수집 2026-09-06)
> 자산 출처: `docs/blocks/05-extra/RESUME.md` §4·§5·§7

---

## §1. JD 요건 정리 (원문 기준)

### 이 자리의 실제 미션

NVIDIA **DRIVE 소프트웨어 스택**(DRIVE OS, NDAS, Alpamayo)을 한국 완성차 파트너에
통합·적용·검증하는 프로그램을 처음부터 끝까지 끌고 간다. 한국·인도·중국·미국 크로스펑셔널
조율이 업무의 절반이고, 파트너와 내부 경영진 양쪽의 **1차 창구이자 1차 에스컬레이션 지점**이다.

**업무**
- DRIVE 프로그램 라이프사이클 리드, SW 납품 일정·내용 정렬
- 4개국 팀 조율로 이슈 해소 및 제품 런칭 견인
- 파트너·경영진 1차 창구 / 1차 에스컬레이션
- 차량·시스템 레벨 요구사항 정렬, 리뷰·교환·협상 조율
- 알려진 이슈·버그 추적/우선순위화, 릴리스 할당, 검증 추적, RCA

**필수 (What we need to see)**
- AI·LLM·Transformer·CPU/GPU 아키텍처 **일반 지식**
- 프로그램 관리 개념 **일반 지식** (태스크 계획, 애자일, 리스크 관리)
- 공학/전산 관련 학위 (BS/MS/PhD)
- **automotive software 개발 6년 이상** (ADAS·AV 선호)
- 자율주행 시스템·센서·차량 버스 통신 규격·SoC·임베디드 SW 원리 이해
- C/C++/Python, QNX 또는 Linux **일반 지식**
- 빌드 파이프라인·리포지토리·CI/CD·컨테이너화 이해
- **복잡한 자동차 프로그램을 양산(series production)까지 리드한 입증된 경험**
- 커뮤니케이션·조직화·시간관리·우선순위
- 파트너 사이트 정기 방문 의지

**우대 (Ways to stand out)**
- Automotive SPICE, ISO 26262, ISO 21448
- 복잡한 임베디드 C++ 시스템 실무 개발
- 한국어 유창
- 로컬 ADAS/AV 업계 네트워크

---

## §2. 자산 매트릭스 — JD 요건 × 보유 근거

| JD 요건 | 판정 | 근거 (RESUME.md) |
|---|:---:|---|
| **automotive SW 개발 6년 이상 (ADAS/AV 선호)** | **미충족 (핵심)** | GINT 2023-02 ~ 현재 = **3년 7개월**. 연구 2년 6개월을 더해도 6년 미만이고, 그 경력은 SW 개발이 아니라 모터 모델링·PHM 시뮬레이션이다 |
| **복잡한 자동차 프로그램을 양산까지 리드** | **부분 충족** | GT-SS500 **풀사이클** — 알고리즘 → DFMEA #201/#210 Step 1~7 → BOM 132 → 양산 초도 16pcs 출하. APQP Phase 2~3 운영 (§4/§5.1). 단 **농업 자율주행 플랫폼**이지 차량 ADAS/AV 프로그램이 아니다 |
| 차량 버스 통신 규격 이해 | **충족 (강)** | CAN·CAN-FD, **DBC 4종 직접 작성/관리**, BusLoad 분석, 5노드 분산 제어 토폴로지(VCU↔구동×2↔팬↔펌프↔BMS), BREAKING CHANGE 4건 사전 검출 (§5.1/§7.3) |
| SoC·임베디드 SW 원리 이해 | **충족** | STM32 · NXP MC9S12ZVMC · Infineon TC23x · RTOS · 3모드 상태머신 · 모터 컨트롤러 FW 코드리뷰 (§7.2) |
| 프로그램 관리 개념 (계획·리스크) | **충족** | 주니어 PM 겸임. WBS, APQP Phase 게이트, DFMEA 리스크 우선순위(AP=H 5건), BOM 재고 미확보 23건 사전 식별, NCR 27건 (§7.7) |
| 이슈 추적·우선순위화·RCA | **충족** | 이슈 128건 트래킹(2026-08), 직접 담당 30건. 현장 RCA 4건(MCB 전해부식·LCD 상태머신·펌프 동파·GND 노이즈)을 근본원인까지 (§4/§5.1) |
| 학위 (공학) | **충족** | 건국대 기계설계 학사 + **석사**(IPMSM 모델링·고장진단) |
| C/C++/Python (일반 지식) | **충족** | Python · C/C++ · Git · Linux (§7.8) |
| QNX 또는 Linux | **부분 충족** | Linux 보유. **QNX 무경험** |
| CI/CD·리포지토리·컨테이너화 | **부분 충족** | Git 실무. Docker는 **학습·활용 단계** 표기 (§7.8) |
| AI·LLM·Transformer·GPU (일반 지식) | **부분 충족** | 3계층 LLM 라우팅 운영, MCP, PM 오케스트레이터(8개 프로젝트), 자동화 스킬 13개. PyTorch·LangChain은 학습 단계 (§7.8). GPU 아키텍처 지식 근거는 없음 |
| 커뮤니케이션·조직화 | **충족** | 혁신제품 실사 4/9 대응, 농진원 대응, DBC·검사 가이드·체크리스트 문서화 이력 |
| 한국어 유창 (우대) | **충족** | 원어민 |
| 영어 | **부분 충족** | TOEIC 920 / Speaking 140(Lv.6 IH) — **둘 다 만료**. 4개국 조율이 업무의 중심이라 실사용 수준이 관건 |
| **자율주행 시스템·센서 이해** | **미충족** | GT-SS500의 자율주행 3모드 상태머신과 ADT PC 페일세이프 핸드셰이크가 최근접. **Radar/Lidar/Camera 퍼셉션 스택 무경험** |
| **ASPICE · ISO 26262 · ISO 21448** | **미충족** | ISO 13849 reading, Functional Safety 매핑 **학습 단계**뿐 (§7.3) |
| **임베디드 C++ 시스템 개발 (우대)** | **부분 충족** | 모터제어 FW는 C 중심. 복잡한 C++ 시스템 개발 근거 없음 |
| **로컬 ADAS/AV 네트워크 (우대)** | **미충족** | 근거 없음 |

---

## §3. 전용 가능한 것 — 지원한다면 이 각도

연차를 되돌릴 수는 없다. 지원한다면 **"자동차 SW PM"이 아니라 "시스템을 양산까지 끌고 간
엔지니어 겸 PM"**으로 서는 것이 유일하게 정직한 각도다.

### 축 1 — 풀사이클을 혼자 관통한 이력

알고리즘 설계에서 시작해 DFMEA, BOM 132 항목, 초도 생산계획, 현장 이슈 128건·고객 인도 5대까지
**한 제품의 전 구간**을 통과했다. JD가 요구하는 "led complex programs to series production"은
규모가 다르지만 **구조는 같다**. 이 자리가 잡는 이슈 추적 → 릴리스 할당 → 검증 추적 →
RCA 루프는 GT-SS500에서 NCR 44건(2회)으로 돌린 그 루프다.

### 축 2 — 분산 시스템의 인터페이스를 정의하고 지킨 경험

5노드 CAN 토폴로지에서 DBC 4종을 직접 관리하며 **BREAKING CHANGE 4건을 배포 전에 잡았다.**
파트너와 요구사항을 정렬하고 변경을 협상하는 일의 축소판이다.

### 축 3 — 크로스펑셔널 1차 창구 경험

혁신제품 실사(4/9)와 농진원 대응에서 외부 기관과 내부 개발 사이의 창구를 맡았다.
JD의 "first point of contact and first level of escalation"과 성격이 같다.

---

## §4. 갭 분석 — 정직하게 남는 것

| 갭 | 메울 수 있나 | 판단 |
|---|---|---|
| automotive SW 6년+ | **불가** | 시간의 문제. 표기로 넘길 수 없다 |
| ADAS/AV 스택 경험 | **불가** | 퍼셉션·플래닝·센서 융합 무경험 |
| ASPICE / ISO 26262 / 21448 | 학습 가능하나 지금은 없음 | 면접 전 개념 학습은 가능. "안다"고 쓰지는 않는다 |
| QNX | 없음 | Linux로 대체 설명 |
| 로컬 AV 네트워크 | 없음 | — |

**부풀리기 금지선**: 연구 경력 2년 6개월을 "automotive software development"에 합산해
6년을 만드는 표기는 하지 않는다. 리크루터가 확인하는 순간 나머지 모든 항목의 신뢰가 같이 깎인다.

---

## §5. 대안 검토 — NVIDIA Korea 21건 전수

2026-09-06 기준 NVIDIA Korea 공고 21건을 전부 확인했다.

| 포지션 | Req | 게이트 | 판정 |
|--------|-----|--------|:----:|
| Vehicle Integration Engineer, AV Test Fleet | JR2020318 | AV 엔지니어링 **5년+** | 내용 최근접(CAN·시험차량 개조·Linux) · 연차 미달 |
| Simulation Engineer, Industrial Physics and Robotics | JR2020130 | **8년+** | 요구사항이 co-simulation·HIL/SIL·test correlation — 석사 연구와 정면 일치하나 연차 크게 미달 |
| Solutions Architect, AI Technology Center for Physical AI | JR2018374 | **박사** + 디지털트윈 5년+ | 학위 미달 |
| Senior Omniverse Engineer, Digital Twins and Robotics | JR2021289 | Omniverse/OpenUSD/Isaac 실무 | 플랫폼 무경험 |
| Senior System Software Engineer – Automotive (3건) | JR2015971 등 | 자동차 SW 엔지니어링 | SW 엔지니어 트랙 — 본인 트랙 아님 |
| 나머지 (Sales / PR / Developer Relations / HPC / GenAI 등) | — | — | 도메인 불일치 |

**결론**: 연차·학위 게이트를 깨끗이 통과하는 자리가 21건 중 없다.
가장 아까운 건 **Simulation Engineer (JR2020130)** — "시뮬레이터를 실물 시스템으로 검증
(test correlation, calibration, HIL/SIL, controller co-simulation)"이라는 요구가
IPMSM Co-simulation + 다이나모 실증과 정확히 겹친다. 8년+ 요건이 벽이다.
**2~3년 뒤 다시 볼 자리로 표시**해두는 편이 실질적이다.

---

## §6. 판정

**지원은 사용자 결정.** 다만 근거를 분명히 남긴다.

- 필수 요건 중 **가장 먼저 걸러지는 두 줄**(경력 6년+, ADAS/AV)이 미충족이다
- 게시 후 4개월이 지난 공고다 — 파이프라인이 이미 찼을 가능성이 높다
- 자료(영문 이력서 PM 톤)를 새로 만들어야 하고, 그 시간은 **Apple 제출**과 경쟁한다.
  Apple은 자료가 이미 완성돼 있고 제출만 남았다

**권고**: NVIDIA는 `applications.json`에 `보류`로 두고, 우선순위는
① Apple 제출 → ② Tesla FSE(요건 충족) → ③ Aptiv 아산 순으로 가는 것.
NVIDIA Korea는 Workday 수집 대상에 추가해두면 조건이 맞는 공고가 열릴 때 자동으로 잡힌다.
