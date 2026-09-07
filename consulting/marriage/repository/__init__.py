"""Repository package."""

from __future__ import annotations

from consulting.marriage.repository.contract import MarriageRepository
from consulting.marriage.repository.placeholder import PlaceholderMarriageRepository

__all__ = [
    "MarriageRepository",
    "PlaceholderMarriageRepository",
]
