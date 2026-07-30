"""Table Renderer — render StructuredDataBlock as tables."""

from __future__ import annotations

import html
import json
from typing import Any, Mapping, Sequence

from engines.analysis_engine.report_generator.models import StructuredDataBlock


class TableRenderer:
    """Render analytical payloads as deterministic tables."""

    def render_html(self, block: StructuredDataBlock) -> str:
        """Render a data block as an HTML table (or key/value table)."""
        table = self._as_table(dict(block.payload))
        if table is not None:
            headers, rows = table
            head = "".join(
                f"<th>{html.escape(str(header))}</th>" for header in headers
            )
            body_rows = []
            for row in rows:
                cells = "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row)
                body_rows.append(f"<tr>{cells}</tr>")
            table_html = (
                '<table class="report-table">\n'
                f"  <thead><tr>{head}</tr></thead>\n"
                f"  <tbody>\n    " + "\n    ".join(body_rows) + "\n  </tbody>\n"
                "</table>"
            )
        else:
            rows_html = []
            for key, value in self._key_value_rows(dict(block.payload)):
                rows_html.append(
                    "<tr>"
                    f"<th>{html.escape(key)}</th>"
                    f"<td>{html.escape(value)}</td>"
                    "</tr>"
                )
            table_html = (
                '<table class="report-table">\n'
                "  <tbody>\n    " + "\n    ".join(rows_html) + "\n  </tbody>\n"
                "</table>"
            )
        return (
            f'    <div class="data-block" id="{html.escape(block.block_id)}">\n'
            f"      <h3>{html.escape(block.title)}</h3>\n"
            f"      {table_html}\n"
            f"    </div>"
        )

    def render_markdown(self, block: StructuredDataBlock) -> str:
        """Render a data block as a Markdown table or fenced JSON fallback."""
        lines = [f"### {block.title}", ""]
        table = self._as_table(dict(block.payload))
        if table is not None:
            headers, rows = table
            lines.append("| " + " | ".join(str(h) for h in headers) + " |")
            lines.append("| " + " | ".join("---" for _ in headers) + " |")
            for row in rows:
                lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
            lines.append("")
            return "\n".join(lines)

        kv = self._key_value_rows(dict(block.payload))
        if kv:
            lines.append("| Field | Value |")
            lines.append("| --- | --- |")
            for key, value in kv:
                lines.append(f"| {key} | {value} |")
            lines.append("")
            return "\n".join(lines)

        lines.append("```json")
        lines.append(
            json.dumps(dict(block.payload), ensure_ascii=False, sort_keys=True, indent=2)
        )
        lines.append("```")
        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _as_table(
        payload: Mapping[str, Any],
    ) -> tuple[tuple[str, ...], list[tuple[str, ...]]] | None:
        """Detect list-of-dicts payloads suitable for tabular rendering."""
        for key in sorted(payload):
            value = payload[key]
            if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
                continue
            items = list(value)
            if not items or not all(isinstance(item, Mapping) for item in items):
                continue
            headers: list[str] = []
            for item in items:
                for child_key in sorted(item):
                    if child_key not in headers:
                        headers.append(str(child_key))
            rows: list[tuple[str, ...]] = []
            for item in items:
                rows.append(tuple(str(item.get(header, "")) for header in headers))
            return tuple(headers), rows
        return None

    @staticmethod
    def _key_value_rows(payload: Mapping[str, Any]) -> list[tuple[str, str]]:
        rows: list[tuple[str, str]] = []
        for key in sorted(payload):
            value = payload[key]
            if isinstance(value, Mapping):
                rendered = ", ".join(
                    f"{child_key}={child_value}"
                    for child_key, child_value in sorted(
                        value.items(), key=lambda item: str(item[0])
                    )
                )
            elif isinstance(value, (list, tuple)):
                if value and all(isinstance(item, Mapping) for item in value):
                    continue
                rendered = ", ".join(str(item) for item in value)
            else:
                rendered = str(value)
            rows.append((str(key), rendered))
        return rows
