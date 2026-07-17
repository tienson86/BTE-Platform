"""
Markdown Renderer
"""

from __future__ import annotations

from .base_renderer import BaseRenderer

from ..models import Chapter


class MarkdownRenderer(BaseRenderer):

    name = "markdown"

    extension = ".md"

    mime_type = "text/markdown"

    def render(
        self,
        chapters: list[Chapter],
    ) -> str:

        lines: list[str] = []

        for chapter in chapters:

            lines.append(
                f"# {chapter.title}"
            )

            lines.append("")

            for paragraph in chapter.paragraphs:

                lines.append(
                    f"## {paragraph.title}"
                )

                lines.append("")

                for sentence in paragraph.sentences:

                    lines.append(
                        sentence.text
                    )

                lines.append("")

        return "\n".join(lines)
