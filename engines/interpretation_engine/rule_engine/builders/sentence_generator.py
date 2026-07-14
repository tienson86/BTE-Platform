"""
sentence_generator.py
=====================

Sentence Generator

Chịu trách nhiệm:

- Sinh câu diễn giải từ RuleResult
- Thay thế biến trong template
- Chuẩn hóa văn bản
"""

from __future__ import annotations

import re
from typing import Optional

from ..models.context import InterpretationContext
from ..models.rule_result import RuleResult


class SentenceGenerator:
    """
    Sinh câu diễn giải từ RuleResult.
    """

    VARIABLE_PATTERN = re.compile(
        r"\{([A-Za-z0-9_.]+)\}"
    )

    def __init__(
        self,
        remove_empty: bool = True,
    ) -> None:

        self.remove_empty = remove_empty

    # =====================================================
    # Public API
    # =====================================================

    def generate(
        self,
        context: InterpretationContext,
        result: RuleResult,
    ) -> str:
        """
        Sinh câu diễn giải.
        """

        if not result.matched:
            return ""

        template = self.get_template(result)

        sentence = self.render(
            template,
            context,
        )

        sentence = self.normalize(sentence)

        return sentence

    # =====================================================
    # Template
    # =====================================================

    def get_template(
        self,
        result: RuleResult,
    ) -> str:
        """
        Lấy template.

        Ưu tiên:
            Rule.result
        """

        return result.text or result.rule.result or ""

    # =====================================================
    # Render
    # =====================================================

    def render(
        self,
        template: str,
        context: InterpretationContext,
    ) -> str:

        def replace(match):

            key = match.group(1)

            value = self.resolve(
                context,
                key,
            )

            if value is None:

                return "" if self.remove_empty else match.group(0)

            return str(value)

        return self.VARIABLE_PATTERN.sub(
            replace,
            template,
        )

    # =====================================================
    # Resolve
    # =====================================================

    def resolve(
        self,
        context: InterpretationContext,
        key: str,
    ):

        if hasattr(context, "resolve"):

            return context.resolve(key)

        if hasattr(context, key):

            return getattr(context, key)

        return None

    # =====================================================
    # Normalize
    # =====================================================

    def normalize(
        self,
        text: str,
    ) -> str:

        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        if not text:
            return ""

        if text[-1] not in ".!?":

            text += "."

        return text

    # =====================================================
    # Preview
    # =====================================================

    def preview(
        self,
        template: str,
        context: InterpretationContext,
    ) -> str:

        return self.normalize(
            self.render(
                template,
                context,
            )
        )
