"""Evidence and trace ID factories. Deterministic, no random UUIDs."""

from __future__ import annotations

from engines.mingju.models import EvidenceItem, TraceItem, WarningItem


class RecordBook:
    """Collects evidence, traces, and warnings in insertion order."""

    def __init__(self) -> None:
        self.evidence: list[EvidenceItem] = []
        self.traces: list[TraceItem] = []
        self.warnings: list[WarningItem] = []
        self._counts: dict[str, int] = {}

    def _next(self, prefix: str) -> str:
        index = self._counts.get(prefix, 0) + 1
        self._counts[prefix] = index
        return f"{prefix}-{index:03d}"

    def add_evidence(self, kind: str, statement_key: str, source: str = "", **details: object) -> str:
        """Append one evidence item and return its ID."""
        evidence_id = self._next("E-MC")
        self.evidence.append(
            EvidenceItem(
                evidence_id=evidence_id,
                kind=kind,
                statement_key=statement_key,
                source=source,
                details=dict(details),
            )
        )
        return evidence_id

    def add_trace(self, stage: str, rule_id: str, summary_key: str, evidence_ids: tuple[str, ...] = ()) -> str:
        """Append one trace item and return its ID."""
        trace_id = self._next("TR-MC")
        self.traces.append(
            TraceItem(
                trace_id=trace_id,
                stage=stage,
                rule_id=rule_id,
                summary_key=summary_key,
                evidence_ids=evidence_ids,
            )
        )
        return trace_id

    def add_warning(self, code: str, message_key: str) -> str:
        """Append one warning and return its ID."""
        warning_id = self._next("WRN-MC")
        self.warnings.append(
            WarningItem(warning_id=warning_id, code=code, message_key=message_key)
        )
        return warning_id

    def next_id(self, prefix: str) -> str:
        """Allocate a deterministic public ID such as DMG-MC-001."""
        return self._next(prefix)
