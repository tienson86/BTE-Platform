"""PresentationValidator — public contract, no debug leakage."""

from __future__ import annotations

import json
import re
from dataclasses import fields
from typing import Any, Iterable

from engines.narrative_v2.communication.communication_context import ConsultingNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation.presentation_errors import PresentationValidationError
from engines.narrative_v2.presentation.presentation_model import (
    InterpretationPresentation,
    NarrativeV2Presentation,
)
from engines.narrative_v2.presentation.presentation_serializer import serialize_customer
from engines.narrative_v2.presentation.presentation_status import (
    ALLOWED_STATUSES,
    PRESENTATION_VERSION,
)

ROOT_FIELDS: tuple[str, ...] = (
    "status",
    "overview",
    "interpretation",
    "action_plan",
    "commercial",
    "metadata",
)

METADATA_FIELDS: tuple[str, ...] = ("status", "language", "version", "created_at")

OVERVIEW_FIELDS: tuple[str, ...] = (
    "headline",
    "summary",
    "identity",
    "balance",
    "conclusion",
)

INTERPRETATION_FIELDS: tuple[str, ...] = (
    "overview",
    "observation",
    "reasoning",
    "meaning",
    "impact",
    "recommendation",
    "closing",
    "consulting_flow",
)

ACTION_PLAN_FIELDS: tuple[str, ...] = (
    "top_priority",
    "actions",
    "warnings",
    "current_period",
)

FORBIDDEN_KEYS: frozenset[str] = frozenset(
    {
        "pipeline_trace",
        "runtime_metrics",
        "source_unit_ids",
        "source_unit_id",
        "knowledge_ids",
        "evidence_ids",
        "rewrite_ids",
        "reasoning_ids",
        "decision_id",
        "decision_ids",
        "action_id",
        "warning_id",
        "source_knowledge_ids",
        "references",
        "rule_id",
        "rule_ids",
        "canonical_analysis",
        "flow",
        "debug",
        "trace",
        "events",
        "builder_registry",
        "runtime_events",
        "reasoning_graph",
        "priority",
        "severity",
    }
)

FORBIDDEN_SUBSTRINGS: tuple[str, ...] = (
    "evidence.strength.level",
    "NR-REL-001",
    "knowledge.pattern.chinh_an",
    "pipeline_trace",
    "source_unit_ids",
    "runtime_metrics",
    "rewrite.pattern.",
    "reasoning.observation.",
    "evidence.pattern.",
    "source_knowledge_ids",
)

_JSON_BLOB = re.compile(r"^\s*[\{\[]")


class PresentationValidator:
    """Validate a packaged Presentation. Does not rewrite content."""

    def validate(
        self,
        presentation: NarrativeV2Presentation,
        *,
        interpretation: InterpretationNarrative | None = None,
        consulting: ConsultingNarrative | None = None,
    ) -> None:
        """Raise if the public contract is violated."""
        if not isinstance(presentation, NarrativeV2Presentation):
            raise PresentationValidationError("Expected NarrativeV2Presentation")
        self._validate_root(presentation)
        payload = serialize_customer(presentation)
        self._validate_payload(payload)
        self._validate_no_leaks(payload)
        self._validate_provenance(presentation, interpretation, consulting)

    def _validate_root(self, presentation: NarrativeV2Presentation) -> None:
        names = tuple(item.name for item in fields(presentation))
        if names != ROOT_FIELDS:
            raise PresentationValidationError("Unexpected Presentation root fields")
        if presentation.status not in ALLOWED_STATUSES:
            raise PresentationValidationError("Invalid Presentation status")
        if presentation.commercial is not None:
            raise PresentationValidationError("Commercial must be absent until Commercial Builder exists")
        meta = presentation.metadata
        if tuple(item.name for item in fields(meta)) != METADATA_FIELDS:
            raise PresentationValidationError("Unexpected metadata fields")
        if meta.version != PRESENTATION_VERSION:
            raise PresentationValidationError("Invalid Presentation version")
        if meta.status not in ALLOWED_STATUSES:
            raise PresentationValidationError("Invalid metadata status")
        if meta.status != presentation.status:
            raise PresentationValidationError("Metadata status must match Presentation status")

    def _validate_payload(self, payload: dict[str, Any]) -> None:
        if tuple(payload.keys()) != ROOT_FIELDS:
            raise PresentationValidationError("Serialized root keys must match contract")
        overview = payload["overview"]
        if overview is not None:
            self._assert_keys(overview, OVERVIEW_FIELDS, "overview")
        interpretation = payload["interpretation"]
        if interpretation is not None:
            self._assert_keys(interpretation, INTERPRETATION_FIELDS, "interpretation")
        action_plan = payload["action_plan"]
        if action_plan is not None:
            self._assert_keys(action_plan, ACTION_PLAN_FIELDS, "action_plan")

    def _validate_provenance(
        self,
        presentation: NarrativeV2Presentation,
        interpretation: InterpretationNarrative | None,
        consulting: ConsultingNarrative | None,
    ) -> None:
        view = presentation.interpretation
        if view is None:
            return
        if interpretation is not None:
            if view.overview != interpretation.overview:
                raise PresentationValidationError("Interpretation overview was rewritten")
            if view.observation != interpretation.observation:
                raise PresentationValidationError("Interpretation observation was rewritten")
            if view.reasoning != interpretation.reasoning:
                raise PresentationValidationError("Interpretation reasoning was rewritten")
            if view.meaning != interpretation.meaning:
                raise PresentationValidationError("Interpretation meaning was rewritten")
            if view.impact != interpretation.impact:
                raise PresentationValidationError("Interpretation impact was rewritten")
            if view.recommendation != interpretation.recommendation:
                raise PresentationValidationError("Interpretation recommendation was rewritten")
            if view.closing != interpretation.closing:
                raise PresentationValidationError("Interpretation closing was rewritten")
        if consulting is not None:
            expected = consulting.flow if consulting.flow and consulting.flow.strip() else None
            if view.consulting_flow != expected:
                raise PresentationValidationError("consulting_flow must copy ConsultingNarrative.flow")
            if view.consulting_flow and _is_recomposed_flow(view):
                raise PresentationValidationError("consulting_flow must not be recomposed")

    def _validate_no_leaks(self, payload: dict[str, Any]) -> None:
        leaked = _collect_keys(payload) & FORBIDDEN_KEYS
        if leaked:
            raise PresentationValidationError(f"Internal key leaked: {sorted(leaked)[0]}")
        rendered = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        for token in FORBIDDEN_SUBSTRINGS:
            if token in rendered:
                raise PresentationValidationError(f"Internal token leaked: {token}")
        for text in _collect_strings(payload):
            stripped = text.strip()
            if _JSON_BLOB.match(stripped):
                raise PresentationValidationError("Raw JSON blob is not customer-safe")

    def _assert_keys(self, value: dict[str, Any], expected: tuple[str, ...], name: str) -> None:
        if tuple(value.keys()) != expected:
            raise PresentationValidationError(f"Unexpected {name} fields")


def _collect_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        keys.update(value.keys())
        for item in value.values():
            keys.update(_collect_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_collect_keys(item))
    return keys


def _collect_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _collect_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _collect_strings(item)


def _is_recomposed_flow(view: InterpretationPresentation) -> bool:
    parts = (
        view.observation,
        view.reasoning,
        view.meaning,
        view.impact,
        view.recommendation,
        view.closing,
    )
    joined = " ".join(part.strip() for part in parts if part and part.strip())
    return bool(joined and view.consulting_flow == joined)


