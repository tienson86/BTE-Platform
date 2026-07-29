"""
BTE Platform
Interpretation Engine Calculator

Điều phối toàn bộ quá trình diễn giải Bát Tự.

.. deprecated:: WP0B
    Không dùng cho InterpretationEngine.run().
    Active pipeline nằm ở ``engine.InterpretationEngine``.
    Giữ lại để tương thích; refactor ở WP1.
"""

from __future__ import annotations

from .loader import InterpretationLoader
from .validator import InterpretationValidator

from .models import (
    InterpretationContext,
    InterpretationResult,
)

from .core.rule_matcher import RuleMatcher
from .core.template_selector import TemplateSelector
from .core.sentence_builder import SentenceBuilder
from .core.paragraph_builder import ParagraphBuilder
from .core.chapter_builder import ChapterBuilder

from .renderer.renderer import Renderer


class InterpretationCalculator:
    """
    Bộ điều phối Interpretation Engine.
    """

    def __init__(
        self,
        loader: InterpretationLoader,
        validator: InterpretationValidator,
    ) -> None:

        self.loader = loader

        self.validator = validator

        self.rule_matcher = RuleMatcher(loader)

        self.template_selector = TemplateSelector(loader)

        self.sentence_builder = SentenceBuilder()

        self.paragraph_builder = ParagraphBuilder()

        self.chapter_builder = ChapterBuilder()

        self.renderer = Renderer()

    # =====================================================
    # Main
    # =====================================================

    def calculate(
        self,
        context: InterpretationContext,
    ) -> InterpretationResult:

        self.validator.validate_context(context)

        # Load toàn bộ dữ liệu
        self.loader.load_all()

        # Match Rule
        matched_rules = self.rule_matcher.match(
            context
        )

        # Chọn Template
        templates = self.template_selector.select(
            matched_rules
        )

        # Sinh câu
        sentences = self.sentence_builder.build(
            templates,
            context,
        )

        # Ghép đoạn
        paragraphs = self.paragraph_builder.build(
            sentences
        )

        # Ghép chương
        chapters = self.chapter_builder.build(
            paragraphs
        )

        # Render
        result = self.renderer.render(
            chapters
        )

        self.validator.validate_result(
            result
        )

        return result
