# Feature: global-collector

## What

Crawls career boards of global technology firms (Aptiv, Tesla, Apple, Applied Materials, Shield AI) across enterprise ATS APIs (Workday, Greenhouse, Ashby, Lever), filters actionable engineering openings with strict visa/sponsorship and owner-domain gates, and compiles HTML reports.

## Entry points

- `python3 scripts/global_collect.py` — Crawl and update global inbox
- `python3 scripts/global_collect.py --telegram` — Crawl and dispatch report via Telegram
- `python3 scripts/global_collect.py --dry-run` — Scan without persisting

## Contract

- Inputs: `config/global_targets.json`, ATS API endpoints
- Outputs: Markdown postings in `docs/jd/_inbox/global/{company}-{id}.md`, state ledger in `docs/jd/_inbox/global/state.json`
- Gate: Work authorization feasibility gates (ITAR exclusion, explicit visa sponsorship required for non-Korea APAC)

## Data and state

- Repository data: `docs/jd/_inbox/global/`, `config/global_targets.json`
- External state: Enterprise ATS endpoints
- Secrets: `PM_BOT_TOKEN`, `PM_BOT_CHAT_ID`

## Tests

- `uv run pytest tests/test_job_collectors.py` (includes global ATS corpus tests and eligibility gates)

## Status

live on server-pc via cron (`50 11 * * *`); draft LaunchAgent prepared in `launchd/hih.portfolio.global-collect.plist`.
