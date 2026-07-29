"""Local machine fingerprint (offline, no DRM)."""

from __future__ import annotations

import hashlib
import platform
import uuid


def get_machine_id() -> str:
    """
    Stable-ish local machine id for offline activation binding.

    Uses hostname + MAC-derived node; not a security DRM mechanism.
    """
    raw = f"{platform.node()}|{uuid.getnode()}|{platform.system()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]
