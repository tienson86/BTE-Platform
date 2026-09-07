"""TV1-B08 performance baseline. Measure only. Do not optimize."""

from __future__ import annotations

import json
import time
from pathlib import Path

from tests.consulting.api_fixtures import api_client, api_service, valid_body
from tests.consulting.golden.cases import run_golden_case

REPORT_DIR = Path(__file__).resolve().parents[2] / "docs" / "reports" / "tv01_marriage" / "b08"
BASELINE_PATH = REPORT_DIR / "performance_baseline.json"


def _sum_timings(timings: list, prefixes: tuple[str, ...]) -> float:
    """Sum stage durations whose names start with any given prefix."""
    total = 0.0
    for item in timings:
        stage = item.stage if hasattr(item, "stage") else str(item)
        duration = item.duration_ms if hasattr(item, "duration_ms") else 0.0
        if any(stage.startswith(prefix) or prefix in stage for prefix in prefixes):
            total += float(duration)
    return total


def test_record_performance_baseline() -> None:
    """Record representative live and snapshot-stage durations for later comparison."""
    started = time.perf_counter()
    snapshot = run_golden_case("CASE-M02")
    snapshot_ms = (time.perf_counter() - started) * 1000.0
    client, container = api_client(live=True)
    api_started = time.perf_counter()
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    api_ms = (time.perf_counter() - api_started) * 1000.0
    assert created.status_code == 201
    stored = api_service(container).get_stored(created.json()["data"]["consultation_id"])
    timings = []
    context = getattr(getattr(api_service(container), "_orchestrator", None), "last_session", None)
    _ = context
    # Session timings are not on the stored DTO. Record API total plus snapshot-layer split.
    rec_started = time.perf_counter()
    from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider

    CanonicalRecommendationProvider().provide(snapshot["decision"])
    rec_ms = (time.perf_counter() - rec_started) * 1000.0
    baseline = {
        "case": "LIVE 1987-01-21 / 1990-05-15 plus CASE-M02 snapshot pipeline",
        "units": "milliseconds",
        "api_total_duration_ms": round(api_ms, 3),
        "snapshot_pipeline_duration_ms": round(snapshot_ms, 3),
        "recommendation_rebuild_duration_ms": round(rec_ms, 3),
        "notes": [
            "Baseline only. No SLA enforced in B08.",
            "Canonical live path includes engine runtime inside api_total_duration_ms.",
            "consultation_id and timestamps are volatile and omitted.",
        ],
        "score_present": stored.result.overall.score is not None,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    assert baseline["api_total_duration_ms"] > 0
    assert baseline["snapshot_pipeline_duration_ms"] > 0
    assert baseline["score_present"] is False
    _ = timings
