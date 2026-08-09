"""Interpretation engine adapter boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from applications.api.adapters.analysis_adapter import extract_birth_kwargs
from applications.api.contracts.analyze_request import AnalyzeRequest
from applications.api.contracts.report_response import (
    InterpretationPayload,
    ReferenceInfo,
    SectionInfo,
    SentenceInfo,
)
from applications.api.services.orchestrator import OrchestratorService


@dataclass(slots=True)
class InterpretationAdaptation:
    """Adapted interpretation section from engine output."""

    interpretation: InterpretationPayload
    engine_payload: dict[str, Any]


def map_interpretation_payload(engine_payload: dict[str, Any]) -> InterpretationPayload:
    """Adapt engine interpretation payload into InterpretationPayload."""
    data = engine_payload.get("interpretation")
    payload = data if isinstance(data, dict) else {}
    sections: list[SectionInfo] = []
    for item in payload.get("sections") or []:
        if not isinstance(item, dict):
            continue
        sections.append(
            SectionInfo(
                id=str(item.get("id") or "") or None,
                title=str(item.get("title") or "") or None,
                content=str(item.get("body") or item.get("content") or "") or None,
            )
        )
    sentences: list[SentenceInfo] = []
    for item in payload.get("sentences") or []:
        if isinstance(item, dict) and item.get("text") is not None:
            sentences.append(
                SentenceInfo(
                    id=str(item.get("id") or "") or None,
                    text=str(item.get("text")),
                )
            )
        elif isinstance(item, str) and item.strip():
            sentences.append(SentenceInfo(id=None, text=item.strip()))
    references: list[ReferenceInfo] = []
    for item in payload.get("references") or []:
        if not isinstance(item, dict):
            continue
        references.append(
            ReferenceInfo(
                id=str(item.get("id") or "") or None,
                source=str(item.get("source") or "") or None,
                locator=str(item.get("locator") or "") or None,
            )
        )
    confidence_raw = payload.get("confidence")
    confidence: float | None
    try:
        confidence = float(confidence_raw) if confidence_raw is not None else None
    except (TypeError, ValueError):
        confidence = None
    return InterpretationPayload(
        sections=sections,
        sentences=sentences,
        references=references,
        confidence=confidence,
    )


class InterpretationAdapter:
    """Isolates Interpretation Engine integration via OrchestratorService."""

    def __init__(self, orchestrator: OrchestratorService | None = None) -> None:
        self._orchestrator = orchestrator or OrchestratorService()

    def execute(self, request: AnalyzeRequest) -> InterpretationAdaptation:
        """Run Interpretation Engine stage and adapt to contract section."""
        birth = extract_birth_kwargs(request)
        engine_payload = self._orchestrator.run_stage("interpretation", **birth)
        return InterpretationAdaptation(
            interpretation=map_interpretation_payload(engine_payload),
            engine_payload=engine_payload,
        )
