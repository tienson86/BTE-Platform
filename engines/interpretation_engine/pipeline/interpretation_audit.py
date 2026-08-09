"""Machine-readable Canonical Interpretation Pipeline audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.interpretation_engine.pipeline.diagnostics import (
    DIAG_COMPOSITION_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_DEP_VIOLATION,
    DIAG_FOUNDATION_MISSING,
    DIAG_KNOWLEDGE_MISSING,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    InterpretationPipelineDiagnostic,
)
from engines.interpretation_engine.pipeline.stage_registry import (
    STAGE_COMPOSITION,
    STAGE_FOUNDATION,
    STAGE_KNOWLEDGE,
)

AUDIT_SCHEMA_KEYS: tuple[str, ...] = (
    "contract_validation",
    "dependency_validation",
    "foundation_legality",
    "knowledge_legality",
    "composition_legality",
    "deterministic_execution",
    "version_compatibility",
    "reason_codes",
    "details",
)


@dataclass(slots=True)
class InterpretationPipelineAudit:
    """Legality audit for one Canonical Interpretation Pipeline run."""

    contract_validation: str
    dependency_validation: str
    foundation_legality: str
    knowledge_legality: str
    composition_legality: str
    deterministic_execution: bool
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the interpretation pipeline audit."""
        return {
            "contract_validation": self.contract_validation,
            "dependency_validation": self.dependency_validation,
            "foundation_legality": self.foundation_legality,
            "knowledge_legality": self.knowledge_legality,
            "composition_legality": self.composition_legality,
            "deterministic_execution": self.deterministic_execution,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
            "details": dict(self.details),
        }


def _legality(stage_id: str, executed: Sequence[str], fail_codes: set[str]) -> str:
    if fail_codes:
        return "fail"
    if stage_id in executed:
        return "pass"
    return "not_run"


def build_interpretation_pipeline_audit(
    *,
    diagnostics: Sequence[InterpretationPipelineDiagnostic],
    executed_stages: Sequence[str],
) -> InterpretationPipelineAudit:
    """Derive audit flags from diagnostics and executed stages."""
    codes = [item.code for item in diagnostics]
    error_codes = {item.code for item in diagnostics if item.severity == "error"}
    contract_fail = DIAG_CONTRACT_VIOLATION in error_codes
    dep_fail = DIAG_DEP_VIOLATION in error_codes
    reason_codes = tuple(
        code
        for code in codes
        if code
        in {
            DIAG_FOUNDATION_MISSING,
            DIAG_KNOWLEDGE_MISSING,
            DIAG_COMPOSITION_MISSING,
            DIAG_CONTRACT_VIOLATION,
            DIAG_DEP_VIOLATION,
            DIAG_OUT_DUPLICATE,
            DIAG_PIPE_FAIL,
            DIAG_PIPE_OK,
        }
    )
    details: dict[str, Any] = {}
    failed = next((item for item in diagnostics if item.code == DIAG_PIPE_FAIL), None)
    if failed is not None:
        details["stop_reason"] = failed.message
    return InterpretationPipelineAudit(
        contract_validation="fail" if contract_fail else "pass",
        dependency_validation="fail" if dep_fail else "pass",
        foundation_legality=_legality(
            STAGE_FOUNDATION, executed_stages, {DIAG_FOUNDATION_MISSING} & error_codes
        ),
        knowledge_legality=_legality(
            STAGE_KNOWLEDGE, executed_stages, {DIAG_KNOWLEDGE_MISSING} & error_codes
        ),
        composition_legality=_legality(
            STAGE_COMPOSITION, executed_stages, {DIAG_COMPOSITION_MISSING} & error_codes
        ),
        deterministic_execution=True,
        version_compatibility="fail" if contract_fail else "pass",
        reason_codes=reason_codes,
        details=details,
    )
