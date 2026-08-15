"""Text helpers for composition — normalize and fingerprint, never invent."""

from __future__ import annotations

import re

_WHITESPACE = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    """Collapse whitespace so copied statements compare stably."""
    return _WHITESPACE.sub(" ", str(value or "").strip())


def fingerprint(value: str) -> str:
    """Identity of an idea for deduplication. Not a new claim."""
    return normalize_text(value).casefold()
