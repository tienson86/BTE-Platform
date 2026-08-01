"""Useful God Interpretation Rule Engine.

Uses Pack 01 ``database/13_useful_god`` via UsefulGodLoader + UsefulGodMatcher
+ PriorityResolver. Does not call UsefulGodEngine.calculate.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from engines.useful_god_engine.loader import UsefulGodLoader
from engines.useful_god_engine.matcher import UsefulGodMatcher
from engines.useful_god_engine.priority import PriorityResolver

from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.extractor import (
    UsefulGodFacts,
)

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_PACK01_USEFUL_GOD_DB = str(_REPO_ROOT / "database" / "13_useful_god")


@dataclass(slots=True)
class UsefulGodRuleMatch:
    """Matched Pack 01 useful-god candidate."""

    rule_id: str
    rule_group: str
    useful_god: str
    favorable_gods: tuple[str, ...]
    unfavorable_gods: tuple[str, ...]
    score: float
    priority: int
    reason: str
    description: str


@dataclass(slots=True)
class UsefulGodRuleEngineResult:
    """Rule-engine output for Useful God Interpreter."""

    useful_god: str
    favorable_gods: tuple[str, ...]
    unfavorable_gods: tuple[str, ...]
    supporting_elements: tuple[str, ...]
    score: float
    priority: int
    matched_candidates: tuple[UsefulGodRuleMatch, ...]
    winner: UsefulGodRuleMatch | None
    matched_rule_ids: tuple[str, ...]
    recommendations: tuple[str, ...]
    reasoning: str


class UsefulGodInterpretationRuleEngine:
    """Rule Engine for Useful God Interpreter."""

    def __init__(
        self,
        *,
        database_path: str | None = None,
        loader: UsefulGodLoader | None = None,
        matcher: UsefulGodMatcher | None = None,
        priority_resolver: PriorityResolver | None = None,
    ) -> None:
        """Initialize with Pack 01 database path and DI collaborators."""
        self.database_path = database_path or DEFAULT_PACK01_USEFUL_GOD_DB
        self.loader = loader or UsefulGodLoader(self.database_path)
        self.matcher = matcher or UsefulGodMatcher()
        self._priority_resolver = priority_resolver
        self._grouped: dict[str, list[dict[str, Any]]] | None = None
        self._priority_rules: list[dict[str, Any]] | None = None

    def evaluate(self, facts: UsefulGodFacts) -> UsefulGodRuleEngineResult:
        """Match Pack 01 rules and resolve useful/favorable/unfavorable gods."""
        grouped = self._get_grouped_rules()
        resolver = self._get_priority_resolver()

        matched: list[UsefulGodRuleMatch] = []
        for group_name, rules in grouped.items():
            for rule in rules:
                if not self._is_active(rule):
                    continue
                if not self._has_match_context(facts, rule):
                    continue
                if not self._safe_match(facts, rule):
                    continue
                matched.append(self._to_match(rule, group_name=group_name))

        matched.sort(key=lambda item: (item.priority, item.score), reverse=True)

        # If Pack 01 matching yields nothing, synthesize from Pack 02 payload.
        if not matched and facts.useful_god:
            matched.append(
                UsefulGodRuleMatch(
                    rule_id="",
                    rule_group="pack02",
                    useful_god=facts.useful_god,
                    favorable_gods=facts.favorable_gods,
                    unfavorable_gods=facts.unfavorable_gods,
                    score=facts.score,
                    priority=facts.priority,
                    reason=facts.reasoning,
                    description=facts.reasoning,
                )
            )

        candidate_dicts = [self._match_to_dict(item) for item in matched]
        winner_dict = resolver.resolve(candidate_dicts) if candidate_dicts else None
        winner = None
        if winner_dict is not None:
            winner = next(
                (
                    item
                    for item in matched
                    if item.rule_id == str(winner_dict.get("rule_id") or "")
                    and item.rule_id
                ),
                None,
            )
            if winner is None and matched:
                # Fallback by comparing useful_god + score.
                for item in matched:
                    if item.useful_god == str(winner_dict.get("useful_god") or ""):
                        winner = item
                        break
            if winner is None and matched:
                winner = matched[0]

        useful_god = (
            winner.useful_god
            if winner is not None and winner.useful_god
            else facts.useful_god
        )
        favorable = (
            winner.favorable_gods
            if winner is not None and winner.favorable_gods
            else facts.favorable_gods
        )
        unfavorable = (
            winner.unfavorable_gods
            if winner is not None and winner.unfavorable_gods
            else facts.unfavorable_gods
        )
        score = (
            float(winner.score)
            if winner is not None and winner.score
            else facts.score
        )
        priority = (
            int(winner.priority)
            if winner is not None and winner.priority
            else facts.priority
        )
        reasoning = ""
        if winner is not None:
            reasoning = winner.reason or winner.description
        if not reasoning:
            reasoning = facts.reasoning

        # Supporting elements: Pack 02 buckets + favorable gods as support set.
        supporting = tuple(
            dict.fromkeys(
                [
                    *facts.supporting_elements,
                    *facts.support_elements,
                    *facts.resource_elements,
                    *facts.companion_elements,
                    *favorable,
                ]
            )
        )

        recommendations = list(facts.recommendations)
        if winner is not None and winner.reason and winner.reason not in recommendations:
            recommendations.append(winner.reason)

        matched_ids = list(facts.matched_rules)
        for item in matched:
            if item.rule_id:
                matched_ids.append(item.rule_id)
        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        logger.info(
            "useful_god_rule_engine_evaluated",
            extra={
                "useful_god": useful_god,
                "favorable_count": len(favorable),
                "unfavorable_count": len(unfavorable),
                "supporting_count": len(supporting),
                "matched_count": len(matched),
                "winner": None if winner is None else winner.rule_id,
            },
        )

        return UsefulGodRuleEngineResult(
            useful_god=useful_god,
            favorable_gods=favorable,
            unfavorable_gods=unfavorable,
            supporting_elements=supporting,
            score=score,
            priority=priority,
            matched_candidates=tuple(matched),
            winner=winner,
            matched_rule_ids=tuple(ordered_ids),
            recommendations=tuple(recommendations),
            reasoning=reasoning,
        )

    def _has_match_context(
        self,
        facts: UsefulGodFacts,
        rule: dict[str, Any],
    ) -> bool:
        """Skip rules whose conditions lack required Pack 02 context."""
        conditions = self.matcher.parse_conditions(rule.get("conditions"))
        if not conditions:
            return True
        for cond in conditions:
            field = str(cond.get("field") or "")
            op = str(cond.get("operator") or "")
            current = getattr(facts, field, None)
            if current is None or current == "" or current == ():
                if op in {"contains", "not_contains", "in", "not_in"}:
                    return False
                if op in {"==", "!=", ">", ">=", "<", "<="}:
                    return False
        return True

    def _safe_match(self, facts: UsefulGodFacts, rule: dict[str, Any]) -> bool:
        """Match Pack 01 rule; missing fields never raise."""
        try:
            return bool(self.matcher.match(facts, rule))
        except (TypeError, ValueError, KeyError) as exc:
            logger.debug(
                "useful_god_rule_match_skipped",
                extra={
                    "rule_id": str(rule.get("rule_id") or ""),
                    "error": str(exc),
                },
            )
            return False

    def _is_active(self, rule: dict[str, Any]) -> bool:
        """Return True when Pack 01 rule is active/enabled."""
        if str(rule.get("status") or "active").lower() not in {"active", "true", "1"}:
            return False
        enabled = rule.get("enabled", True)
        if isinstance(enabled, str):
            return enabled.strip().lower() in {"1", "true", "yes", "y"}
        return bool(enabled)

    def _get_grouped_rules(self) -> dict[str, list[dict[str, Any]]]:
        """Lazy-load Pack 01 rule groups."""
        if self._grouped is None:
            self._grouped = self.loader.load_rule_groups()
        return self._grouped

    def _get_priority_resolver(self) -> PriorityResolver:
        """Lazy-load Pack 01 priority resolver."""
        if self._priority_resolver is None:
            if self._priority_rules is None:
                self._priority_rules = self.loader.load_priority_rules()
            self._priority_resolver = PriorityResolver(self._priority_rules)
        return self._priority_resolver

    def _to_match(
        self,
        rule: dict[str, Any],
        *,
        group_name: str,
    ) -> UsefulGodRuleMatch:
        """Convert Pack 01 CSV row to UsefulGodRuleMatch."""
        return UsefulGodRuleMatch(
            rule_id=str(rule.get("rule_id") or ""),
            rule_group=str(rule.get("rule_group") or group_name),
            useful_god=str(rule.get("useful_god") or ""),
            favorable_gods=self._parse_list(rule.get("favorable_gods")),
            unfavorable_gods=self._parse_list(rule.get("unfavorable_gods")),
            score=float(rule.get("score") or 0.0),
            priority=int(rule.get("priority") or 0),
            reason=str(rule.get("reason") or ""),
            description=str(rule.get("description") or ""),
        )

    @staticmethod
    def _match_to_dict(item: UsefulGodRuleMatch) -> dict[str, Any]:
        """Convert match to PriorityResolver candidate dict."""
        return {
            "rule_id": item.rule_id,
            "rule_group": item.rule_group,
            "useful_god": item.useful_god,
            "favorable_gods": list(item.favorable_gods),
            "unfavorable_gods": list(item.unfavorable_gods),
            "score": item.score,
            "priority": item.priority,
            "reason": item.reason,
            "description": item.description,
        }

    @staticmethod
    def _parse_list(raw: Any) -> tuple[str, ...]:
        """Parse JSON list / CSV cell into string tuple."""
        if raw is None:
            return ()
        if isinstance(raw, (list, tuple, set, frozenset)):
            return tuple(str(item) for item in raw if item not in (None, ""))
        if isinstance(raw, str):
            text = raw.strip()
            if not text:
                return ()
            if text.startswith("["):
                try:
                    parsed = json.loads(text)
                except json.JSONDecodeError:
                    return (text,)
                if isinstance(parsed, list):
                    return tuple(str(item) for item in parsed if item not in (None, ""))
            return (text,)
        return ()
