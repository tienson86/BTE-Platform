"""Read-only golden Presentation comparison. Does not write Golden Dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]

GOLDEN_PRESENTATION: dict[str, Path] = {
    "CASE-0001": (
        REPO
        / "implementation"
        / "narrative_v2"
        / "n_imp_09a"
        / "case0001_presentation_v2_1.json"
    ),
}


def golden_path_for(case_id: str) -> Path | None:
    """Return the frozen V2 Presentation snapshot path, if one exists."""
    path = GOLDEN_PRESENTATION.get(case_id)
    if path is None or not path.is_file():
        return None
    return path


def load_golden_presentation(case_id: str) -> dict[str, Any] | None:
    """Load frozen Presentation JSON. Returns None when no snapshot exists."""
    path = golden_path_for(case_id)
    if path is None:
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def diff_presentations(
    current: dict[str, Any] | None,
    golden: dict[str, Any] | None,
) -> list[dict[str, str]]:
    """Leaf diffs of Presentation fields. Does not mutate either object."""
    if golden is None:
        return [{"path": "", "kind": "missing_golden", "current": "", "golden": ""}]
    if current is None:
        return [{"path": "", "kind": "missing_current", "current": "", "golden": ""}]
    rows: list[dict[str, str]] = []
    _walk("", current, golden, rows)
    return rows


def _walk(prefix: str, current: object, golden: object, rows: list[dict[str, str]]) -> None:
    if type(current) is not type(golden) and not _both_mapping(current, golden) and not _both_list(
        current, golden
    ):
        if current != golden:
            rows.append(
                {
                    "path": prefix or "/",
                    "kind": "changed",
                    "current": _fmt(current),
                    "golden": _fmt(golden),
                }
            )
        return
    if isinstance(current, dict) and isinstance(golden, dict):
        keys = sorted(set(current) | set(golden))
        for key in keys:
            path = f"{prefix}.{key}" if prefix else key
            if key not in current:
                rows.append(
                    {"path": path, "kind": "missing_current", "current": "", "golden": _fmt(golden[key])}
                )
            elif key not in golden:
                rows.append(
                    {"path": path, "kind": "extra_current", "current": _fmt(current[key]), "golden": ""}
                )
            else:
                _walk(path, current[key], golden[key], rows)
        return
    if isinstance(current, list) and isinstance(golden, list):
        length = max(len(current), len(golden))
        for index in range(length):
            path = f"{prefix}[{index}]"
            if index >= len(current):
                rows.append(
                    {"path": path, "kind": "missing_current", "current": "", "golden": _fmt(golden[index])}
                )
            elif index >= len(golden):
                rows.append(
                    {"path": path, "kind": "extra_current", "current": _fmt(current[index]), "golden": ""}
                )
            else:
                _walk(path, current[index], golden[index], rows)
        return
    if current != golden:
        rows.append(
            {
                "path": prefix or "/",
                "kind": "changed",
                "current": _fmt(current),
                "golden": _fmt(golden),
            }
        )


def _both_mapping(left: object, right: object) -> bool:
    return isinstance(left, dict) and isinstance(right, dict)


def _both_list(left: object, right: object) -> bool:
    return isinstance(left, list) and isinstance(right, list)


def _fmt(value: object) -> str:
    if value is None:
        return "null"
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    if len(text) > 240:
        return text[:237] + "..."
    return text
