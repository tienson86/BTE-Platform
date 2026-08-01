"""Extract strength facts from Pack 02 FinalResult."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.analysis_engine.models.final_result import FinalResult

from engines.interpretation_engine.interpreter_runtime.interpreters.strength.constants import (
    BALANCE_KEYS,
    BODY_KEYS,
    DRAIN_KEYS,
    FINAL_LEVEL_KEYS,
    FINAL_SCORE_KEYS,
    ROOT_KEYS,
    SEASON_KEYS,
    STEM_KEYS,
    STEM_SUPPORT_RULE_CODES,
    STEM_SUPPORT_TYPE,
    STRENGTH_MODULE_IDS,
    SUPPORT_KEYS,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class StrengthFacts:
    """Normalized strength facts extracted from FinalResult."""

    body_strength: float = 0.0
    season_strength: float = 0.0
    root_strength: float = 0.0
    stem_strength: float = 0.0
    support_score: float = 0.0
    drain_score: float = 0.0
    balance_score: float | None = None
    final_strength: str = ""
    final_strength_score: float = 0.0
    confidence: float = 0.0
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    root_level: str = ""
    month_status: str = ""
    support_type: str = ""
    drain_type: str = ""
    control_score: float = 0.0
    control_type: str = ""
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    found: bool = False

    # Aliases for StrengthMatcher getattr(field) compatibility.
    @property
    def strength_score(self) -> float:
        """Pack 01 level rules match against ``strength_score``."""
        return self.final_strength_score

    @property
    def season_score(self) -> float:
        """Season component alias."""
        return self.season_strength

    @property
    def root_score(self) -> float:
        """Root component alias."""
        return self.root_strength

    @property
    def stem_score(self) -> float:
        """Stem component alias."""
        return self.stem_strength


class StrengthFactExtractor:
    """Read-only extractor: FinalResult → StrengthFacts.

    Does not call Pack 01 scoring engines. Reads Pack 02 payloads only.
    """

    def extract(self, final_result: FinalResult) -> StrengthFacts:
        """Extract strength facts from FinalResult module/scores/payload."""
        payload = self._collect_payload(final_result)
        if not payload and not self._has_strength_scores(final_result):
            return StrengthFacts(found=False)

        body = self._first_float(payload, BODY_KEYS, default=0.0)
        season = self._first_float(payload, SEASON_KEYS, default=0.0)
        root = self._first_float(payload, ROOT_KEYS, default=0.0)
        stem = self._first_float(payload, STEM_KEYS, default=0.0)
        support = self._first_float(payload, SUPPORT_KEYS, default=0.0)
        drain = self._first_float(payload, DRAIN_KEYS, default=0.0)
        balance = self._first_float_optional(payload, BALANCE_KEYS)
        final_score = self._first_float(payload, FINAL_SCORE_KEYS, default=body)
        final_level = self._first_str(payload, FINAL_LEVEL_KEYS, default="")

        # Dimension scores on FinalResult / nested analysis.
        body = self._merge_dimension(final_result, body, ("body_strength", "strength"))
        season = self._merge_dimension(
            final_result, season, ("season_strength", "season", "month_strength")
        )
        root = self._merge_dimension(final_result, root, ("root_strength", "root"))
        stem = self._merge_dimension(final_result, stem, ("stem_strength", "stem"))
        support = self._merge_dimension(
            final_result, support, ("support_score", "support")
        )
        drain = self._merge_dimension(final_result, drain, ("drain_score", "drain"))
        final_score = self._merge_dimension(
            final_result, final_score, ("strength", "strength_score", "final_strength")
        )

        if stem == 0.0:
            stem = self._infer_stem_from_payload(payload)

        matched = self._as_str_tuple(
            payload.get("matched_rules") or payload.get("matched_rule_ids")
        )
        confidence = self._as_float(payload.get("confidence"), default=0.0)
        reasoning = str(payload.get("reasoning") or payload.get("reason") or "")

        found = any(
            (
                bool(payload),
                body != 0.0,
                season != 0.0,
                root != 0.0,
                stem != 0.0,
                support != 0.0,
                drain != 0.0,
                bool(final_level),
                bool(matched),
            )
        )

        facts = StrengthFacts(
            body_strength=body if body != 0.0 else final_score,
            season_strength=season,
            root_strength=root,
            stem_strength=stem,
            support_score=support,
            drain_score=drain,
            balance_score=balance,
            final_strength=final_level,
            final_strength_score=final_score if final_score != 0.0 else body,
            confidence=confidence,
            matched_rules=matched,
            reasoning=reasoning,
            root_level=str(payload.get("root_level") or ""),
            month_status=str(
                payload.get("month_status") or payload.get("season_status") or ""
            ),
            support_type=str(payload.get("support_type") or ""),
            drain_type=str(payload.get("drain_type") or ""),
            control_score=self._as_float(payload.get("control_score"), default=0.0),
            control_type=str(payload.get("control_type") or ""),
            raw_payload=dict(payload),
            found=found,
        )
        logger.debug(
            "strength_facts_extracted",
            extra={
                "found": facts.found,
                "final_strength": facts.final_strength,
                "final_strength_score": facts.final_strength_score,
            },
        )
        return facts

    def _collect_payload(self, final_result: FinalResult) -> dict[str, Any]:
        """Merge strength-related payloads from module and analysis results."""
        merged: dict[str, Any] = {}

        for module in final_result.module_results:
            if str(module.module_id).lower() in STRENGTH_MODULE_IDS:
                merged.update(self._mapping(module.payload))
                for stage in module.stage_results:
                    if str(stage.stage_id).lower() in STRENGTH_MODULE_IDS or str(
                        stage.stage_id
                    ).lower() in {"strength", "classify", "score"}:
                        merged.update(self._mapping(stage.payload))

        analysis = final_result.analysis_result
        if analysis is not None:
            for module in getattr(analysis, "module_results", ()) or ():
                if str(getattr(module, "module_id", "")).lower() in STRENGTH_MODULE_IDS:
                    merged.update(self._mapping(getattr(module, "payload", {})))
            for stage in getattr(analysis, "stage_results", ()) or ():
                stage_id = str(getattr(stage, "stage_id", "")).lower()
                if stage_id in STRENGTH_MODULE_IDS or stage_id == "strength":
                    merged.update(self._mapping(getattr(stage, "payload", {})))
            nested = getattr(analysis, "payload", None)
            if isinstance(nested, Mapping):
                strength_nested = nested.get("strength")
                if isinstance(strength_nested, Mapping):
                    merged.update(dict(strength_nested))

        # Direct strength object serialization (StrengthResult.to_portal_dict).
        for key in ("strength", "strength_result", "strength_section"):
            value = merged.get(key)
            if isinstance(value, Mapping):
                merged.update(dict(value))

        return merged

    def _has_strength_scores(self, final_result: FinalResult) -> bool:
        """True when FinalResult scores include a strength dimension."""
        for score in final_result.scores:
            dimension = str(getattr(score, "dimension", "")).lower()
            if "strength" in dimension or dimension in {
                "season",
                "root",
                "stem",
                "support",
                "drain",
                "balance",
            }:
                return True
        analysis = final_result.analysis_result
        if analysis is None:
            return False
        for score in getattr(analysis, "scores", ()) or ():
            dimension = str(getattr(score, "dimension", "")).lower()
            if "strength" in dimension:
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

    def _infer_stem_from_payload(self, payload: Mapping[str, Any]) -> float:
        """Infer stem strength from Pack 02 labels / matched rule ids."""
        support_type = str(payload.get("support_type") or "")
        if support_type == STEM_SUPPORT_TYPE:
            return self._as_float(payload.get("support_score"), default=0.0)

        matched = payload.get("matched_rules") or payload.get("matched_rule_ids") or []
        if isinstance(matched, (list, tuple, set)):
            for rule_id in matched:
                if str(rule_id) in STEM_SUPPORT_RULE_CODES:
                    return self._as_float(payload.get("support_score"), default=0.0)

        stem_detail = payload.get("stem") or payload.get("stem_support")
        if isinstance(stem_detail, Mapping):
            return self._as_float(
                stem_detail.get("score") or stem_detail.get("value"),
                default=0.0,
            )
        return 0.0

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
    def _first_float(
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
        *,
        default: float,
    ) -> float:
        for key in keys:
            if key in payload and payload[key] not in (None, ""):
                return StrengthFactExtractor._as_float(payload[key], default=default)
        return default

    @staticmethod
    def _first_float_optional(
        payload: Mapping[str, Any],
        keys: tuple[str, ...],
    ) -> float | None:
        for key in keys:
            if key in payload and payload[key] not in (None, ""):
                return StrengthFactExtractor._as_float(payload[key], default=0.0)
        return None

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
            return (value,) if value else ()
        if isinstance(value, (list, tuple, set, frozenset)):
            return tuple(str(item) for item in value if item not in (None, ""))
        return ()
