"""Canonical snapshot models. Selection and binding only. No interpretation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from consulting.marriage.models.enums import FiveElement, TenGodVisibility, YinYang
from consulting.marriage.models.person import MarriagePersonReference


@dataclass(slots=True)
class EvidenceReference:
    """Reference from a snapshot field back to Canonical evidence."""

    path: str
    value: Any = None


@dataclass(slots=True)
class PillarValue:
    """One pillar value copied from Canonical Truth."""

    stem: str
    branch: str
    can_chi: str
    hidden_stems: list[str] | None = None
    ten_god: str | None = None
    growth_stage: str | None = None
    na_yin: str | None = None


@dataclass(slots=True)
class PillarSnapshot:
    """Four-pillar snapshot. Hour may be absent."""

    year: PillarValue
    month: PillarValue
    day: PillarValue
    hour: PillarValue | None = None


@dataclass(slots=True)
class DayMasterSnapshot:
    """Day master snapshot."""

    stem: str
    element: FiveElement
    yin_yang: YinYang


@dataclass(slots=True)
class FiveElementSnapshot:
    """Five-element distribution snapshot. No quality judgment."""

    distribution: dict[FiveElement, float]
    normalized: dict[FiveElement, float] | None = None
    dominant: list[FiveElement] | None = None
    weak: list[FiveElement] | None = None
    absent: list[FiveElement] | None = None


@dataclass(slots=True)
class StrengthSnapshot:
    """Strength snapshot copied from Canonical Strength."""

    classification: str
    score: float | None = None
    confidence: float | None = None
    reasons: list[EvidenceReference] | None = None


@dataclass(slots=True)
class PatternSnapshot:
    """Pattern snapshot copied from Canonical Pattern."""

    pattern_id: str | None = None
    pattern_name: str | None = None
    grade: str | None = None
    purity: str | None = None
    status: str | None = None
    confidence: float | None = None


@dataclass(slots=True)
class ElementOrStemReference:
    """Useful / favorable / unfavorable element or stem reference."""

    element: FiveElement | None = None
    stem: str | None = None
    role: str | None = None


@dataclass(slots=True)
class UsefulGodSnapshot:
    """Useful God snapshot. Roles are not collapsed into good/bad lists."""

    useful: list[ElementOrStemReference] | None = None
    favorable: list[ElementOrStemReference] | None = None
    unfavorable: list[ElementOrStemReference] | None = None
    temperature_need: str | None = None
    confidence: float | None = None


@dataclass(slots=True)
class TenGodItem:
    """One ten-god item from Canonical Ten Gods."""

    name: str
    source_pillar: str | None = None
    source_stem: str | None = None
    visibility: TenGodVisibility | None = None
    strength: float | None = None


@dataclass(slots=True)
class TenGodSnapshot:
    """Ten Gods snapshot."""

    visible: list[TenGodItem] | None = None
    hidden: list[TenGodItem] | None = None
    dominant_roles: list[str] | None = None
    deficient_roles: list[str] | None = None
    structural_findings: list[EvidenceReference] | None = None


@dataclass(slots=True)
class LuckCycleSnapshot:
    """One luck cycle copied from Canonical Luck. Not recalculated."""

    index: int
    start_year: int
    end_year: int
    can_chi: str
    stem: str
    branch: str
    interpretation_tags: list[str] | None = None


@dataclass(slots=True)
class LuckSnapshot:
    """Luck snapshot."""

    cycles: list[LuckCycleSnapshot] = field(default_factory=list)
    current_cycle: LuckCycleSnapshot | None = None


@dataclass(slots=True)
class ShenShaItem:
    """One Shen Sha item. Secondary evidence only."""

    name: str
    id: str | None = None
    pillar: str | None = None
    category: str | None = None
    polarity: str | None = None
    confidence: float | None = None


@dataclass(slots=True)
class ShenShaSnapshot:
    """Shen Sha snapshot."""

    items: list[ShenShaItem] = field(default_factory=list)


@dataclass(slots=True)
class FengShuiSnapshot:
    """Feng Shui reference snapshot. Not primary marriage evidence."""

    cung_phi: str | None = None
    element: FiveElement | None = None
    group: str | None = None


@dataclass(slots=True)
class MarriageCanonicalSnapshot:
    """Selected Canonical Truth for one person. No new interpretation."""

    person: MarriagePersonReference
    pillars: PillarSnapshot
    day_master: DayMasterSnapshot
    five_elements: FiveElementSnapshot
    strength: StrengthSnapshot
    pattern: PatternSnapshot
    useful_god: UsefulGodSnapshot
    ten_gods: TenGodSnapshot
    source_analysis_id: str
    luck: LuckSnapshot | None = None
    shen_sha: ShenShaSnapshot | None = None
    feng_shui: FengShuiSnapshot | None = None
