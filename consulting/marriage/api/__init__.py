"""API package."""

from __future__ import annotations

from consulting.marriage.api.contract import MarriageApiContract
from consulting.marriage.api.placeholder import PlaceholderMarriageApi
from consulting.marriage.api.service import MarriageConsultationApi

__all__ = [
    "MarriageApiContract",
    "MarriageConsultationApi",
    "PlaceholderMarriageApi",
]
