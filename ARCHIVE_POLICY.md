# ARCHIVE_POLICY

## Principle

Keep root files small and current. Preserve evidence and completed work in
monthly archive folders. Do not archive durable decisions.

## File Classes

| Class | Files | Policy |
|---|---|---|
| Manifest | `AGENTS.md`, `LLM_PROVIDERS.json`, `LLM_BUDGET.md`, `TMUX_COLLAB.md` | Keep current in root. Version through git. |
| Live state | `HANDOFF.md`, `REVIEW.md`, `TEST_LOG.md`, `WORK_LOG.md`, task files | Keep current in root. Snapshot or roll older sections into archive. |
| Durable truth | `DECISIONS.md` | Append-only. Do not archive away from root. |
| Work details | `WORK_ITEMS/{work_id}.md` | Keep active items in `WORK_ITEMS/`; move completed/stale items to `archive/YYYY-MM/WORK_ITEMS/` using `completed:` date. |
| Provider evidence | `debate/runs/{run_id}/` | Keep in place by default. Archive as index-only unless no inbound references exist. |
| Scratch pane output | `debate/*.md`, ad hoc captures | Promote useful parts or archive/delete after review. |

## Archive Criteria

Archive candidates:

- completed `WORK_ITEMS` older than 30 days, based on frontmatter `completed:`
- provider runs older than 30 days with `decision.md`, marked in archive index only
- `TEST_LOG.md` sections older than 60 days, after summary remains
- resolved `REVIEW.md` provider-run sections after a monthly summary exists

Do not archive:

- unresolved work
- current handoff
- `DECISIONS.md`
- files referenced by an active task unless the reference is updated

## Commands

Dry-run:

```bash
/home/gint_pcd/projects/hih-skills/scripts/archive-collab.py /path/to/project
```

Apply:

```bash
/home/gint_pcd/projects/hih-skills/scripts/archive-collab.py /path/to/project --apply
```

The tool is conservative. It moves only completed work items. Provider runs are
index-only by default so existing `REVIEW.md` links do not break.

## Work ID

Use:

```text
{PROJECT}-{YYYYMMDD}-{NN}
```

Examples:

- `PM-20260622-01`
- `HI2-20260622-01`

Use the same ID in `WORK_LOG.md`, `WORK_ITEMS/{work_id}.md`, `DECISIONS.md`
source links, and related debate prompts.
