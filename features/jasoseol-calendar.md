# Feature: jasoseol-calendar

## What

Synchronizes actionable Jasoseol application deadlines directly to the operator's personal Google Calendar, ensuring urgent deadlines are visible in the user's primary schedule.

## Entry points

- `python3 scripts/jasoseol_calendar.py` — Dry-run synchronization plan
- `python3 scripts/jasoseol_calendar.py --apply` — Applies event creations, updates, or deletions to calendar

## Contract

- Inputs: Staged postings in `docs/jd/_inbox/jasoseol/*.md`, event tracking ledger `docs/jd/_inbox/jasoseol/calendar_events.json`
- Outputs: Calendar events on personal Google Calendar, updated ledger records
- Gate: Idempotent event markers (`[jasoseol:<id>]`) preventing duplicate entries

## Data and state

- Repository data: `docs/jd/_inbox/jasoseol/calendar_events.json`
- External state: Google Calendar API via `hih-schedule` CLI
- Secrets: Google Calendar OAuth token managed by harness

## Tests

- `uv run pytest tests/test_jasoseol_calendar.py` (9 tests covering event planning, idempotency, updates, and CLI parsing)

## Status

live on server-pc via cron (`34 8 * * *`); draft LaunchAgent prepared in `launchd/hih.portfolio.jasoseol-calendar.plist`.
