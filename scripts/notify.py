#!/usr/bin/env python3
"""Harness notification and secret access for the portfolio jobs.

Notifications go through the harness ops bot with `hih notify` — never a
per-project Telegram bot and never a plaintext env file. The harness resolves
the ops bot's token/chat id from the macOS Keychain (via `hih-secret`) and gates
the send on `notify.enabled`; while the ops channel is disabled nothing leaves
the machine and `hih notify` still exits 0, so scheduled runs stay quiet.

`secret()` is the sanctioned Keychain accessor (`hih-secret get NAME`) for any
credential a job needs. Values are returned to the caller only; they are never
written to argv, a log or the repository.

Both helpers swallow their own errors by design: a notification or secret
problem must never fail a collection run that already succeeded.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

def _resolve(binary: str, env_names: tuple[str, ...]) -> str:
    """Resolve a harness CLI to an absolute path.

    Accepts an override that names either the binary itself or the bin
    directory that holds it (the harness exports HIH_BIN as that directory),
    then falls back to PATH and finally to the harness checkout.
    """
    for name in env_names:
        raw = os.environ.get(name)
        if not raw:
            continue
        candidate = Path(raw)
        candidate = candidate / binary if candidate.is_dir() else candidate
        if candidate.is_file():
            return str(candidate)
    found = shutil.which(binary)
    if found:
        return found
    return str(Path.home() / "Workspace" / "harness" / "bin" / binary)


HIH_BIN = _resolve("hih", ("HIH_BIN",))
HIH_SECRET_BIN = _resolve("hih-secret", ("HIH_SECRET_BIN",))


def send(text: str, *, title: str = "portfolio", level: str = "info",
         timeout: int = 60, runner=None) -> bool:
    """Send one message through `hih notify`. Returns True when the harness
    accepted it; `disabled`/`skipped` also count as accepted (the gate worked).
    Returns False only on a real failure or when the harness binary is absent."""
    runner = runner or subprocess.run
    try:
        result = runner(
            [HIH_BIN, "notify", "--title", title, "--level", level, text],
            capture_output=True, text=True, timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def secret(name: str, *, timeout: int = 30, runner=None) -> str | None:
    """Read one secret from the Keychain via `hih-secret get NAME`. Returns the
    value, or None when the secret is absent or the CLI is unavailable."""
    runner = runner or subprocess.run
    try:
        result = runner(
            [HIH_SECRET_BIN, "get", name],
            capture_output=True, text=True, timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None
