"""Combination Interpreter service — orchestration for combination business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.combination.constants import (
    COMBINATION_INTERPRETER_ID,
    COMBINATION_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.extractor import (
    CombinationFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.models import (
    CombinationComponentResult,
    CombinationInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.combination.rule_engine import (
    CombinationInterpretationRuleEngine,
    CombinationRuleEngineResult,
)

logger = logging.getLogger(__name__)


class CombinationInterpreterService:
    """Build CombinationInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 quan_he + combination_score rules via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: CombinationFactExtractor | None = None,
        rule_engine: CombinationInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or CombinationFactExtractor()
        self.rule_engine = rule_engine or CombinationInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> CombinationInterpretationSection | None:
        """Interpret combination from context.final_result.

        Returns None when FinalResult has no combination payload.
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "combination_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{COMBINATION_INTERPRETER_ID}_{context.id}"

        typed = CombinationInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=COMBINATION_SECTION_TYPE,
                title_ref="combination.title",
                interpreter_id=COMBINATION_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("combination_interpreter_ok",),
                attributes={},
            ),
            stem_combinations=engine_result.stem_combinations,
            branch_combinations=engine_result.branch_combinations,
            transformations=engine_result.transformations,
            combination_score=engine_result.combination_score,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("combination_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=COMBINATION_SECTION_TYPE,
            title_ref="combination.title",
            interpreter_id=COMBINATION_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("combination_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return CombinationInterpretationSection(
            section=section,
            stem_combinations=typed.stem_combinations,
            branch_combinations=typed.branch_combinations,
            transformations=typed.transformations,
            combination_score=typed.combination_score,
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
    ) -> CombinationInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="combination_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: CombinationRuleEngineResult,
    ) -> dict[str, CombinationComponentResult]:
        """Map engine results into Stem/Branch/Transform/Score components."""
        stem_score = sum(item.score for item in engine_result.stem_combinations)
        branch_score = sum(item.score for item in engine_result.branch_combinations)
        transform_score = sum(item.score for item in engine_result.transformations)
        return {
            "stem_combination": CombinationComponentResult(
                component_id="stem_combination",
                value=",".join(
                    item.item_id for item in engine_result.stem_combinations
                ),
                score=stem_score,
                count=len(engine_result.stem_combinations),
                items=engine_result.stem_combinations,
                description="Stem Combination (Thiên Can hợp)",
            ),
            "branch_combination": CombinationComponentResult(
                component_id="branch_combination",
                value=",".join(
                    item.item_id for item in engine_result.branch_combinations
                ),
                score=branch_score,
                count=len(engine_result.branch_combinations),
                items=engine_result.branch_combinations,
                description="Branch Combination (Địa Chi hợp)",
            ),
            "transformation": CombinationComponentResult(
                component_id="transformation",
                value=",".join(item.item_id for item in engine_result.transformations),
                score=transform_score,
                count=len(engine_result.transformations),
                items=engine_result.transformations,
                description="Transformation (Hợp hóa)",
            ),
            "combination_score": CombinationComponentResult(
                component_id="combination_score",
                value=str(engine_result.combination_score),
                score=engine_result.combination_score,
                count=1,
                items=(),
                description="Combination Score from Pack 01 score rules",
                attributes={"matched_rules": list(engine_result.matched_rule_ids)},
            ),
        }
