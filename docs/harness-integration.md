# Harness Integration (docs/harness-integration.md)

How `portfolio` (포트폴리오) uses the HIH harness, as required by the shared
project standard ("Harness integration"). This supersedes the earlier design
where the report scripts talked to Telegram directly.

---

## 1. Notifications (`hih notify`)

- `scripts/notify.py::send(text, title=..., level=...)` runs the harness entry
  point `hih notify --title <t> --level <l> <text>` with `subprocess`. It
  resolves the entry point from `HIH_BIN` (binary or bin directory), then
  `PATH`, then the harness checkout.
- `hih notify` is **text only** and send-only. It gates on `notify.enabled`:
  while the ops channel is off it prints `[disabled]` and exits 0, so scheduled
  runs stay quiet by construction.
- The four report jobs (`jasoseol_report`, `applications_report`,
  `wanted_collect`, `global_collect`) send one Korean summary per run. The HTML
  report is still written locally (`docs/jd/report/`, `docs/jd/_inbox/*/report/`)
  and its path is included in the message instead of being attached.
- The old per-project Telegram bot (`PM_BOT_TOKEN` / `PM_BOT_CHAT_ID`) and the
  `--env` flag are retired.

## 2. Secrets (`hih-secret`)

- No portfolio script reads a secret directly. `scripts/notify.py::secret(name)`
  wraps `hih-secret get <NAME>` as the sanctioned accessor if a job ever needs
  one; values are never logged, printed, or committed.
- The harness resolves the ops-bot token/chat id from the macOS Keychain itself.
  The relevant names live in the shared secret-name index (names only).
- LaunchAgents load in the `Aqua` session so the Keychain is reachable.

## 3. Schedules (`launchd/`)

Six prepared LaunchAgents, one per server cron line, with absolute paths
(venv interpreter, script, working directory, log), the exact server times and
arguments, and `LimitLoadToSessionType = Aqua`:

| Label | Time (Asia/Seoul) | argv |
|---|---|---|
| `hih.portfolio.jasoseol-collect` | 08:30 | `scripts/jasoseol_collect.py` |
| `hih.portfolio.jasoseol-calendar` | 08:34 | `scripts/jasoseol_calendar.py --apply` |
| `hih.portfolio.jasoseol-report` | 08:36 | `scripts/jasoseol_report.py --html --telegram` |
| `hih.portfolio.wanted-collect` | 11:40 | `scripts/wanted_collect.py` |
| `hih.portfolio.applications-report` | 11:47 | `scripts/applications_report.py --html --telegram` |
| `hih.portfolio.global-collect` | 11:50 | `scripts/global_collect.py --html --telegram` |

They are **not loaded** until the per-job cutover; see `docs/cutover.md` for the
job table, state files to rsync, rollback, and the `infra/data/nodes/mac.yaml`
block.

## 4. Portability

- No `/home/window11` or old `project-manager` path remains in the six scripts
  or anything they import.
- `jasoseol_calendar.py` defaults `HIH_SCHEDULE_CLI` to `~/bin/hih-schedule` and
  executes that CLI directly (its own Google-API venv); the env override is
  kept.
- All intra-repository paths resolve from `Path(__file__).resolve().parent.parent`.

## 5. Legacy replacements

| Legacy component | Replacement | Switch |
|---|---|---|
| Per-project Telegram bot + plaintext env file | `hih notify` (ops bot) via `scripts/notify.py` | t34 step 1 (2026-09-29) |
| Server cron schedule | `launchd/hih.portfolio.*.plist` (per-job cutover) | t34 step 2 |
| `hih-schedule` under `sys.executable` | `~/bin/hih-schedule` invoked directly | t34 step 1 |
| In-repo work tracking | plan cards in `project-manager/plans/` | done (Phase 1) |
| runtime_v2 (preflight, context envelopes) | retired; no replacement gate | done |
| Run receipts | `<project>/records/runs/` via hih-worker | done (Phase 1) |
| Web site preview | Astro (`npm run dev` / `npm run build`) | done (Phase 1) |
