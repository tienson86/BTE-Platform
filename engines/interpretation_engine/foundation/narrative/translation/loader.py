"""Load Expert Translation knowledge. Read-only. No business rewriting."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from engines.interpretation_engine.foundation.narrative.translation.models import (
    ConfidenceBand,
    ForbiddenTermSet,
    TranslationRule,
)

_KNOWLEDGE_ROOT = (
    Path(__file__).resolve().parents[5] / "knowledge" / "expert_translation"
)


class ExpertTranslationLoadError(Exception):
    """Raised when translation knowledge files are missing or invalid."""


def knowledge_root() -> Path:
    """Return the Expert Translation knowledge directory."""
    return _KNOWLEDGE_ROOT


@lru_cache(maxsize=1)
def load_translation_rules() -> tuple[TranslationRule, ...]:
    """Load and order translation rules. Higher priority applies first."""
    payload = _read_json(_KNOWLEDGE_ROOT / "translation_rules.json")
    raw_rules = payload.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ExpertTranslationLoadError("translation_rules.json has no rules")
    rules = [_parse_rule(item) for item in raw_rules]
    return tuple(sorted(rules, key=lambda item: (-item.priority, item.id)))


@lru_cache(maxsize=1)
def load_confidence_bands() -> tuple[ConfidenceBand, ...]:
    """Load confidence band labels."""
    payload = _read_json(_KNOWLEDGE_ROOT / "confidence_bands.json")
    raw_bands = payload.get("bands")
    if not isinstance(raw_bands, list) or not raw_bands:
        raise ExpertTranslationLoadError("confidence_bands.json has no bands")
    bands = tuple(_parse_band(item) for item in raw_bands)
    return tuple(sorted(bands, key=lambda item: item.min_inclusive, reverse=True))


@lru_cache(maxsize=1)
def load_forbidden_terms() -> ForbiddenTermSet:
    """Load customer-text leak detector terms."""
    payload = _read_json(_KNOWLEDGE_ROOT / "forbidden_terms.json")
    phrases = tuple(str(item) for item in payload.get("phrases") or ())
    regex = tuple(str(item) for item in payload.get("regex") or ())
    if not phrases and not regex:
        raise ExpertTranslationLoadError("forbidden_terms.json is empty")
    return ForbiddenTermSet(
        phrases=phrases,
        regex=regex,
        version=str(payload.get("version") or ""),
    )


def _parse_rule(payload: Mapping[str, Any]) -> TranslationRule:
    """Parse one TranslationRule object."""
    examples_raw = payload.get("examples") or []
    examples: list[tuple[str, str]] = []
    if not isinstance(examples_raw, list):
        raise ExpertTranslationLoadError(f"invalid examples on {payload.get('id')}")
    for item in examples_raw:
        if not isinstance(item, list) or len(item) != 2:
            raise ExpertTranslationLoadError(f"invalid example on {payload.get('id')}")
        examples.append((str(item[0]), str(item[1])))
    return TranslationRule(
        id=str(payload.get("id") or ""),
        source_pattern=str(payload.get("source_pattern") or ""),
        target_pattern=str(payload.get("target_pattern") or ""),
        scope=str(payload.get("scope") or ""),
        priority=int(payload.get("priority") or 0),
        examples=tuple(examples),
        notes=str(payload.get("notes") or ""),
    )


def _parse_band(payload: Mapping[str, Any]) -> ConfidenceBand:
    """Parse one confidence band."""
    return ConfidenceBand(
        id=str(payload.get("id") or ""),
        min_inclusive=float(payload.get("min_inclusive")),
        max_inclusive=float(payload.get("max_inclusive")),
        label=str(payload.get("label") or ""),
    )


def _read_json(path: Path) -> dict[str, Any]:
    """Read one JSON object from knowledge."""
    if not path.is_file():
        raise ExpertTranslationLoadError(f"missing knowledge file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ExpertTranslationLoadError(f"invalid JSON object: {path}")
    return payload
