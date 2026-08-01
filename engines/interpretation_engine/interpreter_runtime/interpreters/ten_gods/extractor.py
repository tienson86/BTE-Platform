"""Extract Ten Gods facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.ten_gods.constants import (
    DISTRIBUTION_KEYS,
    FAVORABILITY_KEYS,
    GOD_CODE_TO_LABEL,
    GOD_ID_TO_LABEL,
    INTERACTION_KEYS,
    PRESENCE_KEYS,
    RELATIONSHIP_KEYS,
    SCORE_KEYS,
    TEN_GODS_MODULE_IDS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class TenGodPresenceFact:
    """One Ten God presence fact from Pack 02."""

    god_id: str = ""
    label: str = ""
    source_pillar: str = ""
    source_stem: str = ""
    polarity_class: str = ""
    count: int = 1
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TenGodRelationFact:
    """Relationship between two Ten Gods."""

    left_god_id: str = ""
    right_god_id: str = ""
    relation: str = ""
    priority: int = 0
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TenGodInteractionFact:
    """Interaction of a Ten God with an upstream classification."""

    dimension: str = ""
    upstream_class: str = ""
    god_id: str = ""
    effect: str = ""
    priority: int = 0
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TenGodFavorabilityFact:
    """Favorability class for a Ten God."""

    god_id: str = ""
    favorability: str = ""
    reason_codes: tuple[str, ...] = ()


@dataclass(slots=True)
class TenGodsFacts:
    """Normalized Ten Gods facts extracted from FinalResult."""

    presence: tuple[TenGodPresenceFact, ...] = ()
    relationships: tuple[TenGodRelationFact, ...] = ()
    interactions: tuple[TenGodInteractionFact, ...] = ()
    favorability: tuple[TenGodFavorabilityFact, ...] = ()
    distribution: Mapping[str, int] = field(default_factory=dict)
    dominant_god: str = ""
    unique_god_ids: tuple[str, ...] = ()
    ten_gods_score: float | None = None
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class TenGodsFactExtractor:
    """Read-only extractor: FinalResult -> TenGodsFacts.

    Reads ten_gods stage payloads. Does not call TenGodsEngine.evaluate.
    """

    def extract(self, final_result: FinalResult) -> TenGodsFacts:
        """Extract Ten Gods / distribution / strength / interaction facts."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_ten_gods_scores(final_result):
            return TenGodsFacts(found=False)

        presence = self._parse_presence(self._first_list(payload, PRESENCE_KEYS))
        relationships = self._parse_relationships(
            self._first_list(payload, RELATIONSHIP_KEYS)
        )
        interactions = self._parse_interactions(
            self._first_list(payload, INTERACTION_KEYS)
        )
        favorability = self._parse_favorability(
            self._first_list(payload, FAVORABILITY_KEYS)
        )

        summary = self._first_mapping(payload, DISTRIBUTION_KEYS)
        distribution = self._build_distribution(presence, summary, payload)
        dominant = str(
            summary.get("dominant_god_id")
            or summary.get("dominant_god")
            or payload.get("dominant_god")
            or ""
        )
        if not dominant and distribution:
            dominant = max(distribution.items(), key=lambda item: item[1])[0]

        unique_ids = self._as_str_tuple(
            summary.get("unique_god_ids") or [item.god_id for item in presence]
        )

        confidence = 0.0
        conf_obj = payload.get("confidence")
        if isinstance(conf_obj, Mapping):
            confidence = self._as_float(conf_obj.get("score"), default=0.0)
        elif conf_obj not in (None, ""):
            confidence = self._as_float(conf_obj, default=0.0)

        ten_gods_score = self._first_float_optional(payload, SCORE_KEYS)
        ten_gods_score = self._merge_dimension(
            final_result,
            ten_gods_score if ten_gods_score is not None else 0.0,
            ("ten_gods", "ten_gods_score", "thap_than"),
        )
        score_opt: float | None = (
            ten_gods_score
            if ten_gods_score != 0.0
            or presence
            or relationships
            or interactions
            else None
        )

        found = any(
            (
                bool(payload),
                bool(presence),
                bool(relationships),
                bool(interactions),
                bool(favorability),
                bool(distribution),
                score_opt is not None,
                bool(self._as_str_tuple(payload.get("matched_rules"))),
            )
        )
        if not found and payload and any(
            key in payload
            for key in (*PRESENCE_KEYS, *RELATIONSHIP_KEYS, *INTERACTION_KEYS)
        ):
            found = True

        facts = TenGodsFacts(
            presence=presence,
            relationships=relationships,
            interactions=interactions,
            favorability=favorability,
            distribution=distribution,
            dominant_god=dominant,
            unique_god_ids=unique_ids,
            ten_gods_score=score_opt,
            confidence=confidence,
            matched_rules=self._as_str_tuple(
                payload.get("matched_rules") or payload.get("matched_rule_ids")
            ),
            reasoning=str(payload.get("reasoning") or payload.get("reason") or ""),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "ten_gods_facts_extracted",
            extra={
                "found": facts.found,
                "presence_count": len(facts.presence),
                "relationship_count": len(facts.relationships),
                "interaction_count": len(facts.interactions),
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge ten-gods-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in TEN_GODS_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in TEN_GODS_MODULE_IDS:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in TEN_GODS_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in TEN_GODS_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                for key in ("ten_gods", "thap_than"):
                    value = nested.get(key)
                    if isinstance(value, Mapping):
                        merged.update(dict(value))

        for key in ("ten_gods", "ten_gods_result", "thap_than"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_ten_gods_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include ten-gods dimensions."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if any(token in dimension for token in ("ten_god", "thap_than")):
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
        return current

    def _parse_presence(self, raw: list[Any]) -> tuple[TenGodPresenceFact, ...]:
        """Parse Pack 02 presence list into facts."""
        items: list[TenGodPresenceFact] = []
        for entry in raw:
            if isinstance(entry, str):
                god_id, label = self._normalize_god(entry)
                items.append(
                    TenGodPresenceFact(god_id=god_id, label=label, count=1)
                )
                continue
            if not isinstance(entry, Mapping):
                continue
            god_raw = str(
                entry.get("god_id")
                or entry.get("ten_god")
                or entry.get("thap_than")
                or entry.get("label")
                or ""
            )
            god_id, label = self._normalize_god(
                god_raw,
                fallback_label=str(entry.get("label") or ""),
            )
            items.append(
                TenGodPresenceFact(
                    god_id=god_id,
                    label=label,
                    source_pillar=str(entry.get("source_pillar") or ""),
                    source_stem=str(entry.get("source_stem") or ""),
                    polarity_class=str(entry.get("polarity_class") or ""),
                    count=max(1, int(self._as_float(entry.get("count"), default=1.0))),
                    details=dict(entry.get("details") or {})
                    if isinstance(entry.get("details"), Mapping)
                    else {},
                )
            )
        return tuple(items)

    def _parse_relationships(self, raw: list[Any]) -> tuple[TenGodRelationFact, ...]:
        """Parse Pack 02 relationship list."""
        items: list[TenGodRelationFact] = []
        for entry in raw:
            if not isinstance(entry, Mapping):
                continue
            items.append(
                TenGodRelationFact(
                    left_god_id=str(
                        entry.get("left_god_id") or entry.get("left") or ""
                    ),
                    right_god_id=str(
                        entry.get("right_god_id") or entry.get("right") or ""
                    ),
                    relation=str(entry.get("relation") or entry.get("type") or ""),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                    details=dict(entry),
                )
            )
        return tuple(items)

    def _parse_interactions(self, raw: list[Any]) -> tuple[TenGodInteractionFact, ...]:
        """Parse Pack 02 interaction list."""
        items: list[TenGodInteractionFact] = []
        for entry in raw:
            if not isinstance(entry, Mapping):
                continue
            items.append(
                TenGodInteractionFact(
                    dimension=str(entry.get("dimension") or ""),
                    upstream_class=str(
                        entry.get("upstream_class") or entry.get("class") or ""
                    ),
                    god_id=str(entry.get("god_id") or ""),
                    effect=str(entry.get("effect") or ""),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                    details=dict(entry),
                )
            )
        return tuple(items)

    def _parse_favorability(
        self, raw: list[Any]
    ) -> tuple[TenGodFavorabilityFact, ...]:
        """Parse Pack 02 favorability list."""
        items: list[TenGodFavorabilityFact] = []
        for entry in raw:
            if not isinstance(entry, Mapping):
                continue
            items.append(
                TenGodFavorabilityFact(
                    god_id=str(entry.get("god_id") or ""),
                    favorability=str(entry.get("favorability") or ""),
                    reason_codes=self._as_str_tuple(entry.get("reason_codes")),
                )
            )
        return tuple(items)

    def _build_distribution(
        self,
        presence: tuple[TenGodPresenceFact, ...],
        summary: Mapping[str, Any],
        payload: Mapping[str, Any],
    ) -> dict[str, int]:
        """Build god_id -> count distribution."""
        dist: dict[str, int] = {}
        raw_dist = summary.get("distribution") or payload.get("distribution")
        if isinstance(raw_dist, Mapping):
            for key, value in raw_dist.items():
                god_id, _ = self._normalize_god(str(key))
                dist[god_id] = int(self._as_float(value, default=0.0))
        for item in presence:
            key = item.god_id or item.label
            if not key:
                continue
            dist[key] = dist.get(key, 0) + max(1, item.count)
        return dist

    def _normalize_god(
        self,
        raw: str,
        *,
        fallback_label: str = "",
    ) -> tuple[str, str]:
        """Normalize god identifier to (god_id, Vietnamese label)."""
        text = (raw or "").strip()
        if not text and fallback_label:
            text = fallback_label.strip()
        if not text:
            return "", fallback_label

        lowered = text.lower().replace(" ", "_").replace("-", "_")
        if lowered in GOD_ID_TO_LABEL:
            return lowered, GOD_ID_TO_LABEL[lowered]
        if lowered in GOD_CODE_TO_LABEL:
            label = GOD_CODE_TO_LABEL[lowered]
            for god_id, mapped in GOD_ID_TO_LABEL.items():
                if mapped == label:
                    return god_id, label
            return lowered, label

        # Already a Vietnamese label.
        for god_id, label in GOD_ID_TO_LABEL.items():
            if text == label or lowered == label.lower().replace(" ", "_"):
                return god_id, label

        label = fallback_label or text
        return lowered, label

    def _first_list(
        self,
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> list[Any]:
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, tuple):
                return list(value)
            if isinstance(value, Mapping) and key == "summary":
                continue
            if isinstance(value, Mapping):
                return [value]
            if isinstance(value, str) and value:
                return [value]
        return []

    def _first_mapping(
        self,
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> dict[str, Any]:
        for key in keys:
            value = payload.get(key)
            if isinstance(value, Mapping):
                return dict(value)
        return {}

    def _first_float_optional(
        self,
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> float | None:
        for key in keys:
            if key in payload and payload[key] not in (None, ""):
                return self._as_float(payload[key], default=0.0)
        return None

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
