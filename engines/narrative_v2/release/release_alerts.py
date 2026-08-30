"""Release alerts. WARNING on fallback. FAIL on invalid Presentation, parity, Golden."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.narrative_v2.release.release_health import (
    HEALTH_FAIL,
    HEALTH_WARNING,
    ReleaseHealth,
)

ALERT_FALLBACK = "fallback_detected"
ALERT_PRESENTATION = "presentation_invalid"
ALERT_PARITY = "export_parity_fail"
ALERT_GOLDEN = "golden_mismatch"


@dataclass(frozen=True, slots=True)
class ReleaseAlert:
    """Internal operational alert. No personal data."""

    level: str
    code: str
    reason: str

    def to_record(self) -> dict[str, Any]:
        """JSON-safe alert row."""
        return {"level": self.level, "code": self.code, "reason": self.reason}


def evaluate_alerts(health: ReleaseHealth) -> tuple[ReleaseAlert, ...]:
    """Raise WARNING when fallback > 0. Raise FAIL for contract breaks."""
    alerts: list[ReleaseAlert] = []
    if health.fallback_count > 0:
        alerts.append(
            ReleaseAlert(
                level=HEALTH_WARNING,
                code=ALERT_FALLBACK,
                reason="fallback_count_gt_zero",
            )
        )
    if health.presentation_status == HEALTH_FAIL:
        alerts.append(
            ReleaseAlert(
                level=HEALTH_FAIL,
                code=ALERT_PRESENTATION,
                reason="presentation_invalid",
            )
        )
    if health.parity_status == HEALTH_FAIL or health.export_status == HEALTH_FAIL:
        alerts.append(
            ReleaseAlert(
                level=HEALTH_FAIL,
                code=ALERT_PARITY,
                reason="export_parity_fail",
            )
        )
    if health.golden_status == HEALTH_FAIL:
        alerts.append(
            ReleaseAlert(
                level=HEALTH_FAIL,
                code=ALERT_GOLDEN,
                reason="golden_mismatch",
            )
        )
    return tuple(alerts)
