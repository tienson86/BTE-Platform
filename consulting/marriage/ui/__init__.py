"""UI package."""

from __future__ import annotations

from consulting.marriage.ui.contract import (
    MarriageUILayoutProfile,
    MarriageUILayoutProfileDescriptor,
)
from consulting.marriage.ui.layout import MarriageCustomerLayoutProfile
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile

__all__ = [
    "MarriageCustomerLayoutProfile",
    "MarriageUILayoutProfile",
    "MarriageUILayoutProfileDescriptor",
    "PlaceholderMarriageUILayoutProfile",
]
