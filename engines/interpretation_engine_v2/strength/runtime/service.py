"""Strength interpretation runtime service."""

from __future__ import annotations

import logging
from pathlib import Path

from engines.interpretation_engine_v2.strength.composer.composer import SentenceComposer
from engines.interpretation_engine_v2.strength.contracts.models import (
    AudienceMode,
    InterpretationMeta,
    InterpretationResult,
    PublishedStrengthFacts,
    ReasoningInput,
)
from engines.interpretation_engine_v2.strength.knowledge_loader.loader import KnowledgeCatalogLoader
from engines.interpretation_engine_v2.strength.narrative.planner import NarrativePlanner
from engines.interpretation_engine_v2.strength.reasoner.engine import StrengthReasoner
from engines.interpretation_engine_v2.strength.runtime.case_0001 import load_case_0001_facts
from engines.interpretation_engine_v2.strength.selector.selector import KnowledgeSelector
from engines.interpretation_engine_v2.strength.validators.input_validator import (
    InputValidator,
)

logger = logging.getLogger(__name__)


class StrengthInterpretationService:
    """Orchestrate Strength interpretation runtime pipeline."""

    def __init__(
        self,
        catalog_loader: KnowledgeCatalogLoader | None = None,
        selector: KnowledgeSelector | None = None,
        reasoner: StrengthReasoner | None = None,
        planner: NarrativePlanner | None = None,
        composer: SentenceComposer | None = None,
        validator: InputValidator | None = None,
    ) -> None:
        self._loader = catalog_loader or KnowledgeCatalogLoader()
        self._selector = selector or KnowledgeSelector()
        self._reasoner = reasoner or StrengthReasoner()
        self._planner = planner or NarrativePlanner()
        self._composer = composer or SentenceComposer()
        self._validator = validator or InputValidator()
        self._units = self._loader.load_all()
        self._units_by_id = {unit.knowledge_id: unit for unit in self._units}

    @property
    def units(self) -> list:
        """Loaded catalog units."""
        return list(self._units)

    def interpret(
        self,
        published: PublishedStrengthFacts,
        audience: AudienceMode = AudienceMode.CUSTOMER,
    ) -> InterpretationResult:
        """Run full pipeline for published Strength facts."""
        self._validator.validate_published(published)
        candidates = self._selector.select_candidates(self._units, published, audience)
        reasoning_input = ReasoningInput(
            published=published,
            candidates=candidates,
            audience=audience,
        )
        plan = self._reasoner.build_plan(reasoning_input)
        plan.meta["confidence_band"] = published.confidence_band
        plan = self._planner.finalize(plan, self._units_by_id)

        validation_sections = self._composer.compose_validation(plan, self._units_by_id)
        customer_sections = self._composer.compose_customer(plan, self._units_by_id)

        return InterpretationResult(
            meta=InterpretationMeta(
                case_id=published.case_id,
                catalog_version="1.0.0",
                reasoning_policy_version="1.0.0",
                knowledge_version="1.0.0",
            ),
            narrative_plan=plan,
            validation_mode=validation_sections,
            customer_mode=customer_sections,
            diagnostics=plan.diagnostics,
        )

    def run_case_0001(self, evidence_path: Path | None = None) -> InterpretationResult:
        """Run complete runtime for CASE-0001."""
        published = load_case_0001_facts(evidence_path)
        logger.info("Running CASE-0001 Strength interpretation runtime")
        return self.interpret(
            published=published,
            audience=AudienceMode.CUSTOMER,
        )
