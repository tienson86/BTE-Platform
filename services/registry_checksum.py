"""Checksum utilities for Registry catalogs and records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json_bytes(payload: Any) -> bytes:
    """Serialize payload to canonical UTF-8 JSON bytes."""
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def checksum_bytes(data: bytes, algorithm: str = "sha256") -> str:
    """Return hex digest for raw bytes."""
    hasher = hashlib.new(algorithm)
    hasher.update(data)
    return hasher.hexdigest()


def checksum_payload(payload: Any, algorithm: str = "sha256") -> str:
    """Return hex digest for a JSON-serializable payload."""
    return checksum_bytes(canonical_json_bytes(payload), algorithm=algorithm)


def checksum_file(path: Path, algorithm: str = "sha256") -> str:
    """Return hex digest for a file's raw bytes."""
    data = path.read_bytes()
    return checksum_bytes(data, algorithm=algorithm)


def checksum_record(record: dict[str, Any], algorithm: str = "sha256") -> str:
    """Return hex digest for a registry record dict."""
    return checksum_payload(record, algorithm=algorithm)


def verify_checksum(
    expected: str,
    payload: Any | None = None,
    *,
    path: Path | None = None,
    algorithm: str = "sha256",
) -> bool:
    """Verify an expected checksum against a payload or file path."""
    if not expected:
        return False
    if path is not None:
        actual = checksum_file(path, algorithm=algorithm)
    elif payload is not None:
        actual = checksum_payload(payload, algorithm=algorithm)
    else:
        raise ValueError("Either payload or path must be provided")
    return actual == expected
