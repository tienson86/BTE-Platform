"""
Sentence Generator
==================

Sinh câu luận giải từ SemanticBlock / InterpretationResult.

Pipeline:

SemanticBlock
    ↓
SentenceGenerator (internal GeneratedSentence)
    ↓
str  (public API)

InterpretationResult may be enriched in place; public ``generate``
always returns ``str``.
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
    ) -> str:
        """
        Public API: always return a string.

        - InterpretationResult: enrich in place, then join sentence text
        - list[SemanticBlock]: generate GeneratedSentence internally, adapt to str
        - other / empty: return ""
        """

        # Late import avoids circular dependency with engine/legacy_builder
        from .legacy_builder import InterpretationResult

        if isinstance(blocks, InterpretationResult):
            self._enrich_result(blocks)
            return self._result_to_text(blocks)

        if isinstance(blocks, list):
            sentences = self.generate_sentences(blocks)
            return self._sentences_to_text(sentences)

        # Backward-compatible empty generate({}) → str
        return ""

    def generate_sentences(
        self,
        blocks: list[SemanticBlock],
    ) -> list[GeneratedSentence]:
        """Internal path: SemanticBlock → GeneratedSentence (unchanged)."""
        sentences: list[GeneratedSentence] = []
        for block in blocks:
            sentences.append(self.generate_sentence(block))
        return sentences

    def _enrich_result(self, result: Any) -> Any:
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

    @staticmethod
    def _sentences_to_text(sentences: list[GeneratedSentence]) -> str:
        """Adapter: GeneratedSentence list → public str."""
        parts = [
            str(item.sentence).strip()
            for item in sentences
            if getattr(item, "sentence", None) and str(item.sentence).strip()
        ]
        return "\n".join(parts)

    @staticmethod
    def _result_to_text(result: Any) -> str:
        """Adapter: InterpretationResult sentences → public str."""
        parts: list[str] = []
        for item in getattr(result, "sentences", None) or []:
            if isinstance(item, dict):
                text = str(item.get("sentence") or "").strip()
            else:
                text = str(getattr(item, "sentence", "") or "").strip()
            if text:
                parts.append(text)
        if parts:
            return "\n".join(parts)
        summary = str(getattr(result, "summary", "") or "").strip()
        return summary

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
) -> str:
    """Public helper — returns str (same contract as SentenceGenerator.generate)."""
    return SentenceGenerator().generate(blocks)
