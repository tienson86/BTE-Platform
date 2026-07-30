"""Diff helpers for Knowledge Console assets."""

from __future__ import annotations

import json
from typing import Any

from applications.knowledge_console.api.models import DiffLine, DiffResult


def dump_content(content: dict[str, Any]) -> list[str]:
    """Serialize content to stable text lines."""
    text = json.dumps(content, ensure_ascii=False, indent=2, sort_keys=True)
    return text.splitlines()


def build_diff(
    *,
    asset_id: str,
    from_version: str,
    to_version: str,
    from_content: dict[str, Any],
    to_content: dict[str, Any],
) -> DiffResult:
    """Build a simple line-oriented diff (deterministic LCS-free scan)."""
    left = dump_content(from_content)
    right = dump_content(to_content)
    lines: list[DiffLine] = []

    # Myers-lite: greedy scan with set membership for removals/adds.
    left_set = set(left)
    right_set = set(right)
    for line in left:
        if line in right_set:
            lines.append(DiffLine(kind="equal", text=line))
        else:
            lines.append(DiffLine(kind="remove", text=line))
    for line in right:
        if line not in left_set:
            lines.append(DiffLine(kind="add", text=line))

    return DiffResult(
        asset_id=asset_id,
        from_version=from_version,
        to_version=to_version,
        lines=lines,
    )
