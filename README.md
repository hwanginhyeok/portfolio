# Portfolio & Recruitment Intelligence

Astro-powered physical AI engineering portfolio website + autonomous multi-channel job collection, scoring, reporting, and calendar synchronization pipeline.

---

## Layout

| Path | What |
|---|---|
| `README.md` | Purpose, layout, operational nodes, and execution guides |
| `docs/plan.md` | Project goals, scope, and migration phases |
| `docs/decisions.md` | Numbered architectural decisions (D1..D11) |
| `docs/runbook.md` | Operations, health diagnostics, and failure recovery runbooks |
| `docs/review-2026-09-28.md` | Comprehensive codebase review & severity audit |
| `docs/harness-integration.md` | Harness migration design (Keychain secrets, `hih notify`, LaunchAgent drafts) |
| `docs/cutover.md` | macOS cutover: job table, state files to rsync, rollback, `mac.yaml` block |
| `docs/history/` | Archived legacy docs: `handoff.md`, `test-log.md`, `handoff-2026-05-19.md` |
| `docs/jd/` | Company application dossiers, materials, and staging inboxes |
| `features/_template.md` | Standard feature specification template |
| `features/README.md` | Feature spec index (one row per `features/*.md`) |
| `features/astro-portfolio.md` | Astro static portfolio web application |
| `features/jasoseol-collector.md` | Jasoseol recruitment calendar crawler & filter engine |
| `features/jasoseol-report.md` | Daily Jasoseol actionable report & Telegram dispatcher |
| `features/jasoseol-calendar.md` | Google Calendar recruitment deadline synchronization |
| `features/wanted-collector.md` | Wanted Korean tech recruitment crawler & state ledger |
| `features/global-collector.md` | Global enterprise ATS job board crawler & report |
| `features/applications-ledger.md` | Application tracking pipeline ledger & status report |
| `features/presentation-builder.md` | Graduate portfolio PPTX presentation deck generators |
| `features/harness-scheduling.md` | macOS LaunchAgent schedule + harness notify/secret integration |
| `ops/ops.yaml` | Operations inventory: services, schedules, state paths, secret names |
| `site/index.html` | Generated static operational dashboard |
| `scripts/generate_site.py` | Script generating `site/index.html` from `features/` and `ops/` |
| `hooks/pre-commit` | Pre-commit hook rebuilding `site/index.html` on change |
| `records/` | Generated worker runs and packs (git-ignored except `records/README.md`) |
| `launchd/` | Draft LaunchAgent plists for macOS scheduling (inactive) |
| `src/` | Astro website source code (pages, components, layouts, styles) |
| `scripts/` | Recruitment collectors, reporting utilities, and data repair tools |
| `tests/` | Hermetic, isolated unit tests (no network) |

---

## Where It Runs

- **Current Node**: `server-pc` (Linux / WSL).
  - *Scheduled Jobs*: 6 crontab jobs (Jasoseol collect 08:30, Jasoseol calendar 08:34, Jasoseol report 08:36, Wanted collect 11:40, Applications report 11:47, Global collect 11:50).
  - *Server Safety*: This repository worktree is a local development checkout on macOS; it does **not** stop, alter, or restart server crontab processes.
- **Target Node**: macOS native.
  - *Secrets*: macOS Keychain via `hih-secret` (names in `ops/ops.yaml`, zero `.env` files).
  - *Notifications*: Centralized ops bot via `hih notify`.
  - *Schedules*: `launchd/hih.portfolio.*.plist` (drafts in `launchd/`, not loaded until cutover).

---

## How to Run

### Setup Environment
```bash
# Frontend setup (from offline cache)
npm ci --prefer-offline --offline --legacy-peer-deps

# Python virtual environment via uv
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install pytest requests pyyaml
```

### Run Web Frontend
```bash
# Start local dev server
npm run dev

# Build static production site (outputs 10 static pages to dist/)
npm run build
```

### Run Automated Tests
```bash
# Run the hermetic unit tests (100% offline, isolated tmp_path)
.venv/bin/python -m pytest tests/
```

### Regenerate Overview Site
```bash
.venv/bin/python scripts/generate_site.py
```
