"""Export cases to JSON / Markdown / HTML."""

from __future__ import annotations

import html
import json
from typing import Literal

from applications.case_management.models import CaseModel

ExportFormat = Literal["json", "markdown", "html"]


class CaseExporter:
    """Format a stored case for download / display."""

    def export(self, case: CaseModel, fmt: ExportFormat = "json") -> str:
        """Export case content in the requested format."""
        if fmt == "json":
            return self.to_json(case)
        if fmt == "markdown":
            return self.to_markdown(case)
        if fmt == "html":
            return self.to_html(case)
        raise ValueError(f"Unsupported export format: {fmt}")

    def to_json(self, case: CaseModel) -> str:
        """Pretty JSON export."""
        return json.dumps(case.to_dict(), ensure_ascii=False, indent=2, default=str)

    def to_markdown(self, case: CaseModel) -> str:
        """Markdown export preferring narrative/report markdown bodies."""
        narrative_md = (case.narrative_result or {}).get("markdown") or ""
        report_md = (case.report_result or {}).get("markdown") or ""
        summary = (case.interpretation_result or {}).get("summary") or ""
        lines = [
            f"# Case {case.case_id}",
            "",
            f"- Customer: `{case.customer_id}`",
            f"- Created: `{case.created_at}`",
            f"- Engine: `{case.engine_version}`",
            "",
            "## Summary",
            "",
            summary or "_No summary_",
            "",
        ]
        if narrative_md:
            lines.extend(["## Narrative", "", narrative_md, ""])
        elif report_md:
            lines.extend(["## Report", "", report_md, ""])
        else:
            lines.extend(
                [
                    "## Input snapshot",
                    "",
                    "```json",
                    json.dumps(case.input_snapshot, ensure_ascii=False, indent=2),
                    "```",
                    "",
                ]
            )
        return "\n".join(lines)

    def to_html(self, case: CaseModel) -> str:
        """HTML export preferring narrative/report HTML bodies."""
        narrative_html = (case.narrative_result or {}).get("html") or ""
        report_html = (case.report_result or {}).get("html") or ""
        summary = html.escape(
            str((case.interpretation_result or {}).get("summary") or "")
        )
        body = narrative_html or report_html or f"<p>{summary or 'No content'}</p>"
        return (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>Case {html.escape(case.case_id)}</title></head><body>"
            f"<h1>Case {html.escape(case.case_id)}</h1>"
            f"<p>Customer: {html.escape(case.customer_id)} · "
            f"{html.escape(case.created_at)} · "
            f"{html.escape(case.engine_version)}</p>"
            f"<section>{body}</section>"
            "</body></html>"
        )
