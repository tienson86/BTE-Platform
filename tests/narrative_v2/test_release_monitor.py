"""N-REL-02 dual-run release monitoring tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.certification.certification_history import CertificationHistory
from engines.narrative_v2.presentation import PRESENTATION_VERSION, NarrativeV2Presentation
from engines.narrative_v2.release import (
    EVENT_FALLBACK_AUTO,
    EVENT_FALLBACK_MANUAL,
    EVENT_PROVIDER,
    HEALTH_FAIL,
    HEALTH_PASS,
    HEALTH_WARNING,
    ReleaseHistory,
    ReleaseHistoryError,
    ReleaseMonitor,
    assess_portal,
    assess_presentation,
    assess_runtime,
    content_hash,
    evaluate_alerts,
    make_event,
    parity_hashes,
    render_dashboard_html,
)
from engines.narrative_v2.runtime import NarrativeRuntime

REPO = Path(__file__).resolve().parents[2]
FROZEN = REPO / "implementation" / "narrative_v2" / "n_imp_09a" / "case0001_presentation_v2_1.json"
CERT = REPO / "implementation" / "narrative_v2" / "n_imp_11a" / "certification_history.json"
PORTAL_APP = REPO / "applications" / "customer_portal" / "app.py"


def _presentation() -> dict[str, Any]:
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def _monitor(tmp_path: Path) -> ReleaseMonitor:
    return ReleaseMonitor(
        history=ReleaseHistory(tmp_path / "release_history.json"),
        certification=CertificationHistory(CERT),
    )


def test_runtime_health_case0001(case_0001_canonical: dict[str, Any], tmp_path: Path) -> None:
    result = NarrativeRuntime().run(case_0001_canonical)
    assert isinstance(result.presentation, NarrativeV2Presentation)
    snapshot = _monitor(tmp_path).observe(
        presentation=result.presentation,
        runtime_ok=True,
        provider="v2",
        portal_selected="v2",
        case_id="CASE-0001",
    )
    assert snapshot.health.runtime_status == HEALTH_PASS
    assert assess_runtime(True) == HEALTH_PASS
    assert assess_runtime(False) == HEALTH_FAIL


def test_presentation_health_accepts_v21() -> None:
    assert assess_presentation(_presentation()) == HEALTH_PASS
    bad = dict(_presentation())
    bad["metadata"] = {**bad["metadata"], "version": "bte.presentation.v2"}
    assert assess_presentation(bad) == HEALTH_FAIL
    assert assess_presentation(None) == HEALTH_FAIL


def test_export_parity_hashes_content_not_bytes() -> None:
    hashes = parity_hashes(_presentation())
    assert hashes["matched"] is True
    assert hashes["status"] == HEALTH_PASS
    assert hashes["portal"] == hashes["pdf"] == hashes["docx"] == hashes["json"]
    assert len(hashes["portal"]) == 64
    texts = ("a", "b")
    assert content_hash(texts) == content_hash(list(texts))
    assert content_hash(("a",)) != content_hash(("b",))


def test_export_parity_fail_on_invalid_presentation() -> None:
    hashes = parity_hashes({"metadata": {"version": "nope"}})
    assert hashes["matched"] is False
    assert hashes["status"] == HEALTH_FAIL


def test_fallback_automatic_raises_warning(tmp_path: Path) -> None:
    snapshot = _monitor(tmp_path).observe(
        presentation=_presentation(),
        runtime_ok=True,
        provider="v2",
        portal_selected="pack05",
        fallback=True,
        fallback_kind="automatic",
        fallback_reason="incompatible_presentation_version",
    )
    assert snapshot.health.fallback_count >= 1
    assert snapshot.health.overall() == HEALTH_WARNING
    assert any(item.event == EVENT_FALLBACK_AUTO for item in snapshot.events)
    assert any(item.code == "fallback_detected" for item in snapshot.alerts)


def test_manual_rollback_is_tracked(tmp_path: Path) -> None:
    snapshot = _monitor(tmp_path).observe(
        presentation=_presentation(),
        runtime_ok=True,
        provider="pack05",
        portal_selected="pack05",
        fallback=True,
        fallback_kind="manual",
        fallback_reason="provider=pack05",
    )
    assert any(item.event == EVENT_FALLBACK_MANUAL for item in snapshot.events)
    assert snapshot.metrics.fallback_manual >= 1


def test_provider_change_is_recorded(tmp_path: Path) -> None:
    monitor = _monitor(tmp_path)
    monitor.observe(
        presentation=_presentation(),
        runtime_ok=True,
        provider="v2",
        portal_selected="v2",
    )
    second = monitor.observe(
        presentation=_presentation(),
        runtime_ok=True,
        provider="pack05",
        portal_selected="pack05",
    )
    assert any(item.event == EVENT_PROVIDER for item in second.events)
    assert second.metrics.provider_changes >= 1
    assert assess_portal(provider="v2", selected="v2", fallback=False) == HEALTH_PASS


def test_dashboard_is_internal_only(tmp_path: Path) -> None:
    snapshot = _monitor(tmp_path).observe(
        presentation=_presentation(),
        runtime_ok=True,
        provider="v2",
        portal_selected="v2",
    )
    html = render_dashboard_html(
        health=snapshot.health,
        alerts=snapshot.alerts,
        metrics=snapshot.metrics,
        parity=snapshot.parity,
    )
    assert 'data-release-dashboard="internal"' in html
    assert 'data-customer-access="false"' in html
    assert "/result" not in html
    assert "Nguyễn" not in html
    assert "1987" not in html
    source = PORTAL_APP.read_text(encoding="utf-8")
    assert "release_dashboard" not in source
    assert "n_rel_02" not in source


def test_alerts_fail_on_invalid_presentation_parity_and_golden(tmp_path: Path) -> None:
    snapshot = _monitor(tmp_path).observe(
        presentation={"metadata": {"version": "bad"}, "status": "invalid"},
        runtime_ok=False,
        provider="v2",
        portal_selected="pack05",
        fallback=True,
        fallback_kind="automatic",
        fallback_reason="invalid",
    )
    codes = {item.code for item in snapshot.alerts}
    assert "presentation_invalid" in codes
    levels = {item.level for item in snapshot.alerts}
    assert HEALTH_FAIL in levels
    assert HEALTH_WARNING in levels
    from engines.narrative_v2.release.release_health import build_health

    mismatch = build_health(
        runtime_status=HEALTH_PASS,
        presentation_status=HEALTH_PASS,
        portal_status=HEALTH_PASS,
        export_status=HEALTH_FAIL,
        provider="v2",
        fallback_count=0,
        parity_status=HEALTH_FAIL,
        golden_status=HEALTH_FAIL,
        certification_status=HEALTH_PASS,
    )
    alerts = evaluate_alerts(mismatch)
    assert {item.code for item in alerts} >= {"export_parity_fail", "golden_mismatch"}


def test_history_is_append_only(tmp_path: Path) -> None:
    history = ReleaseHistory(tmp_path / "history.json")
    history.append(make_event("runtime", provider="v2", status=HEALTH_PASS, reason="ok"))
    history.append(make_event("runtime", provider="v2", status=HEALTH_FAIL, reason="boom"))
    rows = history.list()
    assert len(rows) == 2
    assert rows[0].status == HEALTH_PASS
    with pytest.raises(ReleaseHistoryError):
        history.replace_all([])
    assert len(history.list()) == 2
    assert FROZEN.exists()
    payload = _presentation()
    assert payload["metadata"]["version"] == PRESENTATION_VERSION
