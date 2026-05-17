# 인성이 ↔ 포트폴리오 자동 동기화

> 인성이프로젝트의 실 운영 지표와 코드 변경을 포트폴리오 케이스 페이지에 자동 반영.

## 방향 1 — 주기적 stats 동기화

```
인성이 Supabase
   ↓ (매주 일요일 03:00 UTC)
.github/workflows/sync-insung-stats.yml
   → scripts/update_insung_stats.py
   → src/data/insung_stats.json 갱신
   ↓ (JSON 변경 시 자동 커밋)
deploy.yml 발동 → GitHub Pages 재배포
```

**조회 테이블** (PostgREST exact-count):
- `comment_activity` — 생성된 댓글 수
- `incoming_comments` — 수신 댓글 수
- `neighbor_candidates` — 발견된 이웃 후보 수
- `example_personas` — 등록 페르소나 수
- `support_tickets` — 지원 티켓 수

→ `insung_stats.json` 의 `live_metrics` 섹션에 저장.

## 방향 2 — 인성이 변경 → 포트폴리오 즉시 재배포

```
인성이프로젝트 master push
  (paths: src/, apps/web/lib/tier.ts, supabase/, README, CLAUDE)
   ↓
.github/workflows/trigger-portfolio-rebuild.yml
   → POST /repos/hwanginhyeok/portfolio/dispatches
       event_type: insung-updated
   ↓
포트폴리오 deploy.yml (repository_dispatch trigger)
   → GitHub Pages 재배포
```

## 필요한 GitHub Secrets

### 포트폴리오 리포 (`hwanginhyeok/portfolio`)

Settings → Secrets and variables → Actions → New repository secret:

| 이름 | 값 | 용도 |
|------|----|----|
| `INSUNG_SUPABASE_URL` | `https://xxx.supabase.co` | Supabase 프로젝트 URL |
| `INSUNG_SUPABASE_SERVICE_ROLE_KEY` | `eyJ...` | service_role key (read-only 권한 권장) |

### 인성이프로젝트 리포 (`hwanginhyeok/insung_blog`)

| 이름 | 값 | 용도 |
|------|----|----|
| `PORTFOLIO_DISPATCH_TOKEN` | `ghp_...` | Personal Access Token (Fine-grained, **portfolio** 리포에 `Contents: read` + `Actions: write`) |

### PAT 생성 방법

1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. **Repository access**: Only select repositories → `hwanginhyeok/portfolio` 선택
3. **Permissions** → Repository permissions:
   - Actions: `Read and write`
   - Contents: `Read-only`
   - Metadata: `Read-only` (자동)
4. Generate → 토큰 복사 → 인성이프로젝트 Secrets에 `PORTFOLIO_DISPATCH_TOKEN`으로 등록

## 수동 트리거

- **Stats 동기화 즉시 실행**: 포트폴리오 → Actions → "Sync Insung Stats" → Run workflow
- **포트폴리오 재배포 즉시**: 인성이프로젝트 → Actions → "Trigger Portfolio Rebuild" → Run workflow

## 로컬 테스트

```bash
# 인성이 .env 로드 후
export INSUNG_SUPABASE_URL=$(grep SUPABASE_URL ~/projects/인성이프로젝트/.env | cut -d= -f2)
export INSUNG_SUPABASE_SERVICE_ROLE_KEY=$(grep SUPABASE_SERVICE_ROLE_KEY ~/projects/인성이프로젝트/.env | cut -d= -f2)
cd ~/projects/포트폴리오
python scripts/update_insung_stats.py
git diff src/data/insung_stats.json
```

## live_metrics 케이스 페이지 노출 (선택)

`src/pages/cases/insung-blog/index.astro` 에서:

```astro
{stats.live_metrics && (
  <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
    <div class="bg-surface rounded-lg p-3 text-center">
      <div class="text-xl font-black text-accent">{stats.live_metrics.comments_generated.toLocaleString()}</div>
      <div class="text-xs text-muted">생성 댓글</div>
    </div>
    ...
  </div>
)}
```

`last_synced` 타임스탬프도 푸터에 표기 가능.
