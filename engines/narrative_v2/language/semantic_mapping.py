"""Map sentence assets to source Meaning. No new astrology knowledge."""

from __future__ import annotations

from engines.narrative_v2.language.sentence_asset import SentenceAsset


def source_meaning(asset: SentenceAsset) -> str:
    """Return the recorded source Meaning for an asset."""
    return dict(asset.metadata).get("source_meaning", "")
