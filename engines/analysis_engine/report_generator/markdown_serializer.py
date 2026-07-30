"""Markdown serializer for StructuredReport."""

from __future__ import annotations

import json

from engines.analysis_engine.report_generator.exceptions import ReportSerializationError
from engines.analysis_engine.report_generator.models import (
    LayoutTemplate,
    MarkdownReportArtifact,
    StructuredReport,
)


class MarkdownSerializer:
    """Serialize StructuredReport to Markdown using layout template."""

    def serialize(
        self,
        report: StructuredReport,
        *,
        template: LayoutTemplate,
    ) -> MarkdownReportArtifact:
        """Render deterministic Markdown artifact."""
        try:
            section_parts: list[str] = []
            for section in report.sections:
                section_parts.append(f"## {section.title}")
                section_parts.append("")
                section_parts.append(section.body)
                section_parts.append("")
            sections_md = "\n".join(section_parts).rstrip() + "\n"

            data_md = ""
            if report.data_blocks:
                lines = ["## Analytical Data", ""]
                for block in report.data_blocks:
                    lines.append(f"### {block.title}")
                    lines.append("")
                    lines.append("```json")
                    lines.append(
                        json.dumps(
                            dict(block.payload),
                            ensure_ascii=False,
                            sort_keys=True,
                            indent=2,
                        )
                    )
                    lines.append("```")
                    lines.append("")
                data_md = "\n".join(lines)

            content = template.markdown_shell.format(
                title=report.metadata.title,
                overview=report.overview,
                sections=sections_md,
                data_blocks=data_md,
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise ReportSerializationError(
                "Markdown serialization failed",
                details={"error": str(exc)},
            ) from exc
        return MarkdownReportArtifact(content=content)
