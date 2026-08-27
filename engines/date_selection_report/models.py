"""Canonical Date Selection report model (PACK 06 P6-01).

Immutable presentation model. No analytical calculation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Metadata:
    """Report identity. Never influences analytical content."""

    report_id: str
    report_schema_version: str
    report_type: str
    generated_at: str
    locale: str
    title: str
    generator: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize metadata."""
        return {
            "report_id": self.report_id,
            "report_schema_version": self.report_schema_version,
            "report_type": self.report_type,
            "generated_at": self.generated_at,
            "locale": self.locale,
            "title": self.title,
            "generator": self.generator,
        }


@dataclass(frozen=True, slots=True)
class Provenance:
    """Traceability. Not shown to the customer."""

    source: str
    search_result_id: str | None
    generated_at: str
    engine_version: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize provenance."""
        return {
            "source": self.source,
            "search_result_id": self.search_result_id,
            "generated_at": self.generated_at,
            "engine_version": self.engine_version,
        }


ProvenanceData = Provenance


@dataclass(frozen=True, slots=True)
class PersonReportData:
    """Customer identity copied from Date Selection SearchResult."""

    full_name: str
    gender: str
    birth_solar: str
    birth_lunar: str
    year_ganzhi: str
    nayin: str
    cung_phi: str
    cung_element: str
    trach_group: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize person block."""
        return {
            "full_name": self.full_name,
            "gender": self.gender,
            "birth_solar": self.birth_solar,
            "birth_lunar": self.birth_lunar,
            "year_ganzhi": self.year_ganzhi,
            "nayin": self.nayin,
            "cung_phi": self.cung_phi,
            "cung_element": self.cung_element,
            "trach_group": self.trach_group,
        }


@dataclass(frozen=True, slots=True)
class SearchPeriodReportData:
    """Target month copied from SearchResult."""

    month: int
    year: int
    display: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize search period."""
        return {"month": self.month, "year": self.year, "display": self.display}


@dataclass(frozen=True, slots=True)
class PositiveKeReportData:
    """One positive khắc copied from Date Selection."""

    index: int
    time_range: str
    result: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize positive khắc."""
        return {
            "index": self.index,
            "time_range": self.time_range,
            "result": self.result,
        }


@dataclass(frozen=True, slots=True)
class CompatibleHourReportData:
    """Same-Trạch hour. Never carries hour_result."""

    branch: str
    time_range: str
    ganzhi: str
    nayin: str
    cung: str
    cung_element: str
    trach_group: str
    positive_ke: tuple[PositiveKeReportData, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize compatible hour."""
        return {
            "branch": self.branch,
            "time_range": self.time_range,
            "ganzhi": self.ganzhi,
            "nayin": self.nayin,
            "cung": self.cung,
            "cung_element": self.cung_element,
            "trach_group": self.trach_group,
            "positive_ke": [item.to_dict() for item in self.positive_ke],
        }


@dataclass(frozen=True, slots=True)
class RecommendedDateReportData:
    """One ranked day copied in canonical SearchResult order."""

    rank: int
    solar_date: str
    lunar_date: str
    year_ganzhi: str
    month_ganzhi: str
    day_ganzhi: str
    day_result: str
    nayin: str
    cung: str
    cung_element: str
    trach_group: str
    compatible_hours: tuple[CompatibleHourReportData, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize recommended day."""
        return {
            "rank": self.rank,
            "solar_date": self.solar_date,
            "lunar_date": self.lunar_date,
            "year_ganzhi": self.year_ganzhi,
            "month_ganzhi": self.month_ganzhi,
            "day_ganzhi": self.day_ganzhi,
            "day_result": self.day_result,
            "nayin": self.nayin,
            "cung": self.cung,
            "cung_element": self.cung_element,
            "trach_group": self.trach_group,
            "compatible_hours": [item.to_dict() for item in self.compatible_hours],
        }


@dataclass(frozen=True, slots=True)
class GuidanceItem:
    """Educational positive-class note. Not a promise."""

    label: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize guidance item."""
        return {"label": self.label, "text": self.text}


@dataclass(frozen=True, slots=True)
class GuidanceReportData:
    """Short educational block for positive classes."""

    title: str
    items: tuple[GuidanceItem, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize guidance."""
        return {
            "title": self.title,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(frozen=True, slots=True)
class DateSelectionReportModel:
    """Single report model shared by future PDF and DOCX renderers."""

    metadata: Metadata
    person: PersonReportData
    search_period: SearchPeriodReportData
    recommendations: tuple[RecommendedDateReportData, ...]
    guidance: GuidanceReportData
    provenance: Provenance

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full report model."""
        return {
            "metadata": self.metadata.to_dict(),
            "person": self.person.to_dict(),
            "search_period": self.search_period.to_dict(),
            "recommendations": [item.to_dict() for item in self.recommendations],
            "guidance": self.guidance.to_dict(),
            "provenance": self.provenance.to_dict(),
        }
