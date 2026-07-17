"""
Paragraph Builder
"""

from __future__ import annotations

from ..models import (
    Paragraph,
    Sentence,
)


class ParagraphBuilder:

    def build(
        self,
        sentences: list[Sentence],
    ) -> list[Paragraph]:

        if not sentences:

            return []

        paragraph = Paragraph(
            title="Nội dung",
            sentences=sentences,
        )

        return [paragraph]
