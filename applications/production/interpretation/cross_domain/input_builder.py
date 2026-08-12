"""Build CrossDomainReasoningInput from engine + domain composition."""

from __future__ import annotations

from applications.production.engine_runner import EnginePipelineOutput
from applications.production.interpretation.contracts import (
    DomainInterpretationResult,
    DomainStatus,
)
from applications.production.interpretation.cross_domain.models import (
    CrossDomainReasoningInput,
    QuestionContext,
)
from applications.production.interpretation.pattern_composer import (
    build_pattern_published_facts,
)
from applications.production.interpretation.ten_gods_composer import (
    build_ten_gods_published_facts,
)
from applications.production.interpretation.useful_god_composer import (
    build_useful_god_published_facts,
)


def build_reasoning_input(
    engine_output: EnginePipelineOutput,
    domains: dict[str, DomainInterpretationResult],
    *,
    question_context: QuestionContext = QuestionContext.GENERAL,
) -> CrossDomainReasoningInput:
    """Assemble canonical CDR input from published engine facts."""
    strength_result = engine_output.strength_result
    pattern_facts = build_pattern_published_facts(engine_output.analysis.pattern)
    tg_facts = build_ten_gods_published_facts(engine_output.ten_gods)
    ug_facts = build_useful_god_published_facts(engine_output.analysis.useful_god)

    missing: list[str] = []
    conclusions: dict[str, str] = {}
    for name, result in domains.items():
        if result.status in {DomainStatus.NOT_AVAILABLE, DomainStatus.INSUFFICIENT}:
            missing.append(name)
        else:
            conclusions[name] = result.conclusion

    families = sorted(tg_facts.family_presence.keys())

    return CrossDomainReasoningInput(
        strength_level=str(strength_result.strength_level or ""),
        strength_score=float(strength_result.strength_score or 0.0),
        pattern_key=pattern_facts.pattern_key,
        pattern_label=pattern_facts.pattern_label,
        pattern_than_vuong_nhuoc=pattern_facts.than_vuong_nhuoc,
        tong_cach=pattern_facts.tong_cach,
        ten_gods_primary=list(tg_facts.primary_labels),
        ten_gods_secondary=list(tg_facts.secondary_labels),
        ten_gods_families=families,
        useful_god=ug_facts.useful_god,
        useful_reasoning=ug_facts.reasoning or "",
        favorable=list(ug_facts.favorable_gods),
        unfavorable=list(ug_facts.unfavorable_gods),
        domain_conclusions=conclusions,
        missing_domains=missing,
        question_context=question_context,
        versions={
            "strength": "v2",
            "ten_gods": "1.0",
            "pattern": "1.0",
            "useful_god": "1.0",
        },
    )
