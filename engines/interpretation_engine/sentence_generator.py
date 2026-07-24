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
        blocks: list[SemanticBlock] | Any,
    ) -> list[GeneratedSentence] | Any:
        """
        Sinh câu từ danh sách SemanticBlock.

        WP4: InterpretationResult — attach sentence text from rule descriptions
        when missing, then pass through.
        """

        # Late import avoids circular dependency with engine/legacy_builder
        from .legacy_builder import InterpretationResult

        if isinstance(blocks, InterpretationResult):
            return self._enrich_result(blocks)

        if not isinstance(blocks, list):
            # Backward-compatible empty generate({}) → str
            return ""

        sentences = []

        for block in blocks:

            sentences.append(
                self.generate_sentence(block)
            )

        return sentences

    def _enrich_result(self, result: InterpretationResult) -> InterpretationResult:
        """Ensure each section rule has a sentence; drop duplicate texts (WP5)."""
        collected: list[dict[str, Any]] = []
        seen_text: set[str] = set()
        for name, section in (result.sections or {}).items():
            for rule in section.rules:
                text = (
                    rule.get("sentence")
                    or rule.get("description")
                    or rule.get("message")
                    or rule.get("rule_name")
                    or ""
                )
                if not text:
                    continue
                key = str(text).strip().lower()
                if key in seen_text:
                    continue
                seen_text.add(key)
                rule["sentence"] = text
                collected.append(
                    {
                        "section": name,
                        "rule_id": rule.get("rule_id"),
                        "sentence": text,
                        "priority": rule.get("priority", 0),
                        "confidence": rule.get("confidence", 0),
                    }
                )
        if collected:
            result.sentences = collected
            result.sentence_count = len(collected)
        result.section_count = sum(
            1 for section in (result.sections or {}).values() if section.rules
        )
        return result

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
