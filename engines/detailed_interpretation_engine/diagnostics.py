"""Development-only Pack 07 runtime diagnostics. Not customer UI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import DiagnosticStatus, EvaluationStatus, ValidationStatus
from engines.detailed_interpretation_engine.factories import (
    api_model_from_runtime,
    consulting_model_from_runtime,
    export_model_from_runtime,
)
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods
from engines.detailed_interpretation_engine.validation import ValidationIssue, ValidationResult
from engines.detailed_interpretation_engine.validators import (
    validate_api_projection,
    validate_canonical_runtime,
    validate_consulting_projection,
    validate_export_projection,
    validate_pack07_context,
)


@dataclass(frozen=True, slots=True)
class Pack07RuntimeDiagnostics:
    """Developer/Product Owner implementation-state view. No reasoning text."""

    analysis_id: str
    contracts: DiagnosticStatus
    contexts: DiagnosticStatus
    validators: DiagnosticStatus
    mc01_reference: DiagnosticStatus
    ten_gods: DiagnosticStatus
    ten_god_combination: DiagnosticStatus
    ten_gods_ecosystem: DiagnosticStatus
    shen_sha: DiagnosticStatus
    evidence_priority: DiagnosticStatus
    domains: DiagnosticStatus
    luck: DiagnosticStatus
    temporal: DiagnosticStatus
    optimization: DiagnosticStatus
    narrative: DiagnosticStatus
    runtime_contract: DiagnosticStatus
    overall_status: DiagnosticStatus
    issues: tuple[ValidationIssue, ...]
    validation: ValidationResult

    def to_dict(self) -> dict[str, Any]:
        """Serialize diagnostics without customer payload fields."""
        return {
            "analysis_id": self.analysis_id,
            "contracts": self.contracts.value,
            "contexts": self.contexts.value,
            "validators": self.validators.value,
            "mc01_reference": self.mc01_reference.value,
            "ten_gods": self.ten_gods.value,
            "ten_god_combination": self.ten_god_combination.value,
            "ten_gods_ecosystem": self.ten_gods_ecosystem.value,
            "shen_sha": self.shen_sha.value,
            "evidence_priority": self.evidence_priority.value,
            "domains": self.domains.value,
            "luck": self.luck.value,
            "temporal": self.temporal.value,
            "optimization": self.optimization.value,
            "narrative": self.narrative.value,
            "runtime_contract": self.runtime_contract.value,
            "overall_status": self.overall_status.value,
            "issues": [item.to_dict() for item in self.issues],
            "validation": self.validation.to_dict(),
        }


def _pass_or_fail(result: ValidationResult) -> DiagnosticStatus:
    if result.status is ValidationStatus.FAIL:
        return DiagnosticStatus.FAIL
    return DiagnosticStatus.PASS


def _layer_status(status: EvaluationStatus, empty: bool) -> DiagnosticStatus:
    if status is EvaluationStatus.NOT_EVALUATED and empty:
        return DiagnosticStatus.NOT_IMPLEMENTED
    if status is EvaluationStatus.RESOLVED:
        return DiagnosticStatus.PASS
    if status in {
        EvaluationStatus.PARTIALLY_RESOLVED,
        EvaluationStatus.INSUFFICIENT_EVIDENCE,
    }:
        return DiagnosticStatus.PARTIAL
    if status is EvaluationStatus.UNRESOLVED:
        return DiagnosticStatus.WARNING
    return DiagnosticStatus.NOT_IMPLEMENTED


def build_pack07_diagnostics(context: CanonicalAnalysisContext) -> Pack07RuntimeDiagnostics:
    """Build development diagnostics from a Pack 07 context chain."""
    context_result = validate_pack07_context(context)
    runtime_result = validate_canonical_runtime(context.runtime)
    export = export_model_from_runtime(context.runtime)
    api = api_model_from_runtime(context.runtime)
    consulting = consulting_model_from_runtime(context.runtime)
    extra = (
        validate_export_projection(export, context.runtime).issues
        + validate_api_projection(api, context.runtime).issues
        + validate_consulting_projection(consulting, context.runtime).issues
    )
    issues = context_result.issues + extra
    mc01 = (
        DiagnosticStatus.NOT_BOUND
        if not context.interpretation.mc01.mingju_result_id
        else DiagnosticStatus.PASS
    )
    validator_status = DiagnosticStatus.FAIL if any(
        item.severity.value == "critical" for item in issues
    ) else DiagnosticStatus.PASS
    natal = context.runtime.interpretation.ten_gods
    ten_gods_status = _layer_status(natal.status, not natal.natal.items)
    combination_status = _layer_status(
        natal.combinations.state, not natal.combinations.items
    )
    ecosystem_status = _layer_status(
        natal.ecosystem.state, not natal.ecosystem.trace_ids and natal.ecosystem.driver.state.value == "not_applicable"
    )
    overall = (
        DiagnosticStatus.FAIL
        if context_result.status is ValidationStatus.FAIL
        else DiagnosticStatus.PASS
    )
    return Pack07RuntimeDiagnostics(
        analysis_id=context.analysis_id,
        contracts=DiagnosticStatus.PASS,
        contexts=_pass_or_fail(context_result),
        validators=validator_status,
        mc01_reference=mc01,
        ten_gods=ten_gods_status,
        ten_god_combination=combination_status,
        ten_gods_ecosystem=ecosystem_status,
        shen_sha=DiagnosticStatus.NOT_IMPLEMENTED,
        evidence_priority=DiagnosticStatus.NOT_IMPLEMENTED,
        domains=DiagnosticStatus.NOT_EVALUATED,
        luck=DiagnosticStatus.NOT_IMPLEMENTED,
        temporal=DiagnosticStatus.NOT_EVALUATED,
        optimization=DiagnosticStatus.NOT_EVALUATED,
        narrative=DiagnosticStatus.NOT_EVALUATED,
        runtime_contract=_pass_or_fail(runtime_result),
        overall_status=overall,
        issues=issues,
        validation=context_result,
    )


def diagnostics_from_payload(payload: Mapping[str, Any]) -> Pack07RuntimeDiagnostics:
    """Build diagnostics from an analyze-shaped payload."""
    context = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(payload),
        payload,
    )
    return build_pack07_diagnostics(context)
