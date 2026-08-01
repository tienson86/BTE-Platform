"""Strength Interpreter service — orchestration for first business module."""

from __future__ import annotations

import logging
from typing import Any

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.strength.constants import (
    STRENGTH_INTERPRETER_ID,
    STRENGTH_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength.extractor import (
    StrengthFactExtractor,
    StrengthFacts,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength.models import (
    StrengthComponentScore,
    StrengthInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.strength.rule_engine import (
    StrengthInterpretationRuleEngine,
    StrengthRuleEngineResult,
)

logger = logging.getLogger(__name__)


class StrengthInterpreterService:
    """Build StrengthInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 Knowledge Base via Rule Engine. No hardcoded thresholds.
    """

    def __init__(
        self,
        *,
        extractor: StrengthFactExtractor | None = None,
        rule_engine: StrengthInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or StrengthFactExtractor()
        self.rule_engine = rule_engine or StrengthInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> StrengthInterpretationSection | None:
        """Interpret strength from context.final_result.

        Returns None when FinalResult has no strength payload
        (caller may fall back to empty skeleton section).
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "strength_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(facts, engine_result)
        section_id = f"section_{STRENGTH_INTERPRETER_ID}_{context.id}"

        typed = StrengthInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=STRENGTH_SECTION_TYPE,
                title_ref="strength.title",
                interpreter_id=STRENGTH_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("strength_interpreter_ok",),
                attributes={},
            ),
            body_strength=engine_result.body_strength,
            season_strength=engine_result.season_strength,
            root_strength=engine_result.root_strength,
            stem_strength=engine_result.stem_strength,
            support_score=engine_result.support_score,
            drain_score=engine_result.drain_score,
            balance_score=engine_result.balance_score,
            final_strength=engine_result.final_strength,
            final_strength_score=engine_result.final_strength_score,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("strength_interpreter_ok",),
        )

        # Attach flattened attributes onto the Pack 03 section shell.
        section = SectionResult(
            id=section_id,
            section_type=STRENGTH_SECTION_TYPE,
            title_ref="strength.title",
            interpreter_id=STRENGTH_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("strength_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return StrengthInterpretationSection(
            section=section,
            body_strength=typed.body_strength,
            season_strength=typed.season_strength,
            root_strength=typed.root_strength,
            stem_strength=typed.stem_strength,
            support_score=typed.support_score,
            drain_score=typed.drain_score,
            balance_score=typed.balance_score,
            final_strength=typed.final_strength,
            final_strength_score=typed.final_strength_score,
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
    ) -> StrengthInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="strength_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        facts: StrengthFacts,
        engine_result: StrengthRuleEngineResult,
    ) -> dict[str, StrengthComponentScore]:
        """Map engine results into named StrengthComponentScore entries."""
        match_by_target: dict[str, Any] = {}
        for match in engine_result.component_matches:
            match_by_target.setdefault(match.score_target, match)

        level_rule = engine_result.level_rule

        def _component(
            component_id: str,
            score: float,
            *,
            target: str,
            level: str = "",
        ) -> StrengthComponentScore:
            match = match_by_target.get(target)
            rule_id = match.rule_id if match is not None else None
            description = ""
            if match is not None:
                description = match.description or match.reason
            if component_id == "final_strength" and level_rule is not None:
                rule_id = level_rule.rule_id
                description = level_rule.description or level_rule.reason
                level = level or level_rule.strength_level
            return StrengthComponentScore(
                component_id=component_id,
                score=score,
                level=level,
                rule_id=rule_id,
                description=description,
            )

        return {
            "body_strength": _component(
                "body_strength",
                engine_result.body_strength,
                target="level",
                level=engine_result.final_strength,
            ),
            "season_strength": _component(
                "season_strength",
                engine_result.season_strength,
                target="season",
                level=facts.month_status,
            ),
            "root_strength": _component(
                "root_strength",
                engine_result.root_strength,
                target="root",
                level=facts.root_level,
            ),
            "stem_strength": _component(
                "stem_strength",
                engine_result.stem_strength,
                target="support",
                level=facts.support_type,
            ),
            "support_score": _component(
                "support_score",
                engine_result.support_score,
                target="support",
                level=facts.support_type,
            ),
            "drain_score": _component(
                "drain_score",
                engine_result.drain_score,
                target="drain",
                level=facts.drain_type,
            ),
            "balance_score": StrengthComponentScore(
                component_id="balance_score",
                score=engine_result.balance_score,
                level="balanced" if engine_result.final_strength == "balanced" else "",
                rule_id=None if level_rule is None else level_rule.rule_id,
                description="Derived from Pack 01 weak/strong thresholds",
                attributes={"config": dict(engine_result.config)},
            ),
            "final_strength": _component(
                "final_strength",
                engine_result.final_strength_score,
                target="level",
                level=engine_result.final_strength,
            ),
        }
