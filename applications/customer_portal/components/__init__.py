"""Shared UI components (markup snippets)."""

from __future__ import annotations


def stage_tabs() -> str:
    """Result stage tab buttons."""
    stages = [
        "calendar",
        "bazi",
        "pattern",
        "score",
        "interpretation",
        "narrative",
    ]
    return "".join(
        f'<button type="button" class="tab" data-stage="{s}">{s.title()}</button>'
        for s in stages
    )
