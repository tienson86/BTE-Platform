"""Presentation package."""

from __future__ import annotations

from consulting.marriage.presentation.adapter import SemanticMarriagePresentationAdapter
from consulting.marriage.presentation.contract import MarriagePresentationAdapter
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter

__all__ = [
    "MarriagePresentationAdapter",
    "PlaceholderMarriagePresentationAdapter",
    "SemanticMarriagePresentationAdapter",
]
