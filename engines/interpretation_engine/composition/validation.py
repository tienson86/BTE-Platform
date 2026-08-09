"""IE-3 assembly validation. No presentation checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.interpretation_engine.composition.chapter_builder import AssembledChapter
from engines.interpretation_engine.composition.composition_context import (
    ASSEMBLY_VERSION,
    InterpretationAssemblyContext,
)
from engines.interpretation_engine.composition.composition_registry import (
    CANONICAL_STAGE_ORDER,
    CompositionRegistry,
)
from engines.interpretation_engine.composition.composition_result import (
    DIAG_CHAPTER_DUPLICATE,
    DIAG_CONTRACT_VIOLATION,
    DIAG_FLOW_VIOLATION,
    DIAG_REFERENCE_BROKEN,
    DIAG_SECTION_DUPLICATE,
    AssemblyDiagnostic,
)
from engines.interpretation_engine.composition.cross_reference_builder import CrossReference
from engines.interpretation_engine.composition.flow_optimizer import FlowPlan
from engines.interpretation_engine.composition.section_builder import AssembledSection
from engines.interpretation_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    INTERPRETATION_VERSION,
    MODULE_OVERVIEW,
    MODULE_SUMMARY,
)

REQUIRED_ANALYSIS_VERSION = "2.0.0"
REQUIRED_DECISION_VERSION = "1.0.0"
REQUIRED_LUCK_VERSION = "1.0.0"


@dataclass(slots=True)
class AssemblyValidationReport:
    """Machine-readable IE-3 validation report."""

    success: bool
    diagnostics: tuple[AssemblyDiagnostic, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the validation report."""
        return {
            "success": self.success,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "details": dict(self.details),
        }


def _diagnostic(code: str, message: str, **details: Any) -> AssemblyDiagnostic:
    return AssemblyDiagnostic(code=code, message=message, details=dict(details))


def validate_versions(context: InterpretationAssemblyContext) -> None:
    """Require AX-2 / AX-3 / AX-4 / IE-1 / IE-3 versions."""
    analysis = str(context.analysis_snapshot().get("pipeline_version") or "")
    decision = str(context.decision_snapshot().get("decision_pipeline_version") or "")
    luck = str(context.luck_snapshot().get("luck_pipeline_version") or "")
    interpretation = str(context.interpretation_snapshot().get("interpretation_version") or "")
    if context.assembly_version != ASSEMBLY_VERSION:
        raise ValueError(f"assembly_version_incompatible:{context.assembly_version}")
    if analysis != REQUIRED_ANALYSIS_VERSION:
        raise ValueError(f"analysis_pipeline_incompatible:{analysis}")
    if decision != REQUIRED_DECISION_VERSION:
        raise ValueError(f"decision_pipeline_incompatible:{decision}")
    if luck != REQUIRED_LUCK_VERSION:
        raise ValueError(f"luck_pipeline_incompatible:{luck}")
    if interpretation != INTERPRETATION_VERSION:
        raise ValueError(f"interpretation_version_incompatible:{interpretation}")


def validate_registry(registry: CompositionRegistry) -> None:
    """Require the canonical deterministic assembly catalog."""
    if registry.registered_ids() != CANONICAL_STAGE_ORDER:
        raise ValueError("registry_stage_mismatch")
    if registry.resolve_order() != CANONICAL_STAGE_ORDER:
        raise ValueError("registry_order_mismatch")


def validate_section_integrity(sections: Sequence[AssembledSection]) -> None:
    """Reject duplicate section ids and unknown modules."""
    ids = [item.section_id for item in sections]
    if len(ids) != len(set(ids)):
        raise ValueError(DIAG_SECTION_DUPLICATE)
    for item in sections:
        if item.module_id not in CANONICAL_MODULE_ORDER:
            raise ValueError(f"unknown_section_module:{item.module_id}")


def validate_chapter_order(chapters: Sequence[AssembledChapter]) -> None:
    """Require unique chapters in registered module order."""
    ids = [item.chapter_id for item in chapters]
    if len(ids) != len(set(ids)):
        raise ValueError(DIAG_CHAPTER_DUPLICATE)
    module_ids = [item.module_id for item in chapters]
    expected = [module_id for module_id in CANONICAL_MODULE_ORDER if module_id in module_ids]
    if module_ids != expected:
        raise ValueError(DIAG_FLOW_VIOLATION)


def validate_flow(plan: FlowPlan, sections: Sequence[AssembledSection]) -> None:
    """Require overview-before-summary grouping and declared operations only."""
    allowed = {"order_by_module", "group_overview_body_summary"}
    if any(operation not in allowed for operation in plan.operations):
        raise ValueError(DIAG_FLOW_VIOLATION)
    section_ids = [item.section_id for item in sections]
    if list(plan.section_order) != section_ids:
        raise ValueError(DIAG_FLOW_VIOLATION)
    overview_ids = [item.section_id for item in sections if item.module_id == MODULE_OVERVIEW]
    summary_ids = [item.section_id for item in sections if item.module_id == MODULE_SUMMARY]
    if overview_ids and summary_ids:
        if section_ids.index(overview_ids[0]) > section_ids.index(summary_ids[0]):
            raise ValueError(DIAG_FLOW_VIOLATION)


def validate_cross_references(
    references: Sequence[CrossReference],
    sections: Sequence[AssembledSection],
    chapters: Sequence[AssembledChapter],
) -> None:
    """Require every reference endpoint to exist in assembled artifacts."""
    section_ids = {item.section_id for item in sections}
    chapter_ids = {item.chapter_id for item in chapters}
    knowledge_ids = {kid for item in sections for kid in item.knowledge_ids}
    evidence_ids = {eid for item in sections for eid in item.evidence_ids}
    reasoning_ids = {rid for item in sections for rid in item.reasoning_ids}
    pools = {
        "section": section_ids,
        "chapter": chapter_ids,
        "knowledge": knowledge_ids,
        "evidence": evidence_ids,
        "reasoning": reasoning_ids,
    }
    ref_ids = [item.reference_id for item in references]
    if len(ref_ids) != len(set(ref_ids)):
        raise ValueError(DIAG_REFERENCE_BROKEN)
    for item in references:
        source_pool = pools.get(item.source_type)
        target_pool = pools.get(item.target_type)
        if source_pool is None or item.source_id not in source_pool:
            raise ValueError(DIAG_REFERENCE_BROKEN)
        if target_pool is None or item.target_id not in target_pool:
            raise ValueError(DIAG_REFERENCE_BROKEN)


def validate_assembly(
    *,
    context: InterpretationAssemblyContext,
    registry: CompositionRegistry,
    sections: Sequence[AssembledSection],
    chapters: Sequence[AssembledChapter],
    flow_plan: FlowPlan,
    references: Sequence[CrossReference],
) -> AssemblyValidationReport:
    """Run the IE-3 validation suite and map failures to diagnostics."""
    diagnostics: list[AssemblyDiagnostic] = []
    try:
        validate_versions(context)
        validate_registry(registry)
        validate_section_integrity(sections)
        validate_chapter_order(chapters)
        validate_flow(flow_plan, sections)
        validate_cross_references(references, sections, chapters)
        return AssemblyValidationReport(success=True, diagnostics=tuple(diagnostics))
    except ValueError as exc:
        message = str(exc)
        if message == DIAG_SECTION_DUPLICATE:
            diagnostics.append(_diagnostic(DIAG_SECTION_DUPLICATE, "Duplicate section id"))
        elif message == DIAG_CHAPTER_DUPLICATE:
            diagnostics.append(_diagnostic(DIAG_CHAPTER_DUPLICATE, "Duplicate chapter id"))
        elif message == DIAG_REFERENCE_BROKEN:
            diagnostics.append(_diagnostic(DIAG_REFERENCE_BROKEN, "Broken cross reference"))
        elif message == DIAG_FLOW_VIOLATION:
            diagnostics.append(_diagnostic(DIAG_FLOW_VIOLATION, "Illegal flow order"))
        else:
            diagnostics.append(
                _diagnostic(DIAG_CONTRACT_VIOLATION, "Assembly contract failed", error=message)
            )
        return AssemblyValidationReport(
            success=False,
            diagnostics=tuple(diagnostics),
            details={"error": message},
        )
