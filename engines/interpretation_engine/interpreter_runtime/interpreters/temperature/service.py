"""Temperature Interpreter service — orchestration for temperature business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.constants import (
    TEMPERATURE_INTERPRETER_ID,
    TEMPERATURE_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.extractor import (
    TemperatureFactExtractor,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.models import (
    TemperatureComponentResult,
    TemperatureInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.rule_engine import (
    TemperatureInterpretationRuleEngine,
    TemperatureRuleEngineResult,
    TemperatureRuleMatch,
)

logger = logging.getLogger(__name__)


class TemperatureInterpreterService:
    """Build TemperatureInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 ``database/11_temperature`` via Rule Engine only.
    """

    def __init__(
        self,
        *,
        extractor: TemperatureFactExtractor | None = None,
        rule_engine: TemperatureInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or TemperatureFactExtractor()
        self.rule_engine = rule_engine or TemperatureInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> TemperatureInterpretationSection | None:
        """Interpret temperature from context.final_result.

        Returns None when FinalResult has no temperature payload
        (caller may fall back to empty skeleton section).
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "temperature_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(engine_result)
        section_id = f"section_{TEMPERATURE_INTERPRETER_ID}_{context.id}"

        typed = TemperatureInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=TEMPERATURE_SECTION_TYPE,
                title_ref="temperature.title",
                interpreter_id=TEMPERATURE_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("temperature_interpreter_ok",),
                attributes={},
            ),
            cold=engine_result.cold,
            hot=engine_result.hot,
            dry=engine_result.dry,
            wet=engine_result.wet,
            balance=engine_result.balance,
            temperature_level=engine_result.temperature_level,
            temperature_score=engine_result.temperature_score,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            recommendations=engine_result.recommendations,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("temperature_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=TEMPERATURE_SECTION_TYPE,
            title_ref="temperature.title",
            interpreter_id=TEMPERATURE_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("temperature_interpreter_ok",),
            attributes=typed.to_attributes(),
        )
        return TemperatureInterpretationSection(
            section=section,
            cold=typed.cold,
            hot=typed.hot,
            dry=typed.dry,
            wet=typed.wet,
            balance=typed.balance,
            temperature_level=typed.temperature_level,
            temperature_score=typed.temperature_score,
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
    ) -> TemperatureInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="temperature_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        engine_result: TemperatureRuleEngineResult,
    ) -> dict[str, TemperatureComponentResult]:
        """Map engine results into Cold/Hot/Dry/Wet/Balance components."""

        def _from_matches(
            component_id: str,
            score: float,
            matches: tuple[TemperatureRuleMatch, ...],
            *,
            level: str = "",
            fallback_rule: TemperatureRuleMatch | None = None,
        ) -> TemperatureComponentResult:
            match = matches[0] if matches else fallback_rule
            return TemperatureComponentResult(
                component_id=component_id,
                score=score,
                level=level or ("" if match is None else match.temperature_level),
                rule_id=None if match is None else match.rule_id,
                description=(
                    ""
                    if match is None
                    else (match.description or match.reason)
                ),
                recommendation="" if match is None else match.recommendation,
            )

        level_rule = engine_result.level_rule
        return {
            "cold": _from_matches(
                "cold",
                engine_result.cold,
                engine_result.cold_matches,
                level="cold" if engine_result.temperature_level in {"cold", "cool"} else "",
                fallback_rule=level_rule
                if engine_result.temperature_level in {"cold", "cool"}
                else None,
            ),
            "hot": _from_matches(
                "hot",
                engine_result.hot,
                engine_result.hot_matches,
                level="hot" if engine_result.temperature_level in {"hot", "warm"} else "",
                fallback_rule=level_rule
                if engine_result.temperature_level in {"hot", "warm"}
                else None,
            ),
            "dry": _from_matches(
                "dry",
                engine_result.dry,
                engine_result.dry_matches,
                level="dry",
            ),
            "wet": _from_matches(
                "wet",
                engine_result.wet,
                engine_result.wet_matches,
                level="wet",
            ),
            "balance": _from_matches(
                "balance",
                engine_result.balance,
                engine_result.balance_matches,
                level="balanced",
                fallback_rule=level_rule,
            ),
        }
