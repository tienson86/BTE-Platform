"""Narrative V2 release monitoring — dual-run operations.

Internal only. Does not retire Pack05. Does not freeze Presentation.
"""

from __future__ import annotations

from engines.narrative_v2.release.release_alerts import (
    ALERT_FALLBACK,
    ALERT_GOLDEN,
    ALERT_PARITY,
    ALERT_PRESENTATION,
    ReleaseAlert,
    evaluate_alerts,
)
from engines.narrative_v2.release.release_dashboard import render_dashboard_html, write_dashboard
from engines.narrative_v2.release.release_errors import ReleaseError, ReleaseHistoryError
from engines.narrative_v2.release.release_events import (
    ALLOWED_EVENTS,
    ALLOWED_PROVIDERS,
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
    ALLOWED_HEALTH,
    HEALTH_FAIL,
    HEALTH_PASS,
    HEALTH_UNKNOWN,
    HEALTH_WARNING,
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
from engines.narrative_v2.release.release_monitor import ReleaseMonitor, ReleaseSnapshot
from engines.narrative_v2.release.release_parity import content_hash, parity_hashes

__all__ = [
    "ALERT_FALLBACK",
    "ALERT_GOLDEN",
    "ALERT_PARITY",
    "ALERT_PRESENTATION",
    "ALLOWED_EVENTS",
    "ALLOWED_HEALTH",
    "ALLOWED_PROVIDERS",
    "EVENT_FALLBACK_AUTO",
    "EVENT_FALLBACK_MANUAL",
    "EVENT_GOLDEN",
    "EVENT_HEALTH",
    "EVENT_PARITY",
    "EVENT_PRESENTATION",
    "EVENT_PROVIDER",
    "EVENT_RUNTIME",
    "HEALTH_FAIL",
    "HEALTH_PASS",
    "HEALTH_UNKNOWN",
    "HEALTH_WARNING",
    "ReleaseAlert",
    "ReleaseError",
    "ReleaseEvent",
    "ReleaseHealth",
    "ReleaseHistory",
    "ReleaseHistoryError",
    "ReleaseMetrics",
    "ReleaseMonitor",
    "ReleaseSnapshot",
    "assess_certification",
    "assess_export",
    "assess_golden",
    "assess_portal",
    "assess_presentation",
    "assess_runtime",
    "build_health",
    "content_hash",
    "evaluate_alerts",
    "make_event",
    "metrics_from_events",
    "parity_hashes",
    "render_dashboard_html",
    "write_dashboard",
]
