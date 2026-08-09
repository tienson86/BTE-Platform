"""Report engine adapter boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from applications.api.adapters.analysis_adapter import extract_birth_kwargs
from applications.api.contracts.analyze_request import AnalyzeRequest
from applications.api.contracts.report_response import (
    LayoutInfo,
    RenderOptionsInfo,
    ReportBlock,
    ReportPayload,
    ThemeInfo,
)
from applications.api.services.orchestrator import OrchestratorService


@dataclass(slots=True)
class ReportAdaptation:
    """Adapted report section from engine output."""

    report: ReportPayload
    engine_payload: dict[str, Any]


def map_report_payload(
    engine_payload: dict[str, Any],
    request: AnalyzeRequest,
) -> ReportPayload:
    """Adapt engine report payload into ReportPayload."""
    data = engine_payload.get("report")
    payload = data if isinstance(data, dict) else {}
    title = str(payload.get("title") or request.report_template or "BTE Report")
    blocks: list[ReportBlock] = []
    markdown = payload.get("markdown")
    if isinstance(markdown, str) and markdown.strip():
        blocks.append(
            ReportBlock(
                id="markdown",
                type="markdown",
                title=title,
                content=markdown,
            )
        )
    html = payload.get("html")
    if isinstance(html, str) and html.strip():
        blocks.append(
            ReportBlock(
                id="html",
                type="html",
                title=title,
                content=html,
            )
        )
    for index, item in enumerate(payload.get("blocks") or []):
        if not isinstance(item, dict):
            continue
        blocks.append(
            ReportBlock(
                id=str(item.get("id") or f"block_{index}") or None,
                type=str(item.get("type") or "") or None,
                title=str(item.get("title") or "") or None,
                content=str(item.get("content") or "") or None,
            )
        )
    return ReportPayload(
        title=title,
        blocks=blocks,
        theme=ThemeInfo(name=request.report_template, variant=None),
        layout=LayoutInfo(name=request.report_template, variant=None),
        render_options=RenderOptionsInfo(format="json", locale=request.language),
    )


class ReportAdapter:
    """Isolates Report Engine integration via OrchestratorService."""

    def __init__(self, orchestrator: OrchestratorService | None = None) -> None:
        self._orchestrator = orchestrator or OrchestratorService()

    def execute(self, request: AnalyzeRequest) -> ReportAdaptation:
        """Run Report Engine through full analyze and adapt to contract section."""
        birth = extract_birth_kwargs(request)
        engine_payload = self._orchestrator.analyze(**birth)
        return ReportAdaptation(
            report=map_report_payload(engine_payload, request),
            engine_payload=engine_payload,
        )
