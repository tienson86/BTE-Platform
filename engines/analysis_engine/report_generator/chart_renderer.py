"""Chart Renderer — deterministic chart components from analytical payloads."""

from __future__ import annotations

import html
from typing import Any, Mapping

from engines.analysis_engine.report_generator.models import StructuredDataBlock


class ChartRenderer:
    """Render simple deterministic bar charts for numeric payload fields.

    No external charting libraries — pure HTML/CSS and Markdown text charts.
    """

    def render_html(self, block: StructuredDataBlock) -> str:
        """Render an HTML chart block when numeric series exist."""
        series = self._numeric_series(dict(block.payload))
        if not series:
            return ""
        max_value = max(value for _, value in series) or 1.0
        bars: list[str] = []
        for label, value in series:
            width = max(0.0, min(100.0, (value / max_value) * 100.0))
            bars.append(
                f'      <div class="chart-row">\n'
                f"        <div>{html.escape(label)}: {value:g}</div>\n"
                f'        <div class="chart-bar-track">'
                f'<div class="chart-bar-fill" style="width:{width:.2f}%"></div>'
                f"</div>\n"
                f"      </div>"
            )
        return (
            f'    <div class="chart-block" id="{html.escape(block.block_id)}-chart">\n'
            f"      <h3>{html.escape(block.title)} Chart</h3>\n"
            + "\n".join(bars)
            + "\n    </div>"
        )

    def render_markdown(self, block: StructuredDataBlock) -> str:
        """Render a Markdown text bar chart when numeric series exist."""
        series = self._numeric_series(dict(block.payload))
        if not series:
            return ""
        max_value = max(value for _, value in series) or 1.0
        lines = [f"### {block.title} Chart", ""]
        for label, value in series:
            units = int(round((value / max_value) * 20)) if max_value else 0
            bar = "#" * units
            lines.append(f"- {label}: {value:g} `{bar}`")
        return "\n".join(lines)

    @staticmethod
    def _numeric_series(payload: Mapping[str, Any]) -> list[tuple[str, float]]:
        """Extract sortable numeric leaf values for charting."""
        series: list[tuple[str, float]] = []
        for key in sorted(payload):
            value = payload[key]
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)):
                series.append((str(key), float(value)))
                continue
            if isinstance(value, Mapping):
                for child_key in sorted(value):
                    child = value[child_key]
                    if isinstance(child, bool):
                        continue
                    if isinstance(child, (int, float)):
                        series.append((f"{key}.{child_key}", float(child)))
        return series
