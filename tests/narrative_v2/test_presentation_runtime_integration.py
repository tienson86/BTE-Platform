"""Runtime integration for Presentation freeze (N-IMP-09)."""

from __future__ import annotations

from typing import Any

from engines.narrative_v2.presentation import NarrativeV2Presentation
from engines.narrative_v2.runtime import BUILDER_STAGES, SHADOW_MODE, NarrativeRuntime
from engines.narrative_v2.runtime.runtime_pipeline import StageResult


def test_p20_shadow_mode_still_enabled(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert SHADOW_MODE is True
    assert runtime.shadow_mode is True
    assert result.runtime_metadata["shadow_mode"] is True


def test_p21_portal_connected_remains_false(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert runtime.portal_connected is False
    assert result.runtime_metadata["portal_connected"] is False


def test_p22_replaces_pack05_remains_false(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert runtime.replaces_pack05 is False
    assert result.runtime_metadata["replaces_pack05"] is False


def test_p23_build_commercial_remains_not_implemented(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    runtime.pipeline.build_evidence()
    runtime.pipeline.build_reasoning()
    runtime.pipeline.resolve_knowledge()
    runtime.pipeline.commercial_rewrite()
    runtime.pipeline.build_summary()
    runtime.pipeline.build_interpretation()
    runtime.pipeline.build_action()
    later = tuple(stage for stage in BUILDER_STAGES if stage == "build_commercial")
    assert later == ("build_commercial",)
    output = runtime.pipeline.execute_stage("build_commercial")
    assert output.payload is NotImplemented
    assert output.status == "not_implemented"


def test_p24_presentation_non_none_after_internal_publish(
    case_0001_canonical: dict[str, Any],
) -> None:
    runtime = NarrativeRuntime()
    result = runtime.run(case_0001_canonical)
    assert isinstance(result.presentation, NarrativeV2Presentation)
    assert runtime.context is not None
    assert runtime.context.presentation is result.presentation
    assert result.runtime_metadata["generates_narrative"] is False


def test_publish_stage_returns_frozen_presentation(case_0001_canonical: dict[str, Any]) -> None:
    runtime = NarrativeRuntime()
    runtime.initialize(case_0001_canonical)
    for stage in (
        "build_evidence",
        "build_reasoning",
        "resolve_knowledge",
        "commercial_rewrite",
        "build_summary",
        "build_interpretation",
        "build_action",
        "build_commercial",
        "validate",
    ):
        runtime.pipeline.execute_stage(stage)
    published = runtime.pipeline.publish()
    assert isinstance(published, StageResult)
    assert published.status == "implemented"
    assert isinstance(published.payload, NarrativeV2Presentation)
