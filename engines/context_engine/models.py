"""Unified Analysis Context V2 models."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

SCHEMA_VERSION = "2.0.0"
CONTEXT_CONTRACT = "UnifiedAnalysisContext@2.0"


@dataclass(slots=True)
class CalendarSection:
    """Normalized calendar slice."""

    solar_year: int | None = None
    solar_month: int | None = None
    solar_day: int | None = None
    solar_hour: int | None = None
    solar_minute: int | None = None
    solar_term: str | None = None
    lunar_year: int | None = None
    lunar_month: int | None = None
    lunar_day: int | None = None
    julian_day: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BaziSection:
    """Normalized bazi slice."""

    day_master: str | None = None
    day_master_element: str | None = None
    year_pillar: str | None = None
    month_pillar: str | None = None
    day_pillar: str | None = None
    hour_pillar: str | None = None
    month_branch: str | None = None
    ten_gods: list[str] = field(default_factory=list)
    hidden_stems: list[str] = field(default_factory=list)
    shensha: list[str] = field(default_factory=list)
    gender: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StrengthSection:
    """Normalized strength slice (from Strength Engine V2)."""

    level: str = "balanced"
    score: float = 0.0
    season_score: float = 0.0
    root_score: float = 0.0
    support_score: float = 0.0
    drain_score: float = 0.0
    control_score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    reasoning: str = ""
    success: bool = True


@dataclass(slots=True)
class TemperatureSection:
    """Normalized temperature slice (from Temperature Engine V2)."""

    level: str = "warm"
    type: str = "warm"
    score: float = 0.0
    warm_score: float = 0.0
    cold_score: float = 0.0
    dry_score: float = 0.0
    humid_score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    reasoning: str = ""
    recommendations: list[str] = field(default_factory=list)
    success: bool = True


@dataclass(slots=True)
class PatternSection:
    """Normalized pattern slice (from Pattern Engine)."""

    main: str = ""
    follow: str | None = None
    name: str = ""
    score: float = 0.0
    priority: int = 0
    success: bool = True
    matched_rules: list[str] = field(default_factory=list)
    description: str = ""
    follow_type: str | None = None
    main_pattern: str | None = None


@dataclass(slots=True)
class UsefulGodSection:
    """Normalized useful-god slice (from Useful God Engine V2)."""

    primary: str = ""
    favorable: list[str] = field(default_factory=list)
    unfavorable: list[str] = field(default_factory=list)
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    reasoning: str = ""
    success: bool = True


@dataclass(slots=True)
class ContextTraceEntry:
    """Single engine trace record."""

    engine: str
    input_keys: list[str] = field(default_factory=list)
    output_keys: list[str] = field(default_factory=list)
    duration_ms: float = 0.0
    confidence: float | None = None
    success: bool = True


@dataclass(slots=True)
class ContextMetadata:
    """Unified context metadata and trace."""

    schema_version: str = SCHEMA_VERSION
    contract: str = CONTEXT_CONTRACT
    builder: str = "context_engine.builder_v2"
    trace: list[ContextTraceEntry] = field(default_factory=list)
    validation: dict[str, Any] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class UnifiedAnalysisContext:
    """Single SSOT context for Interpretation, Report, and downstream engines."""

    calendar: CalendarSection = field(default_factory=CalendarSection)
    bazi: BaziSection = field(default_factory=BaziSection)
    strength: StrengthSection = field(default_factory=StrengthSection)
    temperature: TemperatureSection = field(default_factory=TemperatureSection)
    pattern: PatternSection = field(default_factory=PatternSection)
    useful_god: UsefulGodSection = field(default_factory=UsefulGodSection)
    metadata: ContextMetadata = field(default_factory=ContextMetadata)

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return asdict(self)
