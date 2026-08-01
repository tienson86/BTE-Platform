"""Conflict Interpreter service — orchestration for conflict business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.constants import (
    CONFLICT_INTERPRETER_ID,
    CONFLICT_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.extractor import (
    ConflictFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.models import (
    ConflictComponentResult,
    ConflictInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.rule_engine import (
    ConflictInterpretationRuleEngine,
    ConflictRuleEngineResult,
)

logger = logging.getLogger(__name__)


class ConflictInterpreterService:
    """Build ConflictInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 quan_he + clash_score rules via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: ConflictFactExtractor | None = None,
        rule_engine: ConflictInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or ConflictFactExtractor()
        self.rule_engine = rule_engine or ConflictInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> ConflictInterpretationSection | None:
        """Interpret conflict from context.final_result.

        Returns None when FinalResult has no conflict payload.
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "conflict_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{CONFLICT_INTERPRETER_ID}_{context.id}"

        typed = ConflictInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=CONFLICT_SECTION_TYPE,
                title_ref="conflict.title",
                interpreter_id=CONFLICT_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("conflict_interpreter_ok",),
                attributes={},
            ),
            clashes=engine_result.clashes,
            punishments=engine_result.punishments,
            harms=engine_result.harms,
            destructions=engine_result.destructions,
            conflict_score=engine_result.conflict_score,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("conflict_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=CONFLICT_SECTION_TYPE,
            title_ref="conflict.title",
            interpreter_id=CONFLICT_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("conflict_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return ConflictInterpretationSection(
            section=section,
            clashes=typed.clashes,
            punishments=typed.punishments,
            harms=typed.harms,
            destructions=typed.destructions,
            conflict_score=typed.conflict_score,
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
    ) -> ConflictInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="conflict_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: ConflictRuleEngineResult,
    ) -> dict[str, ConflictComponentResult]:
        """Map engine results into Clash/Punishment/Harm/Destruction components."""
        return {
            "clash": ConflictComponentResult(
                component_id="clash",
                value=",".join(item.item_id for item in engine_result.clashes),
                score=sum(item.score for item in engine_result.clashes),
                count=len(engine_result.clashes),
                items=engine_result.clashes,
                description="Clash (Xung)",
            ),
            "punishment": ConflictComponentResult(
                component_id="punishment",
                value=",".join(item.item_id for item in engine_result.punishments),
                score=sum(item.score for item in engine_result.punishments),
                count=len(engine_result.punishments),
                items=engine_result.punishments,
                description="Punishment (Hinh)",
            ),
            "harm": ConflictComponentResult(
                component_id="harm",
                value=",".join(item.item_id for item in engine_result.harms),
                score=sum(item.score for item in engine_result.harms),
                count=len(engine_result.harms),
                items=engine_result.harms,
                description="Harm (Hai)",
            ),
            "destruction": ConflictComponentResult(
                component_id="destruction",
                value=",".join(item.item_id for item in engine_result.destructions),
                score=sum(item.score for item in engine_result.destructions),
                count=len(engine_result.destructions),
                items=engine_result.destructions,
                description="Destruction (Pha)",
            ),
        }
