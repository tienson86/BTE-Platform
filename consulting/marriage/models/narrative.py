"""Narrative result models. Communication only. No new findings or actions."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import MarriageDomain


@dataclass(slots=True)
class MarriageNarrativeHighlight:
    """One highlight bound to source findings. Not a new finding."""

    highlight_id: str
    kind: str
    catalog_key: str
    text: str
    source_finding_ids: list[str] = field(default_factory=list)
    source_recommendation_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MarriageNarrativeBlock:
    """One communication block. Meaning is keyed by catalog, not invented."""

    block_id: str
    stage: str
    catalog_key: str
    text: str
    domain: MarriageDomain | None = None
    source_finding_ids: list[str] = field(default_factory=list)
    source_recommendation_ids: list[str] = field(default_factory=list)
    visibility: str = "customer"
    priority: str | None = None
    confidence: float | None = None


@dataclass(slots=True)
class MarriageNarrativeSection:
    """One narrative section assembled from catalog entries."""

    section_id: str
    title_key: str
    blocks: list[MarriageNarrativeBlock] = field(default_factory=list)
    domain: MarriageDomain | None = None


@dataclass(slots=True)
class MarriageNarrativeResult:
    """Structured narrative output. Downstream of Decision and Recommendation."""

    consultation_id: str
    language: str
    audience: str
    version: str
    catalog_version: str
    composer_version: str
    sections: list[MarriageNarrativeSection] = field(default_factory=list)
    highlights: list[MarriageNarrativeHighlight] = field(default_factory=list)
