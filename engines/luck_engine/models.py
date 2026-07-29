"""
Immutable Luck runtime models (Sprint 4.1).

Data containers only — no favorable/unfavorable evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


def _freeze_mapping(data: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Return a read-only mapping view."""
    if data is None:
        return MappingProxyType({})
    if isinstance(data, MappingProxyType):
        return data
    return MappingProxyType(dict(data))


def _freeze_tuple(values: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    """Normalize sequence fields to an immutable tuple."""
    if not values:
        return ()
    return tuple(values)


@dataclass(frozen=True, slots=True)
class DayunPeriod:
    """One Đại vận decade pillar (runtime data)."""

    index: int
    start_age: int
    end_age: int
    start_year: int
    end_year: int
    heavenly_stem: str
    earthly_branch: str
    element: str
    yin_yang: str
    ten_god: str
    hidden_stems: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "hidden_stems", _freeze_tuple(self.hidden_stems))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    @property
    def ganzhi(self) -> str:
        """Can Chi label."""
        return f"{self.heavenly_stem} {self.earthly_branch}"

    def to_dict(self) -> dict[str, Any]:
        """Serialize for pipeline payload."""
        return {
            "index": self.index,
            "start_age": self.start_age,
            "end_age": self.end_age,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "ganzhi": self.ganzhi,
            "element": self.element,
            "yin_yang": self.yin_yang,
            "ten_god": self.ten_god,
            "hidden_stems": list(self.hidden_stems),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LiunianPeriod:
    """One Lưu niên annual pillar (runtime data)."""

    year: int
    ganzhi: str
    heavenly_stem: str
    earthly_branch: str
    element: str
    yin_yang: str
    ten_god: str
    hidden_stems: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "hidden_stems", _freeze_tuple(self.hidden_stems))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for pipeline payload."""
        return {
            "year": self.year,
            "ganzhi": self.ganzhi,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "element": self.element,
            "yin_yang": self.yin_yang,
            "ten_god": self.ten_god,
            "hidden_stems": list(self.hidden_stems),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LiuyuePeriod:
    """One Lưu nguyệt monthly pillar (runtime data)."""

    year: int
    month: int
    month_index: int
    ganzhi: str
    heavenly_stem: str
    earthly_branch: str
    solar_term: str
    element: str
    yin_yang: str
    ten_god: str
    hidden_stems: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "hidden_stems", _freeze_tuple(self.hidden_stems))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for pipeline payload."""
        return {
            "year": self.year,
            "month": self.month,
            "month_index": self.month_index,
            "ganzhi": self.ganzhi,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "solar_term": self.solar_term,
            "element": self.element,
            "yin_yang": self.yin_yang,
            "ten_god": self.ten_god,
            "hidden_stems": list(self.hidden_stems),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LiuriPeriod:
    """One Lưu nhật daily pillar (runtime data — calendar conversion only)."""

    year: int
    month: int
    day: int
    ganzhi: str
    heavenly_stem: str
    earthly_branch: str
    element: str
    yin_yang: str
    ten_god: str
    hidden_stems: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "hidden_stems", _freeze_tuple(self.hidden_stems))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for pipeline payload."""
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "ganzhi": self.ganzhi,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "element": self.element,
            "yin_yang": self.yin_yang,
            "ten_god": self.ten_god,
            "hidden_stems": list(self.hidden_stems),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True, slots=True)
class LiushiPeriod:
    """One Lưu thì hourly pillar (runtime data — calendar conversion only)."""

    year: int
    month: int
    day: int
    hour: int
    minute: int
    ganzhi: str
    heavenly_stem: str
    earthly_branch: str
    element: str
    yin_yang: str
    ten_god: str
    hidden_stems: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested collections."""
        object.__setattr__(self, "hidden_stems", _freeze_tuple(self.hidden_stems))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Serialize for pipeline payload."""
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "ganzhi": self.ganzhi,
            "heavenly_stem": self.heavenly_stem,
            "earthly_branch": self.earthly_branch,
            "element": self.element,
            "yin_yang": self.yin_yang,
            "ten_god": self.ten_god,
            "hidden_stems": list(self.hidden_stems),
            "metadata": dict(self.metadata),
        }
