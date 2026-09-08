"""Lossless reconstruction of the Wanted dedup ledger from local evidence.

Use ``--hydrate-zero-byte`` for a bounded detail-only network read of the
currently empty Wanted JD files; normal search and delivery paths are not
invoked by that mode.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

try:  # direct script execution and package imports both work
    from scripts.state_utils import atomic_write_json, atomic_write_text
    from scripts.wanted_collect import JD_SECTIONS, PoliteSession, fetch_detail, render_markdown
except ModuleNotFoundError:  # pragma: no cover - exercised by CLI execution
    from state_utils import atomic_write_json, atomic_write_text
    from wanted_collect import JD_SECTIONS, PoliteSession, fetch_detail, render_markdown


ID_FROM_FILENAME = re.compile(r"^(\d+)-")
DATE_FROM_HEADING = re.compile(r"(\d{4}-\d{2}-\d{2})")
ID_FROM_LINK = re.compile(r"\[#(\d+)\]\(")
LEDGER_FIELDS = ("first_seen", "company", "position")
HYDRATE_DELAY_SECONDS = 1.0


def _parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return raw.strip('"\'')


def read_frontmatter(path: Path) -> dict[str, Any]:
    """Read the JSON-compatible scalar frontmatter used by Wanted files."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return {}
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        values[key.strip()] = _parse_scalar(raw)
    return values


def _posting_id(path: Path, frontmatter: Mapping[str, Any]) -> str | None:
    value = frontmatter.get("wanted_id")
    if value not in (None, ""):
        return str(value)
    match = ID_FROM_FILENAME.match(path.name)
    return match.group(1) if match else None


def _posting_entry(path: Path) -> tuple[str, dict[str, Any]] | None:
    frontmatter = read_frontmatter(path)
    posting_id = _posting_id(path, frontmatter)
    if not posting_id:
        return None
    fallback_company = path.stem.split("-", 1)[1] if "-" in path.stem else ""
    entry = {
        "first_seen": str(frontmatter.get("first_seen") or ""),
        "company": str(frontmatter.get("company") or fallback_company),
        "position": str(frontmatter.get("position") or ""),
    }
    return posting_id, entry


def _digest_entries(path: Path) -> list[tuple[str, dict[str, Any]]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    digest_date = ""
    for line in lines[:8]:
        match = DATE_FROM_HEADING.search(line)
        if match:
            digest_date = match.group(1)
            break
    entries: list[tuple[str, dict[str, Any]]] = []
    for line in lines:
        if not line.startswith("|"):
            continue
        match = ID_FROM_LINK.search(line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        entries.append(
            (
                match.group(1),
                {
                    "first_seen": digest_date,
                    "company": cells[0],
                    "position": cells[1],
                },
            )
        )
    return entries


def _merge_entry(target: dict[str, Any], supplement: Mapping[str, Any]) -> None:
    """Fill only absent values; committed ledger values remain authoritative."""
    for field in LEDGER_FIELDS:
        if target.get(field) in (None, "") and supplement.get(field) not in (None, ""):
            target[field] = supplement[field]


def reconstruct_wanted_state(
    baseline_state: Mapping[str, Any],
    posting_dir: Path,
    digest_dir: Path,
) -> dict[str, Any]:
    """Merge committed entries with every local posting and digest entry.

    The committed ledger is the immutable baseline. Existing files and digests
    can add missing IDs and fill blank metadata, but never overwrite a baseline
    row. No posting file is touched or removed.
    """
    baseline_seen = baseline_state.get("seen") if isinstance(baseline_state, Mapping) else None
    if not isinstance(baseline_seen, Mapping):
        raise ValueError("baseline state must contain a seen mapping")
    repaired = copy.deepcopy(dict(baseline_state))
    repaired["seen"] = {str(key): copy.deepcopy(value) for key, value in baseline_seen.items()}

    for path in sorted(Path(posting_dir).glob("*.md")):
        parsed = _posting_entry(path)
        if parsed is None:
            continue
        posting_id, entry = parsed
        target = repaired["seen"].setdefault(posting_id, {})
        if not isinstance(target, dict):
            target = {}
            repaired["seen"][posting_id] = target
        _merge_entry(target, entry)

    for path in sorted(Path(digest_dir).glob("*.md")):
        for posting_id, entry in _digest_entries(path):
            target = repaired["seen"].setdefault(posting_id, {})
            if not isinstance(target, dict):
                target = {}
                repaired["seen"][posting_id] = target
            _merge_entry(target, entry)

    # A zero-byte or otherwise incomplete local JD can prove only its filename
    # and company slug. Keep the ID losslessly and make the ledger schema
    # explicit without inventing a position or date.
    for target in repaired["seen"].values():
        if isinstance(target, dict):
            for field in LEDGER_FIELDS:
                target.setdefault(field, "")

    return repaired


def _zero_byte_files(posting_dir: Path) -> list[tuple[str, Path]]:
    """Return only numeric-ID JD files that are still exactly zero bytes."""
    targets: list[tuple[str, Path]] = []
    for path in sorted(Path(posting_dir).glob("*.md")):
        try:
            is_zero = path.is_file() and path.stat().st_size == 0
        except OSError:
            continue
        if not is_zero:
            continue
        match = ID_FROM_FILENAME.match(path.name)
        if match:
            targets.append((match.group(1), path))
    return targets


def _has_hydratable_detail(job: Mapping[str, Any]) -> bool:
    detail = job.get("detail")
    if not isinstance(detail, Mapping):
        return False
    return any(detail.get(field) not in (None, "", [], {}) for field, _ in JD_SECTIONS)


def hydrate_zero_byte_files(
    posting_dir: Path,
    state: Mapping[str, Any],
    *,
    delay: float = HYDRATE_DELAY_SECONDS,
    session: Any | None = None,
    detail_fetcher: Callable[[Any, int], Mapping[str, Any] | None] = fetch_detail,
) -> list[dict[str, str]]:
    """Fetch and atomically fill only currently zero-byte Wanted JD files.

    The operation performs one bounded detail lookup per target (plus the
    existing API fallback when needed). It does not search, inspect Telegram,
    publish, or remove a posting. A target that becomes non-zero while the
    network request is in flight is skipped rather than overwritten.
    """
    seen = state.get("seen") if isinstance(state, Mapping) else {}
    if not isinstance(seen, Mapping):
        raise ValueError("state must contain a seen mapping")
    client = session if session is not None else PoliteSession(delay)
    results: list[dict[str, str]] = []

    for posting_id, path in _zero_byte_files(posting_dir):
        entry = seen.get(posting_id) or {}
        if not isinstance(entry, Mapping):
            entry = {}
        try:
            job = detail_fetcher(client, int(posting_id))
        except Exception as exc:  # network/client failures become receipt rows
            results.append({
                "id": posting_id,
                "path": str(path),
                "status": "failed",
                "detail": f"{type(exc).__name__}: {exc}",
            })
            continue
        if not isinstance(job, Mapping):
            results.append({
                "id": posting_id,
                "path": str(path),
                "status": "failed",
                "detail": "detail-unavailable",
            })
            continue
        returned_id = job.get("id")
        if returned_id not in (None, "") and str(returned_id) != posting_id:
            results.append({
                "id": posting_id,
                "path": str(path),
                "status": "failed",
                "detail": f"id-mismatch:{returned_id}",
            })
            continue
        if not str(job.get("position") or entry.get("position") or "").strip():
            results.append({
                "id": posting_id,
                "path": str(path),
                "status": "failed",
                "detail": "position-missing",
            })
            continue
        if not _has_hydratable_detail(job):
            results.append({
                "id": posting_id,
                "path": str(path),
                "status": "failed",
                "detail": "jd-detail-empty",
            })
            continue

        filename_company = path.stem.split("-", 1)[1] if "-" in path.stem else ""
        meta = {
            "id": int(posting_id),
            "company": str(entry.get("company") or filename_company),
            "position": str(entry.get("position") or job.get("position") or ""),
            "location": str(entry.get("location") or ""),
            "first_seen": str(entry.get("first_seen") or ""),
            "matched_keywords": set(),
        }
        try:
            content = render_markdown(dict(job), meta)
            if not content.strip():
                raise ValueError("rendered-content-empty")
            if path.stat().st_size != 0:
                results.append({
                    "id": posting_id,
                    "path": str(path),
                    "status": "skipped",
                    "detail": "target-changed-to-nonzero",
                })
                continue
            atomic_write_text(path, content)
        except (OSError, TypeError, ValueError) as exc:
            results.append({
                "id": posting_id,
                "path": str(path),
                "status": "failed",
                "detail": f"{type(exc).__name__}: {exc}",
            })
            continue
        results.append({
            "id": posting_id,
            "path": str(path),
            "status": "success",
            "detail": "jd-written",
        })
    return results


def _committed_state(repo_root: Path, relative_path: str) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=repo_root,
        text=True,
    )
    state = json.loads(raw)
    if not isinstance(state, dict) or not isinstance(state.get("seen"), dict):
        raise ValueError("committed Wanted state has no seen mapping")
    return state


def _valid_state(path: Path) -> bool:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(value, dict) and isinstance(value.get("seen"), dict)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--force", action="store_true", help="rebuild even when the target is valid")
    parser.add_argument(
        "--hydrate-zero-byte",
        action="store_true",
        help="network-read and fill only currently zero-byte Wanted JD files",
    )
    parser.add_argument(
        "--hydrate-delay",
        type=float,
        default=HYDRATE_DELAY_SECONDS,
        help=f"seconds between hydrate requests (default: {HYDRATE_DELAY_SECONDS})",
    )
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    relative_state = "docs/jd/_inbox/wanted/state.json"
    state_path = repo_root / relative_state
    posting_dir = repo_root / "docs/jd/_inbox/wanted"
    digest_dir = posting_dir / "digest"

    if args.hydrate_zero_byte:
        baseline = _committed_state(repo_root, relative_state)
        if _valid_state(state_path):
            current_state = json.loads(state_path.read_text(encoding="utf-8"))
        else:
            current_state = baseline
        results = hydrate_zero_byte_files(
            posting_dir,
            current_state,
            delay=max(0.0, args.hydrate_delay),
        )
        for result in results:
            print(
                f"[hydrate {result['id']}] {result['status']} "
                f"{result['detail']} — {result['path']}"
            )
        repaired = reconstruct_wanted_state(baseline, posting_dir, digest_dir)
        atomic_write_json(state_path, repaired)
        successes = sum(result["status"] == "success" for result in results)
        failures = sum(result["status"] == "failed" for result in results)
        skipped = sum(result["status"] == "skipped" for result in results)
        print(
            f"hydrate receipt: targets={len(results)} successes={successes} "
            f"failures={failures} skipped={skipped}"
        )
        print(
            f"repaired wanted ledger after hydrate: entries={len(repaired['seen'])} "
            f"baseline={len(baseline['seen'])} "
            f"added_from_local={len(repaired['seen']) - len(baseline['seen'])}"
        )
        return 1 if failures else 0

    if _valid_state(state_path) and not args.force:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        print(f"state already valid; entries={len(state['seen'])}")
        return 0

    baseline = _committed_state(repo_root, relative_state)
    repaired = reconstruct_wanted_state(baseline, posting_dir, digest_dir)
    atomic_write_json(state_path, repaired)
    added = len(repaired["seen"]) - len(baseline["seen"])
    print(
        f"repaired wanted ledger: entries={len(repaired['seen'])} "
        f"baseline={len(baseline['seen'])} added_from_local={added}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
