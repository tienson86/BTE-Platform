"""Canonical adapter package."""

from __future__ import annotations

from consulting.marriage.adapters.contract import CanonicalAnalysis, CanonicalRuntimeAdapter
from consulting.marriage.adapters.placeholder import PlaceholderCanonicalRuntimeAdapter

__all__ = [
    "CanonicalAnalysis",
    "CanonicalRuntimeAdapter",
    "PlaceholderCanonicalRuntimeAdapter",
]
