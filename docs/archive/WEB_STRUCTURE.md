# 포트폴리오 홈페이지 구조 설계

> 기반: THEME_MAP.md 테마 중심 5섹션 구조
> 형식: 정적 사이트 (Next.js/GitHub Pages 또는 Astro)
> 톤: 미니멀, 데이터 중심, 기술 깊이를 시각적으로

---

## 페이지 구조

```
/                          ← Hero + 핵심 메시지
/about                     ← 커리어 내러티브 (D-1)
/skills                    ← 기술 역량 맵 (테마 교차 시각화)
/cases                     ← 케이스 스터디 허브
  /cases/battery           ← D-2 배터리 정합성
  /cases/test-driven       ← D-12 시험장비 스토리
  /cases/state-machine     ← (예정) 제어권 상태머신
  /cases/pump-analysis     ← (예정) 펌프 전력 분석
/philosophy                ← 엔지니어링 철학 (5단계 프로세스)
/contact                   ← 연락처 + GitHub + LinkedIn
```

---

## 섹션별 상세 설계

### 1. Hero (/)

**레이아웃**: 풀스크린, SS500 제품 사진 배경 + 오버레이 텍스트

**콘텐츠**:
```
황인혁
모터제어 개발자 · Physical AI 브릿지 엔지니어

"소프트웨어가 물리 세계와 만나는 접점에서 제품을 만듭니다"
```

**핵심 수치 카드 (3개)**:
| 카드 | 수치 | 설명 |
|------|------|------|
| 특허 | 2건 | 모터 초기위치 검출 + 저온기동 |
| 이슈 해결 | 37건+ | Notion 기반 체계적 트래킹 |
| 시험 체계 | 9개 | 직접 설계/구축/운영 |

**필요 이미지**:
| ID | 용도 | 소스 | 상태 |
|----|------|------|------|
| hero-1 | SS500 제품 전면 사진 | `92)기타/샘플사진/KakaoTalk_20250325_105211688.jpg` ~ `_16.jpg` | 20장 중 선별 필요 |
| hero-2 | SS500 작업 현장 사진 | `92)기타/샘플사진/KakaoTalk_20250325_133621647.jpg` | 확인 필요 |

---

### 2. About (/about)

**레이아웃**: 타임라인 + 텍스트

**콘텐츠**: `cases/D1_career_narrative.md` 기반

**타임라인 구조**:
```
2022 ─── SCU (현대/DIC) ── BLDC 구동, 자동차 규격 통과
  │
2023 ─── EOP 400W 국책과제 ── SVPWM, 다이나모미터, 특허 출원
  │        ├ 특허 #1: 모터 초기위치 검출
  │        └ 다이나모미터 토크제어 시스템 개발
  │
2024 ─── EOP 완료 + ADT 모터 개선 ── 저온기동 특허, Zbench +60%
  │
2025 ─── SS500 착수 ── CAN 5노드, 배터리 BMS, 상태머신
  │
2026 ─── SS500 양산 준비 ── APQP, 37건 이슈, 시험체계 9종
```

**필요 이미지**:
| ID | 용도 | 소스 | 상태 |
|----|------|------|------|
| about-1 | 프로필 사진 | 없음 | **촬영 필요** |
| about-2 | GINT 사무실/작업 환경 | 없음 | **촬영 또는 수집 필요** |

---

### 3. Skills (/skills)

**레이아웃**: 인터랙티브 역량 맵 (테마 × 프로젝트 히트맵)

**콘텐츠**: `cases/THEME_MAP.md` 기반

**시각화 컴포넌트**:

1) **테마 교차 히트맵** (메인)
```
           SCU    EOP    ADT    SS500   특허
모터제어    ■■■    ■■■    ■■     ■■      ■■■
CAN설계    ■■     ■■            ■■■
PCB/HW     ■■■    ■■            ■■
시험장비           ■■■    ■      ■■■
데이터      ■      ■■■    ■■     ■■■     ■
양산품질    ■■■                   ■■■
문제해결                          ■■■
```

2) **기술 스택 태그 클라우드**
- HW: BLDC, PMSM, FOC, SVPWM, CAN-FD, BMS, DC-DC, PCB
- MCU: STM32, Infineon TC23x, MC9S12ZVMC
- 도구: CANoe, Vector VN1600, SPICE, Matlab/Simulink, Oscilloscope
- SW: Python, C/C++, ROS2
- PM: APQP, DFMEA, DRBFM, Notion, WBS

**필요 이미지**: 없음 (코드로 생성하는 SVG/차트 컴포넌트)

---

### 4. Cases (/cases)

#### 4-a. 배터리 정합성 (/cases/battery)

**레이아웃**: STAR 포맷 스크롤 스토리

**콘텐츠**: `cases/D2_battery_compatibility_case.md` 기반

**핵심 비주얼**:
- SOC 162% 데이터 시각화 (차트)
- 셀별 전압 편차 히트맵
- 3차 검증 타임라인
- Before/After 비교 테이블

**필요 이미지**:
| ID | 용도 | 소스 | 상태 |
|----|------|------|------|
| batt-1 | 배터리 팩 사진 | 없음 | **수집 필요** (48V 460Ah 팩 실물) |
| batt-2 | CAN 로그 분석 화면 | 직접 캡처 가능 | 작성 시 생성 |
| batt-3 | WBS 시트 캡처 | `72_배터리정합성/GINT_SS_*.xlsx` | 캡처 필요 |

#### 4-b. 시험장비 스토리 (/cases/test-driven)

**레이아웃**: Phase 1→2→3 스크롤 진행, 각 시험별 카드

**콘텐츠**: `cases/D12_test_driven_engineer.md` 기반 (BLACKTAN 제거 완료, 9개 사례)

**핵심 비주얼**:
- Phase 진화 다이어그램 (단일장비→방법론→시스템)
- 각 시험의 Before/After 카드
- 정량 수치 하이라이트 (큰 숫자 강조)

**필요 이미지**:
| ID | 용도 | 소스 | 상태 |
|----|------|------|------|
| test-1 | 다이나모미터 시스템 사진 | 없음 | **촬영 필요** |
| test-2 | 다이나모 PID 제어 파형 | `도구/Oscilloscope/Data/DYNAMO_PID/PID_*.png` | **있음** (4장) |
| test-3 | PWM 온도 비교 차트 | `PWM절환/시험데이터/Chart_*.jpg` | **있음** (8장) |
| test-4 | 펌프 벤치 시스템 사진 | `시험검정/90)SS기_시험/KakaoTalk_20260219_*.jpg` | **있음** (2장, 확인 필요) |
| test-5 | 팬 벤치 셋업 사진 | 없음 | **촬영 필요** |
| test-6 | 범퍼 장착 사진 | 없음 | **촬영 필요** |
| test-7 | 기성모델 비교 현장 | 없음 | **촬영/수집 필요** |

#### 4-c. 제어권 상태머신 (/cases/state-machine) — 예정

**필요 이미지**:
| ID | 용도 | 소스 | 상태 |
|----|------|------|------|
| sm-1 | DM 로직 다이어그램 | `SS기/SS500_SW_DM_LOGIC.jpg` | **있음** |
| sm-2 | 상태 전이도 | 직접 제작 (Mermaid/SVG) | 작성 시 생성 |

#### 4-d. 펌프 전력 분석 (/cases/pump-analysis) — 예정

**필요 이미지**:
| ID | 용도 | 소스 | 상태 |
|----|------|------|------|

---

### 5. Philosophy (/philosophy)

**레이아웃**: 5단계 프로세스 인터랙티브 카드

**콘텐츠**: 5단계 × SS500 적용 사례

```
1. 요구사항을 의심하라 → 아세아텍 벤치마킹 기준 재검토
2. 삭제하라             → 제어권 NONE 상태 삭제
3. 단순화/최적화하라    → CAN 메시지 표준화
4. 속도를 높여라        → 배터리 정합성 자동 체크리스트
5. 자동화하라           → Claude Code 5-에이전트 시스템
```

**필요 이미지**: 없음 (아이콘/일러스트로 대체)

---

### 6. Contact (/contact)

- GitHub: hwanginhyeok
- Email: (확인 필요)
- LinkedIn: (확인 필요)

---

## 이미지 자산 총괄

### 현재 보유 (HIH_2에서 가져올 수 있는 것)

| 카테고리 | 파일 수 | 위치 | 홈페이지 용도 |
|----------|---------|------|-------------|
| **SS500 제품 사진** | 20장 | `92)기타/샘플사진/` | Hero 배경, About 타임라인 |
| **동파 RCA 사진** | 9장 | `이슈관리/images/058_동파문제/` | RCA 케이스 (여과기파손, 오링불량 등) |
| **비상정지 테스트** | 1장 | `이슈관리/images/120_비상정지/` | 안전 시스템 케이스 |
| **펌프교체 분사비교** | 1장 | `이슈관리/images/115_펌프교체/` | 펌프 케이스 |
| **금형 일정** | 1장 | `이슈관리/images/059_금형발주/` | PM 케이스 |
| **PWM 온도 차트** | 8장 | `PWM절환/시험데이터/Chart_*.jpg` | 시험장비 스토리 Phase 2 |
| **EOP PCB 레이어** | 8장 | `완료보고서_보완자료/PCB_*.jpg` | HW 설계 역량 (T-3) |
| **오실로스코프 파형** | 20+장 | `도구/Oscilloscope/Data/` | 기술 깊이 배경 |
| **다이나모 PID** | 4장 | `Oscilloscope/DYNAMO_PID/` | 시험장비 Phase 1 |
| **SCU PWM 파형** | 2장 | `Oscilloscope/SCU/` | 모터제어 역량 |
| **DM 로직 다이어그램** | 1장 | `SS기/SS500_SW_DM_LOGIC.jpg` | 상태머신 케이스 |
| **벤치 자료** | 2장 | `92)기타/벤치자료/` | 시험 현장 |
| **시험 현장** | 2장 | `시험검정/KakaoTalk_20260219_*.jpg` | 시험 현장 |
| **부품 사진** | 2장 | `2)부품/IMG_*.jpg` | 부품 갤러리 |

### 촬영/수집 필요

| 우선순위 | 항목 | 용도 |
|----------|------|------|
| **P1** | 프로필 사진 | About 페이지 |
| **P1** | SS500 전체 외관 고해상도 | Hero 배경 |
| P2 | 다이나모미터 시스템 전경 | 시험장비 Phase 1 |
| P2 | 팬 벤치 셋업 | 시험장비 Phase 3 |
| P2 | 범퍼 장착 사진 | 안전 시스템 |
| P2 | VCU PCB 실물 | HW 역량 |
| P3 | 배터리 팩 실물 | 배터리 케이스 |
| P3 | CAN 분석 장비(Vector) 작업 화면 | CAN 역량 |

### 직접 제작 (코드/도구로 생성)

| 항목 | 제작 방법 | 용도 |
|------|----------|------|
| 시스템 아키텍처 다이어그램 | Mermaid/D2/Excalidraw | About, Cases |
| 상태 전이도 (RC/LCD/ADT) | Mermaid state diagram | 상태머신 케이스 |
| CAN 네트워크 구성도 | D2 diagram | 기술 딥다이브 |
| 테마 교차 히트맵 | React + CSS Grid | Skills 페이지 |
| Before/After 비교 차트 | Chart.js / Recharts | Cases 전반 |
| 타임라인 | CSS timeline | About 페이지 |
| 5단계 프로세스 카드 | React 컴포넌트 | Philosophy |

---

## 이미지 복사 스크립트 (실행 시)

```bash
# 포트폴리오 이미지 디렉토리 생성
mkdir -p ~/포트폴리오/public/images/{hero,about,cases,skills,philosophy}

# SS500 제품 사진 → hero
cp ~/HIH_2/1)프로젝트/5)농업/92)기타/샘플사진/*.jpg ~/포트폴리오/public/images/hero/

# 동파 RCA 사진 → cases
cp ~/HIH_2/1)프로젝트/5)농업/91)문서/이슈관리/images/058_동파문제/*.{jpg,png} ~/포트폴리오/public/images/cases/

# PWM 온도 차트 → cases
cp ~/HIH_2/2)HIH_개인/4)포트폴리오/2024/17)PWM절환/1)시험데이터/240424_HSG#26_*/Chart_*.jpg ~/포트폴리오/public/images/cases/

# EOP PCB → skills
cp ~/HIH_2/2)HIH_개인/4)포트폴리오/2024/완료보고서_보완자료/보충자료/PCB_*.jpg ~/포트폴리오/public/images/skills/

# 다이나모 PID → cases
cp ~/HIH_2/3)도구/1)Oscilloscope/Data/DYNAMO_PID/*.png ~/포트폴리오/public/images/cases/

# DM 로직 → cases
cp ~/HIH_2/2)HIH_개인/4)포트폴리오/SS기/SS500_SW_DM_LOGIC.jpg ~/포트폴리오/public/images/cases/

# 시험 현장 → cases
cp ~/HIH_2/1)프로젝트/5)농업/5)시험검정/90)SS기_시험/KakaoTalk_20260219_*.jpg ~/포트폴리오/public/images/cases/

# 벤치 자료 → cases
cp ~/HIH_2/1)프로젝트/5)농업/92)기타/벤치자료/*.jpg ~/포트폴리오/public/images/cases/

# 비상정지/펌프교체 → cases
cp ~/HIH_2/1)프로젝트/5)농업/91)문서/이슈관리/images/120_비상정지/*.png ~/포트폴리오/public/images/cases/
cp ~/HIH_2/1)프로젝트/5)농업/91)문서/이슈관리/images/115_펌프교체/*.png ~/포트폴리오/public/images/cases/
```

---

## 기술 스택 후보

| 옵션 | 장점 | 단점 |
|------|------|------|
| **Next.js + Vercel** | 인터랙티브 차트, SSG, 빠른 배포 | 오버엔지니어링일 수 있음 |
| **Astro + GitHub Pages** | 경량, 마크다운 네이티브, 무료 호스팅 | 인터랙티브 제한 |
| **Notion → Super/Oopy** | 가장 빠름, 마크다운 즉시 활용 | 커스터마이징 한계 |

**추천**: 콘텐츠 준비가 충분하므로 **Astro + GitHub Pages**가 가성비 최적. 인터랙티브 차트가 필요한 부분만 React island로 처리.

---

## 다음 단계

| 순서 | 작업 | 비고 |
|------|------|------|
| 1 | **이미지 선별**: SS500 제품 사진 20장 중 Hero용 2~3장 선정 | 본인 확인 |
| 2 | **촬영 목록 확인**: P1 항목(프로필, SS500 고해상도) 촬영 가능 여부 | 본인 확인 |
| 3 | **기술 스택 결정**: Astro vs Next.js vs Notion | 논의 |
| 4 | **다이어그램 제작**: 시스템 아키텍처, 상태전이도, CAN 구성도 | 코드로 생성 |
| 5 | **사이트 scaffolding**: 선택한 스택으로 초기 구조 생성 | 코딩 |
