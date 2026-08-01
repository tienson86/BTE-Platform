"""Interpreter factory — create interpreters by id via registry (no switch/case)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Mapping

from engines.interpretation_engine.interpreter_framework.base_interpreter import (
    BaseInterpreter,
)
from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    ConfigurationError,
)

InterpreterConstructor = Callable[..., BaseInterpreter]


class InterpreterFactory:
    """Create BaseInterpreter instances by interpreter_id using a registry.

    No hardcoded switch/case. Lookup is registry-driven.
    """

    def __init__(
        self,
        *,
        registry: Mapping[str, InterpreterConstructor] | None = None,
    ) -> None:
        """Initialize with optional constructor registry."""
        self._registry: dict[str, InterpreterConstructor] = dict(registry or {})

    def register(
        self,
        interpreter_id: str,
        constructor: InterpreterConstructor,
    ) -> None:
        """Register a constructor for an interpreter id."""
        if not interpreter_id:
            raise ConfigurationError("interpreter_id is required for registration")
        if constructor is None:
            raise ConfigurationError("constructor is required for registration")
        self._registry[interpreter_id] = constructor

    def unregister(self, interpreter_id: str) -> None:
        """Remove a constructor registration."""
        self._registry.pop(interpreter_id, None)

    def registered_ids(self) -> tuple[str, ...]:
        """Return registered interpreter ids."""
        return tuple(sorted(self._registry.keys()))

    def has(self, interpreter_id: str) -> bool:
        """True when interpreter_id is registered."""
        return interpreter_id in self._registry

    def create(self, interpreter_id: str, **kwargs: Any) -> BaseInterpreter:
        """Create an interpreter instance by id."""
        constructor = self._registry.get(interpreter_id)
        if constructor is None:
            raise ConfigurationError(
                f"interpreter not registered: {interpreter_id!r}"
            )
        instance = constructor(**kwargs)
        if not isinstance(instance, BaseInterpreter):
            raise ConfigurationError(
                f"constructor for {interpreter_id!r} did not return BaseInterpreter"
            )
        if instance.interpreter_id != interpreter_id:
            # Allow class default id to match registration key.
            if not instance.interpreter_id:
                raise ConfigurationError(
                    f"created interpreter missing interpreter_id for {interpreter_id!r}"
                )
        return instance

    def create_all(self, **kwargs: Any) -> tuple[BaseInterpreter, ...]:
        """Create one instance for every registered id."""
        return tuple(self.create(interpreter_id, **kwargs) for interpreter_id in self.registered_ids())
