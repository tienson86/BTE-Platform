"""Runtime Sentence Library service. Select only. Never generate prose."""

from __future__ import annotations

from engines.narrative_v2.language.language_asset_status import SENTENCE_LIBRARY_VERSION
from engines.narrative_v2.language.sentence_asset import SentenceAsset
from engines.narrative_v2.language.sentence_registry import SentenceRegistry
from engines.narrative_v2.language.sentence_selector import SentenceSelector
from engines.narrative_v2.language.sentence_validator import SentenceAssetValidator


class SentenceLibrary:
    """Approved customer-language assets for Commercial Communication."""

    def __init__(
        self,
        *,
        registry: SentenceRegistry | None = None,
        selector: SentenceSelector | None = None,
        validator: SentenceAssetValidator | None = None,
    ) -> None:
        self._registry = registry or SentenceRegistry()
        self._selector = selector or SentenceSelector(self._registry)
        self._validator = validator or SentenceAssetValidator()

    def version(self) -> str:
        """Return the loaded library version."""
        return self._registry.version() or SENTENCE_LIBRARY_VERSION

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
        """Return one approved asset, or None when unresolved."""
        asset = self._selector.select(
            semantic_key,
            category=category,
            locale=locale,
            audience=audience,
            domain=domain,
            meaning_key=meaning_key,
        )
        if asset is None:
            return None
        outcome = self._validator.validate(asset)
        if not outcome.passed:
            return None
        return asset

    def select_all(
        self,
        semantic_key: str,
        *,
        category: str,
        locale: str = "vi",
        audience: str = "customer",
        domain: str | None = None,
        meaning_key: str | None = None,
    ) -> tuple[SentenceAsset, ...]:
        """Return approved assets for one exact key, or empty when unresolved."""
        selected: list[SentenceAsset] = []
        for asset in self._selector.select_all(
            semantic_key,
            category=category,
            locale=locale,
            audience=audience,
            domain=domain,
            meaning_key=meaning_key,
        ):
            outcome = self._validator.validate(asset)
            if outcome.passed:
                selected.append(asset)
        return tuple(selected)
