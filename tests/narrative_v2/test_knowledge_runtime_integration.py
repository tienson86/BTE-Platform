"""Runtime integration for Knowledge Resolver (N-IMP-04)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.knowledge import NarrativeKnowledgeContext
from engines.narrative_v2.runtime import BUILDER_STAGES, SHADOW_MODE, NarrativeRuntime
from engines.narrative_v2.runtime.runtime_pipeline import StageResult

IMPLEMENTED = frozenset({"build_evidence", "build_reasoning", "resolve_knowledge"})


def test_k15_runtime_resolve_knowledge_returns_context(
    case_0001_canonical: dict[str, Any],
) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    runtime.pipeline.build_evidence()
    runtime.pipeline.build_reasoning()
    result = runtime.pipeline.resolve_knowledge()
    assert isinstance(result, StageResult)
    assert result.status == "implemented"
    assert isinstance(result.payload, NarrativeKnowledgeContext)
    assert runtime.context is not None
    assert runtime.context.knowledge is result.payload


def test_k16_later_stages_remain_not_implemented(
    case_0001_canonical: dict[str, Any],
) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    runtime.pipeline.build_evidence()
    runtime.pipeline.build_reasoning()
    runtime.pipeline.resolve_knowledge()
    later = tuple(stage for stage in BUILDER_STAGES if stage not in IMPLEMENTED)
    for stage in later:
        output = runtime.pipeline.execute_stage(stage)
        assert output.payload is NotImplemented
        assert output.status == "not_implemented"


def test_shadow_mode_unchanged(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert SHADOW_MODE is True
    assert runtime.shadow_mode is True
    assert runtime.replaces_pack05 is False
    assert runtime.portal_connected is False
    assert result.presentation is None
    assert result.runtime_metadata["shadow_mode"] is True
    assert result.runtime_metadata["generates_narrative"] is False
