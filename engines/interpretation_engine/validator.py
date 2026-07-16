"""
BTE Platform
Interpretation Engine Validator

Kiểm tra dữ liệu đầu vào và đầu ra của Interpretation Engine.
"""

from __future__ import annotations

from typing import Any

from .models import (
    InterpretationContext,
    InterpretationResult,
    Chapter,
    Paragraph,
    Sentence,
)

from .exceptions import (
    InterpretationValidationError,
    InvalidContextError,
    InvalidTemplateError,
)

from engines.bazi_engine.models import BaziResult


class InterpretationValidator:
    """
    Validator của Interpretation Engine.
    """

    # ======================================================
    # Context
    # ======================================================

    def validate_context(
        self,
        context: InterpretationContext,
    ) -> None:
        """
        Kiểm tra InterpretationContext.
        """

        if context is None:
            raise InvalidContextError(
                "InterpretationContext không được để trống."
            )

        if not isinstance(
            context,
            InterpretationContext,
        ):
            raise InvalidContextError(
                "Sai kiểu dữ liệu InterpretationContext."
            )

        self.validate_bazi_result(
            context.bazi_result
        )

    # ======================================================
    # Bazi Result
    # ======================================================

    def validate_bazi_result(
        self,
        result: BaziResult,
    ) -> None:
        """
        Kiểm tra BaziResult.
        """

        if result is None:
            raise InterpretationValidationError(
                "BaziResult không được để trống."
            )

        if not isinstance(
            result,
            BaziResult,
        ):
            raise InterpretationValidationError(
                "Sai kiểu dữ liệu BaziResult."
            )

        if not result.success:
            raise InterpretationValidationError(
                "Bazi Engine chưa thực thi thành công."
            )

        if result.four_pillars is None:
            raise InterpretationValidationError(
                "Thiếu dữ liệu Tứ Trụ."
            )

    # ======================================================
    # Template
    # ======================================================

    def validate_template(
        self,
        template: Any,
    ) -> None:
        """
        Kiểm tra template đã được nạp.
        """

        if template is None:
            raise InvalidTemplateError(
                "Template không tồn tại."
            )

    # ======================================================
    # Sentence
    # ======================================================

    def validate_sentence(
        self,
        sentence: Sentence,
    ) -> None:

        if not isinstance(
            sentence,
            Sentence,
        ):
            raise InterpretationValidationError(
                "Sai kiểu dữ liệu Sentence."
            )

        if not sentence.text.strip():
            raise InterpretationValidationError(
                "Sentence không được rỗng."
            )

    # ======================================================
    # Paragraph
    # ======================================================

    def validate_paragraph(
        self,
        paragraph: Paragraph,
    ) -> None:

        if not isinstance(
            paragraph,
            Paragraph,
        ):
            raise InterpretationValidationError(
                "Sai kiểu dữ liệu Paragraph."
            )

        if not paragraph.title.strip():
            raise InterpretationValidationError(
                "Paragraph phải có tiêu đề."
            )

        for sentence in paragraph.sentences:
            self.validate_sentence(
                sentence
            )

    # ======================================================
    # Chapter
    # ======================================================

    def validate_chapter(
        self,
        chapter: Chapter,
    ) -> None:

        if not isinstance(
            chapter,
            Chapter,
        ):
            raise InterpretationValidationError(
                "Sai kiểu dữ liệu Chapter."
            )

        if not chapter.title.strip():
            raise InterpretationValidationError(
                "Chapter phải có tiêu đề."
            )

        for paragraph in chapter.paragraphs:
            self.validate_paragraph(
                paragraph
            )

    # ======================================================
    # Result
    # ======================================================

    def validate_result(
        self,
        result: InterpretationResult,
    ) -> None:
        """
        Kiểm tra kết quả cuối cùng.
        """

        if not isinstance(
            result,
            InterpretationResult,
        ):
            raise InterpretationValidationError(
                "Sai kiểu dữ liệu InterpretationResult."
            )

        for chapter in result.chapters:
            self.validate_chapter(
                chapter
            )

    # ======================================================
    # Markdown
    # ======================================================

    def validate_markdown(
        self,
        markdown: str,
    ) -> None:

        if markdown is None:
            raise InterpretationValidationError(
                "Markdown không được None."
            )

    # ======================================================
    # HTML
    # ======================================================

    def validate_html(
        self,
        html: str,
    ) -> None:

        if html is None:
            raise InterpretationValidationError(
                "HTML không được None."
            )

    # ======================================================
    # JSON
    # ======================================================

    def validate_json(
        self,
        data: dict[str, Any],
    ) -> None:

        if data is None:
            raise InterpretationValidationError(
                "JSON không được None."
            )

        if not isinstance(
            data,
            dict,
        ):
            raise InterpretationValidationError(
                "JSON phải là dict."
            )

    # ======================================================
    # Generic Helpers
    # ======================================================

    @staticmethod
    def ensure_not_none(
        value: Any,
        name: str,
    ) -> None:

        if value is None:
            raise InterpretationValidationError(
                f"{name} không được để trống."
            )

    @staticmethod
    def ensure_not_empty(
        value: str,
        name: str,
    ) -> None:

        if not value.strip():
            raise InterpretationValidationError(
                f"{name} không được rỗng."
            )

    @staticmethod
    def ensure_positive(
        value: float,
        name: str,
    ) -> None:

        if value < 0:
            raise InterpretationValidationError(
                f"{name} phải >= 0."
            )
