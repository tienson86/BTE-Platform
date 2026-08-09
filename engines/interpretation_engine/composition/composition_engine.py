"""IE-3 Interpretation Composition & Assembly Engine. Never raises to API."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable

from engines.interpretation_engine.composition.chapter_builder import ChapterBuilder
from engines.interpretation_engine.composition.composition_context import (
    ASSEMBLY_ENGINE_ID,
    ASSEMBLY_VERSION,
    AssemblyError,
    InterpretationAssemblyContext,
    build_assembly_context,
)
from engines.interpretation_engine.composition.composition_registry import (
    STAGE_ASSEMBLY,
    STAGE_CHAPTER,
    STAGE_CROSS_REFERENCE,
    STAGE_FLOW,
    STAGE_SECTION,
    CompositionRegistry,
)
from engines.interpretation_engine.composition.composition_result import (
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    AssemblyDiagnostic,
    CanonicalInterpretationResult,
    build_audit,
    build_trace,
)
from engines.interpretation_engine.composition.cross_reference_builder import CrossReferenceBuilder
from engines.interpretation_engine.composition.flow_optimizer import FlowOptimizer
from engines.interpretation_engine.composition.section_builder import SectionBuilder
from engines.interpretation_engine.composition.validation import validate_assembly
from engines.interpretation_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    INTERPRETATION_VERSION,
)

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class InterpretationCompositionEngine:
    """Assemble IE-2 candidates into the canonical Interpretation Result."""

    engine_id: str = ASSEMBLY_ENGINE_ID
    assembly_version: str = ASSEMBLY_VERSION

    def __init__(
        self,
        *,
        registry: CompositionRegistry | None = None,
        section_builder: SectionBuilder | None = None,
        chapter_builder: ChapterBuilder | None = None,
        flow_optimizer: FlowOptimizer | None = None,
        cross_reference_builder: CrossReferenceBuilder | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize deterministic assembly collaborators."""
        self._registry = registry or CompositionRegistry.default()
        self._sections = section_builder or SectionBuilder()
        self._chapters = chapter_builder or ChapterBuilder()
        self._flow = flow_optimizer or FlowOptimizer()
        self._references = cross_reference_builder or CrossReferenceBuilder()
        self._clock = clock or _utc_now

    def run(
        self,
        *,
        analysis_result: Any,
        decision_result: Any,
        luck_result: Any,
        interpretation_context: Any,
        composition_result: Any,
        sentence_candidates: Any = None,
        context: InterpretationAssemblyContext | None = None,
    ) -> CanonicalInterpretationResult:
        """Assemble the official interpretation result. Failures become diagnostics."""
        started_at = _iso(self._clock())
        diagnostics: list[AssemblyDiagnostic] = []
        errors: list[str] = []
        sections = ()
        chapters = ()
        references = ()
        flow_plan = None
        stage_order: tuple[str, ...] = ()
        success = False
        assembly_context: InterpretationAssemblyContext | None = context
        try:
            assembly_context = context or build_assembly_context(
                analysis_result=analysis_result,
                decision_result=decision_result,
                luck_result=luck_result,
                interpretation_context=interpretation_context,
                composition_result=composition_result,
                sentence_candidates=sentence_candidates,
            )
            stage_order = self._registry.resolve_order()
            sections = self._sections.build(assembly_context)
            assembly_context.publish(STAGE_SECTION, [item.to_dict() for item in sections])
            chapters = self._chapters.build(sections)
            assembly_context.publish(STAGE_CHAPTER, [item.to_dict() for item in chapters])
            sections, chapters, flow_plan = self._flow.optimize(sections, chapters)
            assembly_context.publish(STAGE_FLOW, flow_plan.to_dict())
            references = self._references.build(sections, chapters)
            assembly_context.publish(
                STAGE_CROSS_REFERENCE,
                [item.to_dict() for item in references],
            )
            report = validate_assembly(
                context=assembly_context,
                registry=self._registry,
                sections=sections,
                chapters=chapters,
                flow_plan=flow_plan,
                references=references,
            )
            diagnostics.extend(report.diagnostics)
            if report.success:
                diagnostics.append(
                    AssemblyDiagnostic(DIAG_PIPE_OK, "Interpretation assembly passed", "info")
                )
                success = True
            else:
                diagnostics.append(
                    AssemblyDiagnostic(DIAG_PIPE_FAIL, "Interpretation assembly failed")
                )
                errors.append(str(report.details.get("error") or "assembly_failed"))
            assembly_context.publish(STAGE_ASSEMBLY, {"success": success})
        except AssemblyError as exc:
            logger.warning("interpretation_assembly_failed %s", exc)
            diagnostics.append(AssemblyDiagnostic(DIAG_PIPE_FAIL, str(exc)))
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("interpretation_assembly_unexpected")
            diagnostics.append(AssemblyDiagnostic(DIAG_PIPE_FAIL, DIAG_PIPE_FAIL))
            errors.append(str(exc))

        completed_at = _iso(self._clock())
        candidates = () if assembly_context is None else assembly_context.candidates()
        trace = build_trace(
            candidates=candidates,
            sections=sections,
            chapters=chapters,
            flow_plan=flow_plan,
            references=references,
            started_at=started_at,
            completed_at=completed_at,
            stage_order=stage_order,
        )
        metadata = {
            "interpretation_version": INTERPRETATION_VERSION,
            "assembly_version": ASSEMBLY_VERSION,
            "engine_id": ASSEMBLY_ENGINE_ID,
            "module_ids": list(CANONICAL_MODULE_ORDER),
            "reports": False,
            "ai_rewrite": False,
            "presentation": False,
        }
        return CanonicalInterpretationResult(
            success=success,
            sections=sections,
            chapters=chapters,
            cross_references=references,
            metadata=metadata,
            interpretation_trace=trace,
            interpretation_audit=build_audit(diagnostics),
            diagnostics=tuple(diagnostics),
            errors=tuple(errors),
        )
