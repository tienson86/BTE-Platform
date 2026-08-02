"""Structured prompt models for AI expert composition."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


PROMPT_SECTION_KEYS: tuple[str, ...] = (
    "facts",
    "evidence",
    "knowledge",
    "reasoning",
    "writing_style",
)

PROMPT_SECTION_TITLES: dict[str, str] = {
    "facts": "Facts",
    "evidence": "Evidence",
    "knowledge": "Knowledge",
    "reasoning": "Reasoning",
    "writing_style": "Writing Style",
}


@dataclass(slots=True)
class PromptSection:
    """One labeled block inside a structured prompt."""

    key: str
    title: str
    lines: list[str] = field(default_factory=list)

    @property
    def content(self) -> str:
        """Render section body without the heading."""
        return "\n".join(self.lines).strip()

    def to_dict(self) -> dict[str, Any]:
        """Serialize section."""
        return {
            "key": self.key,
            "title": self.title,
            "lines": list(self.lines),
            "content": self.content,
        }


@dataclass(slots=True)
class StructuredPrompt:
    """Prompt with explicitly separated Fact / Evidence / Knowledge / Reasoning / Style blocks."""

    sections: dict[str, PromptSection]
    metadata: dict[str, Any] = field(default_factory=dict)
    appendix: str = ""

    def section(self, key: str) -> PromptSection | None:
        """Return one section by key."""
        return self.sections.get(str(key or "").strip().lower())

    @property
    def text(self) -> str:
        """Assemble full prompt text with section separators."""
        blocks: list[str] = []
        for key in PROMPT_SECTION_KEYS:
            section = self.sections.get(key)
            if section is None:
                continue
            body = section.content
            if not body:
                body = "(none)"
            blocks.append(f"## {section.title}\n{body}")
        appendix = str(self.appendix or "").strip()
        if appendix:
            blocks.append(appendix)
        return "\n\n".join(blocks).strip() + "\n"

    def to_dict(self) -> dict[str, Any]:
        """Serialize structured prompt."""
        return {
            "sections": {key: section.to_dict() for key, section in self.sections.items()},
            "text": self.text,
            "appendix": self.appendix,
            "metadata": dict(self.metadata),
        }
