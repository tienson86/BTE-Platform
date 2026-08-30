"""Assemble a read-only Narrative Studio review from runtime + Pack05 archive."""

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass
from typing import Any, Mapping

from applications.api.services.orchestrator import OrchestratorService
from applications.narrative_studio.catalog import StudioCase, get_case
from applications.narrative_studio.golden import diff_presentations, load_golden_presentation
from engines.narrative_v2.action.decision_builder import DecisionBuilder
from engines.narrative_v2.presentation import PRESENTATION_VERSION, serialize_customer
from engines.narrative_v2.runtime import NarrativeRuntime

logger = logging.getLogger(__name__)

TRACE_STAGES = (
    "evidence",
    "reasoning",
    "knowledge",
    "rewrite",
    "conversation",
    "consulting",
    "presentation",
)

CONTRACT_GAPS = (
    "overview.identity is null",
    "overview.balance is null",
    "overview.conclusion is null",
    "commercial is null (Commercial Builder not implemented)",
    "action_plan.current_period is null",
    "interpretation.closing duplicates observation (upstream)",
)


@dataclass(frozen=True, slots=True)
class StudioReview:
    """Immutable studio snapshot. Safe to render. Not a write API."""

    case_id: str
    full_name: str
    presentation: dict[str, Any] | None
    pack05: dict[str, Any] | None
    consulting_flow: str | None
    structured: dict[str, str | None]
    trace: dict[str, list[dict[str, object]]]
    decisions: list[dict[str, object]]
    actions: list[dict[str, object]]
    knowledge: dict[str, object]
    contract: dict[str, object]
    quality: dict[str, object]
    golden_diffs: list[dict[str, str]]
    golden_available: bool
    runtime_status: str
    presentation_fingerprint: str


class NarrativeStudioService:
    """Load cases for internal review. Never writes Narrative or Knowledge."""

    def __init__(self, orchestrator: OrchestratorService | None = None) -> None:
        self._orchestrator = orchestrator or OrchestratorService()
        self._cache: dict[str, StudioReview] = {}

    def load(self, case_id: str) -> StudioReview:
        """Return a cached read-only review for one catalog case."""
        if case_id not in self._cache:
            self._cache[case_id] = self._build(get_case(case_id))
        return self._cache[case_id]

    def _build(self, case: StudioCase) -> StudioReview:
        payload = self._orchestrator.analyze(
            year=case.year,
            month=case.month,
            day=case.day,
            hour=case.hour,
            minute=case.minute,
            gender=case.gender,
            timezone=case.timezone,
        )
        pack05 = copy.deepcopy(payload.get("narrative_result"))
        runtime = NarrativeRuntime()
        result = runtime.run(dict(payload))
        context = runtime.require_context()
        presentation_obj = result.presentation
        presentation = (
            serialize_customer(presentation_obj) if presentation_obj is not None else None
        )
        interpretation = getattr(context.presentation, "interpretation", None) if context.presentation else None
        consulting_flow = getattr(interpretation, "consulting_flow", None) if interpretation else None
        if not consulting_flow and context.consulting is not None:
            consulting_flow = getattr(context.consulting, "flow", None)
        structured = _structured(interpretation)
        knowledge = _knowledge_panel(context.knowledge)
        decisions = _decision_rows(context.rewrite, context.interpretation)
        actions = _action_rows(context.action)
        golden = load_golden_presentation(case.case_id)
        diffs = diff_presentations(presentation, golden)
        review = StudioReview(
            case_id=case.case_id,
            full_name=case.full_name,
            presentation=presentation,
            pack05=_pack05_snippet(pack05 if isinstance(pack05, dict) else None),
            consulting_flow=consulting_flow if isinstance(consulting_flow, str) else None,
            structured=structured,
            trace=_trace_panel(context),
            decisions=decisions,
            actions=actions,
            knowledge=knowledge,
            contract=_contract_panel(presentation, result.status),
            quality=_quality_panel(context, presentation),
            golden_diffs=diffs,
            golden_available=golden is not None,
            runtime_status=result.status,
            presentation_fingerprint=_fingerprint(presentation),
        )
        logger.info("narrative_studio.loaded case=%s status=%s", case.case_id, result.status)
        return review


def _structured(interpretation: object | None) -> dict[str, str | None]:
    keys = (
        "observation",
        "reasoning",
        "meaning",
        "impact",
        "recommendation",
        "closing",
    )
    if interpretation is None:
        return {key: None for key in keys}
    return {key: _text(getattr(interpretation, key, None)) for key in keys}


def _trace_panel(context: object) -> dict[str, list[dict[str, object]]]:
    evidence = getattr(context, "evidence", None)
    reasoning = getattr(context, "reasoning", None)
    knowledge = getattr(context, "knowledge", None)
    rewrite = getattr(context, "rewrite", None)
    conversation = getattr(context, "conversation", None)
    consulting = getattr(context, "consulting", None)
    presentation = getattr(context, "presentation", None)
    return {
        "evidence": _safe_records(evidence),
        "reasoning": _safe_records(reasoning),
        "knowledge": _safe_records(knowledge),
        "rewrite": _rewrite_records(rewrite),
        "conversation": _conversation_records(conversation),
        "consulting": _consulting_records(consulting),
        "presentation": _presentation_records(presentation),
    }


def _safe_records(value: object | None) -> list[dict[str, object]]:
    method = getattr(value, "to_trace_records", None)
    if callable(method):
        rows = method()
        return [dict(row) for row in rows] if isinstance(rows, list) else []
    return []


def _rewrite_records(rewrite: object | None) -> list[dict[str, object]]:
    if rewrite is None:
        return []
    rows: list[dict[str, object]] = []
    for item in getattr(rewrite, "items", ()) or ():
        record = getattr(item, "to_trace_record", None)
        if callable(record):
            rows.append(dict(record()))
            continue
        rows.append(
            {
                "rewrite_id": getattr(item, "rewrite_id", None),
                "semantic_key": getattr(item, "semantic_key", None),
                "status": getattr(item, "status", None),
                "customer_language": getattr(item, "customer_language", None),
            }
        )
    unresolved = getattr(rewrite, "unresolved", ()) or ()
    for item in unresolved:
        method = getattr(item, "to_trace_record", None)
        if callable(method):
            rows.append(dict(method()))
    return rows


def _conversation_records(conversation: object | None) -> list[dict[str, object]]:
    if conversation is None:
        return []
    return [
        {
            "flow": getattr(conversation, "flow", None),
            "status": getattr(conversation, "status", None),
        }
    ]


def _consulting_records(consulting: object | None) -> list[dict[str, object]]:
    if consulting is None:
        return []
    return [
        {
            "flow": getattr(consulting, "flow", None),
            "status": getattr(consulting, "status", None),
            "style_profile": getattr(consulting, "style_profile", None),
        }
    ]


def _presentation_records(presentation: object | None) -> list[dict[str, object]]:
    if presentation is None:
        return []
    metadata = getattr(presentation, "metadata", None)
    return [
        {
            "status": getattr(presentation, "status", None),
            "version": getattr(metadata, "version", None),
            "language": getattr(metadata, "language", None),
        }
    ]


def _knowledge_panel(knowledge: object | None) -> dict[str, object]:
    if knowledge is None:
        return {
            "status": None,
            "ids": [],
            "approved": [],
            "unresolved": [],
            "contract_gaps": [],
        }
    items = tuple(getattr(knowledge, "items", ()) or ())
    unresolved = tuple(getattr(knowledge, "unresolved", ()) or ())
    gaps = tuple(getattr(knowledge, "contract_gaps", ()) or ())
    approved = [
        {
            "knowledge_id": item.knowledge_id,
            "status": item.status,
            "semantic_key": item.semantic_key,
        }
        for item in items
        if getattr(item, "status", "") == "approved"
    ]
    return {
        "status": getattr(knowledge, "status", None),
        "ids": [item.knowledge_id for item in items],
        "approved": approved,
        "unresolved": [
            {
                "semantic_key": item.semantic_key,
                "reason": item.reason,
            }
            for item in unresolved
        ],
        "contract_gaps": [
            {"field": getattr(item, "field", None), "reason": getattr(item, "reason", None)}
            for item in gaps
        ],
    }


def _decision_rows(rewrite: object | None, interpretation: object | None) -> list[dict[str, object]]:
    if rewrite is None or interpretation is None:
        return []
    context = DecisionBuilder().build(rewrite, interpretation)
    return [item.to_trace_record() for item in context.items]


def _action_rows(plan: object | None) -> list[dict[str, object]]:
    if plan is None:
        return []
    rows: list[dict[str, object]] = []
    top = getattr(plan, "top_priority", None)
    if top is not None:
        rows.append(
            {
                "kind": "priority",
                "title": getattr(top, "title", None),
                "description": getattr(top, "description", None),
                "decision_id": getattr(top, "decision_id", None),
            }
        )
    for item in getattr(plan, "actions", ()) or ():
        rows.append(item.to_trace_record() if hasattr(item, "to_trace_record") else {"title": str(item)})
    return rows


def _pack05_snippet(payload: dict[str, Any] | None) -> dict[str, Any] | None:
    if not payload:
        return None
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    return {
        "contract": payload.get("contract"),
        "status": payload.get("status"),
        "identity": summary.get("identity") if isinstance(summary, dict) else None,
        "priority_recommendation": (
            summary.get("priority_recommendation") if isinstance(summary, dict) else None
        ),
    }


def _contract_panel(presentation: dict[str, Any] | None, runtime_status: str) -> dict[str, object]:
    metadata = presentation.get("metadata") if isinstance(presentation, dict) else None
    version = metadata.get("version") if isinstance(metadata, dict) else None
    status = presentation.get("status") if isinstance(presentation, dict) else None
    valid = version == PRESENTATION_VERSION and presentation is not None
    return {
        "schema": PRESENTATION_VERSION,
        "version": version,
        "status": status,
        "runtime_status": runtime_status,
        "validation": "pass" if valid else "reject",
        "root_fields": ["status", "overview", "interpretation", "action_plan", "commercial", "metadata"],
    }


def _quality_panel(context: object, presentation: dict[str, Any] | None) -> dict[str, object]:
    consulting = getattr(context, "consulting", None)
    conversation = getattr(context, "conversation", None)
    preserved = 0
    mismatched = 0
    segments = tuple(getattr(consulting, "segments", ()) or ()) if consulting is not None else ()
    for segment in segments:
        source = getattr(segment, "source_text", "") or ""
        styled = getattr(segment, "styled_text", "") or ""
        if source and styled and source in styled or getattr(segment, "meaning_fingerprint", None):
            preserved += 1
        else:
            mismatched += 1
    overview = presentation.get("overview") if isinstance(presentation, dict) else {}
    missing = [
        key
        for key in ("identity", "balance", "conclusion")
        if isinstance(overview, dict) and overview.get(key) is None
    ]
    return {
        "validation": _contract_panel(presentation, "studio").get("validation"),
        "conversation_status": getattr(conversation, "status", None),
        "consulting_status": getattr(consulting, "status", None),
        "meaning_preserved_segments": preserved,
        "meaning_mismatch_segments": mismatched,
        "contract_gaps": list(CONTRACT_GAPS) + [f"overview.{key} missing" for key in missing],
    }


def _fingerprint(presentation: Mapping[str, Any] | None) -> str:
    if not presentation:
        return "empty"
    interpretation = presentation.get("interpretation") if isinstance(presentation, dict) else None
    flow = ""
    if isinstance(interpretation, dict):
        flow = str(interpretation.get("consulting_flow") or "")
    return str(len(flow))


def _text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    return value if value.strip() else None
