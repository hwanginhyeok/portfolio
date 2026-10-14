# Portfolio macOS cutover (t34) — done 2026-09-29

**Status: done.** The six jobs moved from the `server-pc` crontab to the macOS
LaunchAgents under `launchd/` on 2026-09-29 (`infra/data/nodes/mac.yaml` lists
them as `approved`, "moved from the server 2026-09-29 (t34)"). All are loaded;
the installed plists in `~/Library/LaunchAgents/` are identical to the repo copies
(checked 2026-10-15). A seventh agent, `hih.portfolio.backup-collected` (12:30), was
added on 2026-10-14 and has no server twin (`features/collected-backup.md`).
The tables below are the historical switch record; the server crontab itself
was not re-checked in this sweep.

## Job table

| Cron time (Asia/Seoul, now the agent schedule) | Former server command | Mac LaunchAgent label | Mac argv | Log |
|---|---|---|---|---|
| `30 8 * * *` | `scripts/jasoseol_collect.py` | `hih.portfolio.jasoseol-collect` | `scripts/jasoseol_collect.py` | `~/Library/Logs/hih/portfolio_jasoseol_collect.log` |
| `34 8 * * *` | `scripts/jasoseol_calendar.py --apply` | `hih.portfolio.jasoseol-calendar` | `scripts/jasoseol_calendar.py --apply` | `...portfolio_jasoseol_calendar.log` |
| `36 8 * * *` | `scripts/jasoseol_report.py --html --telegram` | `hih.portfolio.jasoseol-report` | `scripts/jasoseol_report.py --html --telegram` | `...portfolio_jasoseol_report.log` |
| `40 11 * * *` | `scripts/wanted_collect.py` | `hih.portfolio.wanted-collect` | `scripts/wanted_collect.py` | `...portfolio_wanted_collect.log` |
| `47 11 * * *` | `scripts/applications_report.py --html --telegram` | `hih.portfolio.applications-report` | `scripts/applications_report.py --html --telegram` | `...portfolio_applications_report.log` |
| `50 11 * * *` | `scripts/global_collect.py --html --telegram` | `hih.portfolio.global-collect` | `scripts/global_collect.py --html --telegram` | `...portfolio_global_collect.log` |

Every plist uses absolute paths only (`~` anywhere in a plist makes launchd fail
the spawn with `EX_CONFIG`):

- interpreter: `/Users/hwang-inhyeok/Workspace/projects/portfolio/.venv/bin/python`
- script: `/Users/hwang-inhyeok/Workspace/projects/portfolio/scripts/<job>.py`
- working directory: `/Users/hwang-inhyeok/Workspace/projects/portfolio`
- logs: `/Users/hwang-inhyeok/Library/Logs/hih/portfolio_<job>.log`
- session: `Aqua` (needed for `hih notify` to read the Keychain)

## State files rsynced before each switch (historical)

| Job | State to rsync (server-pc -> mac) |
|---|---|
| jasoseol-collect | `docs/jd/_inbox/jasoseol/state.json` (and `docs/jd/_inbox/jasoseol/.cache/`) |
| jasoseol-calendar | `docs/jd/_inbox/jasoseol/calendar_events.json` |
| jasoseol-report | none (renders from the inbox) |
| wanted-collect | `docs/jd/_inbox/wanted/state.json` |
| applications-report | `docs/jd/applications.json` |
| global-collect | `docs/jd/_inbox/global/state.json` |

## Switch and rollback (historical; current reload steps are in `docs/runbook.md` section 5)

Switch one job in the same step on both sides so a side-effecting job never runs
twice:

    # mac
    cp launchd/<label>.plist $HOME/Library/LaunchAgents/
    launchctl bootstrap gui/$(id -u) $HOME/Library/LaunchAgents/<label>.plist
    # server-pc: comment out the matching cron line

Rollback = unload the agent and uncomment the server line:

    launchctl bootout gui/$(id -u) $HOME/Library/LaunchAgents/<label>.plist

State is rsynced, not moved, so rollback loses nothing. Watch 2 days on the Mac
alone before deleting the server copy.

## Harness integration changes in this step

- **Notifications** — the four report jobs no longer build Telegram HTTP
  requests. `scripts/notify.py` sends one text message through the harness ops
  bot (`hih notify`); the HTML report stays local under `docs/jd/report/` or
  `docs/jd/_inbox/*/report/` and its path is included in the message. The
  per-project PM bot credentials and the `--env` flag are gone.
- **Secrets** — no portfolio script reads a secret directly any more. The
  harness owns the ops-bot Keychain entries it needs; `scripts/notify.py`
  exposes `secret()` (`hih-secret get NAME`) as the sanctioned accessor for any
  future credential. Names live in the shared secret-name index.
- **Calendar** — `jasoseol_calendar.py` still writes through `hih-schedule`,
  now invoked directly (`~/bin/hih-schedule`, its own Google venv) instead of
  the removed server path. `HIH_SCHEDULE_CLI` still overrides it.
- **Paths** — no `/home/window11` or old `project-manager` path remains in the
  six scripts or anything they import.
- **Account emails** — none of the six scripts use an account email, so no
  `infra/data/identities.yaml` id was needed.

## `infra/data/nodes/mac.yaml`

The six cutover agents are listed under `desired.launch_agents` with
`status: approved`. `hih.portfolio.backup-collected` is installed and loaded but
is not listed there yet (open finding, 2026-10-15).

## Skipped gates

The old runtime_v2 gates (preflight and context envelopes) were **skipped** for
this step: the project standard retires runtime_v2, so there is no preflight or
context-envelope check to run. No replacement gate was added here.
