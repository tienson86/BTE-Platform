"""Extract Shensha facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.shensha.constants import (
    AUSPICIOUS_KEYS,
    INAUSPICIOUS_KEYS,
    INTERACTION_KEYS,
    PRESENCE_KEYS,
    SCORE_KEYS,
    SHENSHA_MODULE_IDS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ShenshaPresenceFact:
    """One detected Shensha presence fact from Pack 02."""

    shensha_id: str = ""
    label: str = ""
    polarity: str = ""
    anchor: str = ""
    anchor_value: str = ""
    location_pillar: str = ""
    location_value: str = ""
    status: str = "active"
    priority: int = 0
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ShenshaInteractionFact:
    """Interaction / conflict between two Shensha."""

    left_id: str = ""
    right_id: str = ""
    relation: str = ""
    effect: str = ""
    priority: int = 0


@dataclass(slots=True)
class ShenshaFacts:
    """Normalized Shensha facts extracted from FinalResult."""

    presence: tuple[ShenshaPresenceFact, ...] = ()
    auspicious: tuple[ShenshaPresenceFact, ...] = ()
    inauspicious: tuple[ShenshaPresenceFact, ...] = ()
    interactions: tuple[ShenshaInteractionFact, ...] = ()
    shensha_score: float | None = None
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    summary: Mapping[str, Any] = field(default_factory=dict)
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class ShenshaFactExtractor:
    """Read-only extractor: FinalResult -> ShenshaFacts.

    Reads shensha stage payloads. Does not call ShenShaEngine.evaluate.
    """

    def extract(self, final_result: FinalResult) -> ShenshaFacts:
        """Extract detected Shensha / interactions / score facts."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_shensha_scores(final_result):
            return ShenshaFacts(found=False)

        presence = self._parse_presence(self._first_list(payload, PRESENCE_KEYS))
        auspicious = self._parse_presence(self._first_list(payload, AUSPICIOUS_KEYS))
        inauspicious = self._parse_presence(
            self._first_list(payload, INAUSPICIOUS_KEYS)
        )
        if not presence:
            presence = self._merge_presence(auspicious, inauspicious)

        interactions = self._parse_interactions(
            self._first_list(payload, INTERACTION_KEYS)
        )
        summary = payload.get("summary")
        summary_map = dict(summary) if isinstance(summary, Mapping) else {}

        confidence = 0.0
        conf_obj = payload.get("confidence")
        if isinstance(conf_obj, Mapping):
            confidence = self._as_float(conf_obj.get("score"), default=0.0)
        elif conf_obj not in (None, ""):
            confidence = self._as_float(conf_obj, default=0.0)

        shensha_score = self._first_float_optional(payload, SCORE_KEYS)
        shensha_score = self._merge_dimension(
            final_result,
            shensha_score if shensha_score is not None else 0.0,
            ("shensha", "shensha_score", "than_sat"),
        )
        score_opt: float | None = (
            shensha_score
            if shensha_score != 0.0 or presence or interactions
            else None
        )

        found = any(
            (
                bool(payload),
                bool(presence),
                bool(auspicious),
                bool(inauspicious),
                bool(interactions),
                score_opt is not None,
                bool(self._as_str_tuple(payload.get("matched_rules"))),
            )
        )
        if not found and payload and any(
            key in payload for key in (*PRESENCE_KEYS, *AUSPICIOUS_KEYS, *INAUSPICIOUS_KEYS)
        ):
            found = True

        facts = ShenshaFacts(
            presence=presence,
            auspicious=auspicious,
            inauspicious=inauspicious,
            interactions=interactions,
            shensha_score=score_opt,
            confidence=confidence,
            matched_rules=self._as_str_tuple(
                payload.get("matched_rules") or payload.get("matched_rule_ids")
            ),
            reasoning=str(payload.get("reasoning") or payload.get("reason") or ""),
            summary=summary_map,
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "shensha_facts_extracted",
            extra={
                "found": facts.found,
                "presence_count": len(facts.presence),
                "interaction_count": len(facts.interactions),
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge shensha-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in SHENSHA_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in SHENSHA_MODULE_IDS:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in SHENSHA_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in SHENSHA_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                for key in ("shensha", "shen_sha", "than_sat"):
                    value = nested.get(key)
                    if isinstance(value, Mapping):
                        merged.update(dict(value))

        for key in ("shensha", "shensha_result", "than_sat", "shen_sha"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_shensha_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include shensha dimensions."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if any(token in dimension for token in ("shensha", "than_sat", "shen_sha")):
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

    def _parse_presence(self, raw: list[Any]) -> tuple[ShenshaPresenceFact, ...]:
        """Parse Pack 02 presence / star list."""
        items: list[ShenshaPresenceFact] = []
        for entry in raw:
            if isinstance(entry, str):
                items.append(ShenshaPresenceFact(shensha_id=entry, label=entry))
                continue
            if not isinstance(entry, Mapping):
                continue
            items.append(
                ShenshaPresenceFact(
                    shensha_id=str(
                        entry.get("shensha_id")
                        or entry.get("id")
                        or entry.get("than_sat")
                        or entry.get("star_name")
                        or ""
                    ),
                    label=str(
                        entry.get("label")
                        or entry.get("ten_han_viet")
                        or entry.get("star_name")
                        or entry.get("than_sat")
                        or ""
                    ),
                    polarity=str(entry.get("polarity") or entry.get("loai") or ""),
                    anchor=str(entry.get("anchor") or ""),
                    anchor_value=str(entry.get("anchor_value") or ""),
                    location_pillar=str(entry.get("location_pillar") or ""),
                    location_value=str(entry.get("location_value") or ""),
                    status=str(entry.get("status") or "active"),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                    details=dict(entry),
                )
            )
        return tuple(items)

    def _parse_interactions(
        self, raw: list[Any]
    ) -> tuple[ShenshaInteractionFact, ...]:
        """Parse Pack 02 interaction list."""
        items: list[ShenshaInteractionFact] = []
        for entry in raw:
            if not isinstance(entry, Mapping):
                continue
            items.append(
                ShenshaInteractionFact(
                    left_id=str(entry.get("left_id") or entry.get("left") or ""),
                    right_id=str(entry.get("right_id") or entry.get("right") or ""),
                    relation=str(entry.get("relation") or ""),
                    effect=str(entry.get("effect") or ""),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                )
            )
        return tuple(items)

    @staticmethod
    def _merge_presence(
        left: tuple[ShenshaPresenceFact, ...],
        right: tuple[ShenshaPresenceFact, ...],
    ) -> tuple[ShenshaPresenceFact, ...]:
        """Merge auspicious + inauspicious into a unique presence list."""
        seen: set[str] = set()
        merged: list[ShenshaPresenceFact] = []
        for item in (*left, *right):
            key = item.shensha_id or item.label
            if not key or key in seen:
                continue
            seen.add(key)
            merged.append(item)
        return tuple(merged)

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
            if isinstance(value, Mapping):
                return [value]
            if isinstance(value, str) and value:
                return [value]
        return []

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
