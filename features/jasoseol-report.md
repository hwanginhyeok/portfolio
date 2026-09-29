# Feature: jasoseol-report

## What

Generates a responsive HTML digest of actionable, non-expired Jasoseol job postings and announces it with an urgent-deadline summary through the harness ops bot (`hih notify`).

## Entry points

- `python3 scripts/jasoseol_report.py --html` — Renders HTML report without dispatch
- `python3 scripts/jasoseol_report.py --telegram` — Renders HTML report and notifies via the harness ops bot
- `python3 scripts/jasoseol_report.py --dry-run` — Renders report to stdout without writing or sending

## Contract

- Inputs: Staged postings in `docs/jd/_inbox/jasoseol/*.md`, `config/jasoseol_targets.json`
- Outputs: HTML report in `docs/jd/report/jasoseol-YYYY-MM-DD.html`, one ops-bot message (report path included)
- Gate: Non-expired deadlines (`is_deadline_passed == False`) and actionable score threshold

## Data and state

- Repository data: `docs/jd/_inbox/jasoseol/`, `docs/jd/report/`
- External state: harness ops bot via `hih notify` (no per-project bot)
- Secrets: none held by portfolio; the harness owns the ops-bot Keychain entries

## Tests

- `.venv/bin/python -m pytest tests/test_jasoseol_report.py` (scoring, HTML rendering, caption formatting, deadline filtering, and ops notification)

## Status

live on server-pc via cron (`36 8 * * *`); prepared macOS LaunchAgent (absolute paths, not loaded); server cron still runs until the per-job cutover (`docs/cutover.md`).
