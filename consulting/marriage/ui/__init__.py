"""UI package."""

from __future__ import annotations

from consulting.marriage.ui.contract import (
    MarriageUILayoutProfile,
    MarriageUILayoutProfileDescriptor,
)
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile

__all__ = [
    "MarriageUILayoutProfile",
    "MarriageUILayoutProfileDescriptor",
    "PlaceholderMarriageUILayoutProfile",
]
