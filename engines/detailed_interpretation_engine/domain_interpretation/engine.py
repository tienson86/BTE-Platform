"""Domain Interpretation Engine. Explains ranked evidence; does not rerank."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domain_interpretation.evaluate import (
    domain_order,
    evaluate_main_domains,
    evaluate_support_domains,
)
from engines.detailed_interpretation_engine.domain_interpretation.facts import collect_domain_facts
from engines.detailed_interpretation_engine.domain_interpretation.graph import build_domain_graph
from engines.detailed_interpretation_engine.domains import (
    AuthorityResult,
    CareerResult,
    DomainSection,
    LegacyResult,
    RelationshipResult,
    VitalityResult,
    WealthResult,
)
from engines.detailed_interpretation_engine.enums import DomainState, EvaluationStatus
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_domain_interpretation_result,
    validate_pack07_context,
)


def evaluate_domain_interpretation(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> DomainSection:
    """Convert Evidence Priority plus MC-01 profiles into natal domain objects."""
    ep = context.runtime.interpretation.evidence_priority
    if not ep.findings:
        return DomainSection()
    facts = collect_domain_facts(context, payload)
    mains = evaluate_main_domains(facts)
    supporting = evaluate_support_domains(facts)
    return DomainSection(
        authority=AuthorityResult(natal=mains["authority"]),
        career=CareerResult(natal=mains["career"]),
        wealth=WealthResult(natal=mains["wealth"]),
        relationship=RelationshipResult(natal=mains["relationship"]),
        legacy=LegacyResult(natal=mains["legacy"]),
        vitality=VitalityResult(natal=mains["vitality"]),
        supporting=supporting,
        order=domain_order(facts),
        graph=build_domain_graph(facts, mains, supporting),
    )


def bind_domain_interpretation(
    context: CanonicalAnalysisContext,
    section: DomainSection,
) -> CanonicalAnalysisContext:
    """Publish DomainSection onto CanonicalRuntimeResult.domains."""
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, domains=section, metadata=cleared)
    serialized = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(serialized))
    runtime = replace(runtime, metadata=metadata)
    status = _section_status(section)
    domain_ctx = replace(context.domain, status=status, domains=section)
    return replace(context, runtime=runtime, domain=domain_ctx)


def interpret_and_bind_domain_interpretation(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context, evaluate domains, bind the canonical result."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    section = evaluate_domain_interpretation(context, payload)
    if _section_status(section) is not EvaluationStatus.NOT_EVALUATED:
        assert_valid(
            validate_domain_interpretation_result(
                section,
                context=context,
            )
        )
    return bind_domain_interpretation(context, section)


def _section_status(section: DomainSection) -> EvaluationStatus:
    states = [
        section.authority.natal.state,
        section.career.natal.state,
        section.wealth.natal.state,
        section.relationship.natal.state,
        section.legacy.natal.state,
        section.vitality.natal.state,
    ]
    if all(item is DomainState.NOT_EVALUATED for item in states):
        return EvaluationStatus.NOT_EVALUATED
    if any(item is DomainState.NOT_EVALUATED for item in states):
        return EvaluationStatus.PARTIALLY_RESOLVED
    if all(item is DomainState.UNRESOLVED for item in states):
        return EvaluationStatus.UNRESOLVED
    return EvaluationStatus.RESOLVED
