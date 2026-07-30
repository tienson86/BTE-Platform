"""Placeholder Binding — substitute template placeholders from AnalysisResult."""

from __future__ import annotations

import re
from typing import Any, Mapping

from engines.analysis_engine.interpretation_engine.exceptions import (
    InterpretationBindingError,
)
from engines.analysis_engine.interpretation_engine.knowledge_access import (
    KnowledgeSession,
)
from engines.analysis_engine.interpretation_engine.models import (
    BoundSentence,
    BoundTemplate,
    InterpretationContext,
)
from engines.analysis_engine.interpretation_engine.terminology_library import (
    TerminologyLibrary,
)
from engines.analysis_engine.interpretation_engine.validators import stage_payload
from engines.analysis_engine.runtime.models import AnalysisResult

_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*)\}")


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return ", ".join(_stringify(item) for item in value if item is not None)
    if isinstance(value, Mapping):
        # Prefer compact size hint for nested maps unless a known key exists.
        if "size" in value:
            return _stringify(value["size"])
        return str(dict(value))
    return str(value)


def build_placeholder_values(context: InterpretationContext) -> dict[str, str]:
    """Build a flat placeholder map from chart and stage payloads."""
    values: dict[str, str] = {}
    for key, raw in dict(context.chart).items():
        if isinstance(raw, (str, int, float)) or isinstance(raw, (list, tuple)):
            values[str(key)] = _stringify(raw)
            values[f"chart.{key}"] = _stringify(raw)

    analysis: AnalysisResult = context.analysis_result
    for stage_id in analysis.stage_results:
        payload = stage_payload(analysis, stage_id)
        for key, raw in payload.items():
            rendered = _stringify(raw)
            values[f"{stage_id}.{key}"] = rendered
            # Unprefixed alias — first writer wins for determinism by stage order.
            values.setdefault(str(key), rendered)

        # Derived helpers for nested summary fields used by luck templates.
        if stage_id == "luck":
            summary = payload.get("summary")
            if isinstance(summary, Mapping):
                for key, raw in summary.items():
                    values[str(key)] = _stringify(raw)
                    values[f"luck.{key}"] = _stringify(raw)
                    values[f"luck.summary.{key}"] = _stringify(raw)

        if stage_id == "ten_gods":
            presence = payload.get("presence")
            if isinstance(presence, (list, tuple)):
                values["presence_count"] = str(len(presence))
                values["ten_gods.presence_count"] = str(len(presence))

        if stage_id == "shensha":
            presence = payload.get("presence")
            if isinstance(presence, (list, tuple)):
                values["presence_count"] = str(len(presence))
                values["shensha.presence_count"] = str(len(presence))

        if stage_id == "useful_god":
            gods = payload.get("useful_gods")
            if gods is not None:
                values["useful_gods"] = _stringify(gods)

    return values


class PlaceholderBinder:
    """Bind placeholders inside template texts."""

    def __init__(
        self,
        *,
        terminology: TerminologyLibrary | None = None,
    ) -> None:
        self._terminology = terminology or TerminologyLibrary()

    def bind(
        self,
        templates: tuple[BoundTemplate, ...],
        context: InterpretationContext,
        *,
        session: KnowledgeSession | None = None,
    ) -> tuple[BoundSentence, ...]:
        """Substitute placeholders; fail closed on required missing values."""
        base_values = build_placeholder_values(context)
        terminology_used: dict[str, tuple[str, ...]] = {}
        if session is not None:
            base_values, _ = self._terminology.apply_to_values(
                base_values,
                session=session,
            )
        bound: list[BoundSentence] = []
        for item in templates:
            values = self._values_for_stage(
                base_values,
                context.analysis_result,
                item.source_stage,
            )
            if session is not None:
                values, used_terms = self._terminology.apply_to_values(
                    values,
                    session=session,
                )
                terminology_used[item.sentence_id] = used_terms
            text, used = self._render(
                item.template_text,
                values,
                required=item.required_placeholders,
                sentence_id=item.sentence_id,
            )
            metadata = dict(item.metadata)
            if item.sentence_id in terminology_used:
                metadata["terminology_ids"] = list(
                    terminology_used[item.sentence_id]
                )
            bound.append(
                BoundSentence(
                    sentence_id=item.sentence_id,
                    section_id=item.section_id,
                    source_stage=item.source_stage,
                    template_id=item.template_id,
                    text=text,
                    priority=item.priority,
                    bound_values=used,
                    metadata=metadata,
                )
            )
        return tuple(bound)

    @staticmethod
    def _values_for_stage(
        base_values: Mapping[str, str],
        analysis: AnalysisResult,
        source_stage: str,
    ) -> dict[str, str]:
        """Prefer source-stage fields so shared aliases stay stage-local."""
        values = dict(base_values)
        payload = stage_payload(analysis, source_stage)
        for key, raw in payload.items():
            values[str(key)] = _stringify(raw)
            values[f"{source_stage}.{key}"] = _stringify(raw)
        if source_stage == "luck":
            summary = payload.get("summary")
            if isinstance(summary, Mapping):
                for key, raw in summary.items():
                    values[str(key)] = _stringify(raw)
        if source_stage in {"ten_gods", "shensha"}:
            presence = payload.get("presence")
            if isinstance(presence, (list, tuple)):
                values["presence_count"] = str(len(presence))
        if source_stage == "useful_god" and payload.get("useful_gods") is not None:
            values["useful_gods"] = _stringify(payload.get("useful_gods"))
        return values

    def _render(
        self,
        template_text: str,
        values: Mapping[str, str],
        *,
        required: tuple[str, ...],
        sentence_id: str,
    ) -> tuple[str, dict[str, str]]:
        used: dict[str, str] = {}
        missing_required: list[str] = []

        def replacer(match: re.Match[str]) -> str:
            key = match.group(1)
            if key not in values or values[key] == "":
                if key in required:
                    missing_required.append(key)
                return match.group(0)
            used[key] = values[key]
            return values[key]

        rendered = _PLACEHOLDER_RE.sub(replacer, template_text)
        for key in required:
            if key not in used:
                if key in values and values[key] != "":
                    used[key] = values[key]
                else:
                    if key not in missing_required:
                        missing_required.append(key)
        if missing_required:
            raise InterpretationBindingError(
                "Required placeholders unresolved",
                details={
                    "sentence_id": sentence_id,
                    "missing": missing_required,
                },
            )
        return rendered, used
