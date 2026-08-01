"""Ten Gods Interpreter service — orchestration for ten-gods business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.constants import (
    TEN_GODS_INTERPRETER_ID,
    TEN_GODS_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.extractor import (
    TenGodsFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.models import (
    TenGodsComponentResult,
    TenGodsInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.rule_engine import (
    TenGodsInterpretationRuleEngine,
    TenGodsRuleEngineResult,
)

logger = logging.getLogger(__name__)


class TenGodsInterpreterService:
    """Build TenGodsInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 thap_than + score + interpretation rules via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: TenGodsFactExtractor | None = None,
        rule_engine: TenGodsInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or TenGodsFactExtractor()
        self.rule_engine = rule_engine or TenGodsInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> TenGodsInterpretationSection | None:
        """Interpret Ten Gods from context.final_result.

        Returns None when FinalResult has no ten-gods payload.
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "ten_gods_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{TEN_GODS_INTERPRETER_ID}_{context.id}"

        typed = TenGodsInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=TEN_GODS_SECTION_TYPE,
                title_ref="ten_gods.title",
                interpreter_id=TEN_GODS_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("ten_gods_interpreter_ok",),
                attributes={},
            ),
            ten_gods=engine_result.ten_gods,
            distribution=engine_result.distribution,
            strength=engine_result.strength,
            interactions=engine_result.interactions,
            ten_gods_score=engine_result.ten_gods_score,
            dominant_god=engine_result.dominant_god,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("ten_gods_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=TEN_GODS_SECTION_TYPE,
            title_ref="ten_gods.title",
            interpreter_id=TEN_GODS_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("ten_gods_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return TenGodsInterpretationSection(
            section=section,
            ten_gods=typed.ten_gods,
            distribution=typed.distribution,
            strength=typed.strength,
            interactions=typed.interactions,
            ten_gods_score=typed.ten_gods_score,
            dominant_god=typed.dominant_god,
            components=typed.components,
            matched_rules=typed.matched_rules,
            confidence=typed.confidence,
            reasoning=typed.reasoning,
            source_final_result_id=typed.source_final_result_id,
            success=typed.success,
            messages=typed.messages,
        )

    def interpret_final_result(
        self,
        final_result: FinalResult,
        *,
        context_id: str = "adhoc",
    ) -> TenGodsInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="ten_gods_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: TenGodsRuleEngineResult,
    ) -> dict[str, TenGodsComponentResult]:
        """Map engine results into TenGods/Distribution/Strength/Interaction."""
        return {
            "ten_gods": TenGodsComponentResult(
                component_id="ten_gods",
                value=",".join(item.label or item.item_id for item in engine_result.ten_gods),
                score=sum(item.score for item in engine_result.ten_gods),
                count=len(engine_result.ten_gods),
                items=engine_result.ten_gods,
                description="Ten Gods (Thap Than)",
            ),
            "distribution": TenGodsComponentResult(
                component_id="distribution",
                value=engine_result.dominant_god,
                score=float(sum(item.count for item in engine_result.distribution)),
                count=len(engine_result.distribution),
                items=engine_result.distribution,
                description="Ten Gods Distribution",
                attributes={"dominant_god": engine_result.dominant_god},
            ),
            "strength": TenGodsComponentResult(
                component_id="strength",
                value=",".join(
                    item.label or item.item_id for item in engine_result.strength
                ),
                score=sum(item.score for item in engine_result.strength),
                count=len(engine_result.strength),
                items=engine_result.strength,
                description="Ten Gods Strength Contribution",
            ),
            "interaction": TenGodsComponentResult(
                component_id="interaction",
                value=",".join(
                    item.label or item.item_id for item in engine_result.interactions
                ),
                score=sum(item.score for item in engine_result.interactions),
                count=len(engine_result.interactions),
                items=engine_result.interactions,
                description="Ten Gods Interaction",
            ),
        }
