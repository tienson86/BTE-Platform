"""IE-3 canonical assembled Interpretation Result. No presentation formats."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.interpretation_engine.composition.chapter_builder import AssembledChapter
from engines.interpretation_engine.composition.composition_context import (
    ASSEMBLY_ENGINE_ID,
    ASSEMBLY_VERSION,
)
from engines.interpretation_engine.composition.cross_reference_builder import CrossReference
from engines.interpretation_engine.composition.flow_optimizer import FlowPlan
from engines.interpretation_engine.composition.section_builder import AssembledSection
from engines.interpretation_engine.foundation_constants import INTERPRETATION_VERSION

DIAG_SECTION_DUPLICATE = "SECTION-DUPLICATE"
DIAG_CHAPTER_DUPLICATE = "CHAPTER-DUPLICATE"
DIAG_REFERENCE_BROKEN = "REFERENCE-BROKEN"
DIAG_FLOW_VIOLATION = "FLOW-VIOLATION"
DIAG_CONTRACT_VIOLATION = "CONTRACT-VIOLATION"
DIAG_PIPE_OK = "PIPE-OK"
DIAG_PIPE_FAIL = "PIPE-FAIL"


@dataclass(slots=True)
class AssemblyDiagnostic:
    """Structured assembly diagnostic. No exception payload."""

    code: str
    message: str
    severity: str = "error"
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize one diagnostic."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "details": dict(self.details),
        }


@dataclass(slots=True)
class InterpretationTrace:
    """Machine-readable IE-3 execution trace."""

    assembly_version: str = ASSEMBLY_VERSION
    candidates_consumed: tuple[str, ...] = ()
    sections_created: tuple[str, ...] = ()
    chapters_created: tuple[str, ...] = ()
    flow_optimization: dict[str, Any] = field(default_factory=dict)
    cross_references: tuple[str, ...] = ()
    started_at: str | None = None
    completed_at: str | None = None
    stage_order: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the interpretation trace."""
        return {
            "assembly_version": self.assembly_version,
            "candidates_consumed": list(self.candidates_consumed),
            "sections_created": list(self.sections_created),
            "chapters_created": list(self.chapters_created),
            "flow_optimization": dict(self.flow_optimization),
            "cross_references": list(self.cross_references),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "stage_order": list(self.stage_order),
        }


@dataclass(slots=True)
class InterpretationAudit:
    """Machine-readable IE-3 legality audit."""

    contract_validation: str
    registry_validation: str
    flow_legality: str
    chapter_legality: str
    section_legality: str
    cross_reference_integrity: str
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the interpretation audit."""
        return {
            "contract_validation": self.contract_validation,
            "registry_validation": self.registry_validation,
            "flow_legality": self.flow_legality,
            "chapter_legality": self.chapter_legality,
            "section_legality": self.section_legality,
            "cross_reference_integrity": self.cross_reference_integrity,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
        }


@dataclass(slots=True)
class CanonicalInterpretationResult:
    """Official assembled Interpretation Result produced by IE-3."""

    interpretation_version: str = INTERPRETATION_VERSION
    assembly_version: str = ASSEMBLY_VERSION
    engine_id: str = ASSEMBLY_ENGINE_ID
    success: bool = True
    sections: tuple[AssembledSection, ...] = ()
    chapters: tuple[AssembledChapter, ...] = ()
    cross_references: tuple[CrossReference, ...] = ()
    metadata: dict[str, Any] | None = None
    interpretation_trace: InterpretationTrace | None = None
    interpretation_audit: InterpretationAudit | None = None
    diagnostics: tuple[AssemblyDiagnostic, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the canonical assembled interpretation result."""
        return {
            "interpretation_version": self.interpretation_version,
            "assembly_version": self.assembly_version,
            "engine_id": self.engine_id,
            "success": self.success,
            "sections": [item.to_dict() for item in self.sections],
            "chapters": [item.to_dict() for item in self.chapters],
            "cross_references": [item.to_dict() for item in self.cross_references],
            "metadata": dict(self.metadata or {}),
            "interpretation_trace": (
                None if self.interpretation_trace is None else self.interpretation_trace.to_dict()
            ),
            "interpretation_audit": (
                None if self.interpretation_audit is None else self.interpretation_audit.to_dict()
            ),
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "errors": list(self.errors),
        }


def build_audit(diagnostics: Sequence[AssemblyDiagnostic]) -> InterpretationAudit:
    """Derive audit flags from diagnostic codes."""
    codes = {item.code for item in diagnostics if item.severity == "error"}
    info_codes = tuple(item.code for item in diagnostics)

    def flag(error_code: str) -> str:
        return "fail" if error_code in codes else "pass"

    version_fail = DIAG_CONTRACT_VIOLATION in codes and any(
        "version" in str(item.details.get("error", item.message)) for item in diagnostics
    )
    return InterpretationAudit(
        contract_validation=flag(DIAG_CONTRACT_VIOLATION),
        registry_validation="fail" if DIAG_CONTRACT_VIOLATION in codes else "pass",
        flow_legality=flag(DIAG_FLOW_VIOLATION),
        chapter_legality=flag(DIAG_CHAPTER_DUPLICATE),
        section_legality=flag(DIAG_SECTION_DUPLICATE),
        cross_reference_integrity=flag(DIAG_REFERENCE_BROKEN),
        version_compatibility="fail" if version_fail else "pass",
        reason_codes=info_codes,
    )


def build_trace(
    *,
    candidates: Sequence[Mapping[str, Any]],
    sections: Sequence[AssembledSection],
    chapters: Sequence[AssembledChapter],
    flow_plan: FlowPlan | None,
    references: Sequence[CrossReference],
    started_at: str | None,
    completed_at: str | None,
    stage_order: Sequence[str],
) -> InterpretationTrace:
    """Assemble the machine-readable interpretation trace."""
    return InterpretationTrace(
        candidates_consumed=tuple(
            str(item.get("sentence_id"))
            for item in candidates
            if item.get("sentence_id")
        ),
        sections_created=tuple(item.section_id for item in sections),
        chapters_created=tuple(item.chapter_id for item in chapters),
        flow_optimization={} if flow_plan is None else flow_plan.to_dict(),
        cross_references=tuple(item.reference_id for item in references),
        started_at=started_at,
        completed_at=completed_at,
        stage_order=tuple(stage_order),
    )
