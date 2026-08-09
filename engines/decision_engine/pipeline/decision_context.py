"""Append-only execution context for the Decision Pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.decision_engine.exceptions import DuplicatePublicationError
from engines.decision_engine.pipeline.diagnostics import DecisionDiagnostic


@dataclass(slots=True)
class DecisionExecutionContext:
    """Shared decision context. Stages append results and never overwrite."""

    snapshot: Mapping[str, Any]
    diagnostics: list[DecisionDiagnostic] = field(default_factory=list)
    _results: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)
    _fields: dict[str, str] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "snapshot", dict(self.snapshot))

    def add_diagnostic(self, diagnostic: DecisionDiagnostic) -> None:
        """Append a structured diagnostic entry."""
        self.diagnostics.append(diagnostic)

    def publish(
        self,
        stage_id: str,
        payload: Mapping[str, Any],
        *,
        declared_outputs: tuple[str, ...] = (),
    ) -> None:
        """Publish a stage result. Duplicate stage or field publication is rejected."""
        if stage_id in self._results:
            raise DuplicatePublicationError(f"duplicate_execution:{stage_id}")
        for name in declared_outputs:
            if name in self._fields:
                raise DuplicatePublicationError(
                    f"duplicate_output:{name}:{self._fields[name]}:{stage_id}"
                )
            self._fields[name] = stage_id
        self._results[stage_id] = dict(payload)

    def get_result(self, stage_id: str) -> dict[str, Any] | None:
        """Return a published stage result, if present."""
        payload = self._results.get(stage_id)
        return None if payload is None else dict(payload)

    def has_result(self, stage_id: str) -> bool:
        """Return True when the stage has already published."""
        return stage_id in self._results

    def published_stage_ids(self) -> tuple[str, ...]:
        """Return published stage identifiers in insertion order."""
        return tuple(self._results)

    @property
    def foundation_result(self) -> dict[str, Any] | None:
        """Foundation stage output."""
        return self.get_result("useful_god_foundation")

    @property
    def priority_result(self) -> dict[str, Any] | None:
        """Priority stage output."""
        return self.get_result("useful_god_priority")

    @property
    def override_result(self) -> dict[str, Any] | None:
        """Override stage output."""
        return self.get_result("useful_god_override")
