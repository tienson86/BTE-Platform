"""InterpretationSection builder — all framework interpreters should use this."""

from __future__ import annotations

from typing import Any, Mapping

from engines.interpretation_engine.interpreter_framework.interpreter_exception import (
    ConfigurationError,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.base_skeleton import (
    InterpretationSection,
)
from engines.interpretation_engine.models.paragraph_result import ParagraphResult


class InterpretationSectionBuilder:
    """Fluent builder for frozen InterpretationSection / SectionResult shells."""

    def __init__(self) -> None:
        """Initialize empty builder state."""
        self._id: str = ""
        self._section_type: str = ""
        self._title_ref: str | None = None
        self._interpreter_id: str | None = None
        self._paragraphs: list[ParagraphResult] = []
        self._success: bool = True
        self._messages: list[str] = []
        self._attributes: dict[str, Any] = {}

    def with_id(self, section_id: str) -> InterpretationSectionBuilder:
        """Set section id."""
        self._id = section_id
        return self

    def with_section_type(self, section_type: str) -> InterpretationSectionBuilder:
        """Set section type."""
        self._section_type = section_type
        return self

    def with_title_ref(self, title_ref: str | None) -> InterpretationSectionBuilder:
        """Set title reference."""
        self._title_ref = title_ref
        return self

    def with_interpreter_id(
        self, interpreter_id: str | None
    ) -> InterpretationSectionBuilder:
        """Set interpreter id."""
        self._interpreter_id = interpreter_id
        return self

    def with_paragraphs(
        self, paragraphs: tuple[ParagraphResult, ...] | list[ParagraphResult]
    ) -> InterpretationSectionBuilder:
        """Replace paragraphs."""
        self._paragraphs = list(paragraphs)
        return self

    def add_paragraph(self, paragraph: ParagraphResult) -> InterpretationSectionBuilder:
        """Append one paragraph."""
        self._paragraphs.append(paragraph)
        return self

    def with_success(self, success: bool) -> InterpretationSectionBuilder:
        """Set success flag."""
        self._success = success
        return self

    def with_messages(
        self, messages: tuple[str, ...] | list[str]
    ) -> InterpretationSectionBuilder:
        """Replace messages."""
        self._messages = list(messages)
        return self

    def add_message(self, message: str) -> InterpretationSectionBuilder:
        """Append one message."""
        self._messages.append(message)
        return self

    def with_attributes(
        self, attributes: Mapping[str, Any]
    ) -> InterpretationSectionBuilder:
        """Replace attributes."""
        self._attributes = dict(attributes)
        return self

    def update_attributes(
        self, attributes: Mapping[str, Any]
    ) -> InterpretationSectionBuilder:
        """Merge attributes."""
        self._attributes.update(dict(attributes))
        return self

    def for_interpreter(
        self,
        *,
        interpreter_id: str,
        section_type: str,
        context_id: str | None = None,
    ) -> InterpretationSectionBuilder:
        """Apply standard id/interpreter/section_type convention."""
        section_id = f"section_{interpreter_id}"
        if context_id:
            section_id = f"section_{interpreter_id}_{context_id}"
        return (
            self.with_id(section_id)
            .with_interpreter_id(interpreter_id)
            .with_section_type(section_type)
        )

    def build(self) -> InterpretationSection:
        """Build immutable InterpretationSection."""
        if not self._id or not self._section_type:
            raise ConfigurationError(
                "InterpretationSectionBuilder requires id and section_type"
            )
        section = InterpretationSection(
            id=self._id,
            section_type=self._section_type,
            title_ref=self._title_ref,
            interpreter_id=self._interpreter_id,
            paragraphs=tuple(self._paragraphs),
            success=self._success,
            messages=tuple(self._messages),
            attributes=dict(self._attributes),
        )
        if not section.validate():
            raise ConfigurationError("built InterpretationSection failed validate()")
        return section


# Alias requested by task naming.
InterpreterBuilder = InterpretationSectionBuilder
