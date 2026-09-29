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
- External state: Google Calendar API via the `hih-schedule` CLI (invoked directly on macOS)
- Secrets: Google Calendar OAuth token managed by harness

## Tests

- `.venv/bin/python -m pytest tests/test_jasoseol_calendar.py` (event planning, idempotency, updates, CLI parsing, and direct CLI exec)

## Status

live on server-pc via cron (`34 8 * * *`); prepared macOS LaunchAgent (absolute paths, not loaded); server cron still runs until the per-job cutover (`docs/cutover.md`).
