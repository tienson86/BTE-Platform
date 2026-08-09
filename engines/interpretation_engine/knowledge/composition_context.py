"""IE-2 Composition Context. Append-only. Immutable upstream."""

from __future__ import annotations

import copy
from typing import Any, Mapping

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)

COMPOSITION_VERSION = "1.0.0"
COMPOSITION_ENGINE_ID = "knowledge_selection_engine"
AI_REWRITE_ENABLED = False

ALLOWED_ROOTS: tuple[str, ...] = (
    "analysis",
    "decision",
    "luck",
    "interpretation",
)


class CompositionError(InterpretationArchitectureError):
    """Base error for IE-2 knowledge selection failures."""


class DuplicatePublicationError(CompositionError):
    """Raised when a composition output is published twice."""


class PlaceholderIntegrityError(CompositionError):
    """Raised when a placeholder path is outside published contracts."""


def snapshot_value(value: Any, *, label: str) -> dict[str, Any]:
    """Copy an upstream object into an isolated mapping."""
    if value is None:
        raise CompositionError(f"missing_{label}")
    if hasattr(value, "to_dict"):
        payload = value.to_dict()
        if not isinstance(payload, Mapping):
            raise CompositionError(f"invalid_{label}")
        return copy.deepcopy(dict(payload))
    if isinstance(value, Mapping):
        return copy.deepcopy(dict(value))
    raise CompositionError(f"invalid_{label}")


def resolve_path(payload: Mapping[str, Any] | None, path: str) -> Any:
    """Resolve a dotted path. Missing nodes return None. No inference."""
    if payload is None or not path:
        return None
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


class CompositionContext:
    """Append-only context over sealed AX-2 / AX-3 / AX-4 / IE-1 snapshots."""

    def __init__(
        self,
        *,
        analysis_snapshot: Mapping[str, Any],
        decision_snapshot: Mapping[str, Any],
        luck_snapshot: Mapping[str, Any],
        interpretation_snapshot: Mapping[str, Any],
        composition_version: str = COMPOSITION_VERSION,
    ) -> None:
        """Seal upstream snapshots. Composition outputs publish separately."""
        self._analysis = dict(analysis_snapshot)
        self._decision = dict(decision_snapshot)
        self._luck = dict(luck_snapshot)
        self._interpretation = dict(interpretation_snapshot)
        self._published: dict[str, Any] = {}
        self.composition_version = composition_version

    def analysis_snapshot(self) -> dict[str, Any]:
        """Return a defensive AX-2 copy."""
        return copy.deepcopy(self._analysis)

    def decision_snapshot(self) -> dict[str, Any]:
        """Return a defensive AX-3 copy."""
        return copy.deepcopy(self._decision)

    def luck_snapshot(self) -> dict[str, Any]:
        """Return a defensive AX-4 copy."""
        return copy.deepcopy(self._luck)

    def interpretation_snapshot(self) -> dict[str, Any]:
        """Return a defensive IE-1 context copy."""
        return copy.deepcopy(self._interpretation)

    def root(self, name: str) -> dict[str, Any]:
        """Return one sealed upstream root by name."""
        if name == "analysis":
            return self.analysis_snapshot()
        if name == "decision":
            return self.decision_snapshot()
        if name == "luck":
            return self.luck_snapshot()
        if name == "interpretation":
            return self.interpretation_snapshot()
        raise PlaceholderIntegrityError(f"unknown_root:{name}")

    def resolve_published(self, binding_path: str) -> Any:
        """Resolve a placeholder against published contract roots only."""
        if "." not in binding_path:
            raise PlaceholderIntegrityError(f"invalid_binding_path:{binding_path}")
        root, remainder = binding_path.split(".", 1)
        if root not in ALLOWED_ROOTS:
            raise PlaceholderIntegrityError(f"unpublished_root:{root}")
        return resolve_path(self.root(root), remainder)

    def publish(self, name: str, value: Any) -> None:
        """Publish a composition-owned output once."""
        reserved = {
            "analysis_snapshot",
            "decision_snapshot",
            "luck_snapshot",
            "interpretation_snapshot",
        }
        if name in reserved:
            raise DuplicatePublicationError(f"reserved_output:{name}")
        if name in self._published:
            raise DuplicatePublicationError(f"duplicate_output:{name}")
        self._published[name] = copy.deepcopy(value) if isinstance(value, Mapping) else value

    def get_published(self, name: str) -> Any:
        """Return a published composition output when present."""
        value = self._published.get(name)
        if isinstance(value, Mapping):
            return copy.deepcopy(dict(value))
        return value

    def published_outputs(self) -> tuple[str, ...]:
        """Return published output names in insertion order."""
        return tuple(self._published)

    def to_dict(self) -> dict[str, Any]:
        """Serialize sealed snapshots and published composition outputs."""
        return {
            "composition_version": self.composition_version,
            "analysis_snapshot": self.analysis_snapshot(),
            "decision_snapshot": self.decision_snapshot(),
            "luck_snapshot": self.luck_snapshot(),
            "interpretation_snapshot": self.interpretation_snapshot(),
            "published_outputs": list(self.published_outputs()),
        }


def build_composition_context(
    *,
    analysis_result: Any,
    decision_result: Any,
    luck_result: Any,
    interpretation_context: Any,
    composition_version: str = COMPOSITION_VERSION,
) -> CompositionContext:
    """Build an append-only composition context from canonical upstream inputs."""
    return CompositionContext(
        analysis_snapshot=snapshot_value(analysis_result, label="canonical_analysis_result"),
        decision_snapshot=snapshot_value(decision_result, label="canonical_decision_result"),
        luck_snapshot=snapshot_value(luck_result, label="canonical_luck_result"),
        interpretation_snapshot=snapshot_value(
            interpretation_context,
            label="interpretation_context",
        ),
        composition_version=composition_version,
    )
