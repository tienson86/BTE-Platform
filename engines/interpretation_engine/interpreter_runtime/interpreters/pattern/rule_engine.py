"""Pattern Interpretation Rule Engine.

Uses Pattern Engine staged APIs:
- Pattern Matching  → PatternMatcher
- Pattern Resolution → resolve_exclusive_conflicts
- Pattern Priority   → PriorityResolver

Pack 01 database: ``database/14_pattern`` via PatternLoader.
Does not call PatternEngine.calculate (no BaZi re-score).
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from engines.pattern_engine.conflict import resolve_exclusive_conflicts
from engines.pattern_engine.loader import PatternLoader
from engines.pattern_engine.matcher import PatternMatcher
from engines.pattern_engine.models.pattern_rule import PatternRule
from engines.pattern_engine.rules.priority import PriorityResolver

from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.extractor import (
    PatternFacts,
)

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_PACK01_PATTERN_DB = str(_REPO_ROOT / "database" / "14_pattern")


@dataclass(slots=True)
class PatternRuleMatch:
    """Matched / resolved Pack 01 pattern candidate."""

    rule_id: str
    pattern: str
    score: float
    priority: int
    description: str
    source: str = ""


@dataclass(slots=True)
class PatternRuleEngineResult:
    """Rule-engine output for Pattern Interpreter."""

    main_pattern: str
    final_pattern: str
    status: str
    score: float
    priority: int
    follow_type: str
    candidate_patterns: tuple[str, ...]
    validated_patterns: tuple[str, ...]
    secondary_patterns: tuple[str, ...]
    discarded_patterns: tuple[str, ...]
    matched_candidates: tuple[PatternRuleMatch, ...]
    resolved_candidates: tuple[PatternRuleMatch, ...]
    priority_winner: PatternRuleMatch | None
    matched_rule_ids: tuple[str, ...]
    reasoning: str
    description: str


class PatternInterpretationRuleEngine:
    """Rule Engine for Pattern Interpreter.

    Pipeline:
    Pattern Matching → Pattern Resolution → Pattern Priority
    """

    def __init__(
        self,
        *,
        database_path: str | None = None,
        loader: PatternLoader | None = None,
        matcher: PatternMatcher | None = None,
        priority_resolver: PriorityResolver | None = None,
    ) -> None:
        """Initialize with Pack 01 database path and Pattern Engine collaborators."""
        self.database_path = database_path or DEFAULT_PACK01_PATTERN_DB
        self.loader = loader or PatternLoader(self.database_path)
        self.matcher = matcher or PatternMatcher()
        self.priority_resolver = priority_resolver or PriorityResolver()
        self._rules: list[dict[str, Any]] | None = None

    def evaluate(self, facts: PatternFacts) -> PatternRuleEngineResult:
        """Evaluate pattern matching, resolution, and priority against facts."""
        rules = self._get_rules()

        # --- Pattern Matching ---
        matched = self._match_patterns(facts, rules)
        pack02_candidates = self._candidates_from_pack02(facts, rules)
        matched = self._merge_matches(matched, pack02_candidates)

        candidate_patterns = tuple(
            dict.fromkeys(
                [
                    *(facts.candidate_patterns),
                    *(item.pattern for item in matched if item.pattern),
                ]
            )
        )

        # --- Pattern Resolution (exclusive conflicts) ---
        candidate_dicts = [self._match_to_dict(item) for item in matched]
        survivors, discarded = resolve_exclusive_conflicts(candidate_dicts)
        resolved = tuple(self._dict_to_match(item) for item in survivors)
        discarded_patterns = tuple(
            str(item.get("pattern") or "")
            for item in discarded
            if item.get("pattern")
        )
        validated_patterns = tuple(
            dict.fromkeys(
                [
                    *(facts.validated_patterns),
                    *(item.pattern for item in resolved if item.pattern),
                ]
            )
        )

        # --- Pattern Priority ---
        priority_winner = self._resolve_priority(resolved)
        if priority_winner is None and facts.final_pattern:
            priority_winner = PatternRuleMatch(
                rule_id="",
                pattern=facts.final_pattern,
                score=facts.score,
                priority=facts.priority,
                description=facts.description or facts.reasoning,
                source="pack02",
            )

        final_pattern = (
            priority_winner.pattern
            if priority_winner is not None
            else (facts.final_pattern or facts.main_pattern)
        )
        main_pattern = facts.main_pattern or final_pattern
        score = (
            float(priority_winner.score)
            if priority_winner is not None and priority_winner.score
            else facts.score
        )
        priority = (
            int(priority_winner.priority)
            if priority_winner is not None and priority_winner.priority
            else facts.priority
        )
        description = (
            priority_winner.description
            if priority_winner is not None and priority_winner.description
            else (facts.description or facts.cach_cuc)
        )
        reasoning = facts.reasoning or description

        secondary = tuple(
            dict.fromkeys(
                [
                    *(facts.secondary_patterns),
                    *(
                        item.pattern
                        for item in resolved
                        if item.pattern and item.pattern != final_pattern
                    ),
                ]
            )
        )

        status = facts.status
        if not status:
            status = "SUCCESS" if final_pattern else "UNKNOWN"

        matched_ids = list(facts.matched_rules)
        for item in matched:
            if item.rule_id:
                matched_ids.append(item.rule_id)
        if priority_winner is not None and priority_winner.rule_id:
            matched_ids.append(priority_winner.rule_id)

        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        follow_type = facts.follow_type
        if not follow_type and final_pattern.startswith("tong_"):
            follow_type = final_pattern

        logger.info(
            "pattern_rule_engine_evaluated",
            extra={
                "final_pattern": final_pattern,
                "matched_count": len(matched),
                "resolved_count": len(resolved),
                "discarded_count": len(discarded_patterns),
                "priority_winner": None
                if priority_winner is None
                else priority_winner.rule_id,
            },
        )

        return PatternRuleEngineResult(
            main_pattern=main_pattern,
            final_pattern=final_pattern,
            status=status,
            score=score,
            priority=priority,
            follow_type=follow_type,
            candidate_patterns=candidate_patterns,
            validated_patterns=validated_patterns,
            secondary_patterns=secondary,
            discarded_patterns=discarded_patterns,
            matched_candidates=matched,
            resolved_candidates=resolved,
            priority_winner=priority_winner,
            matched_rule_ids=tuple(ordered_ids),
            reasoning=reasoning,
            description=description,
        )

    def _match_patterns(
        self,
        facts: PatternFacts,
        rules: list[dict[str, Any]],
    ) -> tuple[PatternRuleMatch, ...]:
        """Pattern Matching: evaluate Pack 01 rules against fact context."""
        matches: list[PatternRuleMatch] = []
        for rule in rules:
            if not rule.get("enabled", True):
                continue
            if not self._has_match_context(facts, rule):
                continue
            if not self._safe_match(facts, rule):
                continue
            matches.append(self._dict_to_match(rule))
        matches.sort(key=lambda item: (item.priority, item.score), reverse=True)
        return tuple(matches)

    def _has_match_context(
        self,
        facts: PatternFacts,
        rule: dict[str, Any],
    ) -> bool:
        """Skip rules whose list/field conditions lack Pack 02 context.

        Prevents false positives such as ``not_contains`` on an empty
        ``ten_gods_list`` matching follow patterns unintentionally.
        """
        conditions = rule.get("conditions") or []
        if not conditions:
            # Unconditional fallback rules are allowed.
            return True
        for cond in conditions:
            if not isinstance(cond, dict):
                return False
            field = str(cond.get("field") or "")
            op = str(cond.get("operator") or "")
            current = getattr(facts, field, None)
            if current is None or current == "" or current == ():
                # Missing scalar / empty collection cannot safely evaluate
                # contains / not_contains / in / not_in semantics.
                if op in {"contains", "not_contains", "in", "not_in"}:
                    return False
                if op in {"==", "!=", ">", ">=", "<", "<="}:
                    return False
        return True

    def _merge_matches(
        self,
        primary: tuple[PatternRuleMatch, ...],
        secondary: tuple[PatternRuleMatch, ...],
    ) -> tuple[PatternRuleMatch, ...]:
        """Merge match lists, preferring higher priority on duplicate keys."""
        by_key: dict[str, PatternRuleMatch] = {}
        for item in (*primary, *secondary):
            key = item.rule_id or item.pattern
            if not key:
                continue
            existing = by_key.get(key)
            if existing is None or (item.priority, item.score) > (
                existing.priority,
                existing.score,
            ):
                by_key[key] = item
        merged = list(by_key.values())
        merged.sort(key=lambda item: (item.priority, item.score), reverse=True)
        return tuple(merged)

    def _candidates_from_pack02(
        self,
        facts: PatternFacts,
        rules: list[dict[str, Any]],
    ) -> tuple[PatternRuleMatch, ...]:
        """Build candidates from Pack 02 pattern codes / matched rule ids."""
        by_id = {
            str(rule.get("rule_id") or ""): rule
            for rule in rules
            if rule.get("rule_id")
        }
        by_pattern: dict[str, list[dict[str, Any]]] = {}
        for rule in rules:
            code = str(rule.get("pattern") or "").strip().lower()
            if code:
                by_pattern.setdefault(code, []).append(rule)

        matches: list[PatternRuleMatch] = []
        for rule_id in facts.matched_rules:
            rule = by_id.get(str(rule_id))
            if rule is not None:
                matches.append(self._dict_to_match(rule))

        codes = [
            *facts.candidate_patterns,
            *facts.validated_patterns,
            facts.final_pattern,
            facts.main_pattern,
        ]
        for code in codes:
            normalized = str(code or "").strip().lower()
            if not normalized:
                continue
            for rule in by_pattern.get(normalized, ()):
                matches.append(self._dict_to_match(rule))

        # Deduplicate by rule_id/pattern.
        seen: set[str] = set()
        unique: list[PatternRuleMatch] = []
        for item in matches:
            key = item.rule_id or item.pattern
            if key in seen:
                continue
            seen.add(key)
            unique.append(item)
        unique.sort(key=lambda item: (item.priority, item.score), reverse=True)
        return tuple(unique)

    def _resolve_priority(
        self,
        resolved: tuple[PatternRuleMatch, ...],
    ) -> PatternRuleMatch | None:
        """Pattern Priority: select highest priority/score survivor."""
        if not resolved:
            return None
        pattern_rules = [
            PatternRule(
                rule_id=item.rule_id,
                pattern=item.pattern,
                priority=item.priority,
                score=item.score,
                description=item.description,
                enabled=True,
                source=item.source,
            )
            for item in resolved
        ]
        winner = self.priority_resolver.resolve(pattern_rules)
        if winner is None:
            return None
        for item in resolved:
            if item.rule_id == winner.rule_id or (
                not winner.rule_id and item.pattern == winner.pattern
            ):
                return item
        return PatternRuleMatch(
            rule_id=winner.rule_id,
            pattern=winner.pattern,
            score=float(winner.score),
            priority=int(winner.priority),
            description=winner.description,
            source=winner.source,
        )

    def _safe_match(self, facts: PatternFacts, rule: dict[str, Any]) -> bool:
        """Match Pack 01 rule; missing fields / bad ops never raise."""
        try:
            return bool(self.matcher.match(facts, rule))
        except (TypeError, ValueError, KeyError) as exc:
            logger.debug(
                "pattern_rule_match_skipped",
                extra={
                    "rule_id": str(rule.get("rule_id") or ""),
                    "error": str(exc),
                },
            )
            return False

    def _get_rules(self) -> list[dict[str, Any]]:
        """Lazy-load and normalize Pack 01 pattern rules."""
        if self._rules is None:
            df = self.loader.load_rules()
            self._rules = [self._normalize_rule(row) for row in df.to_dict("records")]
        return self._rules

    def _normalize_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        """Normalize CSV row types for PatternMatcher."""
        normalized = dict(rule)
        normalized["conditions"] = self._parse_conditions(normalized.get("conditions"))
        try:
            normalized["priority"] = int(normalized.get("priority") or 0)
        except (TypeError, ValueError):
            normalized["priority"] = 0
        try:
            score = normalized.get("score")
            if score is None or (isinstance(score, float) and pd.isna(score)):
                normalized["score"] = 0.0
            else:
                normalized["score"] = float(score)
        except (TypeError, ValueError):
            normalized["score"] = 0.0
        enabled = normalized.get("enabled", True)
        if isinstance(enabled, str):
            normalized["enabled"] = enabled.strip().lower() in {
                "1",
                "true",
                "yes",
                "y",
            }
        else:
            try:
                normalized["enabled"] = (
                    bool(enabled) if not pd.isna(enabled) else True
                )
            except TypeError:
                normalized["enabled"] = bool(enabled)
        return normalized

    @staticmethod
    def _parse_conditions(raw: Any) -> list[dict[str, Any]]:
        """Parse conditions cell from CSV into list[dict]."""
        if raw is None:
            return []
        try:
            if pd.isna(raw):
                return []
        except TypeError:
            pass
        if isinstance(raw, list):
            return [item for item in raw if isinstance(item, dict)]
        if isinstance(raw, str):
            text = raw.strip()
            if not text:
                return []
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return []
            if isinstance(parsed, list):
                return [item for item in parsed if isinstance(item, dict)]
            return []
        return []

    @staticmethod
    def _match_to_dict(item: PatternRuleMatch) -> dict[str, Any]:
        """Convert match to conflict-resolver candidate dict."""
        return {
            "rule_id": item.rule_id,
            "pattern": item.pattern,
            "score": item.score,
            "priority": item.priority,
            "description": item.description,
            "source": item.source,
        }

    @staticmethod
    def _dict_to_match(rule: dict[str, Any]) -> PatternRuleMatch:
        """Convert rule/candidate dict to PatternRuleMatch."""
        return PatternRuleMatch(
            rule_id=str(rule.get("rule_id") or ""),
            pattern=str(rule.get("pattern") or ""),
            score=float(rule.get("score") or 0.0),
            priority=int(rule.get("priority") or 0),
            description=str(rule.get("description") or ""),
            source=str(rule.get("source") or ""),
        )
