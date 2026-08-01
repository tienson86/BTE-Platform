"""Deterministic UTF-8 I/O helpers for registry compiler outputs."""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def sha256_file(path: Path) -> str:
    """Return SHA-256 hex digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    """Return SHA-256 hex digest of UTF-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json_dumps(payload: Any) -> str:
    """Serialize JSON deterministically."""
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    ) + "\n"


def write_json(path: Path, payload: Any) -> str:
    """Write deterministic JSON and return checksum."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json_dumps(payload)
    path.write_text(text, encoding="utf-8", newline="\n")
    logger.debug("Wrote %s", path)
    return sha256_text(text)


def write_text(path: Path, text: str) -> str:
    """Write UTF-8 text with LF endings and return checksum."""
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.replace("\r\n", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")
    return sha256_text(normalized)


def read_json(path: Path) -> Any:
    """Read a UTF-8 JSON file."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def relative_posix(path: Path, root: Path) -> str:
    """Return stable relative POSIX path."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()
