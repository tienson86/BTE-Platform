"""Extract conflict facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.conflict.constants import (
    CLASH_KEYS,
    CONFLICT_MODULE_IDS,
    DESTRUCTION_KEYS,
    HARM_KEYS,
    PUNISHMENT_KEYS,
    SCORE_KEYS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ConflictRelationFact:
    """One conflict relation fact from Pack 02."""

    relation_id: str = ""
    relation_type: str = ""
    members: tuple[str, ...] = ()
    pillars: tuple[str, ...] = ()
    status: str = ""
    priority: int = 0
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ConflictFacts:
    """Normalized conflict facts extracted from FinalResult."""

    clashes: tuple[ConflictRelationFact, ...] = ()
    punishments: tuple[ConflictRelationFact, ...] = ()
    harms: tuple[ConflictRelationFact, ...] = ()
    destructions: tuple[ConflictRelationFact, ...] = ()
    conflict_score: float | None = None
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class ConflictFactExtractor:
    """Read-only extractor: FinalResult → ConflictFacts.

    Reads combination/conflict stage payloads. Does not call CombinationEngine.
    """

    def extract(self, final_result: FinalResult) -> ConflictFacts:
        """Extract clash/punishment/harm/destruction facts from FinalResult."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_conflict_scores(final_result):
            return ConflictFacts(found=False)

        clashes = self._parse_relations(
            self._first_list(payload, CLASH_KEYS),
            default_type="clash",
        )
        punishments = self._parse_relations(
            self._first_list(payload, PUNISHMENT_KEYS),
            default_type="punishment",
        )
        harms = self._parse_relations(
            self._first_list(payload, HARM_KEYS),
            default_type="harm",
        )
        destructions = self._parse_relations(
            self._first_list(payload, DESTRUCTION_KEYS),
            default_type="destruction",
        )

        conflict_score = self._first_float_optional(payload, SCORE_KEYS)
        confidence = 0.0
        conf_obj = payload.get("confidence")
        if isinstance(conf_obj, Mapping):
            confidence = self._as_float(conf_obj.get("score"), default=0.0)
        elif conf_obj not in (None, ""):
            confidence = self._as_float(conf_obj, default=0.0)

        conflict_score = self._merge_dimension(
            final_result,
            conflict_score if conflict_score is not None else 0.0,
            ("conflict", "conflict_score", "clash_score"),
        )
        conflict_score_opt: float | None
        if conflict_score == 0.0 and not (
            clashes or punishments or harms or destructions
        ):
            conflict_score_opt = None if confidence == 0.0 else confidence
        else:
            conflict_score_opt = conflict_score if conflict_score != 0.0 else None

        found = any(
            (
                bool(payload),
                bool(clashes),
                bool(punishments),
                bool(harms),
                bool(destructions),
                conflict_score_opt is not None,
                bool(self._as_str_tuple(payload.get("matched_rules"))),
            )
        )
        # Empty clashes list alone in stub payloads should still count as found
        # when combination module is present with conflict keys.
        if not found and payload and any(
            key in payload for key in (*CLASH_KEYS, *PUNISHMENT_KEYS, *HARM_KEYS, *DESTRUCTION_KEYS)
        ):
            found = True

        facts = ConflictFacts(
            clashes=clashes,
            punishments=punishments,
            harms=harms,
            destructions=destructions,
            conflict_score=conflict_score_opt,
            confidence=confidence,
            matched_rules=self._as_str_tuple(
                payload.get("matched_rules") or payload.get("matched_rule_ids")
            ),
            reasoning=str(payload.get("reasoning") or payload.get("reason") or ""),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "conflict_facts_extracted",
            extra={
                "found": facts.found,
                "clash_count": len(facts.clashes),
                "punishment_count": len(facts.punishments),
                "harm_count": len(facts.harms),
                "destruction_count": len(facts.destructions),
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge conflict-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in CONFLICT_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in CONFLICT_MODULE_IDS or stage_id in {
                        "clash",
                        "conflict",
                        "detect",
                    }:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in CONFLICT_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in CONFLICT_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                for key in ("conflict", "combination"):
                    value = nested.get(key)
                    if isinstance(value, Mapping):
                        merged.update(dict(value))

        for key in (
            "conflict",
            "conflict_result",
            "combination",
            "combination_result",
        ):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_conflict_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include conflict dimensions."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if any(
                token in dimension
                for token in ("conflict", "clash", "harm", "punish", "destruction")
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

    def _parse_relations(
        self,
        raw: list[Any],
        *,
        default_type: str,
    ) -> tuple[ConflictRelationFact, ...]:
        """Parse Pack 02 relation list into ConflictRelationFact tuples."""
        items: list[ConflictRelationFact] = []
        for entry in raw:
            if isinstance(entry, str):
                items.append(
                    ConflictRelationFact(
                        relation_id=entry,
                        relation_type=default_type,
                        members=(entry,),
                    )
                )
                continue
            if not isinstance(entry, Mapping):
                continue
            items.append(
                ConflictRelationFact(
                    relation_id=str(
                        entry.get("relation_id") or entry.get("id") or ""
                    ),
                    relation_type=str(
                        entry.get("relation_type") or default_type
                    ),
                    members=self._as_str_tuple(
                        entry.get("members") or entry.get("pair")
                    ),
                    pillars=self._as_str_tuple(entry.get("pillars")),
                    status=str(entry.get("status") or ""),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                    details=dict(entry.get("details") or {})
                    if isinstance(entry.get("details"), Mapping)
                    else {},
                )
            )
        return tuple(items)

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
