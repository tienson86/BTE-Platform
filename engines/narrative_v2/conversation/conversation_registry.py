"""Registered conversation transitions. Deterministic. No random connectors."""

from __future__ import annotations

ALLOWED_TRANSITIONS: tuple[str, ...] = (
    "Điều này",
    "Vì vậy",
    "Từ đó",
    "Đồng thời",
    "Mặt khác",
    "Nhờ đó",
    "Tuy nhiên",
)

FLOW_STAGES: tuple[str, ...] = (
    "observation",
    "reasoning",
    "meaning",
    "impact",
    "recommendation",
    "closing",
)

# (from_stage, to_stage) → registered connector. Missing pairs are invalid.
_STAGE_TRANSITIONS: dict[tuple[str, str], str] = {
    ("observation", "reasoning"): "Vì vậy",
    ("observation", "meaning"): "Từ đó",
    ("observation", "impact"): "Nhờ đó",
    ("observation", "recommendation"): "Đồng thời",
    ("observation", "closing"): "Điều này",
    ("reasoning", "meaning"): "Từ đó",
    ("reasoning", "impact"): "Nhờ đó",
    ("reasoning", "recommendation"): "Đồng thời",
    ("reasoning", "closing"): "Điều này",
    ("meaning", "impact"): "Nhờ đó",
    ("meaning", "recommendation"): "Đồng thời",
    ("meaning", "closing"): "Điều này",
    ("impact", "recommendation"): "Đồng thời",
    ("impact", "closing"): "Điều này",
    ("recommendation", "closing"): "Điều này",
}


class ConversationRegistry:
    """Stable transition lookup. No random choice."""

    def connector(self, from_stage: str, to_stage: str) -> str:
        """Return the registered connector for one stage pair."""
        key = (from_stage, to_stage)
        if key not in _STAGE_TRANSITIONS:
            raise KeyError(f"No registered transition: {from_stage} → {to_stage}")
        return _STAGE_TRANSITIONS[key]
