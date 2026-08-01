"""Standard interpreter result model for the framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.interpreter_framework.interpreter_metadata import (
    InterpreterMetadata,
)
from engines.interpretation_engine.interpreter_framework.interpreter_trace import (
    InterpreterTrace,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpretationSection,
)


@dataclass(frozen=True, slots=True)
class ExecutionStatistics:
    """Lightweight execution statistics for one interpreter run."""

    started_at: str = ""
    finished_at: str = ""
    duration_ms: float = 0.0
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate statistics."""
        return self.duration_ms >= 0.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize statistics."""
        return {
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": self.duration_ms,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class FrameworkInterpreterResult:
    """Standard framework output for BaseInterpreter.interpret().

    Wraps frozen InterpretationSection (SectionResult) plus framework fields.
    """

    section: InterpretationSection
    metadata: InterpreterMetadata
    trace: InterpreterTrace = field(default_factory=InterpreterTrace)
    confidence: float = 0.0
    warnings: tuple[str, ...] = ()
    statistics: ExecutionStatistics = field(default_factory=ExecutionStatistics)
    success: bool = True
    messages: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate framework result integrity."""
        if not self.section.validate():
            return False
        if not self.metadata.validate():
            return False
        if not self.trace.validate():
            return False
        if not self.statistics.validate():
            return False
        if self.confidence < 0.0 or self.confidence > 1.0:
            # Allow 0-100 scale as well.
            if not (0.0 <= self.confidence <= 100.0):
                return False
        return self.success is True or self.success is False

    def to_payload(self) -> dict[str, Any]:
        """Flatten into RuntimeExecuteResult payload keys."""
        return {
            "interpreter_id": self.metadata.interpreter_id,
            "version": self.metadata.version,
            "section": self.section,
            "interpretation_section": self.section,
            "framework_result": self,
            "metadata": self.metadata.to_dict(),
            "trace": self.trace.to_dict(),
            "confidence": self.confidence,
            "warnings": list(self.warnings),
            "statistics": self.statistics.to_dict(),
            "attributes": dict(self.attributes),
        }
