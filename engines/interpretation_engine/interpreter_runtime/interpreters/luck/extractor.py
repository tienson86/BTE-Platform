"""Extract Luck facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.luck.constants import (
    DAYUN_KEYS,
    INTERACTION_KEYS,
    LIUNIAN_KEYS,
    LIUYUE_KEYS,
    LUCK_MODULE_IDS,
    SCORE_KEYS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LuckLayerFact:
    """One luck-layer fact (Dayun / Liunian / Liuyue)."""

    layer: str = ""
    stem: str = ""
    branch: str = ""
    ganzhi: str = ""
    label: str = ""
    status: str = ""
    favorability: str = ""
    activation: str = ""
    timing_phase: str = ""
    priority: int = 0
    ten_god: str = ""
    element: str = ""
    start_age: int | None = None
    end_age: int | None = None
    year: int | None = None
    month: int | None = None
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LuckInteractionFact:
    """Luck interaction with natal / upstream classifications."""

    layer: str = ""
    dimension: str = ""
    upstream_class: str = ""
    effect: str = ""
    priority: int = 0
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LuckFacts:
    """Normalized Luck facts extracted from FinalResult."""

    dayun: tuple[LuckLayerFact, ...] = ()
    liunian: tuple[LuckLayerFact, ...] = ()
    liuyue: tuple[LuckLayerFact, ...] = ()
    interactions: tuple[LuckInteractionFact, ...] = ()
    luck_score: float | None = None
    support_level: float | None = None
    attack_level: float | None = None
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    summary: Mapping[str, Any] = field(default_factory=dict)
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class LuckFactExtractor:
    """Read-only extractor: FinalResult -> LuckFacts.

    Reads luck stage payloads (Pack 02 LuckResult and live current_* shapes).
    Does not call LuckEngine.evaluate.
    """

    def extract(self, final_result: FinalResult) -> LuckFacts:
        """Extract Dayun / Liunian / Liuyue / Interaction facts."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_luck_scores(final_result):
            return LuckFacts(found=False)

        dayun = self._parse_layers(self._first_entries(payload, DAYUN_KEYS), default_layer="dayun")
        liunian = self._parse_layers(
            self._first_entries(payload, LIUNIAN_KEYS), default_layer="liunian"
        )
        liuyue = self._parse_layers(
            self._first_entries(payload, LIUYUE_KEYS), default_layer="liuyue"
        )
        interactions = self._parse_interactions(
            self._first_entries(payload, INTERACTION_KEYS)
        )

        summary = payload.get("summary")
        summary_map = dict(summary) if isinstance(summary, Mapping) else {}

        confidence = 0.0
        conf_obj = payload.get("confidence")
        if isinstance(conf_obj, Mapping):
            confidence = self._as_float(conf_obj.get("score"), default=0.0)
        elif conf_obj not in (None, ""):
            confidence = self._as_float(conf_obj, default=0.0)

        luck_score = self._first_float_optional(payload, SCORE_KEYS)
        luck_score = self._merge_dimension(
            final_result,
            luck_score if luck_score is not None else 0.0,
            ("luck", "luck_score", "dai_van"),
        )
        support_level = self._first_float_optional(
            payload, ("support_level", "luck_support")
        )
        attack_level = self._first_float_optional(
            payload, ("attack_level", "luck_attack")
        )

        score_opt: float | None = (
            luck_score
            if luck_score != 0.0 or dayun or liunian or liuyue or interactions
            else None
        )

        found = any(
            (
                bool(payload),
                bool(dayun),
                bool(liunian),
                bool(liuyue),
                bool(interactions),
                score_opt is not None,
                support_level is not None,
                attack_level is not None,
                bool(self._as_str_tuple(payload.get("matched_rules"))),
            )
        )
        if not found and payload and any(
            key in payload for key in (*DAYUN_KEYS, *LIUNIAN_KEYS, *LIUYUE_KEYS)
        ):
            found = True

        facts = LuckFacts(
            dayun=dayun,
            liunian=liunian,
            liuyue=liuyue,
            interactions=interactions,
            luck_score=score_opt,
            support_level=support_level,
            attack_level=attack_level,
            confidence=confidence,
            matched_rules=self._as_str_tuple(
                payload.get("matched_rules") or payload.get("matched_rule_ids")
            ),
            reasoning=str(
                payload.get("reasoning")
                or payload.get("luck_summary")
                or payload.get("reason")
                or ""
            ),
            summary=summary_map,
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "luck_facts_extracted",
            extra={
                "found": facts.found,
                "dayun_count": len(facts.dayun),
                "liunian_count": len(facts.liunian),
                "liuyue_count": len(facts.liuyue),
                "interaction_count": len(facts.interactions),
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge luck-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in LUCK_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in LUCK_MODULE_IDS:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in LUCK_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in LUCK_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                for key in ("luck", "dai_van", "dayun"):
                    value = nested.get(key)
                    if isinstance(value, Mapping):
                        merged.update(dict(value))

        for key in ("luck", "luck_result", "dai_van", "dayun"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_luck_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include luck dimensions."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if any(
                token in dimension
                for token in ("luck", "dai_van", "dayun", "liunian", "liuyue")
            ):
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

    def _parse_layers(
        self,
        raw: list[Any],
        *,
        default_layer: str,
    ) -> tuple[LuckLayerFact, ...]:
        """Parse Pack 02 layer list or live current_* period object(s)."""
        items: list[LuckLayerFact] = []
        for entry in raw:
            if isinstance(entry, str):
                items.append(
                    LuckLayerFact(layer=default_layer, label=entry, ganzhi=entry)
                )
                continue
            if not isinstance(entry, Mapping):
                continue
            pillar = entry.get("pillar")
            pillar_map = dict(pillar) if isinstance(pillar, Mapping) else {}
            stem = str(
                entry.get("heavenly_stem")
                or entry.get("stem")
                or pillar_map.get("stem")
                or ""
            )
            branch = str(
                entry.get("earthly_branch")
                or entry.get("branch")
                or pillar_map.get("branch")
                or ""
            )
            ganzhi = str(
                entry.get("ganzhi")
                or pillar_map.get("label")
                or f"{stem}{branch}".strip()
            )
            items.append(
                LuckLayerFact(
                    layer=str(entry.get("layer") or default_layer),
                    stem=stem,
                    branch=branch,
                    ganzhi=ganzhi,
                    label=str(
                        entry.get("label")
                        or ganzhi
                        or pillar_map.get("label")
                        or default_layer
                    ),
                    status=str(entry.get("status") or ""),
                    favorability=str(
                        entry.get("favorability")
                        or entry.get("luck_stage")
                        or ""
                    ),
                    activation=str(entry.get("activation") or ""),
                    timing_phase=str(entry.get("timing_phase") or ""),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                    ten_god=str(entry.get("ten_god") or ""),
                    element=str(entry.get("element") or ""),
                    start_age=self._as_int_optional(entry.get("start_age")),
                    end_age=self._as_int_optional(entry.get("end_age")),
                    year=self._as_int_optional(entry.get("year")),
                    month=self._as_int_optional(
                        entry.get("month") or entry.get("month_index")
                    ),
                    details=dict(entry),
                )
            )
        return tuple(items)

    def _parse_interactions(
        self, raw: list[Any]
    ) -> tuple[LuckInteractionFact, ...]:
        """Parse Pack 02 interaction list."""
        items: list[LuckInteractionFact] = []
        for entry in raw:
            if not isinstance(entry, Mapping):
                continue
            items.append(
                LuckInteractionFact(
                    layer=str(entry.get("layer") or ""),
                    dimension=str(entry.get("dimension") or ""),
                    upstream_class=str(
                        entry.get("upstream_class") or entry.get("class") or ""
                    ),
                    effect=str(entry.get("effect") or entry.get("relation") or ""),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                    details=dict(entry),
                )
            )
        return tuple(items)

    def _first_entries(
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
    def _as_int_optional(value: Any) -> int | None:
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
