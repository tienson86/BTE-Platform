"""Commercial Knowledge Adapter — Retrieval Contract entrypoint."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

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

    Default allow-list is Wave 1.1 (backward compatible).

    Production Result wiring passes ``PRODUCTION_ALLOW_LIST``
    (Wave 1.1 + Career Selection Assessment only — no other Domain 01 caps).
    Narrative must consume the Bundle / payload — never raw KU rows.
    """

    def __init__(
        self,
        *,
        retrieval: RetrievalService | None = None,
        builder: BundleBuilder | None = None,
        csv_path: Path | None = None,
        csv_paths: Sequence[Path] | None = None,
        default_allow_list: frozenset[str] | None = None,
    ) -> None:
        """Inject retrieval/builder for tests."""
        if retrieval is not None:
            self._retrieval = retrieval
        else:
            self._retrieval = RetrievalService(csv_path=csv_path, csv_paths=csv_paths)
        self._builder = builder or BundleBuilder()
        self._default_allow_list = default_allow_list or WAVE_1_1_ALLOW_LIST

    def adapt(
        self,
        *,
        analysis: dict[str, Any] | None,
        scenario_id: str = "default",
        run_id: str = "",
        interpretation: dict[str, Any] | None = None,
        allow_list_ids: frozenset[str] | None = None,
    ) -> tuple[CommercialKnowledgeBundle, NarrativeKnowledgePayload]:
        """
        Run retrieval + bundle build for commercial knowledge.

        ``interpretation`` is accepted for contract completeness (hints only);
        Interpretation Engine logic is not invoked or modified.
        Pass ``allow_list_ids=PRODUCTION_ALLOW_LIST`` for Career Selection V1.
        """
        _ = interpretation  # read-only reserved
        request = RetrievalRequest(
            analysis_signals={},
            scenario_id=scenario_id or "default",
            allow_list_ids=allow_list_ids or self._default_allow_list,
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
