"""
Engine Pipeline

Điều phối toàn bộ Engine trong BTE Platform.
"""

from __future__ import annotations

from typing import Iterable

from .base_engine import BaseEngine
from .context import EngineContext


class EnginePipeline:
    """
    Pipeline chạy tuần tự các Engine.
    """

    def __init__(self) -> None:

        self._engines: list[BaseEngine] = []

    # =====================================================
    # Register
    # =====================================================

    def add_engine(
        self,
        engine: BaseEngine,
    ) -> None:

        self._engines.append(engine)

    def add_engines(
        self,
        engines: Iterable[BaseEngine],
    ) -> None:

        self._engines.extend(engines)

    # =====================================================
    # Execute
    # =====================================================

    def run(
        self,
        context: EngineContext,
    ) -> EngineContext:

        for engine in self._engines:

            if not engine.is_enabled:
                continue

            if not engine.validate(context):

                context.add_error(
                    engine.name,
                    "Validation failed.",
                )

                break

            result = engine.execute(context)

            context.set_stage(
                engine.name.lower(),
                result.data,
            )

            if result.failed:

                context.add_error(
                    engine.name,
                    "Engine execution failed.",
                )

                break

        return context

    # =====================================================
    # Helper
    # =====================================================

    @property
    def engines(self) -> tuple[BaseEngine, ...]:

        return tuple(self._engines)

    def clear(self) -> None:

        self._engines.clear()

    def __len__(self) -> int:

        return len(self._engines)

    def __iter__(self):

        return iter(self._engines)

    def __repr__(self) -> str:

        return f"EnginePipeline(engines={len(self._engines)})"
