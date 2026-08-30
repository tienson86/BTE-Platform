"""ReleaseMonitor — dual-run observation facade. No customer Narrative rewrite."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from engines.narrative_v2.certification.certification_history import CertificationHistory
from engines.narrative_v2.export.export_errors import IncompatiblePresentationVersion
from engines.narrative_v2.export.export_serializer import presentation_from_mapping
from engines.narrative_v2.golden.golden_dataset import GoldenDataset
from engines.narrative_v2.presentation.presentation_model import NarrativeV2Presentation
from engines.narrative_v2.presentation.presentation_serializer import serialize_customer
from engines.narrative_v2.release.release_alerts import ReleaseAlert, evaluate_alerts
from engines.narrative_v2.release.release_events import (
    EVENT_FALLBACK_AUTO,
    EVENT_FALLBACK_MANUAL,
    EVENT_GOLDEN,
    EVENT_HEALTH,
    EVENT_PARITY,
    EVENT_PRESENTATION,
    EVENT_PROVIDER,
    EVENT_RUNTIME,
    ReleaseEvent,
    make_event,
)
from engines.narrative_v2.release.release_health import (
    HEALTH_FAIL,
    HEALTH_PASS,
    ReleaseHealth,
    assess_certification,
    assess_export,
    assess_golden,
    assess_portal,
    assess_presentation,
    assess_runtime,
    build_health,
)
from engines.narrative_v2.release.release_history import ReleaseHistory
from engines.narrative_v2.release.release_metrics import ReleaseMetrics, metrics_from_events
from engines.narrative_v2.release.release_parity import parity_hashes

CASE_0001 = "CASE-0001"
CERT_CASE0001 = (
    Path(__file__).resolve().parents[3]
    / "implementation"
    / "narrative_v2"
    / "n_imp_11a"
    / "certification_history.json"
)


@dataclass(frozen=True, slots=True)
class ReleaseSnapshot:
    """One dual-run observation. No personal data."""

    health: ReleaseHealth
    alerts: tuple[ReleaseAlert, ...]
    parity: Mapping[str, Any]
    events: tuple[ReleaseEvent, ...]
    metrics: ReleaseMetrics

    def to_record(self) -> dict[str, Any]:
        """JSON-safe snapshot."""
        return {
            "health": self.health.to_record(),
            "alerts": [item.to_record() for item in self.alerts],
            "parity": dict(self.parity),
            "metrics": {
                "runtime_success": self.metrics.runtime_success,
                "runtime_failure": self.metrics.runtime_failure,
                "presentation_success": self.metrics.presentation_success,
                "presentation_failure": self.metrics.presentation_failure,
                "fallback_automatic": self.metrics.fallback_automatic,
                "fallback_manual": self.metrics.fallback_manual,
                "provider_changes": self.metrics.provider_changes,
                "parity_fail": self.metrics.parity_fail,
                "golden_mismatch": self.metrics.golden_mismatch,
                "fallback_count": self.metrics.fallback_count,
            },
        }


class ReleaseMonitor:
    """Observe production dual-run. Pack05 remains fallback. No retirement."""

    def __init__(
        self,
        *,
        history: ReleaseHistory | None = None,
        golden: GoldenDataset | None = None,
        certification: CertificationHistory | None = None,
    ) -> None:
        self._history = history or ReleaseHistory()
        self._golden = golden or GoldenDataset()
        cert_path = CERT_CASE0001 if CERT_CASE0001.exists() else None
        self._certification = certification or CertificationHistory(cert_path)

    def observe(
        self,
        *,
        presentation: NarrativeV2Presentation | Mapping[str, Any] | None,
        provider: str = "v2",
        portal_selected: str = "v2",
        runtime_ok: bool | None = None,
        fallback: bool = False,
        fallback_kind: str | None = None,
        fallback_reason: str = "",
        case_id: str = CASE_0001,
    ) -> ReleaseSnapshot:
        """Record one production observation and return health."""
        runtime_status = assess_runtime(runtime_ok)
        presentation_status = assess_presentation(presentation)
        parity = parity_hashes(presentation if presentation_status == HEALTH_PASS else None)
        golden_matched = _golden_matched(self._golden, case_id, presentation, presentation_status)
        cert_status = self._certification.current_status(case_id)
        events = self._record_events(
            provider=provider,
            portal_selected=portal_selected,
            runtime_status=runtime_status,
            presentation_status=presentation_status,
            fallback=fallback,
            fallback_kind=fallback_kind,
            fallback_reason=fallback_reason,
            parity=parity,
            golden_matched=golden_matched,
        )
        metrics = metrics_from_events(self._history.list())
        health = build_health(
            runtime_status=runtime_status,
            presentation_status=presentation_status,
            portal_status=assess_portal(
                provider=provider,
                selected=portal_selected,
                fallback=fallback,
            ),
            export_status=assess_export(parity.get("matched") if isinstance(parity.get("matched"), bool) else None),
            provider=provider,
            fallback_count=metrics.fallback_count,
            parity_status=str(parity.get("status") or HEALTH_FAIL),
            golden_status=assess_golden(golden_matched),
            certification_status=assess_certification(cert_status),
        )
        alerts = evaluate_alerts(health)
        self._history.append(
            make_event(
                EVENT_HEALTH,
                provider=provider,
                status=health.overall(),
                reason="snapshot",
            )
        )
        return ReleaseSnapshot(
            health=health,
            alerts=alerts,
            parity=parity,
            events=tuple(events),
            metrics=metrics_from_events(self._history.list()),
        )

    def metrics(self) -> ReleaseMetrics:
        """Current counters from append-only history."""
        return metrics_from_events(self._history.list())

    def _record_events(
        self,
        *,
        provider: str,
        portal_selected: str,
        runtime_status: str,
        presentation_status: str,
        fallback: bool,
        fallback_kind: str | None,
        fallback_reason: str,
        parity: Mapping[str, Any],
        golden_matched: bool | None,
    ) -> list[ReleaseEvent]:
        previous = self._history.latest()
        rows: list[ReleaseEvent] = [
            make_event(EVENT_RUNTIME, provider=provider, status=runtime_status, reason="runtime"),
            make_event(
                EVENT_PRESENTATION,
                provider=provider,
                status=presentation_status,
                reason="presentation",
            ),
        ]
        if previous and previous.provider != provider:
            rows.append(
                make_event(
                    EVENT_PROVIDER,
                    provider=provider,
                    status=HEALTH_PASS,
                    reason=f"{previous.provider}->{provider}",
                )
            )
        if fallback:
            kind = EVENT_FALLBACK_MANUAL if fallback_kind == "manual" else EVENT_FALLBACK_AUTO
            rows.append(
                make_event(
                    kind,
                    provider=portal_selected,
                    status=HEALTH_FAIL if presentation_status == HEALTH_FAIL else HEALTH_PASS,
                    reason=fallback_reason or fallback_kind or "fallback",
                )
            )
        parity_status = str(parity.get("status") or HEALTH_FAIL)
        rows.append(
            make_event(
                EVENT_PARITY,
                provider=provider,
                status=parity_status,
                reason=str(parity.get("reason") or ""),
            )
        )
        if golden_matched is not None:
            rows.append(
                make_event(
                    EVENT_GOLDEN,
                    provider=provider,
                    status=HEALTH_PASS if golden_matched else HEALTH_FAIL,
                    reason="matched" if golden_matched else "mismatch",
                )
            )
        for row in rows:
            self._history.append(row)
        return rows


def _golden_matched(
    golden: GoldenDataset,
    case_id: str,
    presentation: NarrativeV2Presentation | Mapping[str, Any] | None,
    presentation_status: str,
) -> bool | None:
    if presentation is None or presentation_status != HEALTH_PASS:
        return False if presentation_status == HEALTH_FAIL else None
    payload = (
        serialize_customer(presentation)
        if isinstance(presentation, NarrativeV2Presentation)
        else dict(presentation)
    )
    try:
        if not isinstance(presentation, NarrativeV2Presentation):
            presentation_from_mapping(payload)
    except IncompatiblePresentationVersion:
        return False
    result = golden.compare(case_id=case_id, presentation=payload)
    if result.get("reason") == "missing_golden":
        return None
    return bool(result.get("matched"))
