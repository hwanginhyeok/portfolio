# Feature: jasoseol-report

## What

Generates a responsive HTML digest of actionable, non-expired Jasoseol job postings and dispatches it with an urgent-deadline summary directly to the operator via Telegram.

## Entry points

- `python3 scripts/jasoseol_report.py --html` — Renders HTML report without dispatch
- `python3 scripts/jasoseol_report.py --telegram` — Renders HTML report and dispatches via Telegram bot
- `python3 scripts/jasoseol_report.py --dry-run` — Renders report to stdout without writing or sending

## Contract

- Inputs: Staged postings in `docs/jd/_inbox/jasoseol/*.md`, `config/jasoseol_targets.json`
- Outputs: HTML report in `docs/jd/report/jasoseol-YYYY-MM-DD.html`, Telegram document attachment
- Gate: Non-expired deadlines (`is_deadline_passed == False`) and actionable score threshold

## Data and state

- Repository data: `docs/jd/_inbox/jasoseol/`, `docs/jd/report/`
- External state: Telegram Bot API (`https://api.telegram.org`)
- Secrets: `PM_BOT_TOKEN`, `PM_BOT_CHAT_ID`

## Tests

- `uv run pytest tests/test_jasoseol_report.py` (26 tests covering scoring, HTML rendering, caption formatting, deadline filtering, and Telegram dispatch)

## Status

live on server-pc via cron (`36 8 * * *`); draft LaunchAgent prepared in `launchd/hih.portfolio.jasoseol-report.plist`.
