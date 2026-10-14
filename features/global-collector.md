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
- Secrets: none (the report notifies through the harness ops bot)

## Failure handling

- Board slugs verified live 2026-10-14: Wayve moved to Ashby (`ashby:wayve`), Shield AI to Lever (`lever:shieldai`); the old slugs returned 404 on every run (pf-4).
- `state.json` keeps `board_failures` (consecutive failed runs per source). One `hih notify --level warn` goes out when a source reaches 3 in a row; recovery resets the count, so a board that stays down does not alert daily.

## Tests

- `.venv/bin/python -m pytest tests/test_job_collectors.py` (includes global ATS corpus tests, eligibility gates, and the board-failure streak alert)

## Status

live on server-pc via cron (`50 11 * * *`); prepared macOS LaunchAgent (absolute paths, not loaded); server cron still runs until the per-job cutover (`docs/cutover.md`).
