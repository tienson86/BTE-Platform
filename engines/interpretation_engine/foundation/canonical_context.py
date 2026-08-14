"""Immutable canonical analysis context — normalized engine truth contract."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class IdentityContext:
    """Birth identity slice."""

    full_name: str
    gender: str
    birth_datetime: str
    timezone: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize identity."""
        return {
            "full_name": self.full_name,
            "gender": self.gender,
            "birth_datetime": self.birth_datetime,
            "timezone": self.timezone,
        }


@dataclass(frozen=True, slots=True)
class CalendarContext:
    """Calendar slice."""

    solar: str
    lunar: str
    timezone: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize calendar."""
        return {
            "solar": self.solar,
            "lunar": self.lunar,
            "timezone": self.timezone,
        }


@dataclass(frozen=True, slots=True)
class BaziContext:
    """BaZi pillar slice."""

    year: str
    month: str
    day: str
    hour: str
    day_master: str
    day_master_element: str
    day_master_yin_yang: str
    shensha_names: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize bazi."""
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "day_master": self.day_master,
            "day_master_element": self.day_master_element,
            "day_master_yin_yang": self.day_master_yin_yang,
            "shensha_names": list(self.shensha_names),
        }


@dataclass(frozen=True, slots=True)
class StrengthContextSlice:
    """Strength analytical truth in canonical context."""

    level: str
    score: float
    label: str
    confidence: float
    evidence: tuple[str, ...]
    rule_ids: tuple[str, ...]
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize strength slice."""
        return {
            "level": self.level,
            "score": self.score,
            "label": self.label,
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "rule_ids": list(self.rule_ids),
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class PatternContextSlice:
    """Pattern analytical truth in canonical context."""

    selected: str
    label: str
    confidence: float
    evidence: tuple[str, ...]
    rule_ids: tuple[str, ...]
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize pattern slice."""
        return {
            "selected": self.selected,
            "label": self.label,
            "confidence": self.confidence,
            "evidence": list(self.evidence),
            "rule_ids": list(self.rule_ids),
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class UsefulGodContextSlice:
    """Useful God analytical truth in canonical context."""

    selected: str
    favorable_gods: tuple[str, ...]
    unfavorable_gods: tuple[str, ...]
    reason: str
    confidence: float
    rule_ids: tuple[str, ...]
    candidate_count: int
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize useful-god slice."""
        return {
            "selected": self.selected,
            "favorable_gods": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "reason": self.reason,
            "confidence": self.confidence,
            "rule_ids": list(self.rule_ids),
            "candidate_count": self.candidate_count,
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class FiveElementsContextSlice:
    """Five Elements analytical counts."""

    wood: int | None
    fire: int | None
    earth: int | None
    metal: int | None
    water: int | None
    dominant: str | None
    missing: tuple[str, ...]
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize five-elements slice."""
        return {
            "wood": self.wood,
            "fire": self.fire,
            "earth": self.earth,
            "metal": self.metal,
            "water": self.water,
            "dominant": self.dominant,
            "missing": list(self.missing),
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class TemperatureContextSlice:
    """Temperature analytical truth — not pattern.dieu_hau."""

    level: str
    score: float
    label: str
    recommendations: tuple[str, ...]
    rule_ids: tuple[str, ...]
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize temperature slice."""
        return {
            "level": self.level,
            "score": self.score,
            "label": self.label,
            "recommendations": list(self.recommendations),
            "rule_ids": list(self.rule_ids),
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class TenGodsContextSlice:
    """Ten Gods summary in canonical context."""

    visible_labels: tuple[str, ...]
    position_count: int
    hidden_count: int
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize ten-gods slice."""
        return {
            "visible_labels": list(self.visible_labels),
            "position_count": self.position_count,
            "hidden_count": self.hidden_count,
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class LuckContextSlice:
    """Luck / Da Yun summary."""

    available: bool
    direction: str
    start_age: int | None
    cycle_count: int
    current_gan_zhi: str
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize luck slice."""
        return {
            "available": self.available,
            "direction": self.direction,
            "start_age": self.start_age,
            "cycle_count": self.cycle_count,
            "current_gan_zhi": self.current_gan_zhi,
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class FengShuiContextSlice:
    """Feng Shui summary."""

    menh: str
    cung: str
    huong: str
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize feng shui slice."""
        return {
            "menh": self.menh,
            "cung": self.cung,
            "huong": self.huong,
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class ScoreContextSlice:
    """Score aggregate — not analytical truth substitute."""

    total_score: float
    grade: str
    owner: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize score slice."""
        return {
            "total_score": self.total_score,
            "grade": self.grade,
            "owner": self.owner,
        }


@dataclass(frozen=True, slots=True)
class CanonicalAnalysisContext:
    """Single immutable/read-only canonical context for interpretation."""

    identity: IdentityContext
    calendar: CalendarContext
    bazi: BaziContext
    strength: StrengthContextSlice
    pattern: PatternContextSlice
    useful_god: UsefulGodContextSlice
    five_elements: FiveElementsContextSlice
    temperature: TemperatureContextSlice
    ten_gods: TenGodsContextSlice
    shensha_count: int
    luck: LuckContextSlice
    feng_shui: FengShuiContextSlice
    score: ScoreContextSlice
    diagnostics: tuple[str, ...] = field(default_factory=tuple)
    contract_version: str = "sprint_a.v1"

    def to_dict(self) -> dict[str, Any]:
        """Serialize canonical context."""
        return {
            "contract_version": self.contract_version,
            "identity": self.identity.to_dict(),
            "calendar": self.calendar.to_dict(),
            "bazi": self.bazi.to_dict(),
            "strength": self.strength.to_dict(),
            "pattern": self.pattern.to_dict(),
            "useful_god": self.useful_god.to_dict(),
            "five_elements": self.five_elements.to_dict(),
            "temperature": self.temperature.to_dict(),
            "ten_gods": self.ten_gods.to_dict(),
            "shensha_count": self.shensha_count,
            "luck": self.luck.to_dict(),
            "feng_shui": self.feng_shui.to_dict(),
            "score": self.score.to_dict(),
            "diagnostics": list(self.diagnostics),
        }
