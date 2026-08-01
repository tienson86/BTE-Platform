"""Pattern Interpreter service — orchestration for pattern business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.constants import (
    PATTERN_INTERPRETER_ID,
    PATTERN_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.extractor import (
    PatternFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.models import (
    PatternComponentResult,
    PatternInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.rule_engine import (
    PatternInterpretationRuleEngine,
    PatternRuleEngineResult,
)

logger = logging.getLogger(__name__)


class PatternInterpreterService:
    """Build PatternInterpretationSection from Pack 02 FinalResult.

    Uses Pattern Engine Matching / Priority / Resolution against Pack 01 rules.
    """

    def __init__(
        self,
        *,
        extractor: PatternFactExtractor | None = None,
        rule_engine: PatternInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or PatternFactExtractor()
        self.rule_engine = rule_engine or PatternInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> PatternInterpretationSection | None:
        """Interpret pattern from context.final_result.

        Returns None when FinalResult has no pattern payload
        (caller may fall back to empty skeleton section).
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "pattern_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{PATTERN_INTERPRETER_ID}_{context.id}"

        typed = PatternInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=PATTERN_SECTION_TYPE,
                title_ref="pattern.title",
                interpreter_id=PATTERN_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("pattern_interpreter_ok",),
                attributes={},
            ),
            main_pattern=engine_result.main_pattern,
            final_pattern=engine_result.final_pattern,
            status=engine_result.status,
            score=engine_result.score,
            priority=engine_result.priority,
            follow_type=engine_result.follow_type,
            candidate_patterns=engine_result.candidate_patterns,
            validated_patterns=engine_result.validated_patterns,
            secondary_patterns=engine_result.secondary_patterns,
            discarded_patterns=engine_result.discarded_patterns,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("pattern_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=PATTERN_SECTION_TYPE,
            title_ref="pattern.title",
            interpreter_id=PATTERN_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("pattern_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return PatternInterpretationSection(
            section=section,
            main_pattern=typed.main_pattern,
            final_pattern=typed.final_pattern,
            status=typed.status,
            score=typed.score,
            priority=typed.priority,
            follow_type=typed.follow_type,
            candidate_patterns=typed.candidate_patterns,
            validated_patterns=typed.validated_patterns,
            secondary_patterns=typed.secondary_patterns,
            discarded_patterns=typed.discarded_patterns,
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
    ) -> PatternInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="pattern_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: PatternRuleEngineResult,
    ) -> dict[str, PatternComponentResult]:
        """Map Matching / Priority / Resolution into typed components."""
        winner = engine_result.priority_winner
        matched = engine_result.matched_candidates
        resolved = engine_result.resolved_candidates

        return {
            "pattern_matching": PatternComponentResult(
                component_id="pattern_matching",
                value=",".join(engine_result.candidate_patterns),
                score=float(matched[0].score) if matched else 0.0,
                priority=int(matched[0].priority) if matched else 0,
                rule_id=matched[0].rule_id if matched else None,
                description="Pattern Matching against Pack 01 rules",
                attributes={
                    "candidate_count": len(matched),
                    "candidates": [item.pattern for item in matched],
                },
            ),
            "pattern_resolution": PatternComponentResult(
                component_id="pattern_resolution",
                value=",".join(engine_result.validated_patterns),
                score=float(resolved[0].score) if resolved else 0.0,
                priority=int(resolved[0].priority) if resolved else 0,
                rule_id=resolved[0].rule_id if resolved else None,
                description="Pattern Resolution via exclusive conflict groups",
                attributes={
                    "validated_count": len(resolved),
                    "discarded": list(engine_result.discarded_patterns),
                    "secondary": list(engine_result.secondary_patterns),
                },
            ),
            "pattern_priority": PatternComponentResult(
                component_id="pattern_priority",
                value=engine_result.final_pattern,
                score=engine_result.score,
                priority=engine_result.priority,
                rule_id=None if winner is None else winner.rule_id,
                description=(
                    "Pattern Priority via PriorityResolver"
                    if winner is not None
                    else "Pattern Priority from Pack 02 final_pattern"
                ),
                attributes={
                    "final_pattern": engine_result.final_pattern,
                    "main_pattern": engine_result.main_pattern,
                    "follow_type": engine_result.follow_type,
                },
            ),
            "pattern_engine": PatternComponentResult(
                component_id="pattern_engine",
                value=engine_result.final_pattern,
                score=engine_result.score,
                priority=engine_result.priority,
                rule_id=None if winner is None else winner.rule_id,
                description=engine_result.description or engine_result.reasoning,
                attributes={
                    "status": engine_result.status,
                    "matched_rules": list(engine_result.matched_rule_ids),
                },
            ),
        }
