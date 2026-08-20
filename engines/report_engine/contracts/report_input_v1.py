"""ReportInputV1 — canonical intermediate contract for Simple Report Export V1."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

REPORT_INPUT_VERSION = "1.0"

_MISSING_DATA_MESSAGE = "Chưa đủ dữ liệu để đưa ra kết luận."


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize_value(value: Any) -> Any:
    """Normalize nested values for deterministic JSON serialization."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if hasattr(value, "to_dict") and callable(value.to_dict):
        return _normalize_mapping(value.to_dict())
    if hasattr(value, "__dataclass_fields__"):
        return _normalize_mapping(asdict(value))
    if isinstance(value, Mapping):
        return _normalize_mapping(dict(value))
    if isinstance(value, (list, tuple)):
        return [_normalize_value(item) for item in value]
    return str(value)


def _normalize_mapping(data: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key in sorted(data.keys(), key=str):
        normalized[str(key)] = _normalize_value(data[key])
    return normalized


@dataclass(slots=True)
class ReportMetadataV1:
    """Report-level metadata."""

    report_version: str = REPORT_INPUT_VERSION
    generated_at: str = field(default_factory=_utc_now_iso)
    engine_version: str = ""
    knowledge_version: str = ""
    case_id: str = ""
    locale: str = "vi-VN"
    timezone: str = "Asia/Bangkok"

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportProfileV1:
    """Subject profile (non-technical)."""

    full_name: str = ""
    gender: str = ""
    birth_date: str = ""
    birth_time: str = ""
    birth_place: str = ""
    timezone: str = "Asia/Bangkok"

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportCalendarV1:
    """Calendar slice for report display."""

    solar_date: str = ""
    lunar_date: str = ""
    lunar_year: int | None = None
    lunar_month: int | None = None
    lunar_day: int | None = None
    leap_month: bool = False
    lunar_year_can_chi: str = ""
    solar_term: str = ""
    solar_term_datetime: str = ""
    calendar_mode: str = ""
    timezone: str = ""
    cung_phi: str = ""
    menh_quai: str = ""
    nhom_trach: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportPillarV1:
    """Single pillar representation."""

    stem: str = ""
    branch: str = ""
    hidden_stems: list[str] = field(default_factory=list)
    na_yin: str = ""
    ten_god: str = ""
    truong_sinh: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportPillarsV1:
    """Four pillars."""

    year: ReportPillarV1 = field(default_factory=ReportPillarV1)
    month: ReportPillarV1 = field(default_factory=ReportPillarV1)
    day: ReportPillarV1 = field(default_factory=ReportPillarV1)
    hour: ReportPillarV1 = field(default_factory=ReportPillarV1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "year": self.year.to_dict(),
            "month": self.month.to_dict(),
            "day": self.day.to_dict(),
            "hour": self.hour.to_dict(),
        }


@dataclass(slots=True)
class ReportFiveElementsV1:
    """Five-element distribution."""

    wood: float | None = None
    fire: float | None = None
    earth: float | None = None
    metal: float | None = None
    water: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)
    normalized: dict[str, Any] = field(default_factory=dict)
    percentages: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportStrengthV1:
    """Strength slice."""

    day_master: str = ""
    score: float | None = None
    level: str = ""
    classification: str = ""
    seasonal_support: float | None = None
    root_support: float | None = None
    supporting_factors: list[str] = field(default_factory=list)
    weakening_factors: list[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportTenGodsV1:
    """Ten-god distribution."""

    visible: list[str] = field(default_factory=list)
    hidden: list[str] = field(default_factory=list)
    summary: str = ""
    visible_entries: list[dict[str, Any]] = field(default_factory=list)
    hidden_entries: list[dict[str, Any]] = field(default_factory=list)
    visible_summary: str = ""
    hidden_summary: str = ""
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Keep the public JSON keys stable for ReportInputV1 snapshots."""
        return _normalize_mapping(
            {
                "visible": self.visible,
                "hidden": self.hidden,
                "summary": self.summary,
            }
        )


@dataclass(slots=True)
class ReportPatternV1:
    """Pattern / cach cuc slice."""

    primary_pattern: str = ""
    secondary_patterns: list[str] = field(default_factory=list)
    follow_pattern: str = ""
    status: str = ""
    confidence: float | None = None
    explanation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportUsefulGodV1:
    """Useful / favorable / unfavorable gods."""

    useful_god: str = ""
    favorable_gods: list[str] = field(default_factory=list)
    unfavorable_gods: list[str] = field(default_factory=list)
    neutral_gods: list[str] = field(default_factory=list)
    temperature_adjustment: str = ""
    balancing_need: str = ""
    climate_evidence: str = ""
    reasoning: str = ""
    useful_ten_god: str = ""
    useful_stem: str = ""
    useful_element: str = ""
    useful_display: str = ""
    favorable_roles: list[dict[str, str]] = field(default_factory=list)
    unfavorable_roles: list[dict[str, str]] = field(default_factory=list)
    favorable_display: str = ""
    unfavorable_display: str = ""
    winning_rule_id: str = ""
    winning_rule_group: str = ""
    overall_incomplete: bool = False
    climate_preference_label: str = ""
    climate_candidate: str = ""
    climate_display: str = ""
    climate_rule_id: str = ""
    climate_rule_group: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Keep legacy keys; G1-06 adds rich Ten God / stem / element."""
        return _normalize_mapping(
            {
                "useful_god": self.useful_god,
                "useful_ten_god": self.useful_ten_god,
                "useful_stem": self.useful_stem,
                "useful_element": self.useful_element,
                "useful_display": self.useful_display,
                "favorable_gods": self.favorable_gods,
                "unfavorable_gods": self.unfavorable_gods,
                "favorable_roles": self.favorable_roles,
                "unfavorable_roles": self.unfavorable_roles,
                "favorable_display": self.favorable_display,
                "unfavorable_display": self.unfavorable_display,
                "winning_rule_id": self.winning_rule_id,
                "winning_rule_group": self.winning_rule_group,
                "neutral_gods": self.neutral_gods,
                "temperature_adjustment": self.temperature_adjustment,
                "balancing_need": self.balancing_need,
                "climate_evidence": self.climate_evidence,
                "reasoning": self.reasoning,
            }
        )


@dataclass(slots=True)
class ReportShenShaItemV1:
    """Structured shen sha entry copied from canonical engine evidence."""

    id: str = ""
    name: str = ""
    category: str = ""
    present: bool = False
    evidence: str = ""
    interpretation: str = ""
    source_type: str = ""
    source_value: str = ""
    target_type: str = ""
    target_value: str = ""
    pillar: str = ""
    location: str = ""
    presence_label: str = ""
    aliases: list[str] = field(default_factory=list)
    rule_source: str = ""
    occurrences: list[dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportLuckCycleV1:
    """Single luck cycle entry."""

    index: int = 0
    start_year: int | None = None
    end_year: int | None = None
    stem: str = ""
    branch: str = ""
    age_start: int | None = None
    age_end: int | None = None
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportLuckCyclesV1:
    """Luck cycle overview."""

    direction: str = ""
    start_age: int | None = None
    start_date: str = ""
    cycles: list[ReportLuckCycleV1] = field(default_factory=list)
    evidence: str = ""
    method_note: str = ""
    precision: str = ""
    current_gan_zhi: str = ""
    current_year_start: int | None = None
    current_year_end: int | None = None
    current_age_start: int | None = None
    current_age_end: int | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "direction": self.direction,
            "start_age": self.start_age,
            "start_date": self.start_date,
            "cycles": [item.to_dict() for item in self.cycles],
            "evidence": self.evidence,
            "method_note": self.method_note,
            "precision": self.precision,
        }
        if self.current_gan_zhi:
            payload["current_gan_zhi"] = self.current_gan_zhi
        if self.current_year_start is not None:
            payload["current_year_start"] = self.current_year_start
        if self.current_year_end is not None:
            payload["current_year_end"] = self.current_year_end
        if self.current_age_start is not None:
            payload["current_age_start"] = self.current_age_start
        if self.current_age_end is not None:
            payload["current_age_end"] = self.current_age_end
        return payload


@dataclass(slots=True)
class ReportInterpretationSectionV1:
    """Normalized interpretation section."""

    id: str = ""
    title: str = ""
    content: str = ""
    priority: int = 0
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportInterpretationV1:
    """Normalized interpretation block."""

    executive_summary: str = ""
    sections: list[ReportInterpretationSectionV1] = field(default_factory=list)
    conclusion: str = ""
    recommendations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "executive_summary": self.executive_summary,
            "sections": [section.to_dict() for section in self.sections],
            "conclusion": self.conclusion,
            "recommendations": list(self.recommendations),
            "warnings": list(self.warnings),
            "confidence": self.confidence,
        }


@dataclass(slots=True)
class ReportDiagnosticsV1:
    """Adapter diagnostics (not shown to end users by default)."""

    missing_fields: list[str] = field(default_factory=list)
    fallbacks_used: list[str] = field(default_factory=list)
    source_contracts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _normalize_mapping(asdict(self))


@dataclass(slots=True)
class ReportInputV1:
    """Canonical Report V1 input contract."""

    metadata: ReportMetadataV1 = field(default_factory=ReportMetadataV1)
    profile: ReportProfileV1 = field(default_factory=ReportProfileV1)
    calendar: ReportCalendarV1 = field(default_factory=ReportCalendarV1)
    pillars: ReportPillarsV1 = field(default_factory=ReportPillarsV1)
    five_elements: ReportFiveElementsV1 = field(default_factory=ReportFiveElementsV1)
    strength: ReportStrengthV1 = field(default_factory=ReportStrengthV1)
    ten_gods: ReportTenGodsV1 = field(default_factory=ReportTenGodsV1)
    pattern: ReportPatternV1 = field(default_factory=ReportPatternV1)
    useful_god: ReportUsefulGodV1 = field(default_factory=ReportUsefulGodV1)
    shensha: list[ReportShenShaItemV1] = field(default_factory=list)
    luck_cycles: ReportLuckCyclesV1 = field(default_factory=ReportLuckCyclesV1)
    interpretation: ReportInterpretationV1 = field(default_factory=ReportInterpretationV1)
    diagnostics: ReportDiagnosticsV1 = field(default_factory=ReportDiagnosticsV1)

    def to_dict(self) -> dict[str, Any]:
        """Deterministic JSON-serializable mapping."""
        return _normalize_mapping(
            {
                "metadata": self.metadata.to_dict(),
                "profile": self.profile.to_dict(),
                "calendar": self.calendar.to_dict(),
                "pillars": self.pillars.to_dict(),
                "five_elements": self.five_elements.to_dict(),
                "strength": self.strength.to_dict(),
                "ten_gods": self.ten_gods.to_dict(),
                "pattern": self.pattern.to_dict(),
                "useful_god": self.useful_god.to_dict(),
                "shensha": [item.to_dict() for item in self.shensha],
                "luck_cycles": self.luck_cycles.to_dict(),
                "interpretation": self.interpretation.to_dict(),
                "diagnostics": self.diagnostics.to_dict(),
            }
        )


def missing_data_message() -> str:
    """Neutral fallback copy for incomplete report sections."""
    return _MISSING_DATA_MESSAGE
