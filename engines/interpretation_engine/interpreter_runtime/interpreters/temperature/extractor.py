"""Extract temperature facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.temperature.constants import (
    BALANCE_KEYS,
    COLD_KEYS,
    DRY_KEYS,
    DRYNESS_LEVEL_KEYS,
    HOT_KEYS,
    HUMIDITY_LEVEL_KEYS,
    LEVEL_KEYS,
    SCORE_KEYS,
    TEMPERATURE_MODULE_IDS,
    WET_KEYS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class TemperatureFacts:
    """Normalized temperature facts extracted from FinalResult."""

    cold_score: float = 0.0
    warm_score: float = 0.0
    dry_score: float = 0.0
    humid_score: float = 0.0
    balance_score: float | None = None
    temperature_score: float = 0.0
    temperature_level: str = ""
    dryness_level: str = ""
    humidity_level: str = ""
    season: str = ""
    climate_type: str = ""
    month_branch: str = ""
    fire_count: int | None = None
    water_count: int | None = None
    earth_count: int | None = None
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    reasoning: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False

    # Matcher-compatible aliases for Pack 01 balance / dryness / humidity rules.
    @property
    def hot_score(self) -> float:
        """Hot alias for warm_score."""
        return self.warm_score

    @property
    def wet_score(self) -> float:
        """Wet alias for humid_score."""
        return self.humid_score


class TemperatureFactExtractor:
    """Read-only extractor: FinalResult → TemperatureFacts.

    Does not call TemperatureEngine.calculate. Reads Pack 02 payloads only.
    """

    def extract(self, final_result: FinalResult) -> TemperatureFacts:
        """Extract cold/hot/dry/wet/balance facts from FinalResult."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_temperature_scores(final_result):
            return TemperatureFacts(found=False)

        cold = self._first_float(payload, COLD_KEYS, default=0.0)
        hot = self._first_float(payload, HOT_KEYS, default=0.0)
        dry = self._first_float(payload, DRY_KEYS, default=0.0)
        wet = self._first_float(payload, WET_KEYS, default=0.0)
        balance = self._first_float_optional(payload, BALANCE_KEYS)
        temperature_score = self._first_float(payload, SCORE_KEYS, default=0.0)
        temperature_level = self._first_str(payload, LEVEL_KEYS, default="")
        dryness_level = self._first_str(payload, DRYNESS_LEVEL_KEYS, default="")
        humidity_level = self._first_str(payload, HUMIDITY_LEVEL_KEYS, default="")

        cold = self._merge_dimension(final_result, cold, ("cold", "cold_score"))
        hot = self._merge_dimension(
            final_result, hot, ("hot", "warm", "warm_score", "hot_score")
        )
        dry = self._merge_dimension(
            final_result, dry, ("dry", "dry_score", "dryness")
        )
        wet = self._merge_dimension(
            final_result, wet, ("wet", "humid", "humid_score", "humidity")
        )
        temperature_score = self._merge_dimension(
            final_result,
            temperature_score,
            ("temperature", "temperature_score"),
        )

        matched = self._as_str_tuple(
            payload.get("matched_rules") or payload.get("matched_rule_ids")
        )
        recommendations = self._as_str_tuple(
            payload.get("recommendations") or payload.get("recommendation")
        )

        found = any(
            (
                bool(payload),
                cold != 0.0,
                hot != 0.0,
                dry != 0.0,
                wet != 0.0,
                balance is not None,
                temperature_score != 0.0,
                bool(temperature_level),
                bool(dryness_level),
                bool(humidity_level),
                bool(matched),
            )
        )

        facts = TemperatureFacts(
            cold_score=cold,
            warm_score=hot,
            dry_score=dry,
            humid_score=wet,
            balance_score=balance,
            temperature_score=temperature_score,
            temperature_level=temperature_level,
            dryness_level=dryness_level,
            humidity_level=humidity_level,
            season=str(payload.get("season") or ""),
            climate_type=str(
                payload.get("climate_type") or payload.get("temperature_type") or ""
            ),
            month_branch=str(payload.get("month_branch") or ""),
            fire_count=self._as_optional_int(payload.get("fire_count")),
            water_count=self._as_optional_int(payload.get("water_count")),
            earth_count=self._as_optional_int(payload.get("earth_count")),
            confidence=self._as_float(payload.get("confidence"), default=0.0),
            matched_rules=matched,
            recommendations=recommendations,
            reasoning=str(payload.get("reasoning") or payload.get("reason") or ""),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "temperature_facts_extracted",
            extra={
                "found": facts.found,
                "temperature_level": facts.temperature_level,
                "cold": facts.cold_score,
                "hot": facts.warm_score,
                "dry": facts.dry_score,
                "wet": facts.humid_score,
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge temperature-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in TEMPERATURE_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in TEMPERATURE_MODULE_IDS or stage_id in {
                        "classify",
                        "score",
                        "balance",
                        "dryness",
                        "humidity",
                    }:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in TEMPERATURE_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in TEMPERATURE_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                value = nested.get("temperature")
                if isinstance(value, Mapping):
                    merged.update(dict(value))

        for key in ("temperature", "temperature_result", "temperature_section"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_temperature_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include temperature dimensions."""
        tokens = ("temperature", "cold", "hot", "warm", "dry", "humid", "wet", "balance")
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if any(token in dimension for token in tokens):
                return True
        analysis = final_result.analysis_result
        if analysis is None:
            return False
        for score in getattr(analysis, "scores", ()) or ():
            dimension = str(getattr(score, "dimension", "")).lower()
            if any(token in dimension for token in tokens):
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
                return TemperatureFactExtractor._as_float(payload[key], default=default)
        return default

    @staticmethod
    def _first_float_optional(
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> float | None:
        for key in keys:
            if key in payload and payload[key] not in (None, ""):
                return TemperatureFactExtractor._as_float(payload[key], default=0.0)
        return None

    @staticmethod
    def _as_float(value: Any, *, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _as_optional_int(value: Any) -> int | None:
        if value in (None, ""):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _as_str_tuple(value: Any) -> tuple[str, ...]:
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,) if value else ()
        if isinstance(value, (list, tuple, set, frozenset)):
            return tuple(str(item) for item in value if item not in (None, ""))
        return ()
