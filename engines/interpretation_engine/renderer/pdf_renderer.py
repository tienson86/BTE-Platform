"""
BTE Platform
PDF Renderer
"""

from __future__ import annotations

from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

from .base_renderer import BaseRenderer
from ..models import Chapter


class PdfRenderer(BaseRenderer):

    name = "pdf"

    extension = ".pdf"

    mime_type = "application/pdf"

    def render(
        self,
        chapters: list[Chapter],
    ) -> bytes:

        buffer = BytesIO()

        document = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        for chapter in chapters:

            story.append(
                Paragraph(
                    f"<b>{chapter.title}</b>",
                    styles["Heading1"],
                )
            )

            for paragraph in chapter.paragraphs:

                story.append(
                    Paragraph(
                        paragraph.title,
                        styles["Heading2"],
                    )
                )

                for sentence in paragraph.sentences:

                    story.append(
                        Paragraph(
                            sentence.text,
                            styles["BodyText"],
                        )
                    )

        document.build(story)

        return buffer.getvalue()
