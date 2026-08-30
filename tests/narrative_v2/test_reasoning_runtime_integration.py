"""Runtime integration for Reasoning Builder (N-IMP-03)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.reasoning import NarrativeReasoningContext
from engines.narrative_v2.runtime import BUILDER_STAGES, SHADOW_MODE, NarrativeRuntime
from engines.narrative_v2.runtime.runtime_pipeline import StageResult

IMPLEMENTED = frozenset(
    {
        "build_evidence",
        "build_reasoning",
        "resolve_knowledge",
        "commercial_rewrite",
        "build_summary",
        "build_interpretation",
    }
)


def test_r14_runtime_build_reasoning_returns_context(
    case_0001_canonical: dict[str, Any],
) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    runtime.pipeline.build_evidence()
    result = runtime.pipeline.build_reasoning()
    assert isinstance(result, StageResult)
    assert result.status == "implemented"
    assert isinstance(result.payload, NarrativeReasoningContext)
    assert runtime.context is not None
    assert runtime.context.reasoning is result.payload


def test_r15_later_stages_remain_not_implemented(
    case_0001_canonical: dict[str, Any],
) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    runtime.pipeline.build_evidence()
    runtime.pipeline.build_reasoning()
    runtime.pipeline.resolve_knowledge()
    runtime.pipeline.commercial_rewrite()
    runtime.pipeline.build_summary()
    runtime.pipeline.build_interpretation()
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
