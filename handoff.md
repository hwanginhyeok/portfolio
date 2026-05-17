# Handoff — 2026-05-17

## 이번 세션 한 일

1. **인성이 블로그 자동화 케이스 페이지 신설** (`cases/insung-blog/`)
   - 4단계 구축기 + 철학(반복 노동 제거 → 아날로그 집중) + SS500과의 연결
   - `block_diagram.png` 시스템 다이어그램 삽입
   - AINative 카드에 링크 추가
   - 디자인 개선 6건 (AI slop 제거, 칩 UI, blockquote 등)
   - 팩트체크 전항목 통과 (Claude Haiku / Playwright / FastAPI / Chrome MV3 / 가격)

2. **자동 동기화 시스템 (포트폴리오↔인성이)**
   - 방향1: 주간 Supabase 동기화 (`sync-insung-stats.yml` + `update_insung_stats.py`)
   - 방향2: 인성이 push → 포트폴리오 자동 재배포 (`repository_dispatch`)
   - 가이드: `docs/automation/insung-sync.md`

## 다음 세션 첫 액션 (사용자 직접 필요)

**B4-05 — GitHub Secrets 등록** (필수, 자동 동기화 활성화 전제):

1. 포트폴리오 리포 (`hwanginhyeok/portfolio`) Secrets:
   - `INSUNG_SUPABASE_URL`
   - `INSUNG_SUPABASE_SERVICE_ROLE_KEY`

2. 인성이 리포 (`hwanginhyeok/insung_blog`) Secrets:
   - `PORTFOLIO_DISPATCH_TOKEN` — Fine-grained PAT, 발급법은 `docs/automation/insung-sync.md` 참조

3. 등록 후 검증:
   - GitHub → 포트폴리오 → Actions → "Sync Insung Stats" → Run workflow
   - 성공하면 `src/data/insung_stats.json` 에 `live_metrics` 섹션 자동 추가됨

**B4-06 — live_metrics 케이스 페이지 노출** (B4-05 검증 후):
- `cases/insung-blog/index.astro` 에 `{stats.live_metrics && ...}` 블록 추가
- 댓글 수/이웃 수/페르소나 수 카드 + `last_synced` 푸터
- 스니펫: `docs/automation/insung-sync.md` 하단

## 컨텍스트 (사용자 결정 사항)

- **자동화 프레임**: "풀스택 자동화 SaaS" 같은 기술 중심 표현 금지. "사람을 본질에 집중시키는 자동화" 톤 유지.
- **인성이프로젝트 미션**: 네이버 블로그 체험단 생태계에 더 좋은 글이 나오도록 기여. 자기만족 + 경제 활동 둘 다.
- **케이스 페이지 위치**: T-5 "엔지니어의 뿌리" 섹션의 AINative 카드 → 케이스 페이지 링크.

## 변경 파일 요약

**포트폴리오:**
- `src/pages/cases/insung-blog/index.astro` (신규)
- `src/data/insung_stats.json` (신규)
- `src/components/AINative.astro` (수정)
- `public/images/cases/insung-blog/block_diagram.png` (신규)
- `scripts/update_insung_stats.py` (신규)
- `.github/workflows/sync-insung-stats.yml` (신규)
- `.github/workflows/deploy.yml` (수정: dispatch trigger 추가)
- `docs/automation/insung-sync.md` (신규)

**인성이프로젝트:**
- `.github/workflows/trigger-portfolio-rebuild.yml` (신규)

## 잔여 이슈

- 인성이프로젝트 루트에 untracked 2건 (`apps/web/data/`, `docs/프로젝트/_portfolio_assets.md`) — 이번 세션 무관. 다음 세션에서 정체 확인 필요.

## 메모리 추가

- `feedback_automation_philosophy.md` — 자동화 프레임 톤
- `reference_portfolio_insung_sync.md` — 동기화 시스템 레퍼런스
