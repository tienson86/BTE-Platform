"""
BTE Platform
Interpretation Renderer
"""

from __future__ import annotations

import json

from ..models import (
    InterpretationResult,
    Chapter,
    Paragraph,
)


class Renderer:
    """
    Renderer trung tâm.

    Chuyển InterpretationResult
    sang Markdown / HTML / JSON.
    """

    # =====================================================
    # Main
    # =====================================================

    def render(
        self,
        chapters: list[Chapter],
    ) -> InterpretationResult:

        result = InterpretationResult()

        result.chapters = chapters

        result.markdown = self.render_markdown(
            chapters
        )

        result.html = self.render_html(
            chapters
        )

        result.json = self.render_json(
            chapters
        )

        return result

    # =====================================================
    # Markdown
    # =====================================================

    def render_markdown(
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

                    lines.append(sentence.text)

                lines.append("")

        return "\n".join(lines)

    # =====================================================
    # HTML
    # =====================================================

    def render_html(
        self,
        chapters: list[Chapter],
    ) -> str:

        html: list[str] = [
            "<html>",
            "<body>",
        ]

        for chapter in chapters:

            html.append(
                f"<h1>{chapter.title}</h1>"
            )

            for paragraph in chapter.paragraphs:

                html.append(
                    f"<h2>{paragraph.title}</h2>"
                )

                html.append("<p>")

                for sentence in paragraph.sentences:

                    html.append(sentence.text)
                    html.append("<br>")

                html.append("</p>")

        html.extend([
            "</body>",
            "</html>",
        ])

        return "\n".join(html)

    # =====================================================
    # JSON
    # =====================================================

    def render_json(
        self,
        chapters: list[Chapter],
    ) -> dict:

        return {
            "chapters": [
                {
                    "title": chapter.title,
                    "paragraphs": [
                        {
                            "title": paragraph.title,
                            "sentences": [
                                sentence.text
                                for sentence in paragraph.sentences
                            ],
                        }
                        for paragraph in chapter.paragraphs
                    ],
                }
                for chapter in chapters
            ]
        }

    def render_json_string(
        self,
        chapters: list[Chapter],
    ) -> str:

        return json.dumps(
            self.render_json(chapters),
            ensure_ascii=False,
            indent=2,
        )
