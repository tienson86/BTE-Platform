"""RE-3 rendering context. Append-only. Immutable upstream layout."""

from __future__ import annotations

import copy
from typing import Any, Mapping

RENDER_VERSION = "1.0.0"
RENDER_ENGINE_ID = "report_rendering_engine"
REQUIRED_LAYOUT_VERSION = "1.0.0"


class RenderingError(Exception):
    """Base error for RE-3 rendering failures."""


class DuplicatePublicationError(RenderingError):
    """Raised when a rendering output is published twice."""


def snapshot_value(value: Any, *, label: str) -> dict[str, Any]:
    """Copy an upstream object into an isolated mapping."""
    if value is None:
        raise RenderingError(f"missing_{label}")
    if hasattr(value, "to_dict"):
        payload = value.to_dict()
        if not isinstance(payload, Mapping):
            raise RenderingError(f"invalid_{label}")
        return copy.deepcopy(dict(payload))
    if isinstance(value, Mapping):
        return copy.deepcopy(dict(value))
    raise RenderingError(f"invalid_{label}")


class RenderingContext:
    """Append-only context over a sealed CanonicalReportLayout snapshot."""

    def __init__(
        self,
        *,
        layout_snapshot: Mapping[str, Any],
        renderer_id: str,
        render_version: str = RENDER_VERSION,
    ) -> None:
        """Seal the layout snapshot. Rendering outputs publish separately."""
        self._layout = dict(layout_snapshot)
        self._published: dict[str, Any] = {}
        self.renderer_id = renderer_id
        self.render_version = render_version

    def layout_snapshot(self) -> dict[str, Any]:
        """Return a defensive CanonicalReportLayout copy."""
        return copy.deepcopy(self._layout)

    def publish(self, name: str, value: Any) -> None:
        """Publish a rendering-owned output once."""
        reserved = {"layout_snapshot"}
        if name in reserved or name in self._published:
            raise DuplicatePublicationError(f"duplicate_output:{name}")
        if isinstance(value, (Mapping, list, tuple)):
            self._published[name] = copy.deepcopy(value)
        else:
            self._published[name] = value

    def get_published(self, name: str) -> Any:
        """Return a published rendering output when present."""
        value = self._published.get(name)
        if isinstance(value, Mapping):
            return copy.deepcopy(dict(value))
        if isinstance(value, list):
            return copy.deepcopy(value)
        return value

    def published_outputs(self) -> tuple[str, ...]:
        """Return published output names in insertion order."""
        return tuple(self._published)

    def to_dict(self) -> dict[str, Any]:
        """Serialize sealed layout and published rendering outputs."""
        return {
            "render_version": self.render_version,
            "renderer_id": self.renderer_id,
            "layout_snapshot": self.layout_snapshot(),
            "published_outputs": list(self.published_outputs()),
        }


def build_rendering_context(
    *,
    layout: Any,
    renderer_id: str,
) -> RenderingContext:
    """Build an append-only rendering context from CanonicalReportLayout."""
    return RenderingContext(
        layout_snapshot=snapshot_value(layout, label="canonical_report_layout"),
        renderer_id=renderer_id,
    )
