"""Extract season facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.season.constants import (
    CLIMATE_KEYS,
    MONTH_BRANCH_KEYS,
    QI_STAGE_KEYS,
    SEASON_KEYS,
    SEASON_MODULE_IDS,
    SEASON_SCORE_KEYS,
    TEMPERATURE_LEVEL_KEYS,
    TEMPERATURE_SCORE_KEYS,
    VN_SEASON_MAP,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SeasonFacts:
    """Normalized season facts extracted from FinalResult."""

    season: str = ""
    month_branch: str = ""
    qi_stage: str = ""
    climate_type: str = ""
    temperature_level: str = ""
    season_score: float = 0.0
    temperature_score: float = 0.0
    month_status: str = ""
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    reasoning: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False

    # Matcher-compatible aliases (Pack 01 temperature rules).
    @property
    def season_phase(self) -> str:
        """Qi stage alias used by Pack 01 season rules."""
        return self.qi_stage

    @property
    def climate(self) -> str:
        """Climate alias."""
        return self.climate_type

    @property
    def temperature_type(self) -> str:
        """Strength/Pattern climate alias."""
        return self.climate_type


class SeasonFactExtractor:
    """Read-only extractor: FinalResult → SeasonFacts.

    Does not recalculate BaZi season maps. Reads Pack 02 payloads only.
    """

    def extract(self, final_result: FinalResult) -> SeasonFacts:
        """Extract season / climate / month-branch facts from FinalResult."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_season_scores(final_result):
            return SeasonFacts(found=False)

        season = self._normalize_season(
            self._first_str(payload, SEASON_KEYS, default="")
        )
        month_branch = self._first_str(payload, MONTH_BRANCH_KEYS, default="")
        qi_stage = self._first_str(payload, QI_STAGE_KEYS, default="")
        climate = self._first_str(payload, CLIMATE_KEYS, default="")
        temperature_level = self._first_str(
            payload, TEMPERATURE_LEVEL_KEYS, default=""
        )
        season_score = self._first_float(payload, SEASON_SCORE_KEYS, default=0.0)
        temperature_score = self._first_float(
            payload, TEMPERATURE_SCORE_KEYS, default=0.0
        )

        season_score = self._merge_dimension(
            final_result, season_score, ("season", "season_score", "season_strength")
        )
        temperature_score = self._merge_dimension(
            final_result,
            temperature_score,
            ("temperature", "temperature_score", "climate"),
        )

        matched = self._as_str_tuple(
            payload.get("matched_rules") or payload.get("matched_rule_ids")
        )
        recommendations = self._as_str_tuple(
            payload.get("recommendations") or payload.get("recommendation")
        )
        confidence = self._as_float(payload.get("confidence"), default=0.0)
        reasoning = str(payload.get("reasoning") or payload.get("reason") or "")
        month_status = str(
            payload.get("month_status") or payload.get("season_status") or ""
        )

        found = any(
            (
                bool(payload),
                bool(season),
                bool(month_branch),
                bool(qi_stage),
                bool(climate),
                bool(temperature_level),
                season_score != 0.0,
                temperature_score != 0.0,
                bool(matched),
            )
        )

        facts = SeasonFacts(
            season=season,
            month_branch=month_branch,
            qi_stage=qi_stage,
            climate_type=climate,
            temperature_level=temperature_level,
            season_score=season_score,
            temperature_score=temperature_score,
            month_status=month_status,
            confidence=confidence,
            matched_rules=matched,
            recommendations=recommendations,
            reasoning=reasoning,
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "season_facts_extracted",
            extra={
                "found": facts.found,
                "season": facts.season,
                "month_branch": facts.month_branch,
                "qi_stage": facts.qi_stage,
                "climate_type": facts.climate_type,
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge season-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in SEASON_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in SEASON_MODULE_IDS or stage_id in {
                        "season",
                        "climate",
                        "classify",
                        "score",
                    }:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in SEASON_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in SEASON_MODULE_IDS or stage_id in {"season", "climate"}:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                for key in ("season", "temperature", "climate", "calendar"):
                    value = nested.get(key)
                    if isinstance(value, Mapping):
                        merged.update(dict(value))

        for key in (
            "season",
            "season_result",
            "temperature",
            "temperature_result",
            "climate",
            "calendar",
        ):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_season_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include season/climate dimensions."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if any(
                token in dimension
                for token in ("season", "climate", "temperature", "qi_stage")
            ):
                return True
        analysis = final_result.analysis_result
        if analysis is None:
            return False
        for score in getattr(analysis, "scores", ()) or ():
            dimension = str(getattr(score, "dimension", "")).lower()
            if "season" in dimension or "temperature" in dimension:
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

    def _normalize_season(self, value: str) -> str:
        """Normalize Vietnamese / English season labels to Pack 01 tokens."""
        text = str(value or "").strip()
        if not text:
            return ""
        lower = text.lower()
        if lower in {"spring", "summer", "autumn", "winter", "fall"}:
            return "autumn" if lower == "fall" else lower
        mapped = VN_SEASON_MAP.get(lower)
        if mapped:
            return mapped
        return text

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
                return SeasonFactExtractor._as_float(payload[key], default=default)
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
