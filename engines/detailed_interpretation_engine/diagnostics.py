"""Development-only Pack 07 runtime diagnostics. Not customer UI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domains import DomainSection
from engines.detailed_interpretation_engine.enums import (
    DiagnosticStatus,
    DomainState,
    EvaluationStatus,
    ValidationStatus,
)
from engines.detailed_interpretation_engine.factories import (
    api_model_from_runtime,
    consulting_model_from_runtime,
    export_model_from_runtime,
)
from engines.detailed_interpretation_engine.mc01 import attach_mc01_reference
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods
from engines.detailed_interpretation_engine.shen_sha.engine import interpret_and_bind_shen_sha
from engines.detailed_interpretation_engine.domain_interpretation.engine import (
    interpret_and_bind_domain_interpretation,
)
from engines.detailed_interpretation_engine.luck_activation.engine import (
    interpret_and_bind_luck_activation,
)
from engines.detailed_interpretation_engine.luck_interaction.engine import (
    interpret_and_bind_luck_interaction,
)
from engines.detailed_interpretation_engine.temporal_activation.engine import (
    interpret_and_bind_temporal_activation,
)
from engines.detailed_interpretation_engine.life_optimization.engine import (
    interpret_and_bind_life_optimization,
)
from engines.detailed_interpretation_engine.narrative_composer.engine import (
    interpret_and_bind_narrative,
)
from engines.detailed_interpretation_engine.evidence_priority.engine import (
    interpret_and_bind_evidence_priority,
)
from engines.detailed_interpretation_engine.validation import ValidationIssue, ValidationResult
from engines.detailed_interpretation_engine.validators import (
    validate_api_projection,
    validate_canonical_runtime,
    validate_consulting_projection,
    validate_domain_interpretation_result,
    validate_evidence_priority_result,
    validate_export_projection,
    validate_luck_activation_result,
    validate_luck_interaction_result,
    validate_pack07_context,
    validate_temporal_activation_result,
    validate_life_optimization_result,
    validate_narrative_result,
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
    shen_sha_ecosystem: DiagnosticStatus
    evidence_priority: DiagnosticStatus
    domains: DiagnosticStatus
    luck: DiagnosticStatus
    luck_interaction: DiagnosticStatus
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
            "shen_sha_ecosystem": self.shen_sha_ecosystem.value,
            "evidence_priority": self.evidence_priority.value,
            "domains": self.domains.value,
            "luck": self.luck.value,
            "luck_interaction": self.luck_interaction.value,
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


def _domains_status(section: DomainSection) -> DiagnosticStatus:
    states = (
        section.authority.natal.state,
        section.career.natal.state,
        section.wealth.natal.state,
        section.relationship.natal.state,
        section.legacy.natal.state,
        section.vitality.natal.state,
    )
    if all(item is DomainState.NOT_EVALUATED for item in states):
        return DiagnosticStatus.NOT_EVALUATED
    if any(item is DomainState.NOT_EVALUATED for item in states):
        return DiagnosticStatus.PARTIAL
    return DiagnosticStatus.PASS


def _luck_status(result: Any) -> DiagnosticStatus:
    empty = not result.items
    return _layer_status(result.status, empty)


def _luck_interaction_status(result: Any) -> DiagnosticStatus:
    empty = not result.findings and not result.graph.edges
    return _layer_status(result.status, empty)


def _temporal_status(result: Any) -> DiagnosticStatus:
    empty = not result.evaluated_layers and not result.domain_results
    if result.state is EvaluationStatus.NOT_EVALUATED and empty:
        return DiagnosticStatus.NOT_EVALUATED
    return _layer_status(result.state, empty)


def _optimization_status(result: Any) -> DiagnosticStatus:
    empty = not result.actions and not result.top_priorities
    if result.state is EvaluationStatus.NOT_EVALUATED and empty:
        return DiagnosticStatus.NOT_EVALUATED
    return _layer_status(result.state, empty)


def _narrative_status(section: Any) -> DiagnosticStatus:
    result = getattr(section, "result", section)
    empty = not getattr(result, "executive_summary", "") and not getattr(result, "blocks", ())
    status = getattr(result, "status", EvaluationStatus.NOT_EVALUATED)
    if status is EvaluationStatus.NOT_EVALUATED and empty:
        return DiagnosticStatus.NOT_EVALUATED
    return _layer_status(status, empty)


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
        + validate_evidence_priority_result(
            context.runtime.interpretation.evidence_priority,
            context=context,
        ).issues
        + validate_domain_interpretation_result(
            context.runtime.domains,
            context=context,
        ).issues
        + validate_luck_activation_result(
            context.runtime.temporal.luck_activation,
            context=context,
        ).issues
        + validate_luck_interaction_result(
            context.runtime.temporal.luck_interaction,
            context=context,
        ).issues
        + validate_temporal_activation_result(
            context.runtime.temporal.temporal_activation,
            context=context,
        ).issues
        + validate_life_optimization_result(
            context.runtime.optimization,
            context=context,
        ).issues
        + validate_narrative_result(
            context.runtime.narrative.result,
            context=context,
        ).issues
    )
    issues = context_result.issues + extra
    mc01 = (
        DiagnosticStatus.PASS
        if context.interpretation.mc01.mingju_result_id
        and context.interpretation.mc01.content_hash
        else DiagnosticStatus.NOT_BOUND
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
    shen = context.runtime.interpretation.shen_sha
    shen_sha_status = _layer_status(shen.status, not shen.individual.items)
    shen_eco_status = _layer_status(
        shen.ecosystem.state, not shen.ecosystem.clusters and not shen.ecosystem.trace_ids
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
        shen_sha=shen_sha_status,
        shen_sha_ecosystem=shen_eco_status,
        evidence_priority=_layer_status(
            context.runtime.interpretation.evidence_priority.status,
            not context.runtime.interpretation.evidence_priority.findings
            and not context.runtime.interpretation.evidence_priority.dominant_evidence,
        ),
        domains=_domains_status(context.runtime.domains),
        luck=_luck_status(context.runtime.temporal.luck_activation),
        luck_interaction=_luck_interaction_status(context.runtime.temporal.luck_interaction),
        temporal=_temporal_status(context.runtime.temporal.temporal_activation),
        optimization=_optimization_status(context.runtime.optimization),
        narrative=_narrative_status(context.runtime.narrative),
        runtime_contract=_pass_or_fail(runtime_result),
        overall_status=overall,
        issues=issues,
        validation=context_result,
    )


def diagnostics_from_payload(payload: Mapping[str, Any]) -> Pack07RuntimeDiagnostics:
    """Build diagnostics from an analyze-shaped payload."""
    bound = dict(payload)
    attach_mc01_reference(bound)
    context = interpret_and_bind_narrative(
        interpret_and_bind_life_optimization(
            interpret_and_bind_temporal_activation(
                interpret_and_bind_luck_interaction(
                    interpret_and_bind_luck_activation(
                        interpret_and_bind_domain_interpretation(
                            interpret_and_bind_evidence_priority(
                                interpret_and_bind_shen_sha(
                                    interpret_and_bind_ten_gods(
                                        build_canonical_analysis_context_from_payload(bound),
                                        bound,
                                    ),
                                    bound,
                                ),
                                bound,
                            ),
                            bound,
                        ),
                        bound,
                    )
                ),
                bound,
            ),
            bound,
        ),
        bound,
    )
    return build_pack07_diagnostics(context)
