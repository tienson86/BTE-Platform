"""Machine-readable Luck Pipeline audit."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from engines.luck_engine.pipeline.diagnostics import (
    DIAG_ANALYSIS_MISSING,
    DIAG_CONTRACT_VIOLATION,
    DIAG_DECISION_MISSING,
    DIAG_DEP_VIOLATION,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    DIAG_PIPE_OK,
    DIAG_TIMELINE_MISSING,
    LuckPipelineDiagnostic,
)
from engines.luck_engine.pipeline.stage_registry import (
    STAGE_ANALYSIS,
    STAGE_DECISION,
    STAGE_TIMELINE,
)


@dataclass(slots=True)
class LuckAudit:
    """Legality audit for one Canonical Luck Pipeline run."""

    contract_validation: str
    dependency_validation: str
    timeline_legality: str
    analysis_legality: str
    decision_legality: str
    deterministic_execution: bool
    version_compatibility: str
    reason_codes: tuple[str, ...] = ()
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the luck audit."""
        return {
            "contract_validation": self.contract_validation,
            "dependency_validation": self.dependency_validation,
            "timeline_legality": self.timeline_legality,
            "analysis_legality": self.analysis_legality,
            "decision_legality": self.decision_legality,
            "deterministic_execution": self.deterministic_execution,
            "version_compatibility": self.version_compatibility,
            "reason_codes": list(self.reason_codes),
            "details": dict(self.details),
        }


AUDIT_SCHEMA_KEYS: tuple[str, ...] = (
    "contract_validation",
    "dependency_validation",
    "timeline_legality",
    "analysis_legality",
    "decision_legality",
    "deterministic_execution",
    "version_compatibility",
    "reason_codes",
    "details",
)


def _legality(stage_id: str, executed: Sequence[str], fail_codes: set[str]) -> str:
    if fail_codes:
        return "fail"
    if stage_id in executed:
        return "pass"
    return "not_run"


def build_luck_audit(
    *,
    diagnostics: Sequence[LuckPipelineDiagnostic],
    executed_stages: Sequence[str],
) -> LuckAudit:
    """Derive audit flags from diagnostics and executed stages."""
    codes = [item.code for item in diagnostics]
    code_set = set(codes)
    error_codes = {item.code for item in diagnostics if item.severity == "error"}
    contract_fail = DIAG_CONTRACT_VIOLATION in error_codes
    dep_fail = DIAG_DEP_VIOLATION in error_codes
    timeline_fail = {DIAG_TIMELINE_MISSING} & error_codes
    analysis_fail = {DIAG_ANALYSIS_MISSING} & error_codes
    decision_fail = {DIAG_DECISION_MISSING} & error_codes
    reason_codes = tuple(
        code
        for code in codes
        if code
        in {
            DIAG_TIMELINE_MISSING,
            DIAG_ANALYSIS_MISSING,
            DIAG_DECISION_MISSING,
            DIAG_CONTRACT_VIOLATION,
            DIAG_DEP_VIOLATION,
            DIAG_OUT_DUPLICATE,
            DIAG_PIPE_FAIL,
            DIAG_PIPE_OK,
        }
    )
    details: dict[str, Any] = {}
    if DIAG_PIPE_FAIL in code_set:
        failed = next((item for item in diagnostics if item.code == DIAG_PIPE_FAIL), None)
        if failed is not None:
            details["stop_reason"] = failed.message
    return LuckAudit(
        contract_validation="fail" if contract_fail else "pass",
        dependency_validation="fail" if dep_fail else "pass",
        timeline_legality=_legality(STAGE_TIMELINE, executed_stages, timeline_fail),
        analysis_legality=_legality(STAGE_ANALYSIS, executed_stages, analysis_fail),
        decision_legality=_legality(STAGE_DECISION, executed_stages, decision_fail),
        deterministic_execution=True,
        version_compatibility="fail" if contract_fail else "pass",
        reason_codes=reason_codes,
        details=details,
    )


def passing_luck_audit(*, reason_codes: tuple[str, ...] = (DIAG_PIPE_OK,)) -> LuckAudit:
    """Return an audit for a fully legal successful run."""
    return LuckAudit(
        contract_validation="pass",
        dependency_validation="pass",
        timeline_legality="pass",
        analysis_legality="pass",
        decision_legality="pass",
        deterministic_execution=True,
        version_compatibility="pass",
        reason_codes=reason_codes,
    )
