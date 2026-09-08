"""Durable JSON state persistence for the local job collectors."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def _fsync_directory(directory: Path) -> None:
    """Best-effort directory fsync after a successful replacement.

    The file fsync is the durability gate. Some platforms do not permit
    opening a directory, so a directory fsync failure must not turn an
    already-successful atomic replacement into a reported write failure.
    """
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        directory_fd = os.open(str(directory), flags)
    except OSError:
        return
    try:
        try:
            os.fsync(directory_fd)
        except OSError:
            return
    finally:
        os.close(directory_fd)


def atomic_write_json(path: Path, value: Any, *, indent: int = 2) -> None:
    """Write JSON without exposing a truncated previous file.

    The temporary file is created in the target's directory so ``os.replace``
    is same-filesystem and atomic. All content is flushed and fsynced before
    replacement. Any failure before replacement leaves the previous target
    untouched, and the temporary file is cleaned up on every path.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temporary_path = Path(temporary_name)
    open_fd = fd
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            open_fd = -1
            json.dump(value, stream, ensure_ascii=False, indent=indent)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    except BaseException:
        if open_fd >= 0:
            try:
                os.close(open_fd)
            except OSError:
                pass
        raise
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            # Never mask the original write error with cleanup noise. The
            # target itself is still protected by the atomic replacement.
            pass


def atomic_write_text(path: Path, value: str, *, encoding: str = "utf-8") -> None:
    """Atomically write text while protecting an existing target.

    This is used for bounded JD hydration. It has the same same-directory,
    flush/fsync, replace, and cleanup guarantees as ``atomic_write_json`` but
    does not reinterpret the fetched document as JSON.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temporary_path = Path(temporary_name)
    open_fd = fd
    try:
        with os.fdopen(fd, "w", encoding=encoding) as stream:
            open_fd = -1
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
        _fsync_directory(path.parent)
    except BaseException:
        if open_fd >= 0:
            try:
                os.close(open_fd)
            except OSError:
                pass
        raise
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            # Never mask the original write error with cleanup noise.
            pass
