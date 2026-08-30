"""Deterministic SentenceAsset selection. No generation. No fuzzy match."""

from __future__ import annotations

from engines.narrative_v2.language.language_asset_status import CUSTOMER_ELIGIBLE
from engines.narrative_v2.language.sentence_asset import SentenceAsset
from engines.narrative_v2.language.sentence_registry import SentenceRegistry


class SentenceSelector:
    """Select one approved asset. Returns None when none matches."""

    def __init__(self, registry: SentenceRegistry | None = None) -> None:
        self._registry = registry or SentenceRegistry()

    def select(
        self,
        semantic_key: str,
        *,
        category: str,
        locale: str = "vi",
        audience: str = "customer",
        domain: str | None = None,
        meaning_key: str | None = None,
    ) -> SentenceAsset | None:
        """Exact-match select. Missing meaning_key does not fuzzy-pick another key."""
        eligible = [
            asset
            for asset in self._registry.assets()
            if asset.status in CUSTOMER_ELIGIBLE
            and asset.semantic_key == semantic_key
            and asset.category == category
            and asset.locale == locale
            and asset.audience == audience
        ]
        if domain is not None:
            eligible = [asset for asset in eligible if asset.domain == domain]
        if meaning_key is not None:
            eligible = [asset for asset in eligible if asset.meaning_key == meaning_key]
        if not eligible:
            return None
        ordered = sorted(eligible, key=lambda asset: (-asset.priority, asset.sentence_id))
        return ordered[0]
