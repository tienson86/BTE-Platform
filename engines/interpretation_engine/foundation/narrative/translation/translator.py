"""Deterministic expert translation. No LLM. No decision changes."""

from __future__ import annotations

import re

from engines.interpretation_engine.foundation.narrative.text import normalize_text
from engines.interpretation_engine.foundation.narrative.translation.loader import (
    load_confidence_bands,
    load_translation_rules,
)
from engines.interpretation_engine.foundation.narrative.translation.models import (
    ConfidenceBand,
    TranslationRule,
)

_FLOAT = re.compile(r"(?<![\d.])(0\.\d{1,4}|1\.0{1,4})(?![\d.])")
_SCORE_PARENS = re.compile(r"\(\s*(0\.\d{1,4}|1\.0{1,4})\s*\)")
_MULTI_SPACE = re.compile(r"\s{2,}")
_PIPE = re.compile(r"\s+\|\s+")

_COMPILED_RULES: tuple[tuple[TranslationRule, re.Pattern[str]], ...] | None = None


def translate_text(text: str, *, debug_mode: bool = False) -> str:
    """Translate one customer-facing string. Empty input stays empty."""
    if debug_mode:
        return text
    source = normalize_text(text)
    if not source:
        return ""
    translated = _apply_rules(source)
    translated = _apply_confidence_bands(translated)
    translated = _PIPE.sub(". ", translated)
    translated = _MULTI_SPACE.sub(" ", translated)
    return normalize_text(translated)


def confidence_label(value: float) -> str:
    """Map a unit-interval score to an expert band label."""
    for band in load_confidence_bands():
        if band.min_inclusive <= value <= band.max_inclusive:
            return band.label
    return load_confidence_bands()[-1].label


def _compiled_rules() -> tuple[tuple[TranslationRule, re.Pattern[str]], ...]:
    """Compile translation rules once per process."""
    global _COMPILED_RULES
    if _COMPILED_RULES is None:
        compiled: list[tuple[TranslationRule, re.Pattern[str]]] = []
        for rule in load_translation_rules():
            compiled.append(
                (rule, re.compile(rule.source_pattern, flags=re.IGNORECASE))
            )
        _COMPILED_RULES = tuple(compiled)
    return _COMPILED_RULES


def _apply_rules(text: str) -> str:
    """Apply knowledge rules in priority order."""
    result = text
    for _rule, pattern in _compiled_rules():
        result = pattern.sub(_rule.target_pattern, result)
    return result


def _apply_confidence_bands(text: str) -> str:
    """Replace remaining unit-interval scores with expert bands."""

    def replace_parens(match: re.Match[str]) -> str:
        label = _band_for(float(match.group(1)))
        return f" — {label.rstrip('.')}"

    def replace_float(match: re.Match[str]) -> str:
        return _band_for(float(match.group(1))).rstrip(".")

    updated = _SCORE_PARENS.sub(replace_parens, text)
    return _FLOAT.sub(replace_float, updated)


def _band_for(value: float) -> str:
    """Resolve one numeric value against configured bands."""
    bands: tuple[ConfidenceBand, ...] = load_confidence_bands()
    for band in bands:
        if band.min_inclusive <= value <= band.max_inclusive:
            return band.label
    return bands[-1].label
