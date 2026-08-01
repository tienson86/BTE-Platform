"""Season Interpreter service — orchestration for season business module."""

from __future__ import annotations

import logging

from engines.analysis_engine.models.final_result import FinalResult
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.models.section_result import SectionResult

from engines.interpretation_engine.interpreter_runtime.interpreters.season.constants import (
    SEASON_INTERPRETER_ID,
    SEASON_SECTION_TYPE,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.season.extractor import (
    SeasonFactExtractor,
    SeasonFacts,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.season.models import (
    SeasonComponentResult,
    SeasonInterpretationSection,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.season.rule_engine import (
    SeasonInterpretationRuleEngine,
    SeasonRuleEngineResult,
)

logger = logging.getLogger(__name__)


class SeasonInterpreterService:
    """Build SeasonInterpretationSection from Pack 02 FinalResult.

    Uses Pack 01 temperature season/climate rules via Rule Engine.
    """

    def __init__(
        self,
        *,
        extractor: SeasonFactExtractor | None = None,
        rule_engine: SeasonInterpretationRuleEngine | None = None,
    ) -> None:
        """Initialize with injectable extractor and rule engine."""
        self.extractor = extractor or SeasonFactExtractor()
        self.rule_engine = rule_engine or SeasonInterpretationRuleEngine()

    def interpret(
        self,
        context: PackInterpretationContext,
    ) -> SeasonInterpretationSection | None:
        """Interpret season from context.final_result.

        Returns None when FinalResult has no season/climate payload
        (caller may fall back to empty skeleton section).
        """
        final_result = context.final_result
        facts = self.extractor.extract(final_result)
        if not facts.found:
            logger.info(
                "season_interpreter_no_facts",
                extra={"context_id": context.id, "final_result_id": final_result.id},
            )
            return None

        engine_result = self.rule_engine.evaluate(facts)
        components = self._build_components(facts, engine_result)
        section_id = f"section_{SEASON_INTERPRETER_ID}_{context.id}"
        attributes_section = SeasonInterpretationSection(
            section=SectionResult(
                id=section_id,
                section_type=SEASON_SECTION_TYPE,
                title_ref="season.title",
                interpreter_id=SEASON_INTERPRETER_ID,
                paragraphs=(),
                success=True,
                messages=("season_interpreter_ok",),
                attributes={},
            ),
            season=engine_result.season,
            month_branch=engine_result.month_branch,
            qi_stage=engine_result.qi_stage,
            climate=engine_result.climate,
            temperature_level=engine_result.temperature_level,
            season_score=engine_result.season_score,
            temperature_score=engine_result.temperature_score,
            components=components,
            matched_rules=engine_result.matched_rule_ids,
            recommendations=engine_result.recommendations,
            confidence=facts.confidence,
            reasoning=engine_result.reasoning,
            source_final_result_id=final_result.id,
            success=True,
            messages=("season_interpreter_ok",),
        )

        section = SectionResult(
            id=section_id,
            section_type=SEASON_SECTION_TYPE,
            title_ref="season.title",
            interpreter_id=SEASON_INTERPRETER_ID,
            paragraphs=(),
            success=True,
            messages=("season_interpreter_ok",),
            attributes=attributes_section.to_attributes(),
        )
        return SeasonInterpretationSection(
            section=section,
            season=attributes_section.season,
            month_branch=attributes_section.month_branch,
            qi_stage=attributes_section.qi_stage,
            climate=attributes_section.climate,
            temperature_level=attributes_section.temperature_level,
            season_score=attributes_section.season_score,
            temperature_score=attributes_section.temperature_score,
            components=attributes_section.components,
            matched_rules=attributes_section.matched_rules,
            recommendations=attributes_section.recommendations,
            confidence=attributes_section.confidence,
            reasoning=attributes_section.reasoning,
            source_final_result_id=attributes_section.source_final_result_id,
            success=attributes_section.success,
            messages=attributes_section.messages,
        )

    def interpret_final_result(
        self,
        final_result: FinalResult,
        *,
        context_id: str = "adhoc",
    ) -> SeasonInterpretationSection | None:
        """Convenience entry for FinalResult-only callers."""
        context = PackInterpretationContext(
            id=context_id,
            version="1.0.0",
            pipeline_id="season_interpreter",
            source_final_result_id=final_result.id,
            final_result=final_result,
            created_at="",
        )
        return self.interpret(context)

    def _build_components(
        self,
        facts: SeasonFacts,
        engine_result: SeasonRuleEngineResult,
    ) -> dict[str, SeasonComponentResult]:
        """Map engine results into named SeasonComponentResult entries."""
        season_match = (
            engine_result.season_matches[0]
            if engine_result.season_matches
            else None
        )
        climate_match = (
            engine_result.climate_matches[0]
            if engine_result.climate_matches
            else None
        )
        qi_match = None
        for match in engine_result.season_matches:
            if "phase" in match.rule_id or "phase" in match.description.lower():
                qi_match = match
                break
        if qi_match is None and engine_result.season_matches:
            # Prefer phase-oriented season rules when season_phase was matched.
            for match in engine_result.season_matches:
                if match.score_target == "season" and facts.qi_stage:
                    qi_match = match
                    break

        return {
            "season_rules": SeasonComponentResult(
                component_id="season_rules",
                value=engine_result.season,
                score=engine_result.season_score,
                level=engine_result.temperature_level,
                rule_id=None if season_match is None else season_match.rule_id,
                description=(
                    ""
                    if season_match is None
                    else (season_match.description or season_match.reason)
                ),
                recommendation=(
                    "" if season_match is None else season_match.recommendation
                ),
            ),
            "temperature_rules": SeasonComponentResult(
                component_id="temperature_rules",
                value=engine_result.temperature_level,
                score=engine_result.temperature_score,
                level=engine_result.temperature_level,
                rule_id=(
                    engine_result.temperature_matches[0].rule_id
                    if engine_result.temperature_matches
                    else (None if climate_match is None else climate_match.rule_id)
                ),
                description=(
                    engine_result.temperature_matches[0].description
                    if engine_result.temperature_matches
                    else (
                        ""
                        if climate_match is None
                        else (climate_match.description or climate_match.reason)
                    )
                ),
                recommendation=(
                    engine_result.temperature_matches[0].recommendation
                    if engine_result.temperature_matches
                    else ("" if climate_match is None else climate_match.recommendation)
                ),
            ),
            "month_branch": SeasonComponentResult(
                component_id="month_branch",
                value=engine_result.month_branch,
                score=0.0,
                level=facts.month_status,
                rule_id=None if climate_match is None else climate_match.rule_id,
                description=(
                    ""
                    if climate_match is None
                    else (climate_match.description or climate_match.reason)
                ),
                recommendation=(
                    "" if climate_match is None else climate_match.recommendation
                ),
            ),
            "qi_stage": SeasonComponentResult(
                component_id="qi_stage",
                value=engine_result.qi_stage,
                score=engine_result.season_score,
                level=engine_result.qi_stage,
                rule_id=None if qi_match is None else qi_match.rule_id,
                description=(
                    ""
                    if qi_match is None
                    else (qi_match.description or qi_match.reason)
                ),
                recommendation="" if qi_match is None else qi_match.recommendation,
                attributes={"season_phase": engine_result.qi_stage},
            ),
            "climate": SeasonComponentResult(
                component_id="climate",
                value=engine_result.climate,
                score=engine_result.temperature_score,
                level=engine_result.climate,
                rule_id=None if climate_match is None else climate_match.rule_id,
                description=(
                    ""
                    if climate_match is None
                    else (climate_match.description or climate_match.reason)
                ),
                recommendation=(
                    "" if climate_match is None else climate_match.recommendation
                ),
            ),
        }
