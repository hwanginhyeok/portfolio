# Feature: collected-backup

## What

Commits and pushes the daily collector output (`docs/jd/_inbox/**`, the ledger and its Markdown view) so it is backed up. Before this job existed 590 collected files sat uncommitted for two weeks (finding pf-2).

## Entry points

- `python3 scripts/backup_collected.py` — dry run, lists what would be committed
- `python3 scripts/backup_collected.py --apply` — `git add -A` + commit + `hih git push` (gitleaks, non-force, both remotes)
- `launchd/hih.portfolio.backup-collected.plist` — 12:30 daily, after the 11:50 global collect (prepared, not loaded)

## Contract

- Inputs: the working tree of the live checkout
- Outputs: one commit `data: collector snapshot YYYY-MM-DD (N files)` touching only `BACKUP_PATHS`; source files are never staged
- Gate: nothing pending is a no-op; a failed commit or push sends one `hih notify --level error` and exits 1

## Data and state

- Repository data: `docs/jd/_inbox`, `docs/jd/applications.json`, `docs/jd/APPLICATIONS.md` (HTML report folders stay gitignored)
- External state: git remotes through `hih git push`
- Secrets: none

## Tests

- `.venv/bin/python -m pytest tests/test_apply_flow.py -k backup` (temp git repo: only collector paths committed, dry run commits nothing, idempotent, failed push alerts)

## Status

built 2026-10-14; plist prepared, not loaded. Review verdict: keep (once per day is enough, runs after the last collector, failure reaches the operator through `hih notify`). The PM runs it once against the live checkout and loads the LaunchAgent.
