"""Append-only Luck Decision context. Upstream snapshots are immutable copies."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from engines.luck_engine.decision_constants import DIAG_OUT_DUPLICATE
from engines.luck_engine.exceptions import DuplicateDecisionError


@dataclass(frozen=True, slots=True)
class LuckDecisionDiagnostic:
    """Machine-readable diagnostic. No exception payload."""

    code: str
    message: str
    severity: str = "error"
    stage_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the diagnostic."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "stage_id": self.stage_id,
            "details": dict(self.details),
        }


def diagnostic(
    code: str,
    message: str,
    *,
    severity: str = "error",
    stage_id: str | None = None,
    details: Mapping[str, Any] | None = None,
) -> LuckDecisionDiagnostic:
    """Build a structured diagnostic."""
    return LuckDecisionDiagnostic(
        code=code,
        message=message,
        severity=severity,
        stage_id=stage_id,
        details=dict(details or {}),
    )


@dataclass(slots=True)
class LuckDecisionContext:
    """Append-only run context. Never mutates timeline / analysis / decision inputs."""

    timeline_snapshot: Mapping[str, Any]
    luck_analysis_snapshot: Mapping[str, Any]
    analysis_snapshot: Mapping[str, Any]
    decision_snapshot: Mapping[str, Any]
    started_at: str
    _published: dict[str, Any] = field(default_factory=dict, repr=False)
    diagnostics: list[LuckDecisionDiagnostic] = field(default_factory=list)
    executed_stages: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Freeze upstream snapshots after copy-in."""
        self.timeline_snapshot = MappingProxyType(dict(self.timeline_snapshot))
        self.luck_analysis_snapshot = MappingProxyType(dict(self.luck_analysis_snapshot))
        self.analysis_snapshot = MappingProxyType(dict(self.analysis_snapshot))
        self.decision_snapshot = MappingProxyType(dict(self.decision_snapshot))

    def publish(self, name: str, value: Any) -> None:
        """Publish one output. Duplicate names are rejected."""
        if name in self._published:
            raise DuplicateDecisionError(f"duplicate_output:{name}")
        self._published[name] = value

    def has_published(self, name: str) -> bool:
        """Return True when an output name is already published."""
        return name in self._published

    def get_published(self, name: str) -> Any:
        """Return a published value or None."""
        return self._published.get(name)

    def published_names(self) -> tuple[str, ...]:
        """Return published names in insertion order."""
        return tuple(self._published.keys())

    def published_copy(self) -> dict[str, Any]:
        """Return a shallow copy of published outputs."""
        return dict(self._published)

    def add_diagnostic(self, item: LuckDecisionDiagnostic) -> None:
        """Append a diagnostic."""
        self.diagnostics.append(item)

    def record_stage(self, stage_id: str) -> None:
        """Record that a stage executed."""
        self.executed_stages.append(stage_id)

    def emit_duplicate(self, name: str, stage_id: str | None = None) -> None:
        """Record OUT-DUPLICATE without raising to callers."""
        self.add_diagnostic(
            diagnostic(
                DIAG_OUT_DUPLICATE,
                f"Duplicate output publication: {name}",
                stage_id=stage_id,
                details={"name": name},
            )
        )
