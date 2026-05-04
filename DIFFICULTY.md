# Difficulties & Know-how

## D-007: 사실 검증 (Fact-Check) 없이 표준명 사후 매핑 → 외부 제출 자료에 부정직 표현 누적
- **날짜**: 2026-05-04
- **상황**: Apple/xAI 영문 cover letter + resume 작성. Sub-agent가 어필력 강화 위해 사용자 RESUME에 없는 표준명을 사후 매핑 — JESD47/JEP122, MIL-STD-810, IEC 60068-2, IEC 60529 IP67, FRACAS, AIAG-VDA 2019, Six Sigma DMAIC, Cpk/Ppk
- **문제**:
  - "직접 시험 수행"과 "표준에 사실상 부합"의 차이 모호화
  - "BOM freezes / line-stop decisions" 등 SSOT에 없는 표현이 자연스럽게 섞여 들어감
  - "ALT design" 표현 사용 (사용자는 옆에서 본 것이지 직접 design 아님)
  - "self-study brief" 1169줄 산출물 어필 — 줄수는 많지만 사용자가 인터뷰에서 답변 가능한 깊이 미도달
  - "the most reliability-demanding component" 같은 검증 불가 단언
- **삽질**:
  - 사용자가 직접 cover letter 읽고 "이 부분 어디서 가져왔니?", "지어낸 듯한 느낌"이라고 지적 → 4~5라운드 정정
  - reliability_competency.md §3 매핑 표가 cover letter에 그대로 흘러들어감 (자가학습 자료 ≠ 제출 가능 어필)
- **해결**:
  - RESUME.md 풀로 grep — "IP67/Cpk/Six Sigma/방수" 검색하면 0건 확인
  - 매핑 표현 모두 제거. 사용자 직접 한 사실만 정량 수치로 (다이나모 0.008%, 팬 +57%, 범퍼 0.082m/308A/467ms, CAN 5노드/DBC 4종, BOM 132/재고 23건)
  - 저자 위치 명시 (3rd/6th/4th author)로 contribution 정직 기재
  - "ALT design" → "instrumenting ALT" / "observed full ALT cycle"로 분리
  - self-study brief 구체 항목 제거, "actively building optics-domain depth" 진행 중 톤
  - "I have not worked on cameras, VCMs, or lens assemblies" 갭 첫 줄에서 솔직 인정
- **노하우**:
  - 외부 제출 자료(cover letter / resume / 지원서)는 **사용자 SSOT(RESUME.md / CONTENT_V2.md) 직접 인용만**
  - Sub-agent에 작성 위임 시 입력으로 "RESUME에 명시된 사실만 사용. 표준명 매핑은 RESUME에 명시된 경우에만" 명시 필요
  - "내가 아는 거 뽐내기" vs "실제로 한 것" 구분 — 인터뷰에서 깊이 답변 가능한지가 기준
  - 자가학습 자료는 줄수가 아니라 **답변 깊이**가 어필 자격. 깊이 미도달 시 산출물 자체를 cover letter에 어필 금지
  - "ALT design / conducted / led" vs "observed / participated / co-authored" 동사 선택 = 정직성의 핵심 지표
  - 매 정정 후 사용자 검토 단계에서 grep으로 RESUME 매핑 재확인 (`grep -n "키워드" RESUME.md`)
- **회고**: D-005 (BMS 정합성 타인 업무) 패턴 재발. AI가 사용자 자료를 풍부하게 보이려 추론·매핑·확장하는 경향 = 정직성과 충돌. **외부 제출 자료 작성 시 sub-agent에 "추가 매핑 금지, SSOT 직접 인용만" 강제 필요**
- **관련 파일**:
  - `docs/jd/apple/materials/cover_letter.md` (5라운드 정정)
  - `docs/jd/apple/materials/resume_en.md` (표준명 매핑 다수 — 추가 검토 필요)
  - `docs/jd/xai/materials/cover_letter_xai.md` (2건 정정)
  - `docs/jd/apple/materials/reliability_competency.md` §3 (매핑 표 — 자가학습 자료 SSOT, 제출자료에는 인용 금지)

## D-006: iCloud for Windows 동기화 폴더 — Read 호출 시 자동 다운로드 트리거
- **날짜**: 2026-04-26
- **상황**: B1-13 양산 전장함 사진 발굴 위해 `/mnt/c/Users/gint pcd/iCloudPhotos/Photos/` 사진 약 10장 Read 도구로 열람
- **문제**: iCloud for Windows는 온디맨드 동기화(스마트 다운로드) — 로컬엔 메타만 있고 실제 파일은 클라우드. Read 호출 시마다 자동 다운로드 발생
- **삽질**: WSL `find -printf` 메타데이터로는 사진 내용 식별 불가. 무작정 샘플링하면서 다운로드 누적
- **해결**: 사용자가 알아채고 중단 요청 → 사용자가 iPhone/iCloud.com에서 직접 IMG 번호 골라주는 방식으로 전환
- **노하우**:
  - iCloud Photos는 약 7400장 규모. 무작위 탐색 절대 금지
  - WSL에서는 썸네일 보기 불가 (Windows Explorer/iCloud 앱은 가능)
  - 사진 식별이 필요하면 **사용자가 직접 골라준 1~2장만 처리**가 정답
  - 큰 파일 다수 자동 다운로드는 디스크/네트워크 부담 + 사용자 메모리 부담
- **관련 파일**: 없음 (원격 PC 환경 이슈)

## D-001: GitHub Pages base URL trailing slash 누락 → 케이스 링크 전부 깨짐
- **날짜**: 2026-04-04
- **상황**: GitHub Pages에 `/portfolio` base path로 배포, 케이스 상세페이지 링크 클릭 시 404
- **이슈**: `base: '/portfolio'`로 설정하니 링크가 `/portfoliocases/eop-400w/`로 이어붙여짐 (슬래시 없이 concat)
- **삽질**: 페이지 라우팅 문제인 줄 알고 pages/ 구조를 의심, Astro 라우팅 설정을 뒤짐
- **해결**: `astro.config.mjs`에서 `base: '/portfolio'` → `base: '/portfolio/'` trailing slash 한 글자 추가
- **대안**: 각 링크에 `/` prefix를 수동 추가하는 방법 — base config를 고치는 게 근본 해결이라 선택 안 함
- **노하우**: Astro/Next.js 등 정적 사이트에서 base path 설정 시 **반드시 trailing slash 포함** 확인. 배포 후 첫 번째로 내부 링크 클릭 테스트
- **회고**: 로컬에서는 base path 없이 동작하므로 발견 불가. 배포 직후 링크 테스트를 체크리스트에 넣어야 함
- **관련 파일**: `astro.config.mjs`

## D-002: Astro 6 + GitHub Actions Node 버전 불일치 → CI 빌드 실패
- **날짜**: 2026-03-30
- **상황**: Astro 6으로 scaffold 후 GitHub Actions 배포 시 빌드 에러
- **이슈**: GitHub Actions 워크플로우가 Node 18 사용 → Astro 6은 Node 22 필요
- **삽질**: Astro 빌드 에러 메시지가 Node 버전을 직접 언급하지 않아서 의존성 문제로 착각
- **해결**: `.github/workflows/deploy.yml`에서 `node-version: 18` → `node-version: 22` 변경
- **대안**: Astro 5로 다운그레이드 — 최신 기능(Content Collections 등) 포기해야 해서 선택 안 함
- **노하우**: 프레임워크 메이저 버전 업그레이드 시 **CI 런타임 버전부터 확인**. `package.json`의 `engines` 필드 체크
- **회고**: scaffold 단계에서 CI 파이프라인까지 한 번에 검증하는 습관 필요. 로컬 빌드 성공 ≠ CI 빌드 성공
- **관련 파일**: `.github/workflows/deploy.yml`

## D-003: AI 슬롭 — Claude가 생성한 UI가 전형적 AI 템플릿 패턴
- **날짜**: 2026-03-31
- **상황**: 디자인 리뷰(/design-review) 돌렸더니 FINDING-001로 AI 슬롭 검출
- **이슈**: 4열 메트릭 카드 그리드, 그라데이션 배경, 전체 중앙정렬 — "ChatGPT가 만든 것 같은" 전형적 패턴
- **삽질**: 처음에는 색상/폰트만 바꾸면 될 줄 알았는데, 레이아웃 구조 자체가 AI 템플릿
- **해결**: 4열 카드 → 인라인 수치 나열, 그라데이션 → 단색 bg, 중앙정렬 → 좌정렬, 영문 서브헤딩 추가로 시각적 리듬 변화
- **대안**: 완전히 새 디자인 시스템 도입 — 시간 대비 효과가 낮아 기존 구조에서 슬롭만 제거하는 방향 선택
- **노하우**: AI로 UI 생성 후 반드시 **슬롭 체크리스트** 적용: ① 4열 카드 그리드? ② 그라데이션? ③ 전체 중앙정렬? ④ 아이콘 남용? → 하나라도 해당되면 수정
- **회고**: AI에게 "포트폴리오 만들어줘"라고 하면 100% 슬롭 나옴. 처음부터 레퍼런스 사이트를 지정하고 "이 스타일로"라고 해야 함
- **관련 파일**: `src/components/Hero.astro`

## D-004: SVPWM 수치 검증 실패 — 경력기술서 수치와 실측 데이터 불일치
- **날짜**: 2026-04-04
- **상황**: EOP 400W 케이스에서 "FET 온도 16~17°C 저감" 수치를 데이터로 뒷받침하려 함
- **이슈**: HIH_2의 CSV 원본 분석 결과, 1Assy vs 2Assy 온도 차이 0~4°C. SVPWM vs DPWM 비교 데이터 자체가 없음 (같은 PWM 조건 데이터만 존재)
- **삽질**: CSV 파일 수십 개 분석, 온도 컬럼 추출·비교 → 결국 "동일 조건 비교" 데이터가 아님을 확인하는 데만 시간 소모
- **해결**: 검증 불가 수치(16~17°C) 제거, 보수적 수치(1~3°C)로 변경. 정확한 수치는 노트북 엑셀 원본에서 확인 필요로 TASK 등록
- **대안**: 수치 자체를 삭제하고 정성적 표현("온도 저감 효과 확인")만 사용 — 정량적 성과가 포트폴리오 핵심이라 수치 유지 선택
- **노하우**: 포트폴리오에 수치 기재 전 **데이터 출처와 비교 조건을 먼저 확인**. "경력기술서에 있으니까 맞겠지"는 위험. 서버에 없는 데이터는 조기에 노트북 작업으로 분류
- **회고**: 데이터 검증을 콘텐츠 작성 후가 아니라 케이스 기획 단계에서 했어야 함. "이 수치의 근거 데이터가 어디 있는가?"를 첫 질문으로
- **관련 파일**: `src/pages/cases/eop-400w/index.astro`

## D-005: 팩트체크에서 본인 업무 범위 오류 발견 — BMS 정합성 검증은 타인 업무
- **날짜**: 2026-03-31
- **상황**: 야간 작업으로 케이스 9종 작성 후, 팩트체크 과정에서 업무 귀속 문제 발견
- **이슈**: "배터리 CAN 정합성 검증"을 본인 시험기획 업무로 포함했으나, 실제로는 배터리팀 업무. 시험 9종 → 8종으로 수정 필요. 특허도 "2건 본인 발명"이 아니라 "1건 본인 발명 + 1건 실험 담당"
- **삽질**: 경력기술서 문구를 그대로 옮겨서 생긴 문제. AI가 경력기술서를 읽고 "이것도 당신 업무겠죠?"라고 추론한 부분이 오류
- **해결**: 팩트체크 7개 항목 수행 — 시험 9종→8종 일괄 수정, 특허 정정, 용어 통일(SS500→GT-SS500), About에서 BMS 태그 제거
- **대안**: 없음. 사실 오류는 수정만이 답
- **노하우**: AI에게 경력 소재를 정리시킬 때 **"이 업무가 정말 본인 것인지"를 반드시 사람이 검증**. 경력기술서 자체가 과장되어 있을 수 있음. 팩트체크 단계를 프로세스에 내장
- **회고**: 콘텐츠 생성 → 팩트체크 순서는 맞았지만, 케이스 작성 초기에 "업무 범위 명세"를 먼저 정의했으면 재작업이 줄었을 것
- **관련 파일**: `src/data/cases.json`, `src/pages/cases/test-engineering/index.astro`
