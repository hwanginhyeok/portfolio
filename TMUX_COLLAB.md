# TMUX_COLLAB

## Layout

Recommended panes:

| Pane | Role |
|---|---|
| 1 | Claude |
| 2 | Codex |
| 3 | provider fan-out / GLM |
| 4 | tests/dev server |
| 5 | git/logs |

## Rules

- Important context goes into files, not chat memory.
- Each model gets an explicit file ownership boundary before editing.
- Use `HANDOFF.md` before switching models.
- Use `REVIEW.md` for cross-check results.
- Use `DEBATE.md` when models disagree.
- Use `git diff` and test logs as the shared source of truth.
- Use `LLM_PROVIDERS.json` to decide which providers run.
- Use `LLM_BUDGET.md` to keep token/subscription usage intentional.
- Use `WORK_LOG.md` to connect discussion, decision, execution, and verification.

## Capture

Capture a pane into a file before handing it to another model:

```bash
tmux capture-pane -p -t {session}:{window}.{pane} > debate/claude.md
```

Append command output to the test log:

```bash
{command} 2>&1 | tee -a TEST_LOG.md
```

## Handoff Loop

1. Current model updates `HANDOFF.md`.
2. Next model reads `HANDOFF.md`, `DECISIONS.md`, `REVIEW.md`, and `git diff`.
3. Next model states the first action before editing.
4. Reviewer model writes findings to `REVIEW.md`.
5. Final decision goes into `DECISIONS.md`.

## Provider Fan-out

Run the same prompt against configured providers:

```bash
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py \
  --project . \
  --level hard \
  --mode debate \
  --prompt "이 변경의 리스크와 반대 의견을 찾아라."
```

Or run fan-out and promotion draft together:

```bash
/home/gint_pcd/projects/hih-skills/scripts/hih-collab.sh \
  --project . \
  --level hard \
  --mode debate \
  --prompt "이 변경의 리스크와 반대 의견을 찾아라."
```

Outputs are written to:

```text
debate/runs/{run_id}/prompt.md
debate/runs/{run_id}/glm.md
debate/runs/{run_id}/codex.md
debate/runs/{run_id}/claude.md
debate/runs/{run_id}/summary.json
```

Use `--dry-run` before expensive calls.

After a run, prepare a promotion draft:

```bash
/home/gint_pcd/projects/hih-skills/scripts/llm-promote-run.py \
  debate/runs/{run_id} \
  --append-review
```

Accept/reject/defer the findings, then copy durable conclusions into the SSOT files.
