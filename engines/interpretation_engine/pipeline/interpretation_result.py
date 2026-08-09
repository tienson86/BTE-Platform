"""Canonical Interpretation Pipeline result — the only official IX-1 output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.interpretation_engine.pipeline.diagnostics import InterpretationPipelineDiagnostic
from engines.interpretation_engine.pipeline.interpretation_audit import InterpretationPipelineAudit
from engines.interpretation_engine.pipeline.interpretation_trace import InterpretationPipelineTrace
from engines.interpretation_engine.pipeline.stage_registry import PIPELINE_ID, PIPELINE_VERSION

RESULT_FIELDS: tuple[str, ...] = (
    "foundation_result",
    "knowledge_result",
    "composition_result",
    "canonical_interpretation",
    "interpretation_trace",
    "interpretation_audit",
    "interpretation_diagnostics",
    "interpretation_pipeline_version",
    "component_versions",
)


@dataclass(slots=True)
class CanonicalInterpretationResult:
    """Official Interpretation Pipeline aggregate. Nested IE-3 assembly is preserved."""

    pipeline_id: str
    interpretation_pipeline_version: str
    success: bool
    foundation_result: dict[str, Any] | None = None
    knowledge_result: dict[str, Any] | None = None
    composition_result: dict[str, Any] | None = None
    canonical_interpretation: dict[str, Any] | None = None
    interpretation_trace: InterpretationPipelineTrace | None = None
    interpretation_audit: InterpretationPipelineAudit | None = None
    interpretation_diagnostics: tuple[InterpretationPipelineDiagnostic, ...] = ()
    component_versions: dict[str, str] = field(default_factory=dict)
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical interpretation pipeline result."""
        return {
            "pipeline_id": self.pipeline_id,
            "interpretation_pipeline_version": self.interpretation_pipeline_version,
            "success": self.success,
            "foundation_result": self.foundation_result,
            "knowledge_result": self.knowledge_result,
            "composition_result": self.composition_result,
            "canonical_interpretation": self.canonical_interpretation,
            "interpretation_trace": (
                None if self.interpretation_trace is None else self.interpretation_trace.to_dict()
            ),
            "interpretation_audit": (
                None if self.interpretation_audit is None else self.interpretation_audit.to_dict()
            ),
            "interpretation_diagnostics": [item.to_dict() for item in self.interpretation_diagnostics],
            "component_versions": dict(self.component_versions),
            "errors": list(self.errors),
        }


def build_canonical_interpretation_result(
    *,
    success: bool,
    foundation_result: Mapping[str, Any] | None,
    knowledge_result: Mapping[str, Any] | None,
    composition_result: Mapping[str, Any] | None,
    interpretation_trace: InterpretationPipelineTrace | None,
    interpretation_audit: InterpretationPipelineAudit | None,
    diagnostics: Sequence[InterpretationPipelineDiagnostic],
    component_versions: Mapping[str, str],
    errors: Sequence[str],
    pipeline_id: str = PIPELINE_ID,
    pipeline_version: str = PIPELINE_VERSION,
) -> CanonicalInterpretationResult:
    """Assemble the official pipeline result from completed stage snapshots."""
    composition = None if composition_result is None else dict(composition_result)
    return CanonicalInterpretationResult(
        pipeline_id=pipeline_id,
        interpretation_pipeline_version=pipeline_version,
        success=success,
        foundation_result=None if foundation_result is None else dict(foundation_result),
        knowledge_result=None if knowledge_result is None else dict(knowledge_result),
        composition_result=composition,
        canonical_interpretation=composition,
        interpretation_trace=interpretation_trace,
        interpretation_audit=interpretation_audit,
        interpretation_diagnostics=tuple(diagnostics),
        component_versions=dict(component_versions),
        errors=tuple(errors),
    )
