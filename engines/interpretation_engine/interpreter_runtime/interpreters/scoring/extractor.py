"""Extract Scoring facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.constants import (
    CONFIDENCE_KEYS,
    DIMENSION_ALIASES,
    DIMENSION_KEYS,
    OVERALL_KEYS,
    QUALITY_KEYS,
    SCORING_MODULE_IDS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ScoringDimensionFact:
    """One dimension score fact from Pack 02."""

    dimension: str = ""
    value: float = 0.0
    unit: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ScoringFacts:
    """Normalized scoring facts extracted from FinalResult."""

    overall_score: float | None = None
    dimensions: tuple[ScoringDimensionFact, ...] = ()
    confidence_value: float | None = None
    confidence_level: str = ""
    quality_label: str = ""
    grade: str = ""
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class ScoringFactExtractor:
    """Read-only extractor: FinalResult -> ScoringFacts.

    Reads scoring module payloads and FinalResult.scores.
    Does not call ScoreEngine.calculate.
    """

    def extract(self, final_result: FinalResult) -> ScoringFacts:
        """Extract overall / dimension / confidence / quality facts."""
        payload = self._collect_payload(final_result)
        score_dims = self._dimensions_from_scores(final_result)
        if not payload and not score_dims and not final_result.scores:
            return ScoringFacts(found=False)

        payload_dims = self._parse_dimensions(
            self._first_mapping_or_list(payload, DIMENSION_KEYS)
        )
        dimensions = self._merge_dimensions(payload_dims, score_dims)

        overall = self._first_float_optional(payload, OVERALL_KEYS)
        if overall is None:
            overall = self._overall_from_scores(final_result)
        if overall is None and dimensions:
            # Leave None; rule engine may weight-aggregate from Pack 01.
            pass

        confidence_value = self._extract_confidence_value(payload, final_result)
        confidence_level = ""
        conf_obj = payload.get("confidence")
        if isinstance(conf_obj, Mapping):
            confidence_level = str(
                conf_obj.get("level") or conf_obj.get("confidence_level") or ""
            )

        quality_label = self._first_str(payload, QUALITY_KEYS)
        grade = str(payload.get("grade") or "")
        if not grade and quality_label and len(quality_label) <= 3:
            grade = quality_label

        found = any(
            (
                bool(payload),
                overall is not None,
                bool(dimensions),
                confidence_value is not None,
                bool(quality_label),
                bool(grade),
                bool(final_result.scores),
                bool(self._as_str_tuple(payload.get("matched_rules"))),
            )
        )
        if not found and payload and any(
            key in payload for key in (*OVERALL_KEYS, *DIMENSION_KEYS, *CONFIDENCE_KEYS)
        ):
            found = True

        facts = ScoringFacts(
            overall_score=overall,
            dimensions=dimensions,
            confidence_value=confidence_value,
            confidence_level=confidence_level,
            quality_label=quality_label,
            grade=grade,
            matched_rules=self._as_str_tuple(
                payload.get("matched_rules") or payload.get("matched_rule_ids")
            ),
            reasoning=str(payload.get("reasoning") or payload.get("reason") or ""),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "scoring_facts_extracted",
            extra={
                "found": facts.found,
                "overall_score": facts.overall_score,
                "dimension_count": len(facts.dimensions),
                "confidence_value": facts.confidence_value,
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge scoring-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in SCORING_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in SCORING_MODULE_IDS:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in SCORING_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in SCORING_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                for key in ("scoring", "score", "final_score"):
                    value = nested.get(key)
                    if isinstance(value, Mapping):
                        merged.update(dict(value))

        for key in ("scoring", "score_result", "final_score", "score"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _dimensions_from_scores(
        self, final_result: FinalResult
    ) -> tuple[ScoringDimensionFact, ...]:
        """Build dimension facts from FinalResult.scores."""
        items: list[ScoringDimensionFact] = []
        for score in final_result.scores:
            dimension = self._normalize_dimension(str(getattr(score, "dimension", "")))
            if not dimension or dimension == "OVERALL":
                continue
            items.append(
                ScoringDimensionFact(
                    dimension=dimension,
                    value=self._as_float(getattr(score, "value", 0.0), default=0.0),
                    unit=str(getattr(score, "unit", "") or ""),
                    details={"source": "final_result.scores", "id": getattr(score, "id", "")},
                )
            )
        return tuple(items)

    def _overall_from_scores(self, final_result: FinalResult) -> float | None:
        """Pick overall/final/total score from FinalResult.scores if present."""
        for score in final_result.scores:
            dimension = self._normalize_dimension(str(getattr(score, "dimension", "")))
            if dimension == "OVERALL":
                return self._as_float(getattr(score, "value", 0.0), default=0.0)
        return None

    def _extract_confidence_value(
        self,
        payload: Mapping[str, Any],
        final_result: FinalResult,
    ) -> float | None:
        """Extract confidence numeric value from payload or scores."""
        conf = payload.get("confidence")
        if isinstance(conf, Mapping):
            for key in ("score", "value", "confidence"):
                if conf.get(key) not in (None, ""):
                    return self._as_float(conf.get(key), default=0.0)
        value = self._first_float_optional(payload, CONFIDENCE_KEYS)
        if value is not None:
            return value
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if "confidence" in dimension:
                return self._as_float(getattr(score, "value", 0.0), default=0.0)
        return None

    def _parse_dimensions(self, raw: Any) -> tuple[ScoringDimensionFact, ...]:
        """Parse dimensions from mapping or list payloads."""
        items: list[ScoringDimensionFact] = []
        if isinstance(raw, Mapping):
            for key, value in raw.items():
                if isinstance(value, Mapping):
                    items.append(
                        ScoringDimensionFact(
                            dimension=self._normalize_dimension(
                                str(value.get("dimension") or key)
                            ),
                            value=self._as_float(
                                value.get("value") or value.get("score"), default=0.0
                            ),
                            unit=str(value.get("unit") or ""),
                            details=dict(value),
                        )
                    )
                else:
                    items.append(
                        ScoringDimensionFact(
                            dimension=self._normalize_dimension(str(key)),
                            value=self._as_float(value, default=0.0),
                        )
                    )
            return tuple(items)

        if isinstance(raw, list):
            for entry in raw:
                if isinstance(entry, Mapping):
                    items.append(
                        ScoringDimensionFact(
                            dimension=self._normalize_dimension(
                                str(
                                    entry.get("dimension")
                                    or entry.get("module")
                                    or entry.get("id")
                                    or ""
                                )
                            ),
                            value=self._as_float(
                                entry.get("value") or entry.get("score"), default=0.0
                            ),
                            unit=str(entry.get("unit") or ""),
                            details=dict(entry),
                        )
                    )
                elif isinstance(entry, (int, float)):
                    continue
        return tuple(item for item in items if item.dimension)

    def _merge_dimensions(
        self,
        left: tuple[ScoringDimensionFact, ...],
        right: tuple[ScoringDimensionFact, ...],
    ) -> tuple[ScoringDimensionFact, ...]:
        """Merge dimension facts; left (payload) wins on conflict."""
        merged: dict[str, ScoringDimensionFact] = {}
        for item in (*right, *left):
            if item.dimension:
                merged[item.dimension] = item
        return tuple(merged.values())

    def _normalize_dimension(self, raw: str) -> str:
        """Normalize dimension name to Pack 01 module code when known."""
        text = (raw or "").strip()
        if not text:
            return ""
        lowered = text.lower().replace(" ", "_").replace("-", "_")
        if lowered in DIMENSION_ALIASES:
            return DIMENSION_ALIASES[lowered]
        upper = text.upper().replace(" ", "_").replace("-", "_")
        if upper in {
            "WUXING",
            "STRENGTH",
            "TEN_GODS",
            "PATTERN",
            "USEFUL_GOD",
            "SHENSHA",
            "LUCK",
            "OVERALL",
        }:
            return upper
        return upper

    def _first_mapping_or_list(
        self,
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> Any:
        for key in keys:
            if key in payload:
                return payload.get(key)
        return None

    def _first_float_optional(
        self,
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> float | None:
        for key in keys:
            if key in payload and payload[key] not in (None, ""):
                value = payload[key]
                if isinstance(value, Mapping):
                    nested = value.get("value") or value.get("score")
                    if nested not in (None, ""):
                        return self._as_float(nested, default=0.0)
                    continue
                return self._as_float(value, default=0.0)
        return None

    def _first_str(
        self,
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> str:
        for key in keys:
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
            if isinstance(value, Mapping):
                label = value.get("level") or value.get("grade") or value.get("label")
                if label:
                    return str(label)
        return ""

    @staticmethod
    def _mapping(value: Any) -> dict[str, Any]:
        if isinstance(value, Mapping):
            return dict(value)
        to_dict = getattr(value, "to_dict", None)
        if callable(to_dict):
            portal = to_dict()
            if isinstance(portal, Mapping):
                return dict(portal)
        return {}

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
