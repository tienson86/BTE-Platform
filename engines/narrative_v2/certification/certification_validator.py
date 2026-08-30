"""Quality-gate evaluation from Presentation and review summaries."""

from __future__ import annotations

import json
from typing import Any, Mapping

from engines.narrative_v2.export import build_export_context, presentation_from_mapping
from engines.narrative_v2.export.export_errors import ExportError
from engines.narrative_v2.presentation.presentation_status import (
    ALLOWED_STATUSES,
    PRESENTATION_VERSION,
)
from engines.narrative_v2.presentation.presentation_validator import FORBIDDEN_SUBSTRINGS

from engines.narrative_v2.certification.certification_context import CertificationContext
from engines.narrative_v2.certification.certification_result import QUALITY_GATES

PASS = "PASS"
FAIL = "FAIL"

NON_CRITICAL_NOTES: tuple[str, ...] = (
    "overview.identity is null",
    "overview.balance is null",
    "overview.conclusion is null",
    "commercial is null",
    "action_plan.current_period is null",
)


class CertificationValidator:
    """Score quality gates. Does not rewrite Presentation."""

    def evaluate(self, context: CertificationContext) -> dict[str, Any]:
        """Return per-gate PASS/FAIL plus notes. Never mutates input."""
        presentation = dict(context.presentation)
        checks = {
            "technical": self._technical(presentation, context.validation_summary),
            "semantic": self._semantic(presentation),
            "language": self._language(presentation),
            "conversation": self._conversation(presentation),
            "consulting": self._consulting(presentation),
            "presentation": self._presentation(presentation),
            "export": self._export(presentation),
            "no_critical_issues": self._no_critical(presentation, context.test_summary),
        }
        notes = [note for note in NON_CRITICAL_NOTES if _note_applies(presentation, note)]
        all_passed = all(checks[name] == PASS for name in QUALITY_GATES)
        return {
            "gates": checks,
            "all_passed": all_passed,
            "notes": notes,
            "studio_verdict": str(context.studio_review.get("verdict") or ""),
            "validation": str(context.validation_summary.get("status") or ""),
            "tests": str(context.test_summary.get("status") or ""),
        }

    def _technical(self, presentation: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
        status = str(presentation.get("status") or "")
        if status not in ALLOWED_STATUSES or status == "invalid":
            return FAIL
        if str(validation.get("status") or "PASS").upper() not in {"PASS", "OK", ""}:
            return FAIL
        return PASS

    def _semantic(self, presentation: Mapping[str, Any]) -> str:
        interpretation = _record(presentation.get("interpretation"))
        if not interpretation:
            return FAIL
        flow = _text(interpretation.get("consulting_flow"))
        meaning = _text(interpretation.get("meaning"))
        observation = _text(interpretation.get("observation"))
        if flow and (meaning or observation):
            return PASS
        return FAIL

    def _language(self, presentation: Mapping[str, Any]) -> str:
        metadata = _record(presentation.get("metadata")) or {}
        language = str(metadata.get("language") or "")
        if language != "vi":
            return FAIL
        blob = json.dumps(presentation, ensure_ascii=False)
        for token in FORBIDDEN_SUBSTRINGS:
            if token in blob:
                return FAIL
        return PASS

    def _conversation(self, presentation: Mapping[str, Any]) -> str:
        interpretation = _record(presentation.get("interpretation")) or {}
        return PASS if _text(interpretation.get("consulting_flow")) else FAIL

    def _consulting(self, presentation: Mapping[str, Any]) -> str:
        return self._conversation(presentation)

    def _presentation(self, presentation: Mapping[str, Any]) -> str:
        metadata = _record(presentation.get("metadata")) or {}
        version = str(metadata.get("version") or "")
        return PASS if version == PRESENTATION_VERSION else FAIL

    def _export(self, presentation: Mapping[str, Any]) -> str:
        try:
            model = presentation_from_mapping(presentation)
            context = build_export_context(model)
        except (ExportError, TypeError, ValueError, KeyError):
            return FAIL
        if not context.blocks:
            return FAIL
        if context.version != PRESENTATION_VERSION:
            return FAIL
        return PASS

    def _no_critical(self, presentation: Mapping[str, Any], tests: Mapping[str, Any]) -> str:
        if str(presentation.get("status") or "") == "invalid":
            return FAIL
        if str(tests.get("status") or "PASS").upper() in {"FAIL", "FAILED", "ERROR"}:
            return FAIL
        blob = json.dumps(presentation, ensure_ascii=False)
        for token in ("pipeline_trace", "NR-REL-", "runtime_metrics"):
            if token in blob:
                return FAIL
        return PASS


def _note_applies(presentation: Mapping[str, Any], note: str) -> bool:
    overview = _record(presentation.get("overview")) or {}
    action = _record(presentation.get("action_plan")) or {}
    if note.startswith("overview.identity") and overview.get("identity") is None:
        return True
    if note.startswith("overview.balance") and overview.get("balance") is None:
        return True
    if note.startswith("overview.conclusion") and overview.get("conclusion") is None:
        return True
    if note.startswith("commercial") and presentation.get("commercial") is None:
        return True
    if note.startswith("action_plan.current_period") and action.get("current_period") is None:
        return True
    return False


def _record(value: object) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""
