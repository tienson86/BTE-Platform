"""
Sentence Builder
"""

from __future__ import annotations

from ..models import (
    InterpretationContext,
    Sentence,
)


class SentenceBuilder:

    def build(
        self,
        templates,
        context: InterpretationContext,
    ) -> list[Sentence]:

        sentences = []

        for template in templates:

            text = template.get(
                "text",
                "",
            )

            sentence = Sentence(
                text=text,
            )

            sentences.append(
                sentence
            )

        return sentences
