"""Framework interpreter context wrapper around PackInterpretationContext."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    ValidationError,
)
from engines.interpretation_engine.interpreter_framework.interpreter_metadata import (
    InterpreterMetadata,
)


@dataclass(frozen=True, slots=True)
class FrameworkInterpreterContext:
    """Standard framework input wrapping frozen PackInterpretationContext.

    Does not replace PackInterpretationContext. Provides convenience accessors
    and runtime metadata for BaseInterpreter.
    """

    pack_context: PackInterpretationContext
    runtime_metadata: InterpreterMetadata | None = None
    attributes: Mapping[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        """Context id."""
        return self.pack_context.id

    @property
    def final_result(self) -> FinalResult:
        """Pack 02 FinalResult."""
        return self.pack_context.final_result

    def validate(self) -> bool:
        """Validate wrapped Pack context and optional metadata."""
        if not self.pack_context.validate():
            return False
        if self.runtime_metadata is not None and not self.runtime_metadata.validate():
            return False
        return True

    def require_valid(self) -> None:
        """Raise ValidationError when context is invalid."""
        if not self.validate():
            raise ValidationError("framework interpreter context is invalid")

    @classmethod
    def from_pack_context(
        cls,
        pack_context: PackInterpretationContext,
        *,
        runtime_metadata: InterpreterMetadata | None = None,
        attributes: Mapping[str, Any] | None = None,
    ) -> FrameworkInterpreterContext:
        """Build framework context from frozen PackInterpretationContext."""
        return cls(
            pack_context=pack_context,
            runtime_metadata=runtime_metadata,
            attributes=dict(attributes or {}),
        )
