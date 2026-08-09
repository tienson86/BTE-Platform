"""Canonical Report Context (RE-1). Append-only. Immutable upstream."""

from __future__ import annotations

import copy
from typing import Any, Mapping

from engines.report_engine.contracts.report_contracts import (
    ReportContext,
    ReportMetadata,
    empty_report_result,
)
from engines.report_engine.exceptions.foundation_error import (
    ReportContextIntegrityError,
    ReportDuplicateIdError,
    ReportFoundationError,
)
from engines.report_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    CONTEXT_STATUS_READY,
    REPORT_VERSION,
    REQUIRED_SCHEMA_VERSION,
)


def snapshot_upstream(value: Any, *, label: str) -> dict[str, Any]:
    """Copy an upstream canonical result into an isolated mapping."""
    if value is None:
        raise ReportFoundationError(f"missing_{label}")
    if hasattr(value, "to_dict"):
        payload = value.to_dict()
        if not isinstance(payload, Mapping):
            raise ReportFoundationError(f"invalid_{label}")
        return copy.deepcopy(dict(payload))
    if isinstance(value, Mapping):
        return copy.deepcopy(dict(value))
    raise ReportFoundationError(f"invalid_{label}")


def interpretation_pipeline_version(snapshot: Mapping[str, Any]) -> str | None:
    """Read IX-1 pipeline version, falling back to interpretation_version."""
    value = snapshot.get("interpretation_pipeline_version")
    if value is None:
        value = snapshot.get("interpretation_version")
    if value is None:
        return None
    return str(value)


class CanonicalReportContext:
    """Append-only runtime context over frozen AX-2 / AX-3 / AX-4 / IX-1 snapshots."""

    def __init__(
        self,
        *,
        analysis_snapshot: Mapping[str, Any],
        decision_snapshot: Mapping[str, Any],
        luck_snapshot: Mapping[str, Any],
        interpretation_snapshot: Mapping[str, Any],
        report_version: str = REPORT_VERSION,
    ) -> None:
        """Seal upstream snapshots. Callers cannot mutate the originals via this context."""
        self._report_version = report_version
        self._analysis = dict(analysis_snapshot)
        self._decision = dict(decision_snapshot)
        self._luck = dict(luck_snapshot)
        self._interpretation = dict(interpretation_snapshot)
        self._published: dict[str, Any] = {}
        self._status = CONTEXT_STATUS_READY

    @property
    def report_version(self) -> str:
        """Return the foundation version bound to this context."""
        return self._report_version

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

    def interpretation_snapshot(self) -> dict[str, Any]:
        """Return a defensive copy of the IX-1 snapshot."""
        return copy.deepcopy(self._interpretation)

    def publish(self, name: str, value: Any) -> None:
        """Publish a foundation-owned output once. Upstream keys are reserved."""
        reserved = {
            "analysis_snapshot",
            "decision_snapshot",
            "luck_snapshot",
            "interpretation_snapshot",
        }
        if name in reserved:
            raise ReportContextIntegrityError(f"reserved_output:{name}")
        if name in self._published:
            raise ReportDuplicateIdError(f"duplicate_output:{name}")
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

    def metadata(self) -> ReportMetadata:
        """Derive version metadata from sealed upstream snapshots."""
        return ReportMetadata(
            report_version=self._report_version,
            schema_version=REQUIRED_SCHEMA_VERSION,
            analysis_pipeline_version=_as_str(self._analysis.get("pipeline_version")),
            decision_pipeline_version=_as_str(self._decision.get("decision_pipeline_version")),
            luck_pipeline_version=_as_str(self._luck.get("luck_pipeline_version")),
            interpretation_pipeline_version=interpretation_pipeline_version(self._interpretation),
            module_ids=CANONICAL_MODULE_ORDER,
        )

    def to_contract(self) -> ReportContext:
        """Project the runtime context onto the published contract."""
        return ReportContext(
            report_version=self._report_version,
            analysis_snapshot=self.analysis_snapshot(),
            decision_snapshot=self.decision_snapshot(),
            luck_snapshot=self.luck_snapshot(),
            interpretation_snapshot=self.interpretation_snapshot(),
            published_outputs=self.published_outputs(),
            metadata=self.metadata(),
            status=self._status,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the published context contract."""
        return self.to_contract().to_dict()

    def empty_result(self) -> dict[str, Any]:
        """Return the RE-1 empty CanonicalReportResult shell."""
        return empty_report_result(
            context=self.to_dict(),
            metadata=self.metadata().to_dict(),
        ).to_dict()


def build_report_context(
    *,
    analysis_result: Any,
    decision_result: Any,
    luck_result: Any,
    interpretation_result: Any,
    report_version: str = REPORT_VERSION,
) -> CanonicalReportContext:
    """Build an append-only Report Context from canonical upstream results."""
    analysis = snapshot_upstream(analysis_result, label="canonical_analysis_result")
    decision = snapshot_upstream(decision_result, label="canonical_decision_result")
    luck = snapshot_upstream(luck_result, label="canonical_luck_result")
    interpretation = snapshot_upstream(
        interpretation_result,
        label="canonical_interpretation_result",
    )
    _assert_upstream_untouched(analysis_result, analysis, label="canonical_analysis_result")
    return CanonicalReportContext(
        analysis_snapshot=analysis,
        decision_snapshot=decision,
        luck_snapshot=luck,
        interpretation_snapshot=interpretation,
        report_version=report_version,
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
        raise ReportContextIntegrityError(f"upstream_mutated:{label}")
