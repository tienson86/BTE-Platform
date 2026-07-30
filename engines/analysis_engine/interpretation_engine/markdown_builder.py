"""Markdown Builder — render InterpretationResult as Markdown."""

from __future__ import annotations

from engines.analysis_engine.interpretation_engine.models import InterpretationResult


class MarkdownBuilder:
    """Build deterministic Markdown from chapters and sections."""

    def build(self, result: InterpretationResult) -> str:
        """Render Markdown narrative for the interpretation."""
        lines: list[str] = [
            "# Luận giải Bát Tự",
            "",
            result.overview.strip(),
            "",
        ]
        if result.chapters:
            for chapter in result.chapters:
                lines.append(f"## {chapter.title}")
                lines.append("")
                for section in chapter.sections:
                    lines.append(f"### {section.title}")
                    lines.append("")
                    lines.append(section.body.strip())
                    lines.append("")
        else:
            for section in result.sections:
                lines.append(f"## {section.title}")
                lines.append("")
                lines.append(section.body.strip())
                lines.append("")
        return "\n".join(lines).rstrip() + "\n"
