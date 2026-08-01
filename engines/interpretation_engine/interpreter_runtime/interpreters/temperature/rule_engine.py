"""Temperature Interpretation Rule Engine.

Loads Pack 01 ``database/11_temperature`` only.
Evaluates Cold / Hot / Dry / Wet / Balance via TemperatureMatcher.
Does not hard-code thresholds or call TemperatureEngine.calculate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from engines.temperature_engine.loader import TemperatureLoader
from engines.temperature_engine.matcher import TemperatureMatcher

from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.extractor import (
    TemperatureFacts,
)

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_PACK01_TEMPERATURE_DB = str(_REPO_ROOT / "database" / "11_temperature")


@dataclass(slots=True)
class TemperatureRuleMatch:
    """Matched Pack 01 temperature rule."""

    rule_id: str
    score_target: str
    temperature_level: str
    score: float
    priority: int
    reason: str
    description: str
    recommendation: str


@dataclass(slots=True)
class TemperatureRuleEngineResult:
    """Rule-engine output for Temperature Interpreter."""

    cold: float
    hot: float
    dry: float
    wet: float
    balance: float
    temperature_level: str
    temperature_score: float
    cold_matches: tuple[TemperatureRuleMatch, ...]
    hot_matches: tuple[TemperatureRuleMatch, ...]
    dry_matches: tuple[TemperatureRuleMatch, ...]
    wet_matches: tuple[TemperatureRuleMatch, ...]
    balance_matches: tuple[TemperatureRuleMatch, ...]
    level_rule: TemperatureRuleMatch | None
    matched_rule_ids: tuple[str, ...]
    recommendations: tuple[str, ...]
    config: dict[str, float]
    reasoning: str


class TemperatureInterpretationRuleEngine:
    """Rule Engine for Temperature Interpreter (Pack 01 only)."""

    def __init__(
        self,
        *,
        database_path: str | None = None,
        loader: TemperatureLoader | None = None,
        matcher: TemperatureMatcher | None = None,
    ) -> None:
        """Initialize with Pack 01 temperature database path and DI collaborators."""
        self.database_path = database_path or DEFAULT_PACK01_TEMPERATURE_DB
        self.loader = loader or TemperatureLoader(self.database_path)
        self.matcher = matcher or TemperatureMatcher()
        self._config: dict[str, float] | None = None
        self._level_rules: list[dict[str, Any]] | None = None
        self._grouped: dict[str, list[dict[str, Any]]] | None = None

    def evaluate(self, facts: TemperatureFacts) -> TemperatureRuleEngineResult:
        """Evaluate Pack 01 rules against extracted Pack 02 temperature facts."""
        config = self._get_config()
        grouped = self._get_grouped_rules()
        level_rules = self._get_level_rules()

        temperature_score = self._normalize_score(facts.temperature_score, config)
        if temperature_score == 0.0 and (facts.warm_score or facts.cold_score):
            # Derive score axis from hot vs cold when overall score missing.
            temperature_score = self._score_from_hot_cold(
                facts.warm_score, facts.cold_score, config
            )
        facts.temperature_score = temperature_score

        cold = self._normalize_score(facts.cold_score, config)
        hot = self._normalize_score(facts.warm_score, config)
        dry = self._normalize_score(facts.dry_score, config)
        wet = self._normalize_score(facts.humid_score, config)

        # Keep matcher-visible fields in normalized domain for balance rules.
        facts.cold_score = cold
        facts.warm_score = hot
        facts.dry_score = dry
        facts.humid_score = wet

        dry_matches = self._match_group(facts, grouped.get("dryness", ()))
        wet_matches = self._match_group(facts, grouped.get("humidity", ()))
        balance_matches = self._match_group(facts, grouped.get("balance", ()))

        # Hot / Cold from season + climate temperature_level hints + level rules.
        season_matches = self._match_group(facts, grouped.get("season", ()))
        climate_matches = self._match_group(facts, grouped.get("climate", ()))
        hot_matches = tuple(
            item
            for item in (*season_matches, *climate_matches)
            if item.temperature_level in {"hot", "warm"}
        )
        cold_matches = tuple(
            item
            for item in (*season_matches, *climate_matches)
            if item.temperature_level in {"cold", "cool"}
        )

        if dry == 0.0 and dry_matches:
            dry = self._normalize_score(
                sum(item.score for item in dry_matches if item.score > 0),
                config,
            )
            facts.dry_score = dry
        if wet == 0.0 and wet_matches:
            wet = self._normalize_score(
                sum(item.score for item in wet_matches if item.score > 0),
                config,
            )
            facts.humid_score = wet

        level_match = self._match_level(facts, level_rules)
        temperature_level = (
            level_match.temperature_level
            if level_match is not None
            else (facts.temperature_level or "")
        )
        if not temperature_level and hot_matches:
            temperature_level = hot_matches[0].temperature_level
        if not temperature_level and cold_matches:
            temperature_level = cold_matches[0].temperature_level

        if facts.balance_score is not None:
            balance = self._normalize_score(float(facts.balance_score), config)
        else:
            balance = self._balance_from_components(cold, hot, dry, wet)
            if balance_matches:
                # Pack 01 balance rules reinforce when matched.
                balance = max(
                    balance,
                    self._normalize_score(
                        sum(item.score for item in balance_matches if item.score > 0),
                        config,
                    ),
                )

        recommendations = list(facts.recommendations)
        all_matches = (
            *cold_matches,
            *hot_matches,
            *dry_matches,
            *wet_matches,
            *balance_matches,
        )
        if level_match is not None:
            all_matches = (*all_matches, level_match)
        for match in all_matches:
            if match.recommendation and match.recommendation not in recommendations:
                recommendations.append(match.recommendation)

        reasoning = ""
        if level_match is not None:
            reasoning = level_match.reason or level_match.description
        elif balance_matches:
            reasoning = balance_matches[0].reason or balance_matches[0].description
        elif dry_matches or wet_matches:
            primary = dry_matches[0] if dry_matches else wet_matches[0]
            reasoning = primary.reason or primary.description
        if not reasoning:
            reasoning = facts.reasoning

        matched_ids = list(facts.matched_rules)
        for match in all_matches:
            if match.rule_id:
                matched_ids.append(match.rule_id)
        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        logger.info(
            "temperature_rule_engine_evaluated",
            extra={
                "temperature_level": temperature_level,
                "cold": cold,
                "hot": hot,
                "dry": dry,
                "wet": wet,
                "balance": balance,
                "level_rule": None if level_match is None else level_match.rule_id,
            },
        )

        return TemperatureRuleEngineResult(
            cold=cold,
            hot=hot,
            dry=dry,
            wet=wet,
            balance=balance,
            temperature_level=temperature_level or "warm",
            temperature_score=temperature_score,
            cold_matches=cold_matches,
            hot_matches=hot_matches,
            dry_matches=dry_matches,
            wet_matches=wet_matches,
            balance_matches=balance_matches,
            level_rule=level_match,
            matched_rule_ids=tuple(ordered_ids),
            recommendations=tuple(recommendations),
            config=dict(config),
            reasoning=reasoning,
        )

    def _match_level(
        self,
        facts: TemperatureFacts,
        level_rules: list[dict[str, Any]],
    ) -> TemperatureRuleMatch | None:
        """Match Pack 01 level rules by priority (highest first)."""
        active = [rule for rule in level_rules if self.matcher.is_active(rule)]
        active.sort(key=lambda rule: int(rule.get("priority") or 0), reverse=True)
        for rule in active:
            if self._safe_match(facts, rule):
                return self._to_match(rule, score_target="level")
        return None

    def _match_group(
        self,
        facts: TemperatureFacts,
        rules: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    ) -> tuple[TemperatureRuleMatch, ...]:
        """Match active Pack 01 rules; skip unsafe comparisons."""
        matches: list[TemperatureRuleMatch] = []
        for rule in rules:
            if not self.matcher.is_active(rule):
                continue
            if not self._safe_match(facts, rule):
                continue
            matches.append(self._to_match(rule))
        matches.sort(key=lambda item: item.priority, reverse=True)
        return tuple(matches)

    def _safe_match(self, facts: TemperatureFacts, rule: dict[str, Any]) -> bool:
        """Match Pack 01 rule; missing fact fields never raise."""
        try:
            return bool(self.matcher.match(facts, rule))
        except (TypeError, ValueError) as exc:
            logger.debug(
                "temperature_rule_match_skipped",
                extra={
                    "rule_id": str(rule.get("rule_id") or ""),
                    "error": str(exc),
                },
            )
            return False

    def _balance_from_components(
        self,
        cold: float,
        hot: float,
        dry: float,
        wet: float,
    ) -> float:
        """Derive balance from opposing component symmetry.

        Used only when Pack 02 omits balance_score and before Pack 01
        balance-rule reinforcement. No hardcoded classification thresholds.
        """
        hot_cold_gap = abs(hot - cold)
        dry_wet_gap = abs(dry - wet)
        gap = (hot_cold_gap + dry_wet_gap) / 2.0
        return max(0.0, min(1.0, 1.0 - gap))

    def _score_from_hot_cold(
        self,
        hot: float,
        cold: float,
        config: dict[str, float],
    ) -> float:
        """Map hot/cold component pair onto temperature_score axis via config."""
        hot_n = self._normalize_score(hot, config)
        cold_n = self._normalize_score(cold, config)
        total = hot_n + cold_n
        if total <= 0:
            return float(config.get("baseline") or 50.0) / float(
                config.get("scale") or 100.0
            )
        # Higher hot → higher temperature_score.
        return max(0.0, min(1.0, hot_n / total))

    def _normalize_score(self, score: float, config: dict[str, float]) -> float:
        """Normalize Pack 02 / Pack 01 raw scores into [0, 1] using config scale."""
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

    def _get_level_rules(self) -> list[dict[str, Any]]:
        """Lazy-load Pack 01 level rules once per engine instance."""
        if self._level_rules is None:
            self._level_rules = self.loader.load_level_rules()
        return self._level_rules

    def _get_grouped_rules(self) -> dict[str, list[dict[str, Any]]]:
        """Lazy-load Pack 01 rule groups once per engine instance."""
        if self._grouped is None:
            self._grouped = self.loader.load_rule_groups()
        return self._grouped

    @staticmethod
    def _to_match(
        rule: dict[str, Any],
        *,
        score_target: str | None = None,
    ) -> TemperatureRuleMatch:
        """Convert Pack 01 CSV row to TemperatureRuleMatch."""
        return TemperatureRuleMatch(
            rule_id=str(rule.get("rule_id") or ""),
            score_target=str(
                score_target
                or rule.get("score_target")
                or rule.get("rule_group")
                or ""
            ),
            temperature_level=str(rule.get("temperature_level") or ""),
            score=float(rule.get("score") or 0.0),
            priority=int(rule.get("priority") or 0),
            reason=str(rule.get("reason") or ""),
            description=str(rule.get("description") or ""),
            recommendation=str(rule.get("recommendation") or ""),
        )
