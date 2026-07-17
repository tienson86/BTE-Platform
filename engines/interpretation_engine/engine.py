"""
BTE Platform
Interpretation Engine

Engine điều phối toàn bộ Interpretation Engine.
"""

from __future__ import annotations

import time

from .config import (
    DEFAULT_CONFIG,
    InterpretationConfig,
)

from .models import (
    InterpretationContext,
    InterpretationResult,
    InterpretationState,
)

from .service import InterpretationService


class InterpretationEngine:
    """
    Engine chính của Interpretation.
    """

    def __init__(
        self,
        config: InterpretationConfig | None = None,
    ) -> None:

        self.config = config or DEFAULT_CONFIG

        self.state = InterpretationState()

        self.service = InterpretationService(
            self.config
        )

        self.initialize()

    # ======================================================
    # Initialize
    # ======================================================

    def initialize(self) -> None:

        self.state.initialized = True

    # ======================================================
    # Execute
    # ======================================================

    def execute(
        self,
        context: InterpretationContext,
    ) -> InterpretationResult:

        start = time.perf_counter()

        result = self.service.interpret(
            context
        )

        self.state.rendered = True

        self.state.elapsed_time = (
            time.perf_counter() - start
        )

        return result

    # ======================================================
    # Reload
    # ======================================================

    def reload(self) -> None:

        self.service.reload()

    # ======================================================
    # Reset
    # ======================================================

    def reset(self) -> None:

        self.state = InterpretationState()

        self.initialize()

    # ======================================================
    # Properties
    # ======================================================

    @property
    def version(self):

        return self.config.engine_version

    @property
    def name(self):

        return self.config.engine_name

    @property
    def cache(self):

        return self.service.cache
