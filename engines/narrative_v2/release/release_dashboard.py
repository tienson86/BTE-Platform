"""Internal release dashboard. Not a customer surface."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Mapping

from engines.narrative_v2.release.release_alerts import ReleaseAlert
from engines.narrative_v2.release.release_health import ReleaseHealth
from engines.narrative_v2.release.release_metrics import ReleaseMetrics

FORBIDDEN_CUSTOMER = ("/result", "canonical-desktop-root", "bte-cdash")


def render_dashboard_html(
    *,
    health: ReleaseHealth,
    alerts: tuple[ReleaseAlert, ...] | list[ReleaseAlert],
    metrics: ReleaseMetrics,
    parity: Mapping[str, Any],
) -> str:
    """Internal HTML. No customer chrome. No personal data."""
    overall = health.overall()
    rows = "".join(
        _row(label, value)
        for label, value in (
            ("Overall", overall),
            ("Runtime", health.runtime_status),
            ("Presentation", health.presentation_status),
            ("Portal", health.portal_status),
            ("Exports", health.export_status),
            ("Parity", health.parity_status),
            ("Golden", health.golden_status),
            ("Certification", health.certification_status),
            ("Provider", health.provider),
            ("Fallbacks", str(health.fallback_count)),
            ("Timestamp", health.timestamp),
        )
    )
    alert_rows = "".join(
        _row(item.level, f"{item.code} ({item.reason})") for item in alerts
    ) or _row("NONE", "no alerts")
    metric_rows = "".join(
        _row(label, str(value))
        for label, value in (
            ("runtime_success", metrics.runtime_success),
            ("runtime_failure", metrics.runtime_failure),
            ("fallback_automatic", metrics.fallback_automatic),
            ("fallback_manual", metrics.fallback_manual),
            ("provider_changes", metrics.provider_changes),
            ("parity_fail", metrics.parity_fail),
        )
    )
    parity_rows = "".join(
        _row(key, str(parity.get(key, "")))
        for key in ("portal", "pdf", "docx", "json", "matched", "status")
    )
    markup = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Narrative V2 Release Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #111; color: #eee; margin: 24px; }}
    h1, h2 {{ font-weight: 600; }}
    table {{ border-collapse: collapse; width: 720px; margin-bottom: 24px; }}
    th, td {{ border: 1px solid #444; padding: 8px 12px; text-align: left; }}
    th {{ width: 220px; background: #1c1c1c; }}
    .PASS {{ color: #7dcea0; }}
    .WARNING {{ color: #f7dc6f; }}
    .FAIL {{ color: #f1948a; }}
    .UNKNOWN {{ color: #aab7b8; }}
  </style>
</head>
<body data-release-dashboard="internal" data-customer-access="false">
  <h1>Narrative V2 Release Dashboard</h1>
  <p>Internal only. Dual-run monitoring. Pack05 remains fallback.</p>
  <h2>Health</h2>
  <table data-section="health">{rows}</table>
  <h2>Alerts</h2>
  <table data-section="alerts">{alert_rows}</table>
  <h2>Metrics</h2>
  <table data-section="metrics">{metric_rows}</table>
  <h2>Parity hashes</h2>
  <table data-section="parity">{parity_rows}</table>
</body>
</html>
"""
    for token in FORBIDDEN_CUSTOMER:
        if token in markup:
            raise ValueError("customer_surface_leak")
    return markup


def write_dashboard(path: Path, markup: str) -> Path:
    """Write the internal dashboard HTML."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markup, encoding="utf-8")
    return path


def _row(label: str, value: str) -> str:
    css = value if value in {"PASS", "WARNING", "FAIL", "UNKNOWN"} else ""
    return (
        f"<tr><th>{escape(label)}</th>"
        f'<td class="{escape(css)}">{escape(value)}</td></tr>'
    )
