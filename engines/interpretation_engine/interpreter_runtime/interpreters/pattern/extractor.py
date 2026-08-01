"""Extract pattern facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.pattern.constants import (
    FOLLOW_KEYS,
    MONTH_BRANCH_TEN_GOD_KEYS,
    PATTERN_KEYS,
    PATTERN_MODULE_IDS,
    PRIORITY_KEYS,
    SCORE_KEYS,
    STATUS_KEYS,
    STRENGTH_LEVEL_KEYS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PatternFacts:
    """Normalized pattern facts extracted from FinalResult."""

    main_pattern: str = ""
    final_pattern: str = ""
    status: str = ""
    score: float = 0.0
    priority: int = 0
    follow_type: str = ""
    candidate_patterns: tuple[str, ...] = ()
    validated_patterns: tuple[str, ...] = ()
    secondary_patterns: tuple[str, ...] = ()
    matched_rules: tuple[str, ...] = ()
    month_branch_ten_god: str = ""
    month_branch: str = ""
    day_master: str = ""
    strength_level: str = ""
    ten_gods_list: tuple[str, ...] = ()
    confidence: float = 0.0
    reasoning: str = ""
    description: str = ""
    cach_cuc: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class PatternFactExtractor:
    """Read-only extractor: FinalResult → PatternFacts.

    Does not call PatternEngine.calculate. Reads Pack 02 payloads only.
    """

    def extract(self, final_result: FinalResult) -> PatternFacts:
        """Extract pattern facts from FinalResult module/stage payloads."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_pattern_scores(final_result):
            return PatternFacts(found=False)

        main_pattern = self._first_str(payload, PATTERN_KEYS, default="")
        final_pattern = str(
            payload.get("final_pattern")
            or payload.get("main_pattern")
            or main_pattern
            or ""
        )
        status = self._first_str(payload, STATUS_KEYS, default="")
        if not status:
            if payload.get("success") is True:
                status = "SUCCESS"
            elif payload.get("success") is False:
                status = "FAIL"

        score = self._first_float(payload, SCORE_KEYS, default=0.0)
        priority = int(self._first_float(payload, PRIORITY_KEYS, default=0.0))
        follow_type = self._first_str(payload, FOLLOW_KEYS, default="")
        month_branch_ten_god = self._first_str(
            payload, MONTH_BRANCH_TEN_GOD_KEYS, default=""
        )
        strength_level = self._first_str(payload, STRENGTH_LEVEL_KEYS, default="")

        score = self._merge_dimension(
            final_result, score, ("pattern", "pattern_score", "score")
        )

        candidates = self._as_str_tuple(
            payload.get("candidate_patterns") or payload.get("candidates")
        )
        validated = self._as_str_tuple(
            payload.get("validated_patterns") or payload.get("validated")
        )
        secondary = self._as_str_tuple(
            payload.get("secondary_patterns") or payload.get("secondary")
        )
        matched = self._as_str_tuple(
            payload.get("matched_rules") or payload.get("matched_rule_ids")
        )
        ten_gods = self._as_str_tuple(
            payload.get("ten_gods_list") or payload.get("ten_gods")
        )

        found = any(
            (
                bool(payload),
                bool(main_pattern),
                bool(final_pattern),
                bool(candidates),
                bool(matched),
                bool(month_branch_ten_god),
                score != 0.0,
            )
        )

        facts = PatternFacts(
            main_pattern=main_pattern,
            final_pattern=final_pattern,
            status=status,
            score=score,
            priority=priority,
            follow_type=follow_type,
            candidate_patterns=candidates,
            validated_patterns=validated,
            secondary_patterns=secondary,
            matched_rules=matched,
            month_branch_ten_god=month_branch_ten_god,
            month_branch=str(payload.get("month_branch") or ""),
            day_master=str(payload.get("day_master") or ""),
            strength_level=strength_level,
            ten_gods_list=ten_gods,
            confidence=self._as_float(payload.get("confidence"), default=0.0),
            reasoning=str(
                payload.get("reasoning")
                or payload.get("reason")
                or payload.get("success_reason")
                or ""
            ),
            description=str(payload.get("description") or ""),
            cach_cuc=str(payload.get("cach_cuc") or ""),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "pattern_facts_extracted",
            extra={
                "found": facts.found,
                "main_pattern": facts.main_pattern,
                "final_pattern": facts.final_pattern,
                "status": facts.status,
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge pattern-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in PATTERN_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in PATTERN_MODULE_IDS or stage_id in {
                        "classify",
                        "match",
                        "priority",
                        "resolve",
                    }:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in PATTERN_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in PATTERN_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                value = nested.get("pattern")
                if isinstance(value, Mapping):
                    merged.update(dict(value))

        for key in ("pattern", "pattern_result", "pattern_section", "rule_context"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                if key == "rule_context":
                    nested_pattern = value.get("pattern")
                    if isinstance(nested_pattern, Mapping):
                        merged.update(dict(nested_pattern))
                else:
                    merged.update(dict(value))

        return merged

    def _has_pattern_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include a pattern dimension."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if "pattern" in dimension or dimension in {"cach_cuc", "follow"}:
                return True
        analysis = final_result.analysis_result
        if analysis is None:
            return False
        for score in getattr(analysis, "scores", ()) or ():
            dimension = str(getattr(score, "dimension", "")).lower()
            if "pattern" in dimension:
                return True
        return False

    def _merge_dimension(
        self,
        final_result: FinalResult,
        current: float,
        dimensions: tuple[str, ...],
    ) -> float:
        """Prefer explicit AnalysisScore dimensions when present."""
        wanted = {item.lower() for item in dimensions}
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if dimension in wanted:
                return self._as_float(getattr(score, "value", current), default=current)
        analysis = final_result.analysis_result
        if analysis is not None:
            for score in getattr(analysis, "scores", ()) or ():
                dimension = str(getattr(score, "dimension", "")).lower()
                if dimension in wanted:
                    return self._as_float(
                        getattr(score, "value", current), default=current
                    )
        return current

    @staticmethod
    def _mapping(value: Any) -> dict[str, Any]:
        if isinstance(value, Mapping):
            return dict(value)
        to_portal = getattr(value, "to_portal_dict", None)
        if callable(to_portal):
            portal = to_portal()
            if isinstance(portal, Mapping):
                return dict(portal)
        return {}

    @staticmethod
    def _first_str(
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
        *,
        default: str,
    ) -> str:
        for key in keys:
            if key in payload and payload[key] not in (None, ""):
                return str(payload[key])
        return default

    @staticmethod
    def _first_float(
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
        *,
        default: float,
    ) -> float:
        for key in keys:
            if key in payload and payload[key] not in (None, ""):
                return PatternFactExtractor._as_float(payload[key], default=default)
        return default

    @staticmethod
    def _as_float(value: Any, *, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _as_str_tuple(value: Any) -> tuple[str, ...]:
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,) if value else ()
        if isinstance(value, (list, tuple, set, frozenset)):
            return tuple(str(item) for item in value if item not in (None, ""))
        return ()
