"""
HTML Renderer
"""

from __future__ import annotations

from .base_renderer import BaseRenderer

from ..models import Chapter


class HtmlRenderer(BaseRenderer):

    name = "html"

    extension = ".html"

    mime_type = "text/html"

    def render(
        self,
        chapters: list[Chapter],
    ) -> str:

        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            '<meta charset="utf-8">',
            "</head>",
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

                    html.append(
                        sentence.text
                    )

                    html.append("<br>")

                html.append("</p>")

        html.extend([
            "</body>",
            "</html>",
        ])

        return "\n".join(html)
