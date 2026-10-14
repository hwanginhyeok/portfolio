# Feature: jasoseol-collector

## What

Automated crawler that queries Jasoseol (자소설닷컴) calendar and recruit APIs, filters experienced job openings matching the candidate's profile (Robotics, HW/SW/Embedded, Power Electronics, Machinery), scores each posting, and stores matching records in an inbox directory.

## Entry points

- `python3 scripts/jasoseol_collect.py` — Standard crawl and sync
- `python3 scripts/jasoseol_collect.py --dry-run` — Dry-run plan without file writes

## Contract

- Inputs: `config/jasoseol_targets.json`, Jasoseol calendar API (`https://jasoseol.com/employment/calendar_list.json`)
- Outputs: Markdown job postings in `docs/jd/_inbox/jasoseol/{id}.md`, deduplication ledger in `docs/jd/_inbox/jasoseol/state.json`
- Gate: Score threshold (min score 28) and strict duty-family exclusions

## Data and state

- Repository data: `docs/jd/_inbox/jasoseol/`, `config/jasoseol_targets.json`
- External state: Jasoseol HTTP API endpoint
- Secrets: None (public calendar API)

## Tests

- `.venv/bin/python -m pytest tests/test_jasoseol_collect.py` (calendar query, detail fetch, score filtering, and dry-run)

## Status

live on macOS: LaunchAgent `hih.portfolio.jasoseol-collect` (08:30 Asia/Seoul, loaded; moved from the server cron 2026-09-29, t34). See `docs/cutover.md`.
