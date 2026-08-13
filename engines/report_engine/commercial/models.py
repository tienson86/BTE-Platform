"""Commercial Report V2 models — product features, not engine dumps."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


COMMERCIAL_REPORT_VERSION = "2.0.0"


class ReportAudience(str, Enum):
    """Who receives the PDF."""

    CUSTOMER = "CUSTOMER"
    ADVISOR = "ADVISOR"


class WritingVariant(str, Enum):
    """Theme Library Layer-3 variant."""

    FORMAL = "formal"
    WARM = "warm"
    PREMIUM = "premium"
    SHORT = "short"


@dataclass(slots=True)
class CommercialSection:
    """One customer-facing feature section."""

    section_id: str
    title: str
    paragraphs: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CommercialChapter:
    """One commercial feature chapter."""

    chapter_id: str
    title: str
    sections: list[CommercialSection] = field(default_factory=list)
    available: bool = True


@dataclass(slots=True)
class CommercialCover:
    """Cover — person and consulting class only."""

    heading: str
    client_name: str
    case_id: str = ""
    consulting_class: str = ""
    subtitle: str = ""
    meta_rows: list[tuple[str, str]] = field(default_factory=list)


@dataclass(slots=True)
class ThemeResolution:
    """Runtime Theme Library selection — not a reasoner."""

    operating_theme_id: str = ""
    customer_name: str = ""
    overlays: list[str] = field(default_factory=list)
    variant: WritingVariant = WritingVariant.FORMAL
    block_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize for advisor diagnostics only."""
        return {
            "operating_theme_id": self.operating_theme_id,
            "customer_name": self.customer_name,
            "overlays": list(self.overlays),
            "variant": self.variant.value,
            "block_ids": list(self.block_ids),
        }


@dataclass(slots=True)
class CommercialReport:
    """Customer consulting report composed from canonical narrative + features."""

    cover: CommercialCover
    chapters: list[CommercialChapter]
    audience: ReportAudience = ReportAudience.CUSTOMER
    theme: ThemeResolution = field(default_factory=ThemeResolution)
    appendix: list[CommercialSection] = field(default_factory=list)
    supporting_chapters: list[CommercialChapter] = field(default_factory=list)
    canonical_narrative: dict[str, Any] | None = None
    footer: str = "BTE · Báo cáo tư vấn"
    version: str = COMMERCIAL_REPORT_VERSION
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CommercialFeatureInput:
    """One product feature payload for the commercial builder."""

    feature_id: str
    title: str
    status: str
    sections: list[tuple[str, str, list[str]]] = field(default_factory=list)
    body: str = ""


@dataclass(slots=True)
class CommercialBuildRequest:
    """Inputs for CommercialReportBuilder — features only."""

    client_name: str
    case_id: str = ""
    birth_date: str = ""
    birth_place: str = ""
    gender: str = ""
    identity: CommercialFeatureInput | None = None
    career: CommercialFeatureInput | None = None
    executive: CommercialFeatureInput | None = None
    primary_theme: str = ""
    active_theme_ids: list[str] = field(default_factory=list)
    capacity_level: str = ""
    has_conflicts: bool = False
    parent_context: bool = False
    purchase_package: str = ""
    reader_role: str = ""
    advisor_mode: bool = False
    writing_variant: str = ""
    appendix_rows: list[tuple[str, str]] = field(default_factory=list)
    appendix_paragraphs: list[str] = field(default_factory=list)
    narrative_result: dict[str, Any] | None = None
