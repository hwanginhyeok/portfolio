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
| `docs/harness-integration.md` | Harness integration (Keychain secrets, `hih notify`, LaunchAgent schedules) |
| `docs/cutover.md` | macOS cutover record (done 2026-09-29): job table, state files, install/rollback commands |
| `docs/history/` | Archived legacy docs: `handoff.md`, `test-log.md`, `handoff-2026-05-19.md` |
| `docs/jd/` | Company application dossiers, materials, and staging inboxes |
| `features/_template.md` | Standard feature specification template |
| `features/README.md` | Feature spec index (one row per `features/*.md`) |
| `features/astro-portfolio.md` | Astro static portfolio web application |
| `features/jasoseol-collector.md` | Jasoseol recruitment calendar crawler & filter engine |
| `features/jasoseol-report.md` | Daily Jasoseol actionable report & `hih notify` announcement |
| `features/jasoseol-calendar.md` | Google Calendar recruitment deadline synchronization |
| `features/wanted-collector.md` | Wanted Korean tech recruitment crawler & state ledger |
| `features/global-collector.md` | Global enterprise ATS job board crawler & report |
| `features/applications-ledger.md` | Application tracking pipeline ledger & status report |
| `features/presentation-builder.md` | Graduate portfolio PPTX presentation deck generators |
| `features/harness-scheduling.md` | macOS LaunchAgent schedule + harness notify/secret integration |
| `features/apply-flow.md` | Shortlist, application kit, form-fill assist, ledger tracking |
| `features/collected-backup.md` | Daily commit + push of collector output |
| `ops/ops.yaml` | Operations inventory: services, schedules, state paths, secret names |
| `site/index.html` | Generated static operational dashboard |
| `scripts/generate_site.py` | Script generating `site/index.html` from `features/` and `ops/` |
| `hooks/pre-commit` | Pre-commit hook rebuilding `site/index.html` on change |
| `records/` | Generated worker runs and packs (git-ignored except `records/README.md`) |
| `launchd/` | The 7 `hih.portfolio.*` LaunchAgent plists (installed copies in `~/Library/LaunchAgents/` match) |
| `src/` | Astro website source code (pages, components, layouts, styles) |
| `scripts/` | Recruitment collectors, reporting utilities, and data repair tools |
| `tests/` | Hermetic, isolated unit tests (no network) |

---

## Where It Runs

- **Node**: macOS (this Mac). The six collector/report jobs moved here from the `server-pc` crontab on 2026-09-29 (t34; `infra/data/nodes/mac.yaml`); a seventh job backs up the collected data.
  - *Scheduled Jobs* (7 LaunchAgents, all loaded; `launchd/hih.portfolio.*.plist`): Jasoseol collect 08:30, Jasoseol calendar 08:34, Jasoseol report 08:36, Wanted collect 11:40, Applications report 11:47, Global collect 11:50, Collected backup 12:30 (Asia/Seoul).
  - *Secrets*: macOS Keychain via `hih-secret`; the harness owns the ops-bot entries (no plaintext env files).
  - *Notifications*: centralized ops bot via `hih notify` (the `--telegram` flag name is kept, delivery goes through `scripts/notify.py`).
  - *Runtime*: jobs run `~/Workspace/projects/portfolio/.venv/bin/python` in an Aqua session; logs in `~/Library/Logs/hih/portfolio_<job>.log`.

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
