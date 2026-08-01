"""Fuzzy and text-matching utilities (stdlib only)."""

from __future__ import annotations

import difflib
import re


_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)


def normalize(text: str) -> str:
    """Lowercase trim for deterministic matching."""
    return text.strip().lower()


def tokens(text: str) -> list[str]:
    """Extract alphanumeric tokens."""
    return [item.lower() for item in _TOKEN_RE.findall(text)]


def exact_match(query: str, candidate: str) -> bool:
    """Exact normalized equality."""
    return normalize(query) == normalize(candidate)


def prefix_match(query: str, candidate: str) -> bool:
    """Prefix match on normalized strings."""
    q = normalize(query)
    c = normalize(candidate)
    return bool(q) and c.startswith(q)


def contains_match(query: str, candidate: str) -> bool:
    """Substring contains match."""
    q = normalize(query)
    return bool(q) and q in normalize(candidate)


def fuzzy_ratio(query: str, candidate: str) -> float:
    """Deterministic similarity ratio in [0, 1]."""
    return difflib.SequenceMatcher(
        a=normalize(query),
        b=normalize(candidate),
        autojunk=False,
    ).ratio()
