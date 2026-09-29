"""Offline unit tests for scripts/notify.py.

Covers the harness integration contract: notifications shell out to `hih
notify` with the expected title/level, secrets come from `hih-secret get`, and
every failure mode degrades to False/None instead of raising.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scripts import notify  # noqa: E402


def fake_run(returncode: int = 0, stdout: str = "", stderr: str = "",
             raises=None, record=None):
    def runner(cmd, **kwargs):
        if record is not None:
            record.append((cmd, kwargs))
        if raises is not None:
            raise raises
        return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)
    return runner


def test_send_invokes_hih_notify_with_title_level_and_text():
    record = []
    ok = notify.send("hello", title="portfolio wanted", level="warn",
                     runner=fake_run(record=record))
    assert ok is True
    cmd, kwargs = record[0]
    assert cmd == [notify.HIH_BIN, "notify", "--title", "portfolio wanted",
                   "--level", "warn", "hello"]
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True


def test_send_defaults_to_portfolio_info():
    record = []
    notify.send("x", runner=fake_run(record=record))
    cmd, _ = record[0]
    assert cmd[2:4] == ["--title", "portfolio"]
    assert cmd[4:6] == ["--level", "info"]


def test_send_disabled_or_skipped_still_counts_as_success():
    assert notify.send("x", runner=fake_run(returncode=0)) is True


def test_send_is_false_on_real_failure():
    assert notify.send("x", runner=fake_run(returncode=2)) is False


def test_send_is_false_when_the_cli_is_missing():
    assert notify.send("x", runner=fake_run(raises=FileNotFoundError())) is False


def test_send_is_false_on_timeout():
    assert notify.send("x", runner=fake_run(raises=subprocess.TimeoutExpired("hih", 1))) is False


def test_secret_reads_the_keychain_value_and_strips_whitespace():
    record = []
    value = notify.secret("TELEGRAM_OPS_BOT_TOKEN",
                          runner=fake_run(stdout="abc123\n", record=record))
    assert value == "abc123"
    assert record[0][0] == [notify.HIH_SECRET_BIN, "get", "TELEGRAM_OPS_BOT_TOKEN"]


def test_secret_returns_none_when_absent():
    assert notify.secret("NOPE", runner=fake_run(returncode=1)) is None


def test_secret_returns_none_on_empty_value():
    assert notify.secret("EMPTY", runner=fake_run(stdout="  \n")) is None


def test_secret_returns_none_when_the_cli_is_missing():
    assert notify.secret("X", runner=fake_run(raises=OSError())) is None


def test_binaries_resolve_to_absolute_paths():
    assert Path(notify.HIH_BIN).name == "hih"
    assert Path(notify.HIH_SECRET_BIN).name == "hih-secret"
    assert notify.HIH_BIN != notify.HIH_SECRET_BIN
