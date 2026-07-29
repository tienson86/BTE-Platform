"""
Chapter Builder
"""

from __future__ import annotations

from ..models import (
    Chapter,
    Paragraph,
)


class ChapterBuilder:

    def build(
        self,
        paragraphs: list[Paragraph],
    ) -> list[Chapter]:

        if not paragraphs:

            return []

        chapter = Chapter(
            title="Diễn giải",
            paragraphs=paragraphs,
        )

        return [chapter]
