# PM-311 — Make this repo's skill file loadable

## Project root

/home/window11/포트폴리오

## The defect

`.claude/skills/case-study.md` is a bare `.md` file sitting directly under
`.claude/skills/`. Claude Code only loads a skill from `<dir>/SKILL.md` with YAML
frontmatter containing `name:` and `description:`, so this file has never been
discovered by any session in this repository.

## Work

1. Read `.claude/skills/case-study.md` and confirm it is an invocable procedure
   (a prior pass saw an explicit trigger and a Situation→Task→Action→Result flow).
   If it is reference material rather than a procedure, say so and move it under
   `docs/` instead of converting — then stop.
2. Create `.claude/skills/case-study/SKILL.md` with the body preserved verbatim
   below new frontmatter:

   ```yaml
   ---
   name: case-study
   description: <one line: what it does and when to invoke it>
   ---
   ```

   Write `description` as a trigger, not a title — the concrete conditions and the
   Korean phrases a user would actually say. For house style, read two or three
   `SKILL.md` files under `~/hih-skills/` (read-only).
3. Remove the original bare file only after the directory form is in place.
4. Verify no bare `.md` remains directly under `.claude/skills/`, and that the
   frontmatter `name:` matches the directory name.

## Constraints

- Do not commit and do not push.
- Do not modify anything outside this repository.
- Do not rewrite the substance of the file — frontmatter and relocation only.
- Preserve the unrelated dirty working-tree file already present.

## Receipt

The `description:` line written, the final `.claude/skills/` listing, and the exact
changed-path list for the PM to commit.
