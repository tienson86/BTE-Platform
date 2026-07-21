"""
Sentence Generator
==================

Sinh câu luận giải từ SemanticBlock.

Pipeline:

SemanticBlock
    ↓
SentenceGenerator
    ↓
GeneratedSentence
"""

from __future__ import annotations

from typing import Any

from .models.generated_sentence import GeneratedSentence
from .models.semantic_block import SemanticBlock


DEFAULT_TEMPLATES = {

    "tong_quan":
        "{title}.",

    "than_vuong_nhuoc":
        "{title}.",

    "dung_than":
        "{title}.",

}


class SentenceGenerator:

    def __init__(
        self,
        templates: dict[str, str] | None = None,
    ):

        self.templates = templates or DEFAULT_TEMPLATES

    def generate(
        self,
        blocks: list[SemanticBlock],
    ) -> list[GeneratedSentence]:

        sentences = []

        for block in blocks:

            sentences.append(
                self.generate_sentence(block)
            )

        return sentences

    def generate_sentence(
        self,
        block: SemanticBlock,
    ) -> GeneratedSentence:

        template = self.templates.get(
            block.topic,
            "{title}."
        )

        sentence = template.format(

            title=block.title,

            **block.metadata,

        )

        return GeneratedSentence(

            topic=block.topic,

            sentence=sentence,

            priority=block.priority,

            confidence=1.0,

            source_rules=block.source_rules.copy(),

            metadata=block.metadata.copy(),

        )


def generate_sentences(
    blocks: list[SemanticBlock],
) -> list[GeneratedSentence]:

    return SentenceGenerator().generate(blocks)
