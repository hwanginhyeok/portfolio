# Architecture Decisions (decisions.md)

This log records numbered architectural decisions (D1, D2, ...) for `portfolio` (포트폴리오), their dates, and rationales.

---

### D1: Job Collector Data Location & Staging Strategy
- **Date**: 2026-09-28
- **Context**: The repository contains ~3,000 tracked job posting markdown files, JSON caches, and state ledgers under `docs/jd/` (`docs/jd/_inbox/jasoseol/`, `docs/jd/_inbox/wanted/`, `docs/jd/_inbox/global/`, `docs/jd/applications.json`). The project standard generally separates code and data (principles: code, facts, rules, and records do not mix; run records and dynamic data live outside code repos). The user prompt asked to decide whether collector data stays in git or moves to `data/` (out of git).
- **Decision**: 
  1. **Phase 1 (Current)**: Maintain collector data and staging inboxes in `docs/jd/` inside git.
     - *Rationale*: Six active cron jobs currently run on `server-pc` writing to `docs/jd/_inbox/`. Furthermore, the regression test suite (`tests/test_job_collectors.py`) relies on specific sample postings in `docs/jd/_inbox/wanted` and `docs/jd/_inbox/global` as realistic corpus test fixtures. Moving or untracking ~3,000 files during Phase 1 would create an unnecessary diff blast and risk desynchronization between `server-pc` and macOS.
  2. **Phase 2 (Cutover to macOS)**: When scheduled workloads are transferred from `server-pc` crontab to macOS LaunchAgents, migrate dynamic collector staging inboxes to `data/jd/` (ignored in `.gitignore`) and preserve test corpus fixtures under `tests/fixtures/`.
- **Consequence**: Full backward compatibility with server-pc cron jobs is preserved; test suites remain deterministic; clean upgrade path defined.

---

### D2: Platform-Aware Path & Configuration Resolution (macOS / Linux WSL)
- **Date**: 2026-09-28
- **Context**: Collector scripts (`applications_report.py`, `global_collect.py`, `wanted_collect.py`, `jasoseol_report.py`, `jasoseol_calendar.py`) contained hardcoded Linux paths (`/home/window11/project-manager/.env` and `/home/window11/hih-skills/hih-schedule/scripts/hih_schedule.py`). On macOS, these paths do not exist.
- **Decision**: Make all external paths configurable via environment variables with fallback to server defaults:
  - `PORTFOLIO_PM_ENV` / `PM_ENV_PATH`: Configures the Telegram credentials `.env` path (defaults to `/home/window11/project-manager/.env`).
  - `HIH_SCHEDULE_CLI`: Configures the Google Calendar synchronization CLI path (defaults to `/home/window11/hih-skills/hih-schedule/scripts/hih_schedule.py`).
- **Consequence**: Code and tests execute seamlessly on macOS without altering default behavior on `server-pc`.

---

### D3: Transition Secrets from `.env` to `hih-secret` (macOS Keychain)
- **Date**: 2026-09-28
- **Context**: The collector scripts read `PM_BOT_TOKEN` and `PM_BOT_CHAT_ID` by parsing `/home/window11/project-manager/.env`. This creates an undesirable dependency on the legacy `project-manager` directory.
- **Decision**: Adopt the project standard: secrets never enter the repository. Catalog all secret names in `ops/ops.yaml` (`PM_BOT_TOKEN`, `PM_BOT_CHAT_ID`). On macOS, runtime shims retrieve credentials via `hih-secret get <name>` from macOS Keychain or environment variable injection.
- **Consequence**: Plaintext `.env` file reads will be retired; credentials are safely quarantined in the Keychain.

---

### D4: Centralize Notifications via `hih notify`
- **Date**: 2026-09-28
- **Context**: `applications_report.py`, `global_collect.py`, `jasoseol_report.py`, and `wanted_collect.py` contain independent urllib-based multipart HTTP implementations to dispatch messages and documents to Telegram.
- **Decision**: Plan transition to the centralized `hih notify` CLI in Phase 2. `hih notify` provides rate-limiting, error handling, and unified dispatch across HIH workloads without requiring per-script Telegram Bot API implementations.
- **Consequence**: Reduces boilerplate in Python scripts and unifies operational alerting under the HIH ops bot.

---

### D5: Retire Legacy Coordination Board, Task Trackers & Multi-Agent State
- **Date**: 2026-09-28
- **Context**: Legacy coordination files (`coordination/`), task trackers (`TASK.md`, `CURRENT_TASK.md`, `PREPARED_TASK.md`, `FINISHED_TASK.md`, `TASK_ARCHIVE/`), and multi-agent debate/ledger files (`WORK_ITEM.md`, `WORK_ITEMS/`, `WORK_LOG.md`, `TMUX_COLLAB.md`, `DEBATE.md`, `debate/`, `REVIEW.md`, `DIFFICULTY.md`, `VERIFY_DATA.md`, `ARCHIVE_POLICY.md`, `LLM_BUDGET.md`, `LLM_PROVIDERS.json`, `LLM_RUNS.md`) were tracked in git.
- **Decision**: Untrack coordination and task files from git tracking (`git rm --cached`), add them to `.gitignore`, and preserve their contents on disk for historical reference. All active and planned tasks are tracked via plan cards in `project-manager/plans/`.
- **Consequence**: Repository git history remains focused on production code and documentation; disk reference is intact.

---

### D6: macOS Case-Collision Resolution (`HANDOFF.md` vs `handoff.md`)
- **Date**: 2026-09-28
- **Context**: The git index contained both `HANDOFF.md` (8.5 KB, recent multi-agent state) and `handoff.md` (3.7 KB, 2026-05-19 historical handoff). On macOS case-insensitive APFS, these files collide, causing git to overwrite one with the other and report a dirty working directory on checkout.
- **Decision**: Resolve the collision using git index operations: extract `handoff.md` to `docs/history/handoff-2026-05-19.md` via `git show HEAD:handoff.md > file`, remove `handoff.md` from the git cache (`git rm --cached`), stage the new historical file, and restore `HANDOFF.md`.
- **Consequence**: Both handoff documents are preserved without loss; `git status` remains clean across macOS and Linux.

---

### D7: Non-Active LaunchAgent Drafts for Job Collectors
- **Date**: 2026-09-28
- **Context**: Under the standard, cron jobs migrate to macOS LaunchAgents listed in `infra/data/nodes/mac.yaml`. However, the six live collector jobs currently run on `server-pc` via crontab.
- **Decision**: Provide draft LaunchAgent `.plist` files under `launchd/` (Jasoseol collect, Jasoseol calendar, Jasoseol report, Wanted collect, Applications report, Global ATS collect). Do not load or bootstrap them into macOS `launchctl` while `server-pc` crontab is active.
- **Consequence**: Prevents duplicate crawling or double notifications to Telegram while making future macOS cutover instantaneous.

---

### D8: Dual Frontend and Data Engine Architecture
- **Date**: 2026-09-28
- **Context**: The repository houses both the Astro web platform (`src/`, `astro.config.mjs`, `tailwind.config.mjs`) and the Python recruitment intelligence pipeline (`scripts/`, `docs/jd/`).
- **Decision**: Maintain clear separation between the Astro presentation layer and the Python data collector pipeline. The Astro site builds independently (`npm run build`) with zero Python runtime dependency; Python collectors execute independently (`pytest tests/`) with zero node_modules dependency.
- **Consequence**: High cohesion, minimal coupling, and independent deployment cycles.

---

### D9: Ops notifications via `hih notify`, retire the per-project Telegram bot
- **Date**: 2026-09-29
- **Context**: `applications_report.py`, `global_collect.py`, `jasoseol_report.py`, and `wanted_collect.py` each built their own multipart `sendDocument`/`sendMessage` calls to `api.telegram.org`, reading `PM_BOT_TOKEN` / `PM_BOT_CHAT_ID` from a server env file. The project standard says notifications use `hih notify` (the ops bot), not per-project Telegram bots.
- **Decision**: Deliver one text message per report job through `hih notify` via a shared `scripts/notify.py` (`send()`), which resolves the harness entry point (env override, `PATH`, then the harness checkout). The HTML report is still written locally and its path rides in the message. The `--env` flag and the per-project bot credentials are removed.
- **Consequence**: No per-project bot or plaintext env read remains. While the harness ops channel is disabled, `hih notify` prints `[disabled]` and exits 0, so scheduled runs stay quiet. Attachments are no longer sent; the operator opens the local HTML by path.

---

### D10: macOS LaunchAgents use absolute paths, the project venv, and a per-job cutover
- **Date**: 2026-09-29
- **Context**: The server runs six crontab lines with `/usr/bin/python3` and a repo-root cwd. Launchd rejects a `~` in a plist (`EX_CONFIG`), and the collectors need `requests`/`pyyaml` from the project venv. Side-effecting jobs (Telegram, Calendar) must never run twice during the move.
- **Decision**: Each `launchd/hih.portfolio.*.plist` names absolute paths only (venv interpreter, script, working directory, log), keeps the exact server times and arguments, and loads in `Aqua` so `hih notify` can read the Keychain. The PM switches one job at a time: load the agent and comment out the matching server cron line in the same step, after rsyncing that job's state files; rollback is `launchctl bootout` + uncomment.
- **Consequence**: `hih node check` can see drift once the agents are listed in `infra/data/nodes/mac.yaml`; the prepared block is in `docs/cutover.md`. Nothing is loaded by the preparation step.

---

### D11: `jasoseol_calendar.py` invokes `hih-schedule` directly on macOS
- **Date**: 2026-09-29
- **Context**: The calendar script ran the server copies of the hih-schedule script under `sys.executable`. On macOS the calendar skill needs its own Google-API venv, and the old `/home/window11/...` path no longer exists.
- **Decision**: Default `HIH_SCHEDULE_CLI` to `~/bin/hih-schedule` and execute that CLI directly (its shebang picks its own interpreter) instead of prefixing `sys.executable`. The env override is kept.
- **Consequence**: No hardcoded server path remains; the calendar still writes only through `hih-schedule`.
