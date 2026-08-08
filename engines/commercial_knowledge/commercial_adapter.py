"""Commercial Knowledge Adapter — Retrieval Contract entrypoint."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .bundle_builder import BundleBuilder
from .models import (
    WAVE_1_1_ALLOW_LIST,
    CommercialKnowledgeBundle,
    NarrativeKnowledgePayload,
    RetrievalRequest,
)
from .retrieval_service import RetrievalService


class CommercialKnowledgeAdapter:
    """
    Adapt Analysis + scenario into CommercialKnowledgeBundle.

    Consumes allow-listed Knowledge Units only (Wave 1.1).
    Narrative must consume the Bundle / payload — never raw KU rows.
    """

    def __init__(
        self,
        *,
        retrieval: RetrievalService | None = None,
        builder: BundleBuilder | None = None,
        csv_path: Path | None = None,
    ) -> None:
        """Inject retrieval/builder for tests."""
        self._retrieval = retrieval or RetrievalService(csv_path=csv_path)
        self._builder = builder or BundleBuilder()

    def adapt(
        self,
        *,
        analysis: dict[str, Any] | None,
        scenario_id: str = "default",
        run_id: str = "",
        interpretation: dict[str, Any] | None = None,
    ) -> tuple[CommercialKnowledgeBundle, NarrativeKnowledgePayload]:
        """
        Run retrieval + bundle build for Wave 1.1.

        ``interpretation`` is accepted for contract completeness (hints only);
        Interpretation Engine logic is not invoked or modified.
        """
        _ = interpretation  # read-only reserved; Wave 1.1 uses Analysis signals
        request = RetrievalRequest(
            analysis_signals={},
            scenario_id=scenario_id or "default",
            allow_list_ids=WAVE_1_1_ALLOW_LIST,
            run_id=run_id,
        )
        selected, dropped, signals = self._retrieval.retrieve(
            analysis=analysis,
            scenario_id=request.scenario_id,
            allow_list_ids=request.allow_list_ids,
            target_components=request.target_components,
        )
        return self._builder.build(
            selected_rows=selected,
            dropped=dropped,
            scenario_id=request.scenario_id,
            run_id=run_id,
            signals=signals,
        )
