"""Policy package."""

from __future__ import annotations

from consulting.marriage.policy.contract import MarriagePolicyDescriptor, MarriagePolicyProvider
from consulting.marriage.policy.placeholder import PlaceholderMarriagePolicyProvider

__all__ = [
    "MarriagePolicyDescriptor",
    "MarriagePolicyProvider",
    "PlaceholderMarriagePolicyProvider",
]
