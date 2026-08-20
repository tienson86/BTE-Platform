"""Normalize runtime objects and internal codes into customer-facing text."""

from __future__ import annotations

import ast
import re
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Mapping

from engines.report_engine.localization.labels_vi import DOMAIN_TABLES, GENERIC_LABELS

_TOKEN_KEYS = tuple(
    key for key in sorted(GENERIC_LABELS, key=len, reverse=True) if len(key) >= 3
)
_TOKEN_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(key) for key in _TOKEN_KEYS) + r")\b",
    re.IGNORECASE,
)


def unwrap_display_object(value: Any) -> str:
    """Extract a human-readable string from dict/enum/dataclass/repr leakage."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return _format_number(value)
    if isinstance(value, Enum):
        return unwrap_display_object(value.value)
    if isinstance(value, str):
        return _unwrap_string(value)
    if is_dataclass(value) and not isinstance(value, type):
        return unwrap_display_object(asdict(value))
    if hasattr(value, "to_dict") and callable(value.to_dict):
        try:
            return unwrap_display_object(value.to_dict())
        except (TypeError, ValueError):
            pass
    if isinstance(value, Mapping):
        return _unwrap_mapping(value)
    if isinstance(value, (list, tuple)):
        parts = [unwrap_display_object(item) for item in value]
        return ", ".join(part for part in parts if part)
    return str(value).strip()


def localize(value: Any, domain: str = "generic") -> str:
    """Map an internal code (or leaked object) to a Vietnamese display label."""
    text = unwrap_display_object(value)
    if not text:
        return ""
    table = DOMAIN_TABLES.get(domain, {})
    key = text.strip().lower()
    if key in table:
        return table[key]
    if domain == "gender":
        return ""
    if key in GENERIC_LABELS:
        return GENERIC_LABELS[key]
    return localize_tokens(text)


def localize_tokens(text: str) -> str:
    """Replace known internal tokens inside mixed customer text."""
    if not text:
        return ""

    def _replace(match: re.Match[str]) -> str:
        token = match.group(1).lower()
        return GENERIC_LABELS.get(token, match.group(1))

    return _TOKEN_PATTERN.sub(_replace, text)


def display_text(value: Any, domain: str = "generic") -> str:
    """Public helper used by all Report V1 renderers."""
    return localize(value, domain)


def _unwrap_string(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return ""
    if stripped[0] in "{[" and ("'name'" in stripped or '"name"' in stripped):
        try:
            parsed = ast.literal_eval(stripped)
        except (SyntaxError, ValueError):
            return stripped
        return unwrap_display_object(parsed)
    return stripped


def _unwrap_mapping(data: Mapping[str, Any]) -> str:
    for key in ("name", "label", "title", "text", "value", "display"):
        if key in data and data[key] not in (None, ""):
            return unwrap_display_object(data[key])
    if len(data) == 1:
        return unwrap_display_object(next(iter(data.values())))
    return ""


def _format_number(value: int | float) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)
