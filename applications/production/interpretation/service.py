"""Multi-domain interpretation service — Sprint 4 composition entry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.interpretation_engine_v2.strength.runtime.service import (
    StrengthInterpretationService,
)

from applications.production.engine_runner import EnginePipelineOutput
from applications.production.interpretation.contracts import (
    DomainInterpretationResult,
    DomainStatus,
    ExecutiveConsultingResult,
    IntegratedInterpretationContext,
)
from applications.production.interpretation.executive_composer import (
    ExecutiveConsultingComposer,
)
from applications.production.interpretation.integrator import CrossDomainIntegrator
from applications.production.interpretation.pattern_composer import (
    PatternDomainComposer,
    build_pattern_published_facts,
)
from applications.production.interpretation.strength_composer import StrengthDomainComposer
from applications.production.interpretation.ten_gods_composer import (
    TenGodsDomainComposer,
    build_ten_gods_published_facts,
)
from applications.production.interpretation.useful_god_composer import (
    UsefulGodDomainComposer,
    build_useful_god_published_facts,
)


@dataclass(slots=True)
class MultiDomainCompositionResult:
    """Full multi-domain composition outcome."""

    domains: dict[str, DomainInterpretationResult]
    integrated: IntegratedInterpretationContext
    executive: ExecutiveConsultingResult
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def customer_domain_payloads(self) -> dict[str, dict[str, Any]]:
        """Customer-safe domain dictionaries."""
        return {
            name: result.to_customer_dict()
            for name, result in self.domains.items()
        }


class MultiDomainInterpretationService:
    """Orchestrate domain composers → integration → executive consulting."""

    def __init__(
        self,
        *,
        strength_service: StrengthInterpretationService | None = None,
    ) -> None:
        self._strength = StrengthDomainComposer(strength_service=strength_service)
        self._ten_gods = TenGodsDomainComposer()
        self._pattern = PatternDomainComposer()
        self._useful_god = UsefulGodDomainComposer()
        self._integrator = CrossDomainIntegrator()
        self._executive = ExecutiveConsultingComposer()

    def compose(
        self,
        *,
        case_id: str,
        engine_output: EnginePipelineOutput,
    ) -> MultiDomainCompositionResult:
        """Compose all in-scope domains from engine pipeline output."""
        strength = self._strength.compose(
            case_id=case_id,
            strength_result=engine_output.strength_result,
            strength_context=engine_output.strength_context,
        )
        ten_gods = self._ten_gods.compose(
            build_ten_gods_published_facts(engine_output.ten_gods)
        )
        pattern = self._pattern.compose(
            build_pattern_published_facts(engine_output.analysis.pattern)
        )
        useful_god = self._useful_god.compose(
            build_useful_god_published_facts(engine_output.analysis.useful_god)
        )

        domains = {
            "strength": strength,
            "ten_gods": ten_gods,
            "pattern": pattern,
            "useful_god": useful_god,
        }
        integrated = self._integrator.integrate(domains)
        executive = self._executive.compose(integrated)

        diagnostics = {
            "domain_statuses": {
                name: result.status.value for name, result in domains.items()
            },
            "knowledge_statuses": {
                name: result.knowledge_status.value for name, result in domains.items()
            },
            "integrated": integrated.to_diagnostics_dict(),
            "executive": dict(executive.diagnostics),
        }
        return MultiDomainCompositionResult(
            domains=domains,
            integrated=integrated,
            executive=executive,
            diagnostics=diagnostics,
        )

    @staticmethod
    def section_status_for(result: DomainInterpretationResult) -> DomainStatus:
        """Expose domain status helper."""
        return result.status
