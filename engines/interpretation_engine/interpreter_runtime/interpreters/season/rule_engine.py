"""Season Interpretation Rule Engine.

Loads Pack 01 ``database/11_temperature`` season + climate (+ temperature) rules.
Matches FinalResult-derived facts with TemperatureMatcher.
Does not hard-code BaZi season maps or scoring formulas.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from engines.temperature_engine.loader import TemperatureLoader
from engines.temperature_engine.matcher import TemperatureMatcher

from engines.interpretation_engine.interpreter_runtime.interpreters.season.extractor import (
    SeasonFacts,
)

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_PACK01_TEMPERATURE_DB = str(_REPO_ROOT / "database" / "11_temperature")


@dataclass(slots=True)
class SeasonRuleMatch:
    """Matched Pack 01 season/temperature rule."""

    rule_id: str
    score_target: str
    temperature_level: str
    score: float
    priority: int
    reason: str
    description: str
    recommendation: str


@dataclass(slots=True)
class SeasonRuleEngineResult:
    """Rule-engine output for Season Interpreter."""

    season: str
    month_branch: str
    qi_stage: str
    climate: str
    temperature_level: str
    season_score: float
    temperature_score: float
    season_matches: tuple[SeasonRuleMatch, ...]
    climate_matches: tuple[SeasonRuleMatch, ...]
    temperature_matches: tuple[SeasonRuleMatch, ...]
    matched_rule_ids: tuple[str, ...]
    recommendations: tuple[str, ...]
    config: dict[str, float]
    reasoning: str


class SeasonInterpretationRuleEngine:
    """Rule Engine for Season Interpreter.

    Responsibilities:
    - load Pack 01 temperature DB season / climate / temperature rules
    - match Season Rules against season / qi_stage (season_phase)
    - match Climate Rules against climate_type / month_branch
    - match related Temperature Rules (dryness/humidity/balance) when facts allow
    """

    def __init__(
        self,
        *,
        database_path: str | None = None,
        loader: TemperatureLoader | None = None,
        matcher: TemperatureMatcher | None = None,
    ) -> None:
        """Initialize with Pack 01 database path and DI collaborators."""
        self.database_path = database_path or DEFAULT_PACK01_TEMPERATURE_DB
        self.loader = loader or TemperatureLoader(self.database_path)
        self.matcher = matcher or TemperatureMatcher()
        self._config: dict[str, float] | None = None
        self._grouped: dict[str, list[dict[str, Any]]] | None = None

    def evaluate(self, facts: SeasonFacts) -> SeasonRuleEngineResult:
        """Evaluate Pack 01 rules against extracted Pack 02 season facts."""
        config = self._get_config()
        grouped = self._get_grouped_rules()

        season_matches = self._match_group(facts, grouped.get("season", ()))
        climate_matches = self._match_group(facts, grouped.get("climate", ()))

        # Broader Temperature Rules used for season climate narrative.
        temperature_matches: list[SeasonRuleMatch] = []
        for group_name in ("dryness", "humidity", "balance"):
            temperature_matches.extend(
                self._match_group(facts, grouped.get(group_name, ()))
            )
        temperature_matches.sort(key=lambda item: item.priority, reverse=True)

        temperature_level = facts.temperature_level
        if not temperature_level and season_matches:
            temperature_level = season_matches[0].temperature_level
        if not temperature_level and climate_matches:
            temperature_level = climate_matches[0].temperature_level

        climate = facts.climate_type
        if not climate and climate_matches:
            climate = climate_matches[0].temperature_level or climate

        season_score = facts.season_score
        if season_score == 0.0 and season_matches:
            season_score = self._normalize_score(
                sum(item.score for item in season_matches),
                config,
            )

        temperature_score = facts.temperature_score
        if temperature_score == 0.0:
            raw = sum(item.score for item in climate_matches) + sum(
                item.score for item in temperature_matches[:3]
            )
            if raw:
                temperature_score = self._normalize_score(raw, config)

        recommendations = list(facts.recommendations)
        for match in (*season_matches, *climate_matches, *temperature_matches):
            if match.recommendation and match.recommendation not in recommendations:
                recommendations.append(match.recommendation)

        reasoning = ""
        if season_matches:
            reasoning = season_matches[0].reason or season_matches[0].description
        elif climate_matches:
            reasoning = climate_matches[0].reason or climate_matches[0].description
        if not reasoning:
            reasoning = facts.reasoning

        matched_ids = list(facts.matched_rules)
        for match in (*season_matches, *climate_matches, *temperature_matches):
            if match.rule_id:
                matched_ids.append(match.rule_id)

        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        logger.info(
            "season_rule_engine_evaluated",
            extra={
                "season": facts.season,
                "month_branch": facts.month_branch,
                "qi_stage": facts.qi_stage,
                "climate": climate,
                "season_match_count": len(season_matches),
                "climate_match_count": len(climate_matches),
            },
        )

        return SeasonRuleEngineResult(
            season=facts.season,
            month_branch=facts.month_branch,
            qi_stage=facts.qi_stage,
            climate=climate,
            temperature_level=temperature_level,
            season_score=season_score,
            temperature_score=temperature_score,
            season_matches=season_matches,
            climate_matches=climate_matches,
            temperature_matches=tuple(temperature_matches),
            matched_rule_ids=tuple(ordered_ids),
            recommendations=tuple(recommendations),
            config=dict(config),
            reasoning=reasoning,
        )

    def _match_group(
        self,
        facts: SeasonFacts,
        rules: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    ) -> tuple[SeasonRuleMatch, ...]:
        """Match active Pack 01 rules; skip unsafe comparisons."""
        matches: list[SeasonRuleMatch] = []
        for rule in rules:
            if not self.matcher.is_active(rule):
                continue
            if not self._safe_match(facts, rule):
                continue
            matches.append(self._to_match(rule))
        matches.sort(key=lambda item: item.priority, reverse=True)
        return tuple(matches)

    def _safe_match(self, facts: SeasonFacts, rule: dict[str, Any]) -> bool:
        """Match Pack 01 rule; missing fact fields never raise."""
        try:
            return bool(self.matcher.match(facts, rule))
        except (TypeError, ValueError) as exc:
            logger.debug(
                "season_rule_match_skipped",
                extra={
                    "rule_id": str(rule.get("rule_id") or ""),
                    "error": str(exc),
                },
            )
            return False

    def _normalize_score(self, score: float, config: dict[str, float]) -> float:
        """Normalize raw Pack 01 scores into [0, 1] using config scale."""
        value = float(score)
        scale = float(config.get("scale") or 100.0)
        if value > 1.0 and scale > 0:
            value = value / scale
        return max(0.0, min(1.0, value))

    def _get_config(self) -> dict[str, float]:
        """Lazy-load Pack 01 config once per engine instance."""
        if self._config is None:
            self._config = self.loader.load_config()
        return self._config

    def _get_grouped_rules(self) -> dict[str, list[dict[str, Any]]]:
        """Lazy-load Pack 01 rule groups once per engine instance."""
        if self._grouped is None:
            self._grouped = self.loader.load_rule_groups()
        return self._grouped

    @staticmethod
    def _to_match(rule: dict[str, Any]) -> SeasonRuleMatch:
        """Convert Pack 01 CSV row to SeasonRuleMatch."""
        return SeasonRuleMatch(
            rule_id=str(rule.get("rule_id") or ""),
            score_target=str(rule.get("score_target") or rule.get("rule_group") or ""),
            temperature_level=str(rule.get("temperature_level") or ""),
            score=float(rule.get("score") or 0.0),
            priority=int(rule.get("priority") or 0),
            reason=str(rule.get("reason") or ""),
            description=str(rule.get("description") or ""),
            recommendation=str(rule.get("recommendation") or ""),
        )
