# Feature: harness-scheduling

## What

Runs the six portfolio jobs on the hih harness instead of the server crontab:
six macOS LaunchAgents whose times and arguments match the server cron exactly,
notifications through the harness ops bot, and secrets through the Keychain.
Daily reports are written locally and announced with one ops message.

## Entry points

- `launchd/hih.portfolio.*.plist` — the six LaunchAgents (prepared, not loaded)
- `scripts/notify.py` — `send()` via `hih notify`; `secret()` via `hih-secret get`
- `scripts/jasoseol_calendar.py` — calendar writes through the `hih-schedule` CLI

## Contract

- Inputs: config files under `config/`, postings under `docs/jd/_inbox/`, and
  the current state ledgers (see `ops/ops.yaml`)
- Outputs: postings, state ledgers, HTML reports, one ops-bot message per report
  job, Google Calendar events
- Gate: cutover is per job — the PM loads the LaunchAgent and turns off the
  matching server cron line in the same step, so a side-effecting job never runs
  twice

## Data and state

- Repository data: `docs/jd/_inbox/{jasoseol,wanted,global}/`, `docs/jd/applications.json`, `dist/`
- External state: Google Calendar (personal), Telegram ops bot (via `hih notify`)
- Secrets: none held by portfolio; the harness owns the ops-bot Keychain entries
  it uses (`hih-secret`, names in the shared secret-name index)

## Tests

- `.venv/bin/python -m pytest tests/test_notify.py tests/test_jasoseol_report.py tests/test_jasoseol_calendar.py tests/test_applications_report.py`
- `.venv/bin/python -m pytest` (full suite)

## Status

Prepared (t34 step 1). Server cron still owns the schedule; the LaunchAgents
are validated with `plutil -lint` and are not loaded. See `docs/cutover.md` for
the job table, state files to rsync, rollback, and the proposed
`infra/data/nodes/mac.yaml` block.
