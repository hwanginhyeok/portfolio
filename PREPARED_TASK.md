# Prepared Tasks

> 넘버링: `B{블록}-{순번}` — 자세히는 [TASK.md](TASK.md) 상단 참조

## B1 — 자료 인벤토리 (17개)

> 2026-04-26 추가: B1-09~B1-18 — 홈페이지 자료 정합성 점검 후 도출된 자료 픽스 항목

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B1-02 | SVPWM 수치 확보 — 효율 +1%/+4% + 온도 저감 | P2 | 노트북 엑셀 이관 | 기존 4-5. N01/N02 (대기 자산) |
| B1-03 | 범퍼 실차시험 사진 확보 | P2 | 핸드폰→PC 이관 | 기존 4-7 잔여. W01 |
| B1-04 | 시험 환경 장비 사진 촬영 (다이나모/팬벤치/범퍼) | P2 | 시험실 방문 | 기존 6-5. W02/W03/W04 |
| B1-05 | 양산 전장함 사진 촬영 | P2 | 회사 촬영 | 기존 6-6. W05. **최신본 필요** (현 control-box-external.webp는 옛날 버전) |
| B1-06 | VCU PCB 실물 + CAN 장비 화면 | P3 | 촬영 | 기존 TODO. W06/W07 |
| B1-07 | GT-SS500 PM 경험 문서화 (APQP/WBS/이슈관리/BOM) | P2 | | 기존 2-3. E01 |
| B1-08 | AI 활용 사례 + 사이드 프로젝트 3종 문서화 | P2 | | 기존 2-4/2-5 병합. E02/E03 |
| B1-17b | 학위논문 정확한 제목/J-01 저널 게재지 확정 | P2 | dcollection.konkuk / KCI 직접 검색 | PAPERS.md 미해결 항목. 현재 patent 페이지 P-1 카드는 CONTENT_V2 인용 제목 사용 중 |

## B2 — 활용 전략 (1개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B2-01 | 타겟 회사·JD 분석 + 핵심 메시지 3~5개 확정 + 자산 매트릭스 + 컷 리스트 | P1 | 사용자 입력 | `USAGE_STRATEGY.md` 골격 완료. §1 타겟 회사 / §2 메시지 확정 사용자 입력 대기 |

## B4 — 디자인 (3개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B4-02 | `/impact` 페이지 구현 | P2 | B4-01 완료 후 | LAYOUT.md §2.4 명세. Hero 4카드 확장판 + LifecycleHeatmap + 메시지별 정량표. nav 미노출, 이력서/LinkedIn 공유용 URL |
| B4-05 | 인성이 자동 동기화 — GitHub Secrets 등록 (사용자 직접) | P1 | — | 포트폴리오 리포: `INSUNG_SUPABASE_URL`, `INSUNG_SUPABASE_SERVICE_ROLE_KEY`. 인성이 리포: `PORTFOLIO_DISPATCH_TOKEN`(Fine-grained PAT). 가이드: `docs/automation/insung-sync.md`. 등록 후 Actions → Sync Insung Stats → Run workflow 1회 실행해 첫 동기화 검증. |
| B4-06 | `live_metrics` 케이스 페이지 노출 (Supabase 첫 sync 후) | P2 | B4-05 | `cases/insung-blog/index.astro`에 `{stats.live_metrics && ...}` 블록 추가. 댓글 수/이웃 수/페르소나 수 카드 표시 + `last_synced` 푸터. `docs/automation/insung-sync.md` 하단 스니펫 참조. |

## JD 지원 — Apple (4개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| JD-A3 | Apple 지원서 최종 제출 (사용자 직접) | P1 | JD-A7, JD-A8 | jobs.apple.com Job ID 200656459-3631. resume v5.1 + cover letter v3 완성. **제출은 사용자 직접 수행** |
| JD-A7 | 학습자료 fact-check 정정 — 1차 자료(P-01·P-02·T-01) 수령 후 | P1 | 사용자 PDF 제공 | FACTCHECK_bondwire.md §6~9 참조. 정정 대상: D1 §3, D2, D6, reliability_competency Block2 Arrhenius, index.html |
| JD-A9 | Apple 인터뷰 학습 Day 1~7 | P2 | — | reliability_competency.md §5.2 7일 코스. ★★★: Stress-Strength / JESD47 / FRACAS. STAR 영문 5종 준비. 추후 진행 예정 |

## JD 지원 — xAI (0개)

> JD-X3 완료 (2026-05-15)

## B5 — 부가자료 (3개)

| # | 태스크 | 우선순위 | depends | 비고 |
|---|--------|:--------:|---------|------|
| B5-01 | 이력서 작성 | P3 | 이메일/사이트 URL 입력 + 토익 재응시 | `RESUME.md` 마스터 완료. 어학 만료 명시 |
| B5-04 | TOEIC + TOEIC Speaking 재응시 | P2 | 사용자 외부 작업 | 이전 점수: TOEIC 920 / TS 140 (IH). 응시 후 RESUME §9 갱신 |
| B5-02 | GitHub 프로필 정비 | P3 | 사용자 실행 | `GITHUB_PROFILE.md` 가이드 완료. P1: profile README + 핀 6개 |
| B5-03 | **i18n 한/영 언어 토글 구현** — 단일 사이트에서 Korean/English 전환 | P1 | B5-03 기존 가이드 | 사용자 지시 2026-05-08: 한 사이트에서 EN/KO 선택 가능하게. Astro i18n 라우팅 (`/en/`, `/ko/`) 또는 클라이언트 토글 방식. `ENGLISH_VERSION.md` 어휘집 + Summary 4종 기존 자료 활용. 메인 페이지·케이스 페이지·about 전체 번역 대상. |
