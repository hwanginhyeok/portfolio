# LLM_BUDGET

## Policy

- Prefer flat-rate or underused providers first.
- Use expensive/high-value providers for final review, architecture disputes, and hard bugs.
- Do not rely on any provider's private memory. Every run must read the shared files.
- Record important conclusions in `DECISIONS.md`, not only in provider output.

## Provider Roles

| Provider | Budget Type | Priority | Best Use | Notes |
|---|---|---:|---|---|
| GLM | flat-rate | 10 | cheap-first critique, broad second opinion | Good default when quota is available. |
| Codex | subscription/API | 20 | implementation, repo-aware validation | Keep sandbox read-only for review runs. |
| Claude | subscription | 30 | architecture, product judgement, adversarial review | Use for hard decisions and final challenge. |

## Run Levels

| Level | Providers | Use When |
|---|---|---|
| quick | GLM | Low-risk sanity check |
| normal | GLM + Codex | Code changes, implementation choices |
| hard | GLM + Codex + Claude | Risky refactor, release gate, architecture dispute |

## Promotion Rule

Provider output under `debate/runs/` is evidence. It does not become project truth
until a human or PM model promotes it into `REVIEW.md`, `DECISIONS.md`, `HANDOFF.md`,
or `TEST_LOG.md`.

Prepare a promotion draft:

```bash
/home/gint_pcd/projects/hih-skills/scripts/llm-promote-run.py debate/runs/{run_id} --append-review
```

## Manual Overrides

Use specific providers when needed:

```bash
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py --project . --level quick --prompt "..."
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py --project . --level normal --prompt "..."
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py --project . --level hard --mode debate --prompt "..."

# Explicit override
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py --project . --providers glm --prompt "..."
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py --project . --providers glm,codex --prompt "..."
/home/gint_pcd/projects/hih-skills/scripts/llm-fanout.py --project . --providers glm,codex,claude --mode debate --prompt "..."
```
