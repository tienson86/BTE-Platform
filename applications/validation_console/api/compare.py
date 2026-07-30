"""Compare expected vs actual golden outputs."""

from __future__ import annotations

from typing import Any

from applications.validation_console.api.models import DiffItem


def compare_outputs(
    expected: dict[str, Any],
    actual: dict[str, Any],
) -> list[DiffItem]:
    """Recursively compare two JSON-like objects."""
    differences: list[DiffItem] = []
    _walk("", expected, actual, differences)
    return differences


def _walk(
    prefix: str,
    expected: Any,
    actual: Any,
    differences: list[DiffItem],
) -> None:
    if isinstance(expected, dict) and isinstance(actual, dict):
        keys = sorted(set(expected.keys()) | set(actual.keys()))
        for key in keys:
            field = f"{prefix}.{key}" if prefix else key
            _walk(field, expected.get(key), actual.get(key), differences)
        return

    if isinstance(expected, list) and isinstance(actual, list):
        max_len = max(len(expected), len(actual))
        for index in range(max_len):
            field = f"{prefix}[{index}]"
            left = expected[index] if index < len(expected) else None
            right = actual[index] if index < len(actual) else None
            _walk(field, left, right, differences)
        return

    if expected != actual:
        differences.append(
            DiffItem(field=prefix or "$", expected=expected, actual=actual)
        )
