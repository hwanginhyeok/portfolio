# Operations & Recovery Runbook (runbook.md)

## 1. Operating Model & Node Architecture

- **Current Operating Node**: `server-pc` (Linux / WSL).
  - Runs six scheduled cron jobs for Jasoseol, Wanted, Global ATS, and Applications reporting.
  - Server jobs must **not** be interrupted, killed, or modified during local development.
- **Migration Node**: macOS.
  - Houses the canonical repository worktree (`~/Workspace/projects/portfolio`).
  - Runs hermetic unit tests (`.venv/bin/python -m pytest tests/`) and Astro static site builds (`npm run build`).
  - Houses prepared LaunchAgents in `launchd/` (absolute paths, exact server times); cutover is per job (`docs/cutover.md`).

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
.venv/bin/python -m pytest tests/

# Run with verbose output
.venv/bin/python -m pytest tests/ -v

# Run a specific test suite
.venv/bin/python -m pytest tests/test_job_collectors.py
```

### 2.3 Job Collectors (On-Demand / Dry-Run)
```bash
# Jasoseol collector (dry-run, no writes)
.venv/bin/python scripts/jasoseol_collect.py --dry-run

# Jasoseol report generation (HTML only, no Telegram)
.venv/bin/python scripts/jasoseol_report.py --html

# Jasoseol Google Calendar sync (dry-run plan)
.venv/bin/python scripts/jasoseol_calendar.py --dry-run

# Wanted collector (dry-run)
.venv/bin/python scripts/wanted_collect.py --dry-run

# Applications status report (markdown & HTML)
.venv/bin/python scripts/applications_report.py --html

# Global ATS collector (dry-run)
.venv/bin/python scripts/global_collect.py --dry-run
```

### 2.4 Diagnostic & Recovery Tools
```bash
# Diagnose and repair Wanted state ledger
.venv/bin/python scripts/wanted_state_repair.py

# Re-generate static operational overview site
.venv/bin/python scripts/generate_site.py
```

---

## 3. Routine Health Checks

| Check | Frequency | Command | Expected Outcome |
|---|---|---|---|
| Python Test Suite | Per commit / PR | `.venv/bin/python -m pytest tests/` | All pass except the date-sensitive live-inbox assertion (needs >=5 future deadlines) |
| Astro Web Build | Per content update | `npm run build` | 10 static routes generated in `dist/` |
| Wanted Ledger Health | Weekly | `python3 scripts/wanted_state_repair.py` | "Ledger is clean, 0 corrupt entries" |
| Overview Site Sync | Pre-commit | `python3 scripts/generate_site.py` | `site/index.html` updated |

---

## 4. Known Failure Modes & Recovery Procedures

### 4.1 Failure: Ops notification not delivered
- **Symptoms**: no ops message arrived; the job log shows
  `[notify] report delivery failed or not attempted`.
- **Root cause**: the harness ops channel is disabled (`notify.enabled` off in
  the Telegram registry), the Keychain entries are missing, or the job did not
  run in an Aqua session (Keychain is unreachable outside it).
- **Recovery**:
  1. Confirm the channel: `hih notify "portfolio test"` prints `[disabled]`
     while the ops channel is off and exits 0.
  2. Confirm the ops-bot entries exist in the Keychain (names in the shared
     secret-name index); import/repair them if absent.
  3. Confirm the LaunchAgent has `LimitLoadToSessionType = Aqua`, then reload it.
- **Note**: the HTML report is still written locally even if the notification
  fails; check `docs/jd/report/` and `docs/jd/_inbox/*/report/`.

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

Per job, in one step so a side-effecting job never runs twice
(project-standard "Cutover"; job table and state files in `docs/cutover.md`):

1. On `server-pc`: leave the job's cron line running until the Mac agent is up.
2. Rsync the job's state files from `server-pc` to the Mac (see `docs/cutover.md`).
3. On macOS:
   ```bash
   cp launchd/<label>.plist $HOME/Library/LaunchAgents/
   launchctl bootstrap gui/$(id -u) $HOME/Library/LaunchAgents/<label>.plist
   ```
4. On `server-pc`: comment out that job's cron line in the same step.
5. Watch 2 days on the Mac alone, then delete the server copy.

Rollback (any time in the 2-day watch):

```bash
launchctl bootout gui/$(id -u) $HOME/Library/LaunchAgents/<label>.plist
```

then uncomment the server cron line. State is rsynced, not moved, so nothing is
lost.

Ensure the project venv exists before the first load (README "Setup
Environment"): `.venv/bin/python` is what every plist runs.
