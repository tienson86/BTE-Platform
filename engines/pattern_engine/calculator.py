"""
Pattern Calculator.

Decision pipeline:

  Candidate Detection
        ↓
  Validation
        ↓
  Conflict Resolution
        ↓
  Priority Resolution  (Priority Engine — no duplicated priority logic)
        ↓
  Final Pattern Selection
"""

from __future__ import annotations

import json
import logging
from typing import Any

import pandas as pd

from engines.priority_engine import PriorityService

from .calculators.follow_pattern import FollowPatternCalculator
from .conflict import (
    category_section,
    pattern_code,
    resolve_exclusive_conflicts,
)
from .loader import PatternLoader
from .matcher import PatternMatcher
from .validator import PatternValidator

logger = logging.getLogger(__name__)

# Map FollowPatternCalculator labels → follow override pattern codes.
_FOLLOW_LABEL_TO_PATTERN: dict[str, str] = {
    "Tòng Tài": "tong_tai",
    "Tòng Quan": "tong_quan",
    "Tòng Sát": "tong_sat",
    "Tòng Nhi": "tong_nhi",
    "Tòng Ấn": "tong_an",
    "Tòng Vượng": "tong_vuong",
    "Tòng Cường": "tong_vuong",
    "Tòng Thế": "tong_vuong",
}
class PatternCalculator:

    def __init__(self, loader: PatternLoader):
        self.loader = loader
        self.matcher = PatternMatcher()
        self.follow_calculator = FollowPatternCalculator()
        self._priority_service = PriorityService.for_matched_rules(
            max_rules_per_section=1,
        )

    def calculate(self, context: Any) -> dict[str, Any]:
        """Run the full Pattern decision pipeline."""
        empty = self._empty_result()

        if not self.loader.rules_exist():
            empty["success"] = False
            empty["error"] = (
                "rules.csv / 01_main_pattern.csv not found "
                f"in {self.loader.database_path}"
            )
            empty["reason"] = empty["error"]
            empty["failure_reason"] = empty["error"]
            return empty

        df = self.loader.load_rules()
        PatternValidator.validate_dataframe(df)
        rules = [self._normalize_rule(raw) for raw in df.to_dict("records")]

        # ---- 1. Candidate Detection (collect only; do not eliminate) ----
        candidates = self.detect_candidates(context, rules)

        # ---- 2. Validation ----
        follow_type = self.follow_calculator.detect(context)
        validated, rejected = self.validate_candidates(
            candidates,
            follow_type=follow_type,
        )

        # ---- 3. Conflict Resolution (exclusive groups) ----
        conflict_survivors, conflict_discarded = resolve_exclusive_conflicts(
            validated
        )

        # ---- 4. Priority Resolution (Priority Engine) ----
        resolved, priority_discarded = self.resolve_priority(conflict_survivors)

        # ---- 5. Final Pattern Selection ----
        return self.select_final(
            candidates=candidates,
            validated=validated,
            resolved=resolved,
            follow_type=follow_type,
            rejected=rejected,
            conflict_discarded=conflict_discarded,
            priority_discarded=priority_discarded,
        )

    # ================================================================
    # Pipeline stages
    # ================================================================

    def detect_candidates(
        self,
        context: Any,
        rules: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Collect every matching enabled rule — no elimination."""
        candidates: list[dict[str, Any]] = []
        for rule in rules:
            if not rule.get("enabled", True):
                continue
            if not self.matcher.match(context, rule):
                continue
            item = dict(rule)
            item["section"] = category_section(item)
            # Priority Engine uses confidence as secondary sort key.
            item["confidence"] = float(item.get("score", 0) or 0)
            candidates.append(item)
        return candidates

    def validate_candidates(
        self,
        candidates: list[dict[str, Any]],
        *,
        follow_type: str | None,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Verify candidates; reject invalid ones."""
        validated: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []

        # Follow rules can match vacuously on empty ten_gods_list; they must
        # not suppress the fallback when no real main/special/combination hit.
        has_substantive = any(
            (not self._is_fallback(item) and not self._is_follow_rule(item))
            for item in candidates
        )
        expected_follow = (
            _FOLLOW_LABEL_TO_PATTERN.get(str(follow_type or "").strip())
            if follow_type
            else None
        )

        for item in candidates:
            reason = self._validation_failure(
                item,
                has_substantive=has_substantive,
                follow_type=follow_type,
                expected_follow_pattern=expected_follow or None,
            )
            if reason:
                rejected.append({**item, "_reject_reason": reason})
                continue
            try:
                PatternValidator.validate_rule(item)
            except ValueError as exc:
                rejected.append({**item, "_reject_reason": str(exc)})
                continue
            validated.append(item)

        return validated, rejected

    def resolve_priority(
        self,
        candidates: list[dict[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Delegate ranking / diversity to Priority Engine."""
        if not candidates:
            return [], []

        prepared: list[dict[str, Any]] = []
        for item in candidates:
            row = dict(item)
            row.setdefault("section", category_section(row))
            row.setdefault("confidence", float(row.get("score", 0) or 0))
            row.setdefault(
                "description",
                row.get("description") or row.get("pattern") or row.get("rule_id"),
            )
            prepared.append(row)

        try:
            resolution = self._priority_service.resolve_matched_interpretation_rules(
                prepared
            )
        except Exception:
            logger.exception(
                "Priority Engine failed for patterns; falling back to priority sort"
            )
            ranked = sorted(
                prepared,
                key=lambda r: (
                    float(r.get("priority", 0) or 0),
                    float(r.get("score", 0) or 0),
                ),
                reverse=True,
            )
            return ranked[:1], ranked[1:]

        resolved = [dict(rule) for rule in resolution.resolved_rules]
        discarded = [
            {
                "rule_id": item.rule_id,
                "pattern": next(
                    (
                        pattern_code(c)
                        for c in prepared
                        if str(c.get("rule_id")) == item.rule_id
                    ),
                    "",
                ),
                "_discard_reason": item.reason,
                "_kept_rule_id": item.kept_rule_id,
                "_detail": item.detail,
            }
            for item in resolution.discarded_rules
        ]
        return resolved, discarded

    def select_final(
        self,
        *,
        candidates: list[dict[str, Any]],
        validated: list[dict[str, Any]],
        resolved: list[dict[str, Any]],
        follow_type: str | None,
        rejected: list[dict[str, Any]],
        conflict_discarded: list[dict[str, Any]],
        priority_discarded: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Build PatternResult payload from resolved winners."""
        result = self._empty_result()
        result["follow_type"] = follow_type
        result["candidate_patterns"] = self._pattern_codes(candidates)
        result["validated_patterns"] = self._pattern_codes(validated)
        result["matched_rules"] = [
            str(item.get("rule_id"))
            for item in candidates
            if item.get("rule_id") is not None
        ]
        result["rejected_rules"] = [
            str(item.get("rule_id"))
            for item in rejected
            if item.get("rule_id") is not None
        ]
        result["discarded_rules"] = [
            {
                "rule_id": item.get("rule_id"),
                "pattern": pattern_code(item),
                "reason": item.get("_discard_reason") or item.get("_reject_reason"),
                "kept_rule_id": item.get("_kept_rule_id"),
            }
            for item in (conflict_discarded + priority_discarded + rejected)
        ]

        if not resolved:
            result["success"] = False
            result["error"] = "no pattern rules matched"
            result["failure_reason"] = result["error"]
            result["reason"] = result["error"]
            result["confidence"] = 0.0
            return result

        winner = resolved[0]
        secondary = resolved[1:]
        final = pattern_code(winner) or None
        score = float(winner.get("score", 0) or 0)
        priority = int(winner.get("priority", 0) or 0)
        description = winner.get("description")

        result["success"] = True
        result["pattern"] = final
        result["final_pattern"] = final
        result["secondary_patterns"] = self._pattern_codes(secondary)
        result["score"] = score
        result["priority"] = priority
        result["description"] = description
        result["cach_cuc"] = description or final
        result["confidence"] = round(min(max(score / 100.0, 0.0), 1.0), 4)
        result["reason"] = str(description or f"Selected pattern '{final}'")
        result["success_reason"] = result["reason"]
        result["resolved_rule_count"] = len(resolved)
        result["candidate_count"] = len(candidates)
        result["validated_count"] = len(validated)
        return result

    # ================================================================
    # Helpers
    # ================================================================

    @staticmethod
    def _empty_result() -> dict[str, Any]:
        return {
            "success": True,
            "pattern": None,
            "final_pattern": None,
            "matched_rules": [],
            "score": 0,
            "priority": 0,
            "description": None,
            "cach_cuc": None,
            "follow_type": None,
            "candidate_patterns": [],
            "validated_patterns": [],
            "secondary_patterns": [],
            "confidence": 0.0,
            "reason": None,
            "rejected_rules": [],
            "discarded_rules": [],
            "resolved_rule_count": 0,
            "candidate_count": 0,
            "validated_count": 0,
            "success_reason": None,
            "failure_reason": None,
            "error": None,
        }

    @staticmethod
    def _pattern_codes(items: list[dict[str, Any]]) -> list[str]:
        codes: list[str] = []
        seen: set[str] = set()
        for item in items:
            code = pattern_code(item)
            if not code or code in seen:
                continue
            seen.add(code)
            codes.append(code)
        return codes

    @staticmethod
    def _is_fallback(item: dict[str, Any]) -> bool:
        rule_id = str(item.get("rule_id") or "")
        conditions = item.get("conditions") or []
        return rule_id == "pat_fallback" or (
            isinstance(conditions, list) and len(conditions) == 0
            and int(item.get("priority", 0) or 0) <= 1
        )

    @staticmethod
    def _is_follow_rule(item: dict[str, Any]) -> bool:
        source = str(item.get("source") or "")
        return source in ("follow_override", "03_follow_pattern.csv") or (
            pattern_code(item).startswith("tong_")
        )

    def _validation_failure(
        self,
        item: dict[str, Any],
        *,
        has_substantive: bool,
        follow_type: str | None,
        expected_follow_pattern: str | None,
    ) -> str | None:
        """Return rejection reason, or None when valid."""
        if not pattern_code(item):
            return "missing_pattern_code"

        if self._is_follow_rule(item):
            if not follow_type:
                return "follow_not_detected"
            if expected_follow_pattern and pattern_code(item) != expected_follow_pattern:
                return "follow_type_mismatch"

        if has_substantive and self._is_fallback(item):
            return "fallback_superseded"

        return None

    def _normalize_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        """Normalize CSV row types for matcher."""
        normalized = dict(rule)
        normalized["conditions"] = self._parse_conditions(normalized.get("conditions"))

        if "priority" in normalized:
            try:
                normalized["priority"] = int(normalized["priority"])
            except (TypeError, ValueError):
                normalized["priority"] = 0

        if "score" in normalized and normalized["score"] is not None:
            try:
                if pd.isna(normalized["score"]):
                    normalized["score"] = 0
                else:
                    normalized["score"] = float(normalized["score"])
            except TypeError:
                normalized["score"] = float(normalized["score"])

        if "enabled" in normalized:
            value = normalized["enabled"]
            if isinstance(value, str):
                normalized["enabled"] = value.strip().lower() in {
                    "1", "true", "yes", "y",
                }
            else:
                try:
                    normalized["enabled"] = bool(value) if not pd.isna(value) else True
                except TypeError:
                    normalized["enabled"] = bool(value)

        return normalized

    @staticmethod
    def _parse_conditions(raw: Any) -> list:
        """Parse conditions cell from CSV into list[dict]."""
        if raw is None:
            return []
        try:
            if pd.isna(raw):
                return []
        except TypeError:
            pass
        if isinstance(raw, list):
            return raw
        if isinstance(raw, str):
            text = raw.strip()
            if not text or text == "[]":
                return []
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return []
            if isinstance(parsed, list):
                return parsed
            return []
        return []
