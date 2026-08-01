"""Deterministic I/O helpers for baseline artifacts."""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def sha256_bytes(data: bytes) -> str:
    """Return lowercase hex SHA-256 of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    """Return SHA-256 of UTF-8 text."""
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path) -> str:
    """Return SHA-256 of a file's binary contents."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_dumps(payload: Any) -> str:
    """Serialize payload to deterministic UTF-8 JSON text."""
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    ) + "\n"


def write_json(path: Path, payload: Any) -> str:
    """Write deterministic JSON and return SHA-256 of written text."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json_dumps(payload)
    path.write_text(text, encoding="utf-8", newline="\n")
    logger.debug("Wrote JSON artifact %s", path)
    return sha256_text(text)


def write_text(path: Path, text: str) -> str:
    """Write UTF-8 text with LF newlines and return SHA-256."""
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.replace("\r\n", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")
    logger.debug("Wrote text artifact %s", path)
    return sha256_text(normalized)


def read_json(path: Path) -> Any:
    """Read a UTF-8 JSON file."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def copy_file(src: Path, dest: Path) -> None:
    """Copy a file, creating parent directories as needed."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def relative_posix(path: Path, root: Path) -> str:
    """Return a stable POSIX-style relative path string."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()
