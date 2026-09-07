"""TV1-B08 performance baseline. Measure only. Do not optimize."""

from __future__ import annotations

import json
import time
from pathlib import Path

from consulting.marriage.api.service import MarriageConsultationApi
from tests.consulting.api_fixtures import api_client, api_service, valid_body

REPORT_DIR = Path(__file__).resolve().parents[2] / "docs" / "reports" / "tv01_marriage" / "b08"
BASELINE_PATH = REPORT_DIR / "performance_baseline.json"

_CANONICAL_STAGES = ("canonical_analysis_a", "canonical_analysis_b")
_DECISION_STAGES = (
    "evidence_builder",
    "evidence_validation",
    "domain_decision",
    "cross_domain_resolver",
    "overall_decision",
    "decision_validation",
)
_RECOMMENDATION_STAGES = ("recommendation_builder", "recommendation_validation")
_NARRATIVE_REPORT_STAGES = (
    "narrative_composer",
    "narrative_validation",
    "report_builder",
    "report_validation",
)


def _sum_named(timings: list, names: tuple[str, ...]) -> float:
    """Sum durations for exact stage names."""
    wanted = set(names)
    return round(sum(item.duration_ms for item in timings if item.stage in wanted), 3)


def test_record_performance_baseline() -> None:
    """Record representative live stage durations for later comparison."""
    client, container = api_client(live=True)
    api = api_service(container)
    assert isinstance(api, MarriageConsultationApi)
    started = time.perf_counter()
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    api_ms = (time.perf_counter() - started) * 1000.0
    assert created.status_code == 201
    stored = api.get_stored(created.json()["data"]["consultation_id"])
    session = getattr(api._orchestrator, "_session", None)
    timings = list(session.context.timings) if session is not None else []
    baseline = {
        "case": "LIVE 1987-01-21 / 1990-05-15",
        "units": "milliseconds",
        "api_total_duration_ms": round(api_ms, 3),
        "canonical_runtime_duration_ms": _sum_named(timings, _CANONICAL_STAGES),
        "decision_duration_ms": _sum_named(timings, _DECISION_STAGES),
        "recommendation_duration_ms": _sum_named(timings, _RECOMMENDATION_STAGES),
        "narrative_report_duration_ms": _sum_named(timings, _NARRATIVE_REPORT_STAGES),
        "stage_names": [item.stage for item in timings],
        "notes": [
            "Baseline only. No SLA enforced in B08.",
            "Canonical live path includes engine runtime inside canonical_runtime_duration_ms.",
            "consultation_id and timestamps are volatile and omitted.",
        ],
        "score_present": stored.result.overall.score is not None,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    assert baseline["api_total_duration_ms"] > 0
    assert baseline["canonical_runtime_duration_ms"] > 0
    assert baseline["decision_duration_ms"] >= 0
    assert baseline["score_present"] is False
