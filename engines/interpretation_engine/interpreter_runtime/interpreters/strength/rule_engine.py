"""Strength Interpretation Rule Engine.

Loads Pack 01 ``database/12_strength`` rules via StrengthLoader.
Matches FinalResult-derived facts with StrengthMatcher.
Does not hard-code thresholds or BaZi scoring formulas.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from engines.strength_engine.loader import StrengthLoader
from engines.strength_engine.matcher import StrengthMatcher

from engines.interpretation_engine.interpreter_runtime.interpreters.strength.extractor import (
    StrengthFacts,
)

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_PACK01_STRENGTH_DB = str(_REPO_ROOT / "database" / "12_strength")


@dataclass(slots=True)
class StrengthRuleMatch:
    """Matched Pack 01 interpretation rule."""

    rule_id: str
    score_target: str
    strength_level: str
    score: float
    priority: int
    reason: str
    description: str


@dataclass(slots=True)
class StrengthRuleEngineResult:
    """Rule-engine output for Strength Interpreter."""

    final_strength: str
    final_strength_score: float
    balance_score: float
    body_strength: float
    season_strength: float
    root_strength: float
    stem_strength: float
    support_score: float
    drain_score: float
    level_rule: StrengthRuleMatch | None
    component_matches: tuple[StrengthRuleMatch, ...]
    matched_rule_ids: tuple[str, ...]
    config: dict[str, float]
    reasoning: str


class StrengthInterpretationRuleEngine:
    """Rule Engine for Strength Interpreter.

    Responsibilities:
    - load Pack 01 strength rules (read-only)
    - classify final strength via level rules
    - interpret component labels via Pack 01 condition rules
    - derive balance score from Pack 01 config thresholds
    """

    def __init__(
        self,
        *,
        database_path: str | None = None,
        loader: StrengthLoader | None = None,
        matcher: StrengthMatcher | None = None,
    ) -> None:
        """Initialize with Pack 01 database path and DI collaborators."""
        self.database_path = database_path or DEFAULT_PACK01_STRENGTH_DB
        self.loader = loader or StrengthLoader(self.database_path)
        self.matcher = matcher or StrengthMatcher()
        self._config: dict[str, float] | None = None
        self._level_rules: list[dict[str, Any]] | None = None
        self._grouped: dict[str, list[dict[str, Any]]] | None = None

    def evaluate(self, facts: StrengthFacts) -> StrengthRuleEngineResult:
        """Evaluate Pack 01 rules against extracted Pack 02 facts."""
        config = self._get_config()
        level_rules = self._get_level_rules()
        grouped = self._get_grouped_rules()
        # Ensure matcher sees normalized strength_score for level rules.
        score_for_level = self._normalize_score(
            facts.final_strength_score or facts.body_strength,
            config,
        )
        facts.final_strength_score = score_for_level
        if facts.body_strength == 0.0:
            facts.body_strength = score_for_level

        level_match = self._match_level(facts, level_rules)
        final_strength = (
            level_match.strength_level
            if level_match is not None
            else (facts.final_strength or "balanced")
        )

        balance_score = (
            float(facts.balance_score)
            if facts.balance_score is not None
            else self._balance_from_config(score_for_level, config)
        )

        component_matches = self._match_components(facts, grouped)
        reasoning = ""
        if level_match is not None:
            reasoning = level_match.reason or level_match.description
        if not reasoning:
            reasoning = facts.reasoning

        matched_ids = list(facts.matched_rules)
        if level_match is not None:
            matched_ids.append(level_match.rule_id)
        matched_ids.extend(item.rule_id for item in component_matches)

        # Deduplicate while preserving order.
        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        logger.info(
            "strength_rule_engine_evaluated",
            extra={
                "final_strength": final_strength,
                "balance_score": balance_score,
                "level_rule": None if level_match is None else level_match.rule_id,
                "component_match_count": len(component_matches),
            },
        )

        return StrengthRuleEngineResult(
            final_strength=final_strength,
            final_strength_score=score_for_level,
            balance_score=balance_score,
            body_strength=facts.body_strength,
            season_strength=facts.season_strength,
            root_strength=facts.root_strength,
            stem_strength=facts.stem_strength,
            support_score=facts.support_score,
            drain_score=facts.drain_score,
            level_rule=level_match,
            component_matches=component_matches,
            matched_rule_ids=tuple(ordered_ids),
            config=dict(config),
            reasoning=reasoning,
        )

    def _match_level(
        self,
        facts: StrengthFacts,
        level_rules: list[dict[str, Any]],
    ) -> StrengthRuleMatch | None:
        """Match Pack 01 level rules by priority (highest first)."""
        active = [rule for rule in level_rules if self.matcher.is_active(rule)]
        active.sort(key=lambda rule: int(rule.get("priority") or 0), reverse=True)
        for rule in active:
            if self._safe_match(facts, rule):
                return self._to_match(rule, score_target="level")
        return None

    def _match_components(
        self,
        facts: StrengthFacts,
        grouped: dict[str, list[dict[str, Any]]],
    ) -> tuple[StrengthRuleMatch, ...]:
        """Match Pack 01 component rules when Pack 02 exposes label fields."""
        eligible: dict[str, bool] = {
            "season": bool(facts.month_status),
            "root": bool(facts.root_level),
            "support": bool(facts.support_type),
            "drain": bool(facts.drain_type),
            "control": bool(facts.control_type),
        }
        matches: list[StrengthRuleMatch] = []
        for group_name, enabled in eligible.items():
            if not enabled:
                continue
            for rule in grouped.get(group_name, ()):
                if not self.matcher.is_active(rule):
                    continue
                if not self._safe_match(facts, rule):
                    continue
                matches.append(
                    self._to_match(
                        rule,
                        score_target=str(
                            rule.get("score_target") or group_name
                        ),
                    )
                )
        matches.sort(key=lambda item: item.priority, reverse=True)
        return tuple(matches)

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

    def _safe_match(self, facts: StrengthFacts, rule: dict[str, Any]) -> bool:
        """Match Pack 01 rule; missing fact fields never raise."""
        try:
            return bool(self.matcher.match(facts, rule))
        except (TypeError, ValueError) as exc:
            logger.debug(
                "strength_rule_match_skipped",
                extra={
                    "rule_id": str(rule.get("rule_id") or ""),
                    "error": str(exc),
                },
            )
            return False

    def _balance_from_config(
        self,
        strength_score: float,
        config: dict[str, float],
    ) -> float:
        """Derive balance score from Pack 01 weak/strong thresholds."""
        weak = float(config.get("weak_threshold") or 0.35)
        strong = float(config.get("strong_threshold") or 0.65)
        mid = (weak + strong) / 2.0
        half_width = max((strong - weak) / 2.0, 1e-9)
        distance = abs(float(strength_score) - mid)
        score = 1.0 - (distance / half_width)
        return max(0.0, min(1.0, score))

    def _normalize_score(self, score: float, config: dict[str, float]) -> float:
        """Normalize Pack 02 scores into Pack 01 level rule domain [0, 1].

        Pack 02 may emit 0–1 or 0–100. Uses Pack 01 ``scale`` when needed.
        """
        value = float(score)
        scale = float(config.get("scale") or 100.0)
        if value > 1.0 and scale > 0:
            value = value / scale
        return max(0.0, min(1.0, value))

    @staticmethod
    def _to_match(rule: dict[str, Any], *, score_target: str) -> StrengthRuleMatch:
        """Convert Pack 01 CSV row to StrengthRuleMatch."""
        return StrengthRuleMatch(
            rule_id=str(rule.get("rule_id") or ""),
            score_target=score_target,
            strength_level=str(rule.get("strength_level") or ""),
            score=float(rule.get("score") or 0.0),
            priority=int(rule.get("priority") or 0),
            reason=str(rule.get("reason") or ""),
            description=str(rule.get("description") or ""),
        )
