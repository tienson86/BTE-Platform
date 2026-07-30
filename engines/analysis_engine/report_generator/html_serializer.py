"""HTML serializer for StructuredReport."""

from __future__ import annotations

import html
import json

from engines.analysis_engine.report_generator.exceptions import ReportSerializationError
from engines.analysis_engine.report_generator.models import (
    HtmlReportArtifact,
    LayoutTemplate,
    ReportTheme,
    StructuredReport,
)


class HtmlSerializer:
    """Serialize StructuredReport to HTML using layout template + theme."""

    def serialize(
        self,
        report: StructuredReport,
        *,
        theme: ReportTheme,
        template: LayoutTemplate,
    ) -> HtmlReportArtifact:
        """Render deterministic HTML artifact."""
        try:
            sections_html = "\n".join(
                (
                    f'  <section id="{html.escape(section.section_id)}">\n'
                    f"    <h2>{html.escape(section.title)}</h2>\n"
                    f"    <p>{html.escape(section.body)}</p>\n"
                    f"  </section>"
                )
                for section in report.sections
            )
            data_html = ""
            if report.data_blocks:
                blocks = ["  <aside class=\"structured-data\">", "    <h2>Analytical Data</h2>"]
                for block in report.data_blocks:
                    payload = html.escape(
                        json.dumps(dict(block.payload), ensure_ascii=False, sort_keys=True)
                    )
                    blocks.append(
                        f'    <div class="data-block" id="{html.escape(block.block_id)}">\n'
                        f"      <h3>{html.escape(block.title)}</h3>\n"
                        f"      <pre>{payload}</pre>\n"
                        f"    </div>"
                    )
                blocks.append("  </aside>")
                data_html = "\n".join(blocks)

            content = template.html_shell.format(
                title=html.escape(report.metadata.title),
                overview=html.escape(report.overview),
                theme_css=theme.css_block(),
                font_family=html.escape(theme.font_family),
                sections=sections_html,
                data_blocks=data_html,
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise ReportSerializationError(
                "HTML serialization failed",
                details={"error": str(exc)},
            ) from exc
        return HtmlReportArtifact(content=content)
