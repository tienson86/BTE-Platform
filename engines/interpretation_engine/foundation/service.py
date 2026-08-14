"""Interpretation Foundation service — Sprint A entry point."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation.builders.analysis_context_builder import (
    build_canonical_analysis_context,
)
from engines.interpretation_engine.foundation.builders.engine_sources import EngineSources
from engines.interpretation_engine.foundation.builders.interpretation_facts_builder import (
    InterpretationFactsBundle,
    build_interpretation_facts,
)
from engines.interpretation_engine.foundation.canonical_context import CanonicalAnalysisContext
from engines.interpretation_engine.foundation.results.domain_result import (
    FoundationDomainInterpretationResult,
    stub_domain_result,
)
from engines.interpretation_engine.foundation.status import DataAvailability
from engines.interpretation_engine.foundation.validation.readiness_validator import (
    InterpretationReadiness,
    evaluate_interpretation_readiness,
)
from engines.interpretation_engine.foundation.validation.score_truth_guard import (
    ScoreTruthGuardResult,
    validate_score_not_used_as_truth,
)


@dataclass(frozen=True, slots=True)
class InterpretationFoundationBundle:
    """Complete Sprint A foundation output for one chart."""

    context: CanonicalAnalysisContext
    facts: InterpretationFactsBundle
    readiness: InterpretationReadiness
    score_guard: ScoreTruthGuardResult
    domain_results: dict[str, FoundationDomainInterpretationResult]
    diagnostics: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize foundation bundle for trace / API."""
        return {
            "context": self.context.to_dict(),
            "facts": self.facts.to_dict(),
            "readiness": self.readiness.to_dict(),
            "score_guard": self.score_guard.to_dict(),
            "domain_results": {
                key: value.to_dict() for key, value in self.domain_results.items()
            },
            "diagnostics": list(self.diagnostics),
        }


def build_interpretation_foundation(
    *,
    payload: Mapping[str, Any] | None = None,
    analysis: Any | None = None,
    calendar: Mapping[str, Any] | None = None,
    luck: Mapping[str, Any] | None = None,
    five_elements: Mapping[str, Any] | None = None,
    feng_shui: Mapping[str, Any] | None = None,
    identity: Mapping[str, Any] | None = None,
    engine_sources: EngineSources | None = None,
    pattern_dieu_hau: str = "",
) -> InterpretationFoundationBundle:
    """Build canonical context, domain facts, readiness, and Sprint B stubs."""
    context = build_canonical_analysis_context(
        payload=payload,
        analysis=analysis,
        calendar=calendar,
        luck=luck,
        five_elements=five_elements,
        feng_shui=feng_shui,
        identity=identity,
        engine_sources=engine_sources,
    )
    facts = build_interpretation_facts(
        context,
        luck_payload=luck,
        engine_sources=engine_sources,
        pattern_dieu_hau=pattern_dieu_hau,
    )
    readiness = evaluate_interpretation_readiness(facts)
    score_payload = _score_payload(payload, analysis)
    score_guard = validate_score_not_used_as_truth(context, facts, score_payload=score_payload)

    all_diagnostics = _collect_diagnostics(facts, score_guard)
    domain_results = _stub_domain_results(facts)

    return InterpretationFoundationBundle(
        context=context,
        facts=facts,
        readiness=readiness,
        score_guard=score_guard,
        domain_results=domain_results,
        diagnostics=all_diagnostics,
    )


def _score_payload(
    payload: Mapping[str, Any] | None,
    analysis: Any | None,
) -> dict[str, Any]:
    """Extract score dict from payload or analysis."""
    if payload is not None:
        score = payload.get("score")
        return dict(score) if isinstance(score, Mapping) else {}
    if analysis is not None and hasattr(analysis, "score") and analysis.score is not None:
        if hasattr(analysis.score, "to_dict"):
            return dict(analysis.score.to_dict())
    return {}


def _collect_diagnostics(
    facts: InterpretationFactsBundle,
    score_guard: ScoreTruthGuardResult,
) -> tuple[str, ...]:
    """Merge domain and guard diagnostics."""
    collected: list[str] = []
    for domain in (
        facts.strength,
        facts.pattern,
        facts.useful_god,
        facts.ten_gods,
        facts.shensha,
        facts.luck,
        facts.temperature,
        facts.five_elements,
    ):
        collected.extend(domain.diagnostics)
    collected.extend(score_guard.violations)
    return tuple(dict.fromkeys(item for item in collected if item))


def _stub_domain_results(
    facts: InterpretationFactsBundle,
) -> dict[str, FoundationDomainInterpretationResult]:
    """Create minimal domain result shells for Sprint B pipeline."""
    mapping = {
        "strength": facts.strength.status,
        "pattern": facts.pattern.status,
        "useful_god": facts.useful_god.status,
        "ten_gods": facts.ten_gods.status,
        "shensha": facts.shensha.status,
        "luck": facts.luck.status,
        "temperature": facts.temperature.status,
    }
    return {
        domain: stub_domain_result(domain, status=status)
        for domain, status in mapping.items()
    }
