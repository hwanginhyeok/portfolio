# 포트폴리오 섹션별 SSOT 완성도 + 내용 품질 트래커

> 최종 수정: 2026-04-26
> 위치: `docs/포트폴리오/SECTION_STATUS.md`
> 운영 원칙: 매 세션 시작 시 이 표를 먼저 본다. 완성도 ↑ 시 갱신 + 커밋.

## 평가 기준

**SSOT 완성도 (S)** — 각 사실/수치/이미지/인용이 1개의 신뢰할 SSOT(원본·검증된 출처)에 매핑되어있나
- 🟢 100%: 전 항목 SSOT 매핑 완료 + 검증
- 🟡 70~99%: 일부 [확인필요] 또는 추정값 잔존
- 🟠 40~70%: 핵심 사실은 OK, 보조 자료/링크 미확보
- 🔴 0~40%: 사실 오류 또는 SSOT 미정

**내용 품질 (Q)** — 메시지 구조, 두괄식, 숫자 인상력, 비주얼/카피 정합
- 🟢 송고 가능: 채용/이력 검토 그대로 가능
- 🟡 다듬기 필요: 토픽 OK, 톤/카피 보강
- 🟠 재구성 필요: 메시지 구조 재정렬
- 🔴 빈자리: 본문 부재 또는 placeholder

---

## 1. 페이지 / 섹션별 표

| # | 섹션 | 위치 | SSOT(S) | Quality(Q) | 핵심 SSOT | 미해결 |
|---|---|---|:---:|:---:|---|---|
| 1 | Hero | `Hero.astro` | 🟡 | 🟡 | CONTENT_V2 §2.2 / FACT_CHECK | 카운트 정합 (저널/학회 편수) |
| 2 | About | `index.astro` line 88~ | 🟡 | 🟠 | CONTENT_V2 §11 | 사이드 프로젝트 6개 표시 정책 미정 |
| 3 | Timeline | `Timeline.astro` | 🟢 | 🟢 | CONTENT_V2 §1 + Timeline 검증 | — |
| 4 | ThemeHeatmap | `ThemeHeatmap.astro` + `theme-map.json` | 🟠 | 🟠 | THEME_MAP_V3 (B3 영역) | LifecycleHeatmap 교체 예정 |
| 5 | SystemArchitecture | `SystemArchitecture.astro` | 🟢 | 🟢 | CONTENT_V2 §4.1 | — |
| 6 | CaseCard | `CaseCard.astro` + `cases.json` | 🟡 | 🟡 | cases.json | v3 6 카드 vs 현재 4 카드 (B3 영역) |
| 7 | Case · EOP-400W | `cases/eop-400w/index.astro` | 🟢 | 🟡 | CONTENT_V2 §4.2, INVENTORY 3-1 | B1-14 SVPWM/DPWM 본문 재정의 (사용자 입력) |
| 8 | Case · SS500 상태머신 | `cases/ss500-state-machine/index.astro` | 🟢 | 🟡 | CONTENT_V2 §4.1, §7A.2 | B1-13 양산 전장함 사진 (사용자 IMG 선택), B1-16 동파 문구 |
| 9 | Case · 시험 기획 (Test Engineering) | `cases/test-engineering/index.astro` | 🟢 | 🟢 | CONTENT_V2 §6 | — |
| 10 | Case · 특허/논문 | `cases/patent/index.astro` | 🟢 | 🟢 | **PAPERS.md (신규 SSOT)** | RISS 외부 링크 적용 (2026-04-26) |
| 11 | 논문/학회 SSOT | `docs/포트폴리오/PAPERS.md` | 🟢 | 🟢 | RISS + DBLP + IEEE + Google Scholar + Crossref | C-01~C-03 한국 학회 PDF, P-02 PCIM 페이지 (잔여) |
| 12 | StateMachine 다이어그램 | `StateMachine.astro` | 🟢 | 🟢 | CONTENT_V2 §7A | — |
| 13 | CAN 5노드 다이어그램 | `CanNetworkDiagram.astro` | 🟢 | 🟢 | CONTENT_V2 §4.1 | — |

---

## 2. 블록(B1~B5) 진행 상태

| 블록 | SSOT 산출물 | 상태 | 미해결 |
|------|------|:----:|---|
| **B1 인벤토리** | `docs/blocks/01-inventory/INVENTORY.md` + `HOMEPAGE_AUDIT_20260426.md` + **PAPERS.md** | 🟢 게이트 통과 가능 | 잔여는 사용자 입력 대기 (B1-13/14/16) — 본 문서 §5 참조 |
| **B2 활용 전략** | `USAGE_STRATEGY.md` (미작성) | 🔴 | B1 완료 후 착수 |
| **B3 배치** | `LAYOUT.md` (미작성) | 🔴 | B2 완료 후 |
| **B4 디자인** | `DESIGN_SYSTEM.md` (미작성) | 🔴 | B3 완료 후 |
| **B5 부가** | 이력서·GitHub·영문 | 🔴 | B4 완료 후 |

---

## 3. 핵심 SSOT 문서 (참조 우선순위)

| 우선 | 문서 | 역할 |
|:---:|---|---|
| 1 | **CONTENT_V2.md** | 전체 사실/수치/카피 통합 SSOT |
| 1 | **PAPERS.md** | 논문/학회 발표 전용 SSOT (2026-04-26 신규) |
| 1 | **THEME_MAP_V3.md** | 5섹션 재구성안 (B3 적용 시 활용) |
| 2 | FACT_CHECK_V1_V6.md | 팩트체크 누적 기록 |
| 2 | INVENTORY.md | 자료 자산 등록표 |
| 3 | HOMEPAGE_AUDIT_20260426.md | 정합성 점검 리포트 |
| 4 | DIFFICULTY.md | 삽질/노하우 |

---

## 4. 즉시 위임 가능한 작업 (사용자 입력 없이 진행 가능)

> 사용자가 "이거 시켜" 하면 그대로 위임 처리.

| ID | 작업 | 상태 |
|---|---|:---:|
| ~~Q-1~~ | RISS에서 T-01 학위논문 control_no 추출 → patent 페이지 외부 링크 추가 | ✅ 2026-04-26 |
| ~~Q-2~~ | P-05 J. Power Electronics 권/페이지 (Vol 24 Issue 5, pp 822-831) | ✅ 2026-04-26 |
| ~~Q-3~~ | P-01 IEEE TIM 권/Article No (Vol 73, pp 1-8, Art. 10726721) | ✅ 2026-04-26 |
| ~~Q-4~~ | P-04 Solar Energy DOI/페이지 (Vol 276, Art 112645) + 저자 순서 정정 | ✅ 2026-04-26 |
| **Q-5** | Hero/Timeline 카운트 표기 통일 (사용자 결정 U-4 받은 후) | 대기 |
| **Q-6** | cases.json metric 갱신 (특허 페이지 카드 수치) | 가능 |
| **Q-7** | EOP-400W 페이지 SVPWM 본문 톤 점검 (B1-14 완료 전 사전 점검) | 가능 |
| **Q-8** | 5섹션 와이어프레임 초안 (B3-01) — THEME_MAP_V3 기반 placeholder | B2 완료 후 |

## 5. 사용자 입력 대기 (즉시 위임 불가)

| ID | 항목 | 필요한 입력 |
|---|---|---|
| U-1 | B1-13 양산 전장함 사진 | iCloud IMG 번호 또는 사진 직접 공유 |
| U-2 | B1-14 SVPWM/DPWM 절환 본문 재정의 | "절환 로직 핵심" 메시지 |
| U-3 | B1-16 동파 파손(#58) 문구 | 원인/대책 톤 결정 |
| U-4 | Hero 카운트 정책 | "저널 3편 · 학회 4편" 또는 보수적 "저널 1편 · 학회 4편" |
| U-5 | About 사이드 프로젝트 6개 정책 | 표시 유지 / 축소 / 제거 |

---

## 6. 운영 규칙

- 세션 시작 시: 이 표 먼저 본다 + 사용자에게 "오늘 어떤 섹션?" 물어본다
- 작업 완료 시: S/Q 업데이트 + 미해결 컬럼 갱신 + 커밋
- B1 종료 조건: 7~10번 모든 페이지 S=🟢, Q≥🟡 + Hero/About S≥🟡
- 신규 SSOT 추가 시: 3절 표에 등록
