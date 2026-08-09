"""IE-3 assembly context. Append-only. Immutable upstream."""

from __future__ import annotations

import copy
from typing import Any, Mapping, Sequence

from engines.interpretation_engine.exceptions.interpretation_error import (
    InterpretationArchitectureError,
)
from engines.interpretation_engine.foundation_constants import INTERPRETATION_VERSION
from engines.interpretation_engine.knowledge.composition_result import (
    CompositionResult,
    SentenceCandidate,
)

ASSEMBLY_VERSION = "1.0.0"
ASSEMBLY_ENGINE_ID = "interpretation_composition_engine"


class AssemblyError(InterpretationArchitectureError):
    """Base error for IE-3 composition assembly failures."""


class DuplicatePublicationError(AssemblyError):
    """Raised when an assembly output is published twice."""


def snapshot_value(value: Any, *, label: str) -> dict[str, Any]:
    """Copy an upstream object into an isolated mapping."""
    if value is None:
        raise AssemblyError(f"missing_{label}")
    if hasattr(value, "to_dict"):
        payload = value.to_dict()
        if not isinstance(payload, Mapping):
            raise AssemblyError(f"invalid_{label}")
        return copy.deepcopy(dict(payload))
    if isinstance(value, Mapping):
        return copy.deepcopy(dict(value))
    raise AssemblyError(f"invalid_{label}")


def extract_candidates(value: Any) -> tuple[dict[str, Any], ...]:
    """Normalize sentence candidates to isolated dictionaries."""
    if value is None:
        return ()
    items: Sequence[Any]
    if isinstance(value, CompositionResult):
        items = value.candidates
    elif isinstance(value, Mapping):
        items = tuple(value.get("candidates") or ())
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        items = value
    else:
        raise AssemblyError("invalid_sentence_candidates")
    normalized: list[dict[str, Any]] = []
    for item in items:
        if isinstance(item, SentenceCandidate):
            normalized.append(copy.deepcopy(item.to_dict()))
        elif isinstance(item, Mapping):
            normalized.append(copy.deepcopy(dict(item)))
        else:
            raise AssemblyError("invalid_sentence_candidate")
    return tuple(normalized)


class InterpretationAssemblyContext:
    """Append-only context over sealed IE-1 / IE-2 / AX snapshots."""

    def __init__(
        self,
        *,
        analysis_snapshot: Mapping[str, Any],
        decision_snapshot: Mapping[str, Any],
        luck_snapshot: Mapping[str, Any],
        interpretation_snapshot: Mapping[str, Any],
        selection_snapshot: Mapping[str, Any],
        candidates: Sequence[Mapping[str, Any]],
        assembly_version: str = ASSEMBLY_VERSION,
        interpretation_version: str = INTERPRETATION_VERSION,
    ) -> None:
        """Seal upstream snapshots. Assembly outputs publish separately."""
        self._analysis = dict(analysis_snapshot)
        self._decision = dict(decision_snapshot)
        self._luck = dict(luck_snapshot)
        self._interpretation = dict(interpretation_snapshot)
        self._selection = dict(selection_snapshot)
        self._candidates = tuple(copy.deepcopy(dict(item)) for item in candidates)
        self._published: dict[str, Any] = {}
        self.assembly_version = assembly_version
        self.interpretation_version = interpretation_version

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

    def selection_snapshot(self) -> dict[str, Any]:
        """Return a defensive IE-2 composition result copy."""
        return copy.deepcopy(self._selection)

    def candidates(self) -> tuple[dict[str, Any], ...]:
        """Return isolated sentence candidate dictionaries."""
        return tuple(copy.deepcopy(item) for item in self._candidates)

    def publish(self, name: str, value: Any) -> None:
        """Publish an assembly-owned output once."""
        reserved = {
            "analysis_snapshot",
            "decision_snapshot",
            "luck_snapshot",
            "interpretation_snapshot",
            "selection_snapshot",
            "sentence_candidates",
        }
        if name in reserved or name in self._published:
            raise DuplicatePublicationError(f"duplicate_output:{name}")
        self._published[name] = copy.deepcopy(value) if isinstance(value, (Mapping, list, tuple)) else value

    def get_published(self, name: str) -> Any:
        """Return a published assembly output when present."""
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
        """Serialize sealed snapshots and published assembly outputs."""
        return {
            "assembly_version": self.assembly_version,
            "interpretation_version": self.interpretation_version,
            "analysis_snapshot": self.analysis_snapshot(),
            "decision_snapshot": self.decision_snapshot(),
            "luck_snapshot": self.luck_snapshot(),
            "interpretation_snapshot": self.interpretation_snapshot(),
            "selection_snapshot": self.selection_snapshot(),
            "sentence_candidates": [copy.deepcopy(item) for item in self._candidates],
            "published_outputs": list(self.published_outputs()),
        }


def build_assembly_context(
    *,
    analysis_result: Any,
    decision_result: Any,
    luck_result: Any,
    interpretation_context: Any,
    composition_result: Any,
    sentence_candidates: Any = None,
) -> InterpretationAssemblyContext:
    """Build an append-only assembly context from canonical upstream inputs."""
    selection = snapshot_value(composition_result, label="composition_result")
    candidates = extract_candidates(
        sentence_candidates if sentence_candidates is not None else composition_result
    )
    return InterpretationAssemblyContext(
        analysis_snapshot=snapshot_value(analysis_result, label="canonical_analysis_result"),
        decision_snapshot=snapshot_value(decision_result, label="canonical_decision_result"),
        luck_snapshot=snapshot_value(luck_result, label="canonical_luck_result"),
        interpretation_snapshot=snapshot_value(
            interpretation_context,
            label="interpretation_context",
        ),
        selection_snapshot=selection,
        candidates=candidates,
    )
