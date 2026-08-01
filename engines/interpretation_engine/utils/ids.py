"""Identifier helpers for Pack 03 architecture."""

from __future__ import annotations

import uuid


def new_id(prefix: str = "interp") -> str:
    """Create a new architecture-scoped identifier."""
    return f"{prefix}_{uuid.uuid4().hex}"
