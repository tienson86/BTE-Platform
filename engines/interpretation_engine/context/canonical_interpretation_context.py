"""Canonical Interpretation Context (IE-1). Append-only. Immutable upstream."""

from __future__ import annotations

import copy
from typing import Any, Mapping

from engines.interpretation_engine.contracts.interpretation_contracts import (
    InterpretationContext,
    InterpretationMetadata,
    empty_interpretation_result,
)
from engines.interpretation_engine.exceptions.foundation_error import (
    InterpretationContextIntegrityError,
    InterpretationDuplicateIdError,
    InterpretationFoundationError,
)
from engines.interpretation_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    CONTEXT_STATUS_READY,
    INTERPRETATION_VERSION,
    REQUIRED_SCHEMA_VERSION,
)


def snapshot_upstream(value: Any, *, label: str) -> dict[str, Any]:
    """Copy an upstream canonical result into an isolated mapping."""
    if value is None:
        raise InterpretationFoundationError(f"missing_{label}")
    if hasattr(value, "to_dict"):
        payload = value.to_dict()
        if not isinstance(payload, Mapping):
            raise InterpretationFoundationError(f"invalid_{label}")
        return copy.deepcopy(dict(payload))
    if isinstance(value, Mapping):
        return copy.deepcopy(dict(value))
    raise InterpretationFoundationError(f"invalid_{label}")


class CanonicalInterpretationContext:
    """Append-only runtime context over frozen AX-2 / AX-3 / AX-4 snapshots."""

    def __init__(
        self,
        *,
        analysis_snapshot: Mapping[str, Any],
        decision_snapshot: Mapping[str, Any],
        luck_snapshot: Mapping[str, Any],
        interpretation_version: str = INTERPRETATION_VERSION,
    ) -> None:
        """Seal upstream snapshots. Callers cannot mutate the originals via this context."""
        self._interpretation_version = interpretation_version
        self._analysis = dict(analysis_snapshot)
        self._decision = dict(decision_snapshot)
        self._luck = dict(luck_snapshot)
        self._published: dict[str, Any] = {}
        self._status = CONTEXT_STATUS_READY

    @property
    def interpretation_version(self) -> str:
        """Return the foundation version bound to this context."""
        return self._interpretation_version

    @property
    def status(self) -> str:
        """Return the context readiness status."""
        return self._status

    def analysis_snapshot(self) -> dict[str, Any]:
        """Return a defensive copy of the AX-2 snapshot."""
        return copy.deepcopy(self._analysis)

    def decision_snapshot(self) -> dict[str, Any]:
        """Return a defensive copy of the AX-3 snapshot."""
        return copy.deepcopy(self._decision)

    def luck_snapshot(self) -> dict[str, Any]:
        """Return a defensive copy of the AX-4 snapshot."""
        return copy.deepcopy(self._luck)

    def publish(self, name: str, value: Any) -> None:
        """Publish a foundation-owned output once. Upstream keys are reserved."""
        reserved = {"analysis_snapshot", "decision_snapshot", "luck_snapshot"}
        if name in reserved:
            raise InterpretationContextIntegrityError(f"reserved_output:{name}")
        if name in self._published:
            raise InterpretationDuplicateIdError(f"duplicate_output:{name}")
        self._published[name] = copy.deepcopy(value) if isinstance(value, Mapping) else value

    def get_published(self, name: str) -> Any:
        """Return a published foundation output when present."""
        value = self._published.get(name)
        if isinstance(value, Mapping):
            return copy.deepcopy(dict(value))
        return value

    def published_outputs(self) -> tuple[str, ...]:
        """Return published output names in insertion order."""
        return tuple(self._published)

    def metadata(self) -> InterpretationMetadata:
        """Derive version metadata from sealed upstream snapshots."""
        return InterpretationMetadata(
            interpretation_version=self._interpretation_version,
            schema_version=REQUIRED_SCHEMA_VERSION,
            analysis_pipeline_version=_as_str(self._analysis.get("pipeline_version")),
            decision_pipeline_version=_as_str(self._decision.get("decision_pipeline_version")),
            luck_pipeline_version=_as_str(self._luck.get("luck_pipeline_version")),
            module_ids=CANONICAL_MODULE_ORDER,
        )

    def to_contract(self) -> InterpretationContext:
        """Project the runtime context onto the published contract."""
        return InterpretationContext(
            interpretation_version=self._interpretation_version,
            analysis_snapshot=self.analysis_snapshot(),
            decision_snapshot=self.decision_snapshot(),
            luck_snapshot=self.luck_snapshot(),
            published_outputs=self.published_outputs(),
            metadata=self.metadata(),
            status=self._status,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the published context contract."""
        return self.to_contract().to_dict()

    def empty_result(self) -> dict[str, Any]:
        """Return the IE-1 empty CanonicalInterpretationResult shell."""
        return empty_interpretation_result(
            context=self.to_dict(),
            metadata=self.metadata().to_dict(),
        ).to_dict()


def build_interpretation_context(
    *,
    analysis_result: Any,
    decision_result: Any,
    luck_result: Any,
    interpretation_version: str = INTERPRETATION_VERSION,
) -> CanonicalInterpretationContext:
    """Build an append-only Interpretation Context from canonical upstream results."""
    analysis = snapshot_upstream(analysis_result, label="canonical_analysis_result")
    decision = snapshot_upstream(decision_result, label="canonical_decision_result")
    luck = snapshot_upstream(luck_result, label="canonical_luck_result")
    _assert_upstream_untouched(analysis_result, analysis, label="canonical_analysis_result")
    return CanonicalInterpretationContext(
        analysis_snapshot=analysis,
        decision_snapshot=decision,
        luck_snapshot=luck,
        interpretation_version=interpretation_version,
    )


def _as_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _assert_upstream_untouched(original: Any, snapshot: Mapping[str, Any], *, label: str) -> None:
    """Ensure snapshot isolation did not require mutating a mapping input."""
    if not isinstance(original, Mapping):
        return
    if "pipeline_id" in original and original.get("pipeline_id") != snapshot.get("pipeline_id"):
        raise InterpretationContextIntegrityError(f"upstream_mutated:{label}")
