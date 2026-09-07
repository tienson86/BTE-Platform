"""Deterministic Language Pack variant selection. No random. No LLM."""

from __future__ import annotations

import hashlib

from consulting.language.exceptions import LanguageSelectionError
from consulting.language.models import LanguageEntry, LanguageVariant, SelectedWording


def select_variant(
    entry: LanguageEntry,
    *,
    semantic_signature: str,
    catalog_version: str,
) -> LanguageVariant:
    """Select one variant from deterministic inputs. Empty variants use default."""
    if not entry.language_key:
        raise LanguageSelectionError("language_key_required")
    variants = entry.variants or [
        LanguageVariant(
            id="default",
            headline=entry.headline,
            meaning=entry.meaning,
            status=entry.status,
        )
    ]
    material = "|".join(
        [entry.language_key, semantic_signature, catalog_version, entry.version]
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(variants)
    return variants[index]


def select_wording(
    entry: LanguageEntry,
    *,
    semantic_signature: str,
    catalog_version: str,
) -> SelectedWording:
    """Return the selected wording record for traces and tests."""
    variant = select_variant(
        entry,
        semantic_signature=semantic_signature,
        catalog_version=catalog_version,
    )
    return SelectedWording(
        language_key=entry.language_key,
        variant_id=variant.id,
        headline=variant.headline or entry.headline,
        meaning=variant.meaning or entry.meaning,
        catalog_version=catalog_version,
        entry_version=entry.version,
    )
