# Operations & Recovery Runbook (runbook.md)

## 1. Operating Model & Node Architecture

- **Current Operating Node**: `server-pc` (Linux / WSL).
  - Runs six scheduled cron jobs for Jasoseol, Wanted, Global ATS, and Applications reporting.
  - Server jobs must **not** be interrupted, killed, or modified during local development.
- **Local Development Node**: macOS.
  - Houses the canonical repository worktree (`~/Workspace/projects/portfolio`).
  - Runs hermetic unit tests (`uv run pytest tests/`) and Astro static site builds (`npm run build`).
  - Houses draft LaunchAgents in `launchd/` ready for future cutover.

---

## 2. Standard Operating Commands

### 2.1 Web Frontend (Astro)
```bash
# Install frontend dependencies (from local offline cache)
npm ci --prefer-offline --offline --legacy-peer-deps

# Start local Astro development server
npm run dev

# Build static production site (outputs to dist/)
npm run build

# Preview compiled production build
npm run preview
```

### 2.2 Python Test Suite
```bash
# Run all 90 hermetic unit tests via uv
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run a specific test suite
uv run pytest tests/test_job_collectors.py
```

### 2.3 Job Collectors (On-Demand / Dry-Run)
```bash
# Jasoseol collector (dry-run, no writes)
uv run python3 scripts/jasoseol_collect.py --dry-run

# Jasoseol report generation (HTML only, no Telegram)
uv run python3 scripts/jasoseol_report.py --html

# Jasoseol Google Calendar sync (dry-run plan)
uv run python3 scripts/jasoseol_calendar.py --dry-run

# Wanted collector (dry-run)
uv run python3 scripts/wanted_collect.py --dry-run

# Applications status report (markdown & HTML)
uv run python3 scripts/applications_report.py --html

# Global ATS collector (dry-run)
uv run python3 scripts/global_collect.py --dry-run
```

### 2.4 Diagnostic & Recovery Tools
```bash
# Diagnose and repair Wanted state ledger
uv run python3 scripts/wanted_state_repair.py

# Re-generate static operational overview site
uv run python3 scripts/generate_site.py
```

---

## 3. Routine Health Checks

| Check | Frequency | Command | Expected Outcome |
|---|---|---|---|
| Python Test Suite | Per commit / PR | `uv run pytest tests/` | 90 passed in <1s |
| Astro Web Build | Per content update | `npm run build` | 10 static routes generated in `dist/` |
| Wanted Ledger Health | Weekly | `python3 scripts/wanted_state_repair.py` | "Ledger is clean, 0 corrupt entries" |
| Overview Site Sync | Pre-commit | `python3 scripts/generate_site.py` | `site/index.html` updated |

---

## 4. Known Failure Modes & Recovery Procedures

### 4.1 Failure: Telegram Notification Fails / Credentials Missing
- **Symptoms**: Console log reports `WARNING: Telegram credentials not found in ...; report not sent` or HTTP 401/403.
- **Root Cause**: The script looks for `/home/window11/project-manager/.env` by default, which does not exist on macOS.
- **Recovery**:
  1. Provide credentials via environment variables:
     ```bash
     export PM_BOT_TOKEN="$(hih-secret get telegram/bot-token)"
     export PM_BOT_CHAT_ID="$(hih-secret get telegram/ops-chat-id)"
     ```
  2. Or specify an explicit `.env` path:
     ```bash
     python3 scripts/jasoseol_report.py --env /path/to/.env --telegram
     ```

### 4.2 Failure: Jasoseol API Rate Limiting or HTTP 500
- **Symptoms**: `ERROR: calendar fetch failed: HTTP 500 Server Error` or empty job lists.
- **Root Cause**: Jasoseol API temporary outage, upstream CDN block, or structural schema update.
- **Recovery**:
  1. Run with `--dry-run` to inspect API response without touching local files.
  2. Verify if cached detail files in `docs/jd/_inbox/jasoseol/.cache/` are intact.
  3. The collector is idempotent: retrying on the next scheduled run will resume fetching remaining IDs without re-fetching cached details.

### 4.3 Failure: Wanted State Ledger Discrepancy or Zero-Byte JDs
- **Symptoms**: `scripts/wanted_collect.py` re-crawls known jobs or skips valid postings.
- **Root Cause**: Process interrupted during write, or disk full condition during crawl.
- **Recovery**:
  1. Run the dedicated repair utility:
     ```bash
     python3 scripts/wanted_state_repair.py
     ```
  2. Verify ledger integrity:
     ```bash
     python3 -c "import json; data=json.load(open('docs/jd/_inbox/wanted/state.json')); print('Total tracked:', len(data))"
     ```

### 4.4 Failure: Google Calendar Sync Authorization Failure
- **Symptoms**: `scripts/jasoseol_calendar.py` reports `Schedule CLI error: OAuth token expired`.
- **Root Cause**: Stale Google Calendar OAuth credentials in local token storage.
- **Recovery**:
  1. Run calendar authentication diagnostic:
     ```bash
     hih-schedule auth check
     ```
  2. Refresh the OAuth token via standard HIH calendar workflow.
  3. Verify synchronization plan with dry-run:
     ```bash
     python3 scripts/jasoseol_calendar.py --dry-run
     ```

### 4.5 Failure: Astro Build Peer Dependency Warning
- **Symptoms**: `npm ci` fails with `ERESOLVE could not resolve peer dependency astro@^3.0.0 || ^4.0.0 || ^5.0.0 from @astrojs/tailwind@6.0.2`.
- **Root Cause**: `@astrojs/tailwind` version 6 has a legacy peer dependency range while Astro 6.1 is installed.
- **Recovery**:
  - Always use `--legacy-peer-deps` with `npm ci`:
    ```bash
    npm ci --prefer-offline --offline --legacy-peer-deps
    ```

---

## 5. Cutover Procedure (Server PC to macOS)

When the operator decides to decommission `server-pc` workloads for `portfolio`:
1. On `server-pc`:
   - Comment out or remove the six portfolio crontab lines:
     - `30 8 * * * ... jasoseol_collect.py`
     - `34 8 * * * ... jasoseol_calendar.py --apply`
     - `36 8 * * * ... jasoseol_report.py --telegram`
     - `40 11 * * * ... wanted_collect.py`
     - `47 11 * * * ... applications_report.py --telegram`
     - `50 11 * * * ... global_collect.py --telegram`
2. On macOS:
   - Ensure macOS Keychain holds `telegram/bot-token` and `telegram/ops-chat-id`.
   - Copy draft plists from `launchd/` to `~/Library/LaunchAgents/`.
   - Load each agent:
     ```bash
     launchctl load ~/Library/LaunchAgents/hih.portfolio.*.plist
     ```
3. Verify next morning's reports arrive in the Telegram ops channel on schedule.
