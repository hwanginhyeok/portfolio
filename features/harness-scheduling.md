# Feature: harness-scheduling

## What

Runs the six portfolio jobs (plus a seventh backup job, `features/collected-backup.md`) on the hih harness instead of the server crontab:
six macOS LaunchAgents whose times and arguments match the former server cron exactly (plus the backup agent),
notifications through the harness ops bot, and secrets through the Keychain.
Daily reports are written locally and announced with one ops message.

## Entry points

- `launchd/hih.portfolio.*.plist` — the seven LaunchAgents (all loaded; installed copies identical)
- `scripts/notify.py` — `send()` via `hih notify`; `secret()` via `hih-secret get`
- `scripts/jasoseol_calendar.py` — calendar writes through the `hih-schedule` CLI

## Contract

- Inputs: config files under `config/`, postings under `docs/jd/_inbox/`, and
  the current state ledgers (see `ops/ops.yaml`)
- Outputs: postings, state ledgers, HTML reports, one ops-bot message per report
  job, Google Calendar events
- Gate: the cutover was per job — the PM loaded the LaunchAgent and turned off
  the matching server cron line in the same step, so a side-effecting job never
  ran twice (done 2026-09-29)

## Data and state

- Repository data: `docs/jd/_inbox/{jasoseol,wanted,global}/`, `docs/jd/applications.json`, `dist/`
- External state: Google Calendar (personal), Telegram ops bot (via `hih notify`)
- Secrets: none held by portfolio; the harness owns the ops-bot Keychain entries
  it uses (`hih-secret`, names in the shared secret-name index)

## Tests

- `.venv/bin/python -m pytest tests/test_notify.py tests/test_jasoseol_report.py tests/test_jasoseol_calendar.py tests/test_applications_report.py`
- `.venv/bin/python -m pytest` (full suite)

## Status

Live. The six jobs moved from the server cron on 2026-09-29 (t34); all seven
agents are loaded and ran with exit 0 on 2026-10-14 (backup-collected had not
fired yet on its first day; verified 2026-10-15 with `launchctl print`). See
`docs/cutover.md` for the historical job table and `docs/runbook.md` for reload
and rollback.
