# Feature: wanted-collector

## What

Crawls tech job postings from the Wanted API, assesses candidate profile fit with owner-domain gating, writes matching postings to `docs/jd/_inbox/wanted/`, and maintains the Wanted deduplication ledger.

## Entry points

- `python3 scripts/wanted_collect.py` — Crawl and update Wanted inbox
- `python3 scripts/wanted_collect.py --dry-run` — Scan without persisting
- `python3 scripts/wanted_state_repair.py` — Verifies and repairs the Wanted state ledger

## Contract

- Inputs: `config/wanted_targets.json`, Wanted API endpoints (`/api/chaos/search/v1/results`, `/api/v4/jobs/`)
- Outputs: Markdown postings in `docs/jd/_inbox/wanted/{id}-{company}.md`, state ledger in `docs/jd/_inbox/wanted/state.json`
- Gate: Strict owner-domain gates (Robotics, Power Electronics, Test & Reliability Engineering)

## Data and state

- Repository data: `docs/jd/_inbox/wanted/`, `config/wanted_targets.json`
- External state: Wanted public API
- Secrets: None for crawl; `PM_BOT_TOKEN`, `PM_BOT_CHAT_ID` if `--telegram` flag used

## Tests

- `uv run pytest tests/test_job_collectors.py` (27 tests covering scoring, address pattern, false-positive exclusion, and state repair)

## Status

live on server-pc via cron (`40 11 * * *`); draft LaunchAgent prepared in `launchd/hih.portfolio.wanted-collect.plist`.
