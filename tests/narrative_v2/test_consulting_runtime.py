"""Runtime integration for Consulting Style (N-IMP-07B)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.communication import ConsultingNarrative
from engines.narrative_v2.interpretation import InterpretationNarrative
from engines.narrative_v2.runtime import BUILDER_STAGES, SHADOW_MODE, NarrativeRuntime

IMPLEMENTED = frozenset(
    {
        "build_evidence",
        "build_reasoning",
        "resolve_knowledge",
        "commercial_rewrite",
        "build_summary",
        "build_interpretation",
        "build_action",
    }
)


def test_runtime_stores_internal_consulting(
    case_0001_canonical: dict[str, Any],
) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    runtime.pipeline.build_evidence()
    runtime.pipeline.build_reasoning()
    runtime.pipeline.resolve_knowledge()
    runtime.pipeline.commercial_rewrite()
    runtime.pipeline.build_summary()
    result = runtime.pipeline.build_interpretation()
    assert isinstance(result.payload, InterpretationNarrative)
    assert runtime.context is not None
    assert isinstance(runtime.context.consulting, ConsultingNarrative)
    assert runtime.context.consulting.flow
    assert result.payload is runtime.context.interpretation


def test_cs20_action_remains_not_implemented(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    runtime.pipeline.build_evidence()
    runtime.pipeline.build_reasoning()
    runtime.pipeline.resolve_knowledge()
    runtime.pipeline.commercial_rewrite()
    runtime.pipeline.build_summary()
    runtime.pipeline.build_interpretation()
    runtime.pipeline.build_action()
    later = tuple(stage for stage in BUILDER_STAGES if stage not in IMPLEMENTED)
    assert "build_commercial" in later
    assert "build_action" not in later
    for stage in later:
        output = runtime.pipeline.execute_stage(stage)
        assert output.payload is NotImplemented


def test_cs19_shadow_mode_unchanged(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert SHADOW_MODE is True
    assert runtime.shadow_mode is True
    assert runtime.replaces_pack05 is False
    assert runtime.portal_connected is False
    assert result.presentation is not None
