"""Reusable validators for the Interpreter Framework."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.interpreter_framework.interpreter_capability import (
    InterpreterCapability,
)
from engines.interpretation_engine.interpreter_framework.interpreter_dependency import (
    DependencyResolver,
    InterpreterDependency,
)
from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    DependencyError,
    ValidationError,
)
from engines.interpretation_engine.interpreter_framework.interpreter_result import (
    FrameworkInterpreterResult,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpretationSection,
)


class InterpreterValidator:
    """Reusable validator for input, contract, dependency, and result checks."""

    def __init__(self, *, dependency_resolver: DependencyResolver | None = None) -> None:
        """Initialize with optional dependency resolver."""
        self.dependency_resolver = dependency_resolver or DependencyResolver()

    def validate_input(self, context: Any) -> bool:
        """Validate PackInterpretationContext input."""
        if not isinstance(context, PackInterpretationContext):
            return False
        return context.validate()

    def require_input(self, context: Any) -> PackInterpretationContext:
        """Validate input or raise ValidationError."""
        if not isinstance(context, PackInterpretationContext):
            raise ValidationError("PackInterpretationContext required")
        if not context.validate():
            raise ValidationError("PackInterpretationContext invalid")
        return context

    def validate_capability(self, capability: InterpreterCapability) -> bool:
        """Validate capability contract."""
        return capability.validate()

    def require_capability(self, capability: InterpreterCapability) -> None:
        """Require valid capability contract."""
        capability.require_valid()

    def validate_section(self, section: InterpretationSection) -> bool:
        """Validate InterpretationSection shell."""
        return section.validate()

    def require_section(self, section: InterpretationSection) -> None:
        """Require valid InterpretationSection."""
        if not section.validate():
            raise ValidationError("InterpretationSection invalid")

    def validate_result(self, result: FrameworkInterpreterResult) -> bool:
        """Validate framework interpreter result."""
        return result.validate()

    def require_result(self, result: FrameworkInterpreterResult) -> None:
        """Require valid framework result."""
        if not result.validate():
            raise ValidationError("FrameworkInterpreterResult invalid")

    def validate_dependencies(
        self,
        *,
        interpreter_ids: Sequence[str],
        required: Mapping[str, Sequence[str]],
        optional: Mapping[str, Sequence[str]] | None = None,
    ) -> bool:
        """Validate dependency graph; False when DependencyError would be raised."""
        try:
            resolution = self.dependency_resolver.resolve(
                interpreter_ids=interpreter_ids,
                required=required,
                optional=optional,
            )
        except DependencyError:
            return False
        return resolution.validate()

    def require_dependencies(
        self,
        *,
        interpreter_ids: Sequence[str],
        required: Mapping[str, Sequence[str]],
        optional: Mapping[str, Sequence[str]] | None = None,
    ) -> tuple[str, ...]:
        """Resolve dependencies or raise DependencyError."""
        resolution = self.dependency_resolver.resolve(
            interpreter_ids=interpreter_ids,
            required=required,
            optional=optional,
        )
        return resolution.order

    def validate_dependency_edge(self, dependency: InterpreterDependency) -> bool:
        """Validate a single dependency edge."""
        return dependency.validate()
