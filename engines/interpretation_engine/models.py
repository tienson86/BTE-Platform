"""
BTE Platform
Interpretation Engine Models
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.bazi_engine.models import BaziResult


# ==========================================================
# Sentence
# ==========================================================

@dataclass(slots=True)
class Sentence:

    text: str

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Paragraph
# ==========================================================

@dataclass(slots=True)
class Paragraph:

    title: str

    sentences: list[Sentence] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Chapter
# ==========================================================

@dataclass(slots=True)
class Chapter:

    title: str

    paragraphs: list[Paragraph] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Interpretation Context
# ==========================================================

@dataclass(slots=True)
class InterpretationContext:

    bazi_result: BaziResult

    options: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Interpretation Result
# ==========================================================

@dataclass(slots=True)
class InterpretationResult:

    success: bool = True

    chapters: list[Chapter] = field(default_factory=list)

    markdown: str = ""

    html: str = ""

    json: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Engine State
# ==========================================================

@dataclass(slots=True)
class InterpretationState:

    initialized: bool = False

    template_loaded: bool = False

    rendered: bool = False

    elapsed_time: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)
