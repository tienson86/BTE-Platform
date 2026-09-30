"""Customer-safe evidence matrix for an explainable marriage comparison."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class MarriageMatrixRow:
    """One auditable comparison row without internal evidence identifiers."""

    key: str
    label: str
    value_a: str
    value_b: str
    relationship: str
    status: str
    confidence: float
    basis: str
    score_effect: float | None = None
    available: bool = True


@dataclass(frozen=True, slots=True)
class MarriageMatrixSection:
    """A related group of comparison rows."""

    key: str
    title: str
    description: str
    rows: tuple[MarriageMatrixRow, ...] = ()


@dataclass(slots=True)
class MarriageCompatibilityMatrix:
    """Versioned explanation layer behind the structural score."""

    version: str
    sections: list[MarriageMatrixSection] = field(default_factory=list)
