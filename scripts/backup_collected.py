#!/usr/bin/env python3
"""Commit and push the collector output so it is backed up (pf-2).

The collectors write ~590 posting files plus state.json under docs/jd/_inbox
every day, but nothing committed them: the last commit was 2026-10-07 while
the data kept changing, so the only copy lived on one disk. This job runs
after the report jobs, stages only the collector paths, commits when something
changed and pushes with `hih git push` (gitleaks, non-force, both remotes).

Usage:
    python3 scripts/backup_collected.py            # dry run: list what would be committed
    python3 scripts/backup_collected.py --apply    # commit + push
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:  # package import when tested; direct import when run as a script
    from scripts.notify import HIH_BIN, send as notify_send
except ModuleNotFoundError:  # pragma: no cover - exercised by CLI execution
    from notify import HIH_BIN, send as notify_send

REPO = Path(__file__).resolve().parent.parent
# Only collector output and the application ledger; never source or other docs.
BACKUP_PATHS = ("docs/jd/_inbox", "docs/jd/applications.json", "docs/jd/APPLICATIONS.md")
KST = timezone(timedelta(hours=9))


def log(message: str) -> None:
    print(message, flush=True)


def git(repo: Path, *args: str, runner=subprocess.run) -> subprocess.CompletedProcess:
    return runner(["git", "-C", str(repo), *args], capture_output=True, text=True)


def existing_paths(repo: Path) -> list[str]:
    """BACKUP_PATHS present on disk (git rejects a pathspec that matches nothing)."""
    return [path for path in BACKUP_PATHS if (repo / path).exists()]


def pending_paths(repo: Path, runner=subprocess.run) -> list[str]:
    """Changed or untracked files under BACKUP_PATHS (gitignored report dirs excluded by git)."""
    paths = existing_paths(repo)
    if not paths:
        return []
    result = git(repo, "status", "--porcelain", "--untracked-files=all", "--", *paths,
                 runner=runner)
    if result.returncode != 0:
        raise RuntimeError(f"git status failed: {result.stderr.strip()}")
    return [line[3:] for line in result.stdout.splitlines() if line.strip()]


def run(repo: Path = REPO, apply: bool = False, runner=subprocess.run, notify=notify_send,
        now: datetime | None = None) -> int:
    now = now or datetime.now(KST)
    try:
        pending = pending_paths(repo, runner)
    except RuntimeError as err:
        log(f"ERROR: {err}")
        notify(f"수집 데이터 백업 실패: {err}", title="portfolio backup", level="error")
        return 1
    if not pending:
        log("[backup] nothing to commit")
        return 0
    paths = existing_paths(repo)
    log(f"[backup] {len(pending)} changed file(s) under {', '.join(paths)}")
    if not apply:
        log("[backup] dry run; pass --apply to commit and push")
        return 0
    message = f"data: collector snapshot {now.date().isoformat()} ({len(pending)} files)"
    for step in (("add", "-A", "--", *paths), ("commit", "-m", message, "--", *paths)):
        result = git(repo, *step, runner=runner)
        if result.returncode != 0:
            log(f"ERROR: git {step[0]} failed: {result.stderr.strip()}")
            notify(f"수집 데이터 백업 실패(git {step[0]}): {result.stderr.strip()[:200]}",
                   title="portfolio backup", level="error")
            return 1
    pushed = runner([HIH_BIN, "git", "push"], cwd=str(repo), capture_output=True, text=True)
    if pushed.returncode != 0:
        log(f"ERROR: hih git push failed: {pushed.stderr.strip()}")
        notify("수집 데이터 커밋은 됐지만 push 실패: " + pushed.stderr.strip()[:200],
               title="portfolio backup", level="error")
        return 1
    log(f"[backup] committed and pushed: {message}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="commit and push (default: dry run)")
    args = parser.parse_args(argv)
    return run(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
