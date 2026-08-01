"""Luck Interpreter service — orchestration for luck business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.luck.constants import (
    LUCK_INTERPRETER_ID,
    LUCK_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.extractor import (
    LuckFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.models import (
    LuckComponentResult,
    LuckInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.luck.rule_engine import (
    LuckInterpretationRuleEngine,
    LuckRuleEngineResult,
)

logger = logging.getLogger(__name__)


class LuckInterpreterService:
    """Build LuckInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 dai_van + luck score + interpretation rules via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: LuckFactExtractor | None = None,
        rule_engine: LuckInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or LuckFactExtractor()
        self.rule_engine = rule_engine or LuckInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> LuckInterpretationSection | None:
        """Interpret luck from context.final_result.

        Returns None when FinalResult has no luck payload.
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "luck_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{LUCK_INTERPRETER_ID}_{context.id}"

        typed = LuckInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=LUCK_SECTION_TYPE,
                title_ref="luck.title",
                interpreter_id=LUCK_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("luck_interpreter_ok",),
                attributes={},
            ),
            dayun=engine_result.dayun,
            liunian=engine_result.liunian,
            liuyue=engine_result.liuyue,
            interactions=engine_result.interactions,
            luck_score=engine_result.luck_score,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("luck_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=LUCK_SECTION_TYPE,
            title_ref="luck.title",
            interpreter_id=LUCK_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("luck_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return LuckInterpretationSection(
            section=section,
            dayun=typed.dayun,
            liunian=typed.liunian,
            liuyue=typed.liuyue,
            interactions=typed.interactions,
            luck_score=typed.luck_score,
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
    ) -> LuckInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="luck_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: LuckRuleEngineResult,
    ) -> dict[str, LuckComponentResult]:
        """Map engine results into Dayun/Liunian/Liuyue/Interaction components."""
        return {
            "dayun": LuckComponentResult(
                component_id="dayun",
                value=",".join(
                    item.label or item.item_id for item in engine_result.dayun
                ),
                score=sum(item.score for item in engine_result.dayun),
                count=len(engine_result.dayun),
                items=engine_result.dayun,
                description="Dayun (Dai Van)",
            ),
            "liunian": LuckComponentResult(
                component_id="liunian",
                value=",".join(
                    item.label or item.item_id for item in engine_result.liunian
                ),
                score=sum(item.score for item in engine_result.liunian),
                count=len(engine_result.liunian),
                items=engine_result.liunian,
                description="Liunian (Luu Nien)",
            ),
            "liuyue": LuckComponentResult(
                component_id="liuyue",
                value=",".join(
                    item.label or item.item_id for item in engine_result.liuyue
                ),
                score=sum(item.score for item in engine_result.liuyue),
                count=len(engine_result.liuyue),
                items=engine_result.liuyue,
                description="Liuyue (Luu Nguyet)",
            ),
            "interaction": LuckComponentResult(
                component_id="interaction",
                value=",".join(
                    item.label or item.item_id for item in engine_result.interactions
                ),
                score=sum(item.score for item in engine_result.interactions),
                count=len(engine_result.interactions),
                items=engine_result.interactions,
                description="Luck Interaction",
            ),
        }
