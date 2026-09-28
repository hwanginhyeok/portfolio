# Migration & Evolution Plan (plan.md)

## 1. Goal

Migrate `portfolio` (server dir `포트폴리오`, GitHub repo `portfolio`) onto the HIH Project Standard (`~/Workspace/agents/project-standard.md`) in accordance with plan card `t19-consolidate-projects.md`. Establish standard documentation, hermetic tests on macOS, an operational inventory (`ops/ops.yaml`), and an integration plan for the HIH harness while keeping existing `server-pc` cron jobs completely undisturbed.

---

## 2. Scope

### In Scope
- Comprehensive code review of server snapshot (`docs/review-2026-09-28.md`).
- Standard repository layout: `README.md` (`Path | What` table), `docs/plan.md`, `docs/decisions.md`, `docs/runbook.md`, `features/` specs, `ops/ops.yaml`, `site/index.html` generator + pre-commit hook.
- Harness integration design: `hih-secret` credential resolution, `hih notify` operational alerts, and LaunchAgent plist drafts under `launchd/`.
- Code changes strictly needed for macOS portability (`PORTFOLIO_PM_ENV`, `HIH_SCHEDULE_CLI`, hermetic test conftest) while preserving server defaults.
- Hermetic test verification of 90 unit tests on macOS under Python 3.12 (`uv`) and Astro static site build (`npm run build`).
- Resolution of macOS case-collision between `HANDOFF.md` and historical `handoff.md` (renamed to `docs/history/handoff-2026-05-19.md`).
- Untracking legacy coordination, multi-agent debate, and TASK-style files from git while retaining contents on disk.

### Out of Scope
- Altering, stopping, or restarting the six running cron jobs on `server-pc`.
- Pushing commits to remote repositories.
- Live external crawling or live Telegram report dispatches during migration.
- Activating/bootstrapping LaunchAgents into macOS `launchctl`.

---

## 3. Phases

```
Phase 1: Project Standardization (Current)
   ├── Resolve macOS case collision (HANDOFF.md vs handoff.md)
   ├── Code review & severity assessment (docs/review-2026-09-28.md)
   ├── Standard documentation & features specs
   ├── Portable path resolution & hermetic test suite (90 passed)
   ├── Astro static site build verification (10 static routes)
   ├── Untrack legacy task/coordination files (.gitignore)
   └── ops/ops.yaml & site/index.html generator
           │
           ▼
Phase 2: Harness Integration (Specification Ready)
   ├── Connect credential resolution to hih-secret (macOS Keychain)
   ├── Route operational alerts and human reports through hih notify
   ├── Migrate Google Calendar sync to direct local REST OAuth (hih schedule)
   └── Prepare LaunchAgents in launchd/ for local execution
           │
           ▼
Phase 3: Operational Cutover & Server PC Decommissioning
   ├── Stop server-pc crontab lines by name (6 cron entries)
   ├── Bootstrap LaunchAgents on macOS
   ├── Verify one week of stable local collector runs & Telegram reports
   ├── Relocate dynamic collector staging inboxes to data/jd/
   └── Archive server bundle and clean up legacy VM copies
```

---

## 4. Verification Gate

| Step | Gate Condition | Verification Tool |
|---|---|---|
| Python Hermetic Tests | 90 unit tests pass with zero network and isolated temp directories | `uv run pytest tests/` |
| Web Static Build | 10 static routes compile cleanly into `dist/` with sitemap | `npm run build` |
| Code Portability | `scripts/` modules run without hardcoded server paths | Hermetic test suite & script checks |
| Static Site Generation | `site/index.html` builds cleanly from `ops/ops.yaml` and `features/*.md` | `python3 scripts/generate_site.py` |
| Pre-Commit Hook | Automatically updates `site/index.html` when ops or features change | `hooks/pre-commit` |
| Secrets Quarantine | Zero plaintext credentials or tokens committed in repository | `grep -E 'sk-|token|password' ops/` |
| Clean Git Index | No case collision on macOS; untracked legacy files preserved on disk | `git status` clean |
