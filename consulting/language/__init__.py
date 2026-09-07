"""Consulting Language Pack. Wording catalog only. Not live TV-01 Narrative."""

from __future__ import annotations

from consulting.language.catalog import get_entry, load_validated_marriage_catalog
from consulting.language.selector import select_wording
from consulting.language.versions import LANGUAGE_PACK_VERSION

__all__ = [
    "LANGUAGE_PACK_VERSION",
    "get_entry",
    "load_validated_marriage_catalog",
    "select_wording",
]
