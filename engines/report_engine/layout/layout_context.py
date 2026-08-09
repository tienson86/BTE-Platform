"""RE-2 layout context. Append-only. Immutable upstream."""

from __future__ import annotations

import copy
from typing import Any, Mapping

from engines.report_engine.context.canonical_report_context import build_report_context
from engines.report_engine.foundation_constants import REPORT_VERSION

LAYOUT_VERSION = "1.0.0"
LAYOUT_ENGINE_ID = "report_layout_engine"


class LayoutError(Exception):
    """Base error for RE-2 layout composition failures."""


class DuplicatePublicationError(LayoutError):
    """Raised when a layout output is published twice."""


def snapshot_value(value: Any, *, label: str) -> dict[str, Any]:
    """Copy an upstream object into an isolated mapping."""
    if value is None:
        raise LayoutError(f"missing_{label}")
    if hasattr(value, "to_dict"):
        payload = value.to_dict()
        if not isinstance(payload, Mapping):
            raise LayoutError(f"invalid_{label}")
        return copy.deepcopy(dict(payload))
    if isinstance(value, Mapping):
        return copy.deepcopy(dict(value))
    raise LayoutError(f"invalid_{label}")


class LayoutContext:
    """Append-only context over sealed RE-1 and IX-1 snapshots."""

    def __init__(
        self,
        *,
        report_snapshot: Mapping[str, Any],
        interpretation_snapshot: Mapping[str, Any],
        layout_version: str = LAYOUT_VERSION,
        report_version: str = REPORT_VERSION,
    ) -> None:
        """Seal upstream snapshots. Layout outputs publish separately."""
        self._report = dict(report_snapshot)
        self._interpretation = dict(interpretation_snapshot)
        self._published: dict[str, Any] = {}
        self.layout_version = layout_version
        self.report_version = report_version

    def report_snapshot(self) -> dict[str, Any]:
        """Return a defensive RE-1 Report Context copy."""
        return copy.deepcopy(self._report)

    def interpretation_snapshot(self) -> dict[str, Any]:
        """Return a defensive IX-1 Canonical Interpretation Result copy."""
        return copy.deepcopy(self._interpretation)

    def analysis_snapshot(self) -> dict[str, Any]:
        """Return the sealed AX-2 snapshot from Report Context."""
        return copy.deepcopy(dict(self._report.get("analysis_snapshot") or {}))

    def decision_snapshot(self) -> dict[str, Any]:
        """Return the sealed AX-3 snapshot from Report Context."""
        return copy.deepcopy(dict(self._report.get("decision_snapshot") or {}))

    def luck_snapshot(self) -> dict[str, Any]:
        """Return the sealed AX-4 snapshot from Report Context."""
        return copy.deepcopy(dict(self._report.get("luck_snapshot") or {}))

    def publish(self, name: str, value: Any) -> None:
        """Publish a layout-owned output once."""
        reserved = {"report_snapshot", "interpretation_snapshot"}
        if name in reserved or name in self._published:
            raise DuplicatePublicationError(f"duplicate_output:{name}")
        if isinstance(value, (Mapping, list, tuple)):
            self._published[name] = copy.deepcopy(value)
        else:
            self._published[name] = value

    def get_published(self, name: str) -> Any:
        """Return a published layout output when present."""
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
        """Serialize sealed snapshots and published layout outputs."""
        return {
            "layout_version": self.layout_version,
            "report_version": self.report_version,
            "report_snapshot": self.report_snapshot(),
            "interpretation_snapshot": self.interpretation_snapshot(),
            "published_outputs": list(self.published_outputs()),
        }


def extract_interpretation_sections(snapshot: Mapping[str, Any]) -> tuple[dict[str, Any], ...]:
    """Normalize IE-3 or IX-1 nested sections to isolated dictionaries."""
    rows = snapshot.get("sections")
    if not isinstance(rows, list):
        nested = snapshot.get("composition_result") or snapshot.get("canonical_interpretation") or {}
        rows = nested.get("sections") if isinstance(nested, Mapping) else ()
    if not isinstance(rows, (list, tuple)):
        return ()
    return tuple(copy.deepcopy(dict(item)) for item in rows if isinstance(item, Mapping))


def build_layout_context(
    *,
    report_context: Any = None,
    interpretation_result: Any = None,
    analysis_result: Any = None,
    decision_result: Any = None,
    luck_result: Any = None,
) -> LayoutContext:
    """Build an append-only layout context from RE-1 and IX-1 inputs."""
    interpretation = snapshot_value(
        interpretation_result,
        label="canonical_interpretation_result",
    )
    if report_context is None:
        report_context = build_report_context(
            analysis_result=analysis_result,
            decision_result=decision_result,
            luck_result=luck_result,
            interpretation_result=interpretation,
        )
    return LayoutContext(
        report_snapshot=snapshot_value(report_context, label="report_context"),
        interpretation_snapshot=interpretation,
    )
