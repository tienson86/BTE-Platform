"""Explanation runtime publisher shell.

Publishes explanation refs into a structural payload. No rendering.
"""

from __future__ import annotations

from typing import Any


class ExplanationPublisher:
    """Publish explanation reference shells."""

    def publish(self, explanation_refs: tuple[str, ...]) -> dict[str, Any]:
        """Return a structural publication payload."""
        return {
            "explanation_refs": list(explanation_refs),
            "published": True,
        }
