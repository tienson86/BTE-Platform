"""Write N-REL-02 CASE-0001 dual-run monitoring artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from applications.api.services.orchestrator import OrchestratorService
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from engines.narrative_v2.certification.certification_history import CertificationHistory
from engines.narrative_v2.presentation import NarrativeV2Presentation
from engines.narrative_v2.release import (
    ReleaseHistory,
    ReleaseMonitor,
    ReleaseSnapshot,
    render_dashboard_html,
    write_dashboard,
)
from engines.narrative_v2.runtime import NarrativeRuntime

OUT = REPO / "implementation" / "narrative_release" / "n_rel_02"
CERT = REPO / "implementation" / "narrative_v2" / "n_imp_11a" / "certification_history.json"


def _run_case0001() -> NarrativeV2Presentation:
    request = CASE_0001_REQUEST
    canonical = OrchestratorService().run_stage(
        "luck",
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
    )
    result = NarrativeRuntime().run(canonical)
    if not isinstance(result.presentation, NarrativeV2Presentation):
        raise RuntimeError("presentation_unavailable")
    return result.presentation


def main() -> None:
    """Observe CASE-0001 production dual-run and write artifacts."""
    OUT.mkdir(parents=True, exist_ok=True)
    history = ReleaseHistory(OUT / "release_history.json")
    if history.path.exists():
        history.path.unlink()
    monitor = ReleaseMonitor(
        history=history,
        certification=CertificationHistory(CERT),
    )
    presentation = _run_case0001()
    production = monitor.observe(
        presentation=presentation,
        runtime_ok=True,
        provider="v2",
        portal_selected="v2",
        case_id="CASE-0001",
    )
    (OUT / "release_health.json").write_text(
        json.dumps(production.health.to_record(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "parity_hashes.json").write_text(
        json.dumps(dict(production.parity), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT / "fallback_report.md").write_text(_fallback_markdown(production), encoding="utf-8")
    markup = render_dashboard_html(
        health=production.health,
        alerts=production.alerts,
        metrics=production.metrics,
        parity=production.parity,
    )
    write_dashboard(OUT / "release_dashboard.html", markup)
    _screenshot(markup, OUT / "release_dashboard.png")


def _fallback_markdown(snapshot: ReleaseSnapshot) -> str:
    health = snapshot.health
    metrics = snapshot.metrics
    lines = [
        "# N-REL-02 Fallback Report",
        "",
        "CASE-0001 production dual-run. Pack05 remains fallback. No retirement.",
        "",
        f"Provider: `{health.provider}`",
        f"Automatic fallback events: {metrics.fallback_automatic}",
        f"Manual rollback events: {metrics.fallback_manual}",
        f"Fallback count: {health.fallback_count}",
        f"Overall health: {health.overall()}",
        "",
        "## Policy",
        "",
        "- Automatic fallback: invalid Presentation → Pack05, record event, do not interrupt.",
        "- Manual rollback: `provider=pack05`, no rebuild.",
        "- CASE-0001 production path in this run used Narrative V2 with no fallback.",
        "",
    ]
    return "\n".join(lines)


def _screenshot(markup: str, path: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 900, "height": 1100})
        page.set_content(markup, wait_until="networkidle")
        page.screenshot(path=str(path), full_page=True)
        browser.close()


if __name__ == "__main__":
    main()
