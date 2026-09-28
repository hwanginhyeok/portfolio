# Feature: applications-ledger

## What

Tracks Hwang Inhyeok's active application pipeline across all companies, maintaining a single source of truth ledger, regenerating the human-readable Markdown view, and rendering an actionable morning Telegram report.

## Entry points

- `python3 scripts/applications_report.py` — Rewrites `docs/jd/APPLICATIONS.md` from ledger
- `python3 scripts/applications_report.py --html` — Renders HTML digest
- `python3 scripts/applications_report.py --html --telegram` — Renders HTML and dispatches to Telegram

## Contract

- Inputs: Ledger JSON `docs/jd/applications.json`
- Outputs: Markdown table in `docs/jd/APPLICATIONS.md`, HTML report in `docs/jd/report/applications-YYYY-MM-DD.html`
- Gate: Valid status values (`미지원`, `준비중`, `준비완료`, `제출`, `서류탈락`, `면접`, `오퍼`, `보류`, `마감`)

## Data and state

- Repository data: `docs/jd/applications.json`, `docs/jd/APPLICATIONS.md`
- External state: Telegram Bot API
- Secrets: `PM_BOT_TOKEN`, `PM_BOT_CHAT_ID`

## Tests

- `uv run pytest tests/test_applications_report.py` (11 tests covering ledger loading, status sorting, HTML rendering, and Telegram delivery)

## Status

live on server-pc via cron (`47 11 * * *`); draft LaunchAgent prepared in `launchd/hih.portfolio.applications-report.plist`.
