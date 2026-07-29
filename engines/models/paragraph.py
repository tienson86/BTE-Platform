"""
paragraph.py
============

Report Paragraph Model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .sentence import ReportSentence


@dataclass(slots=True)
class ReportParagraph:
    """
    Một đoạn văn trong báo cáo.
    """

    title: str = ""

    description: str = ""

    sentences: list[ReportSentence] = field(default_factory=list)

    rule_count: int = 0

    order: int = 0

    @property
    def text(self) -> str:
        return " ".join(sentence.text for sentence in self.sentences)

    def add_sentence(self, sentence: ReportSentence) -> None:
        self.sentences.append(sentence)
