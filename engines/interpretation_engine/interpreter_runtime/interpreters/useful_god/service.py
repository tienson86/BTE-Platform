"""Useful God Interpreter service — orchestration for useful-god business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.constants import (
    USEFUL_GOD_INTERPRETER_ID,
    USEFUL_GOD_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.extractor import (
    UsefulGodFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.models import (
    UsefulGodComponentResult,
    UsefulGodInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.rule_engine import (
    UsefulGodInterpretationRuleEngine,
    UsefulGodRuleEngineResult,
)

logger = logging.getLogger(__name__)


class UsefulGodInterpreterService:
    """Build UsefulGodInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 ``database/13_useful_god`` via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: UsefulGodFactExtractor | None = None,
        rule_engine: UsefulGodInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or UsefulGodFactExtractor()
        self.rule_engine = rule_engine or UsefulGodInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> UsefulGodInterpretationSection | None:
        """Interpret useful god from context.final_result.

        Returns None when FinalResult has no useful-god / related payload
        (caller may fall back to empty skeleton section).
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "useful_god_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{USEFUL_GOD_INTERPRETER_ID}_{context.id}"

        typed = UsefulGodInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=USEFUL_GOD_SECTION_TYPE,
                title_ref="useful_god.title",
                interpreter_id=USEFUL_GOD_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("useful_god_interpreter_ok",),
                attributes={},
            ),
            useful_god=engine_result.useful_god,
            favorable_gods=engine_result.favorable_gods,
            unfavorable_gods=engine_result.unfavorable_gods,
            supporting_elements=engine_result.supporting_elements,
            score=engine_result.score,
            priority=engine_result.priority,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            recommendations=engine_result.recommendations,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("useful_god_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=USEFUL_GOD_SECTION_TYPE,
            title_ref="useful_god.title",
            interpreter_id=USEFUL_GOD_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("useful_god_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return UsefulGodInterpretationSection(
            section=section,
            useful_god=typed.useful_god,
            favorable_gods=typed.favorable_gods,
            unfavorable_gods=typed.unfavorable_gods,
            supporting_elements=typed.supporting_elements,
            score=typed.score,
            priority=typed.priority,
            components=typed.components,
            matched_rules=typed.matched_rules,
            recommendations=typed.recommendations,
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
    ) -> UsefulGodInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="useful_god_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: UsefulGodRuleEngineResult,
    ) -> dict[str, UsefulGodComponentResult]:
        """Map engine results into Useful/Favorable/Unfavorable/Supporting components."""
        winner = engine_result.winner
        return {
            "useful_god": UsefulGodComponentResult(
                component_id="useful_god",
                value=engine_result.useful_god,
                values=(engine_result.useful_god,) if engine_result.useful_god else (),
                score=engine_result.score,
                priority=engine_result.priority,
                rule_id=None if winner is None else winner.rule_id,
                description=engine_result.reasoning,
            ),
            "favorable_god": UsefulGodComponentResult(
                component_id="favorable_god",
                value=",".join(engine_result.favorable_gods),
                values=engine_result.favorable_gods,
                score=engine_result.score,
                priority=engine_result.priority,
                rule_id=None if winner is None else winner.rule_id,
                description="Hỷ thần / Favorable God",
            ),
            "unfavorable_god": UsefulGodComponentResult(
                component_id="unfavorable_god",
                value=",".join(engine_result.unfavorable_gods),
                values=engine_result.unfavorable_gods,
                score=engine_result.score,
                priority=engine_result.priority,
                rule_id=None if winner is None else winner.rule_id,
                description="Kỵ thần / Unfavorable God",
            ),
            "supporting_elements": UsefulGodComponentResult(
                component_id="supporting_elements",
                value=",".join(engine_result.supporting_elements),
                values=engine_result.supporting_elements,
                score=engine_result.score,
                priority=engine_result.priority,
                rule_id=None if winner is None else winner.rule_id,
                description="Supporting elements for Useful God",
            ),
        }
