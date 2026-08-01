"""Extract useful-god facts from Pack 02 FinalResult."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.useful_god.constants import (
    FAVORABLE_KEYS,
    PATTERN_KEYS,
    SEASON_KEYS,
    STRENGTH_LEVEL_KEYS,
    SUPPORTING_KEYS,
    TEMPERATURE_KEYS,
    UNFAVORABLE_KEYS,
    USEFUL_GOD_KEYS,
    USEFUL_GOD_MODULE_IDS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class UsefulGodFacts:
    """Normalized useful-god facts extracted from FinalResult."""

    useful_god: str = ""
    favorable_gods: tuple[str, ...] = ()
    unfavorable_gods: tuple[str, ...] = ()
    supporting_elements: tuple[str, ...] = ()
    support_elements: tuple[str, ...] = ()
    resource_elements: tuple[str, ...] = ()
    wealth_elements: tuple[str, ...] = ()
    officer_elements: tuple[str, ...] = ()
    output_elements: tuple[str, ...] = ()
    companion_elements: tuple[str, ...] = ()
    strength_level: str = ""
    season: str = ""
    temperature_level: str = ""
    main_pattern: str = ""
    follow_pattern: str = ""
    special_pattern: str = ""
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    reasoning: str = ""
    score: float = 0.0
    priority: int = 0
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class UsefulGodFactExtractor:
    """Read-only extractor: FinalResult → UsefulGodFacts.

    Does not call UsefulGodEngine.calculate. Reads Pack 02 payloads only.
    """

    def extract(self, final_result: FinalResult) -> UsefulGodFacts:
        """Extract useful/favorable/unfavorable/supporting facts."""
        payload = self._collect_payload(final_result)
        if not payload:
            return UsefulGodFacts(found=False)

        useful_god = self._first_str(payload, USEFUL_GOD_KEYS, default="")
        if not useful_god:
            gods = self._as_str_tuple(payload.get("useful_gods"))
            useful_god = gods[0] if gods else ""

        favorable = self._first_str_tuple(payload, FAVORABLE_KEYS)
        unfavorable = self._first_str_tuple(payload, UNFAVORABLE_KEYS)
        supporting = self._first_str_tuple(payload, SUPPORTING_KEYS)

        # Broader supporting element buckets from Pack 02 / context payloads.
        resource = self._as_str_tuple(payload.get("resource_elements"))
        wealth = self._as_str_tuple(payload.get("wealth_elements"))
        officer = self._as_str_tuple(payload.get("officer_elements"))
        output = self._as_str_tuple(payload.get("output_elements"))
        companion = self._as_str_tuple(payload.get("companion_elements"))
        support_elements = self._as_str_tuple(
            payload.get("support_elements") or supporting
        )
        if not supporting:
            supporting = tuple(
                dict.fromkeys([*support_elements, *resource, *companion])
            )

        found = any(
            (
                bool(payload),
                bool(useful_god),
                bool(favorable),
                bool(unfavorable),
                bool(supporting),
                bool(self._first_str(payload, STRENGTH_LEVEL_KEYS, default="")),
                bool(self._as_str_tuple(payload.get("matched_rules"))),
            )
        )

        facts = UsefulGodFacts(
            useful_god=useful_god,
            favorable_gods=favorable,
            unfavorable_gods=unfavorable,
            supporting_elements=supporting,
            support_elements=support_elements,
            resource_elements=resource,
            wealth_elements=wealth,
            officer_elements=officer,
            output_elements=output,
            companion_elements=companion,
            strength_level=self._first_str(payload, STRENGTH_LEVEL_KEYS, default=""),
            season=self._first_str(payload, SEASON_KEYS, default=""),
            temperature_level=self._first_str(payload, TEMPERATURE_KEYS, default=""),
            main_pattern=self._first_str(payload, PATTERN_KEYS, default=""),
            follow_pattern=str(
                payload.get("follow_pattern") or payload.get("follow_type") or ""
            ),
            special_pattern=str(payload.get("special_pattern") or ""),
            confidence=self._as_float(payload.get("confidence"), default=0.0),
            matched_rules=self._as_str_tuple(
                payload.get("matched_rules") or payload.get("matched_rule_ids")
            ),
            recommendations=self._as_str_tuple(
                payload.get("recommendations") or payload.get("recommendation")
            ),
            reasoning=str(payload.get("reasoning") or payload.get("reason") or ""),
            score=self._as_float(payload.get("score"), default=0.0),
            priority=int(self._as_float(payload.get("priority"), default=0.0)),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "useful_god_facts_extracted",
            extra={
                "found": facts.found,
                "useful_god": facts.useful_god,
                "favorable_count": len(facts.favorable_gods),
                "unfavorable_count": len(facts.unfavorable_gods),
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge useful-god payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in USEFUL_GOD_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in USEFUL_GOD_MODULE_IDS or stage_id in {
                        "classify",
                        "priority",
                        "flow",
                    }:
                        merged.update(self._mapping(stage.payload))

        # Also harvest related upstream module signals when present.
        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in {"strength", "pattern", "season", "temperature"}:
                payload = self._mapping(module.payload)
                if module_id == "strength" and "strength_level" not in merged:
                    level = payload.get("strength_level") or payload.get("level")
                    if level:
                        merged["strength_level"] = level
                if module_id == "pattern" and "main_pattern" not in merged:
                    pattern = (
                        payload.get("main_pattern")
                        or payload.get("final_pattern")
                        or payload.get("pattern")
                    )
                    if pattern:
                        merged["main_pattern"] = pattern
                    if payload.get("follow_type"):
                        merged.setdefault("follow_pattern", payload["follow_type"])
                if module_id in {"season", "temperature"}:
                    for key in ("season", "temperature_level", "climate_type"):
                        if key in payload and key not in merged:
                            merged[key] = payload[key]

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in USEFUL_GOD_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in USEFUL_GOD_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                value = nested.get("useful_god")
                if isinstance(value, Mapping):
                    merged.update(dict(value))

        for key in ("useful_god", "useful_god_result", "useful_god_section"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _first_str_tuple(
        self,
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> tuple[str, ...]:
        for key in keys:
            if key in payload and payload[key] not in (None, "", [], ()):
                return self._as_str_tuple(payload[key])
        return ()

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
            text = value.strip()
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
        if isinstance(value, (list, tuple, set, frozenset)):
            return tuple(str(item) for item in value if item not in (None, ""))
        return ()
