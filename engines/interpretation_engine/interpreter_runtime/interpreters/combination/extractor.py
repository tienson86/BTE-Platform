"""Extract combination facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.combination.constants import (
    BRANCH_KEYS,
    COMBINATION_MODULE_IDS,
    SCORE_KEYS,
    STEM_KEYS,
    TRANSFORM_KEYS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class CombinationRelationFact:
    """One stem/branch relation fact from Pack 02."""

    relation_id: str = ""
    relation_type: str = ""
    members: tuple[str, ...] = ()
    pillars: tuple[str, ...] = ()
    status: str = ""
    result_element: str = ""
    priority: int = 0
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CombinationTransformFact:
    """One transformation fact from Pack 02."""

    source_relation_id: str = ""
    success: bool = False
    result_element: str = ""
    reason_codes: tuple[str, ...] = ()
    priority: int = 0


@dataclass(slots=True)
class CombinationFacts:
    """Normalized combination facts extracted from FinalResult."""

    stem_combinations: tuple[CombinationRelationFact, ...] = ()
    branch_combinations: tuple[CombinationRelationFact, ...] = ()
    transformations: tuple[CombinationTransformFact, ...] = ()
    combination_score: float | None = None
    confidence: float = 0.0
    summary: Mapping[str, Any] = field(default_factory=dict)
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False


class CombinationFactExtractor:
    """Read-only extractor: FinalResult → CombinationFacts.

    Does not call CombinationEngine.evaluate/calculate.
    """

    def extract(self, final_result: FinalResult) -> CombinationFacts:
        """Extract stem/branch/transform/score facts from FinalResult."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_combination_scores(final_result):
            return CombinationFacts(found=False)

        stems = self._parse_relations(
            self._first_list(payload, STEM_KEYS),
            default_type="stem_combination",
        )
        branches = self._parse_relations(
            self._first_list(payload, BRANCH_KEYS),
            default_type="branch_combination",
        )
        transforms = self._parse_transforms(
            self._first_list(payload, TRANSFORM_KEYS)
        )

        combination_score = self._first_float_optional(payload, SCORE_KEYS)
        confidence = 0.0
        conf_obj = payload.get("confidence")
        if isinstance(conf_obj, Mapping):
            confidence = self._as_float(conf_obj.get("score"), default=0.0)
            if combination_score is None:
                combination_score = confidence
        elif conf_obj not in (None, ""):
            confidence = self._as_float(conf_obj, default=0.0)

        combination_score = self._merge_dimension(
            final_result,
            combination_score if combination_score is not None else 0.0,
            ("combination", "combination_score"),
        )
        if combination_score == 0.0 and confidence == 0.0:
            combination_score_opt: float | None = None
        else:
            combination_score_opt = (
                combination_score if combination_score != 0.0 else confidence
            )

        summary = payload.get("summary")
        summary_map = dict(summary) if isinstance(summary, Mapping) else {}

        found = any(
            (
                bool(payload),
                bool(stems),
                bool(branches),
                bool(transforms),
                combination_score_opt is not None,
                bool(self._as_str_tuple(payload.get("matched_rules"))),
            )
        )

        facts = CombinationFacts(
            stem_combinations=stems,
            branch_combinations=branches,
            transformations=transforms,
            combination_score=combination_score_opt,
            confidence=confidence,
            summary=summary_map,
            matched_rules=self._as_str_tuple(
                payload.get("matched_rules") or payload.get("matched_rule_ids")
            ),
            reasoning=str(payload.get("reasoning") or payload.get("reason") or ""),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "combination_facts_extracted",
            extra={
                "found": facts.found,
                "stem_count": len(facts.stem_combinations),
                "branch_count": len(facts.branch_combinations),
                "transform_count": len(facts.transformations),
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge combination payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            module_id = str(module.module_id).lower()
            if module_id in COMBINATION_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    stage_id = str(stage.stage_id).lower()
                    if stage_id in COMBINATION_MODULE_IDS or stage_id in {
                        "detect",
                        "transform",
                        "score",
                    }:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                module_id = str(getattr(module, "module_id", "")).lower()
                if module_id in COMBINATION_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in COMBINATION_MODULE_IDS:
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                value = nested.get("combination")
                if isinstance(value, Mapping):
                    merged.update(dict(value))

        for key in ("combination", "combination_result", "combination_section"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_combination_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include combination dimensions."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if "combination" in dimension or "hop" in dimension:
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
    ) -> tuple[CombinationRelationFact, ...]:
        """Parse Pack 02 relation list into CombinationRelationFact tuples."""
        items: list[CombinationRelationFact] = []
        for entry in raw:
            if isinstance(entry, str):
                items.append(
                    CombinationRelationFact(
                        relation_id=entry,
                        relation_type=default_type,
                        members=(entry,),
                    )
                )
                continue
            if not isinstance(entry, Mapping):
                continue
            items.append(
                CombinationRelationFact(
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
                    result_element=str(
                        entry.get("result_element")
                        or entry.get("ket_qua")
                        or entry.get("ngu_hanh")
                        or ""
                    ),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
                    details=dict(entry.get("details") or {})
                    if isinstance(entry.get("details"), Mapping)
                    else {},
                )
            )
        return tuple(items)

    def _parse_transforms(
        self,
        raw: list[Any],
    ) -> tuple[CombinationTransformFact, ...]:
        """Parse Pack 02 transformation list."""
        items: list[CombinationTransformFact] = []
        for entry in raw:
            if not isinstance(entry, Mapping):
                continue
            items.append(
                CombinationTransformFact(
                    source_relation_id=str(
                        entry.get("source_relation_id")
                        or entry.get("relation_id")
                        or ""
                    ),
                    success=bool(entry.get("success")),
                    result_element=str(entry.get("result_element") or ""),
                    reason_codes=self._as_str_tuple(entry.get("reason_codes")),
                    priority=int(self._as_float(entry.get("priority"), default=0.0)),
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
        to_portal = getattr(value, "to_portal_dict", None)
        if callable(to_portal):
            portal = to_portal()
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
