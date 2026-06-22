# AGENTS.md

## Project Operating Contract

This repository is operated by multiple coding agents and LLM providers.
Do not rely on private chat memory. Read the shared files before making decisions.

## Required Startup Read

For handoff, review, debate, or implementation work, read:

- `HANDOFF.md`
- `DECISIONS.md`
- `REVIEW.md`
- `TEST_LOG.md`
- `LLM_BUDGET.md`
- `LLM_PROVIDERS.json`
- `WORK_LOG.md`
- latest `debate/runs/*/summary.json` when relevant

## Source of Truth

- Current task state: `HANDOFF.md`
- Durable decisions: `DECISIONS.md`
- Review findings and gates: `REVIEW.md`
- Verification commands/results: `TEST_LOG.md`
- Provider routing and budget policy: `LLM_PROVIDERS.json`, `LLM_BUDGET.md`
- Work history and rationale: `WORK_LOG.md`, `WORK_ITEMS/{work_id}.md`
- Raw model outputs: `debate/runs/{run_id}/`

Raw provider output is evidence, not final truth. Promote accepted conclusions into
`DECISIONS.md`, `REVIEW.md`, or `HANDOFF.md`.

Use `WORK_LOG.md` to connect why work started, which discussion/decision led to
it, how it was executed, and how it was verified.

Create `WORK_ITEMS/{work_id}.md` for non-trivial work that spans sessions,
involves provider fan-out, creates durable decisions, changes SSOT files, or has
risky/reversible consequences. Work ID format: `{PROJECT}-{YYYYMMDD}-{NN}`.

## Multi-Agent Rules

- State file ownership before editing.
- Avoid parallel edits to the same file unless explicitly coordinated.
- Use read-only provider runs for review.
- Use `--level quick` for cheap sanity checks, `--level normal` for normal work,
  and `--level hard` for risky changes or architecture disputes.
- Record tests and known failures in `TEST_LOG.md`.

## Provider Fan-out

Run the same context package through configured providers:

```bash
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py \
  --project . \
  --level hard \
  --mode debate \
  --prompt "Review this change and argue against weak assumptions."
```

Use `--dry-run` first when changing provider config.

## Validation

For the shared skill/provider infrastructure:

```bash
/home/gint_pcd/projects/hih-skills/scripts/check-ssot.sh
```
