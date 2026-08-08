"""Public Narrative Runtime facade (Sprint D1)."""

from __future__ import annotations

import logging
from typing import Any

from .composer import NarrativeComposerRuntime
from .input_adapter import build_runtime_input
from .models import NarrativeTree, RuntimeInput

logger = logging.getLogger(__name__)


class NarrativeRuntime:
    """
    Sprint D1 public entry for NarrativeTree composition.

    Does not produce NarrativeResult.
    Does not generate natural language.
    """

    version = "d1.0.0"

    def __init__(self, composer: NarrativeComposerRuntime | None = None) -> None:
        self._composer = composer or NarrativeComposerRuntime()

    def compose_tree(self, runtime_input: RuntimeInput) -> NarrativeTree:
        """Compose NarrativeTree from a prepared RuntimeInput."""
        return self._composer.compose(runtime_input)

    def compose_tree_from_sources(
        self,
        analysis: Any = None,
        interpretation: Any = None,
        *,
        run_id: str = "",
        analysis_valid: bool | None = None,
        interpretation_valid: bool | None = None,
    ) -> NarrativeTree:
        """
        Adapt analysis / interpretation structures into RuntimeInput, then compose.

        Adapter extracts references and evidence kinds only — never prose output.
        """
        runtime_input = build_runtime_input(
            analysis=analysis,
            interpretation=interpretation,
            run_id=run_id,
            analysis_valid=analysis_valid,
            interpretation_valid=interpretation_valid,
        )
        logger.info(
            "narrative_runtime.compose_from_sources evidence=%s interp=%s",
            len(runtime_input.evidence),
            len(runtime_input.interpretation_refs),
        )
        return self.compose_tree(runtime_input)
