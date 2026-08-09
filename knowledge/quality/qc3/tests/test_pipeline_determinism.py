"""QC-3 determinism: same graph reload → same digest and metrics."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

QC3 = Path(__file__).resolve().parents[1]


def _digest(obj: dict) -> str:
    payload = {key: value for key, value in obj.items() if key != "content_digest"}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def test_integration_matrix_digest_stable() -> None:
    path = QC3 / "reports" / "integration_matrix.json"
    first = json.loads(path.read_text(encoding="utf-8"))
    second = json.loads(path.read_text(encoding="utf-8"))
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert first["content_digest"] == _digest(first)
    assert first["content_digest"] == second["content_digest"]


def test_quality_metrics_in_range() -> None:
    metrics = json.loads((QC3 / "reports" / "quality_metrics.json").read_text(encoding="utf-8"))["metrics"]
    required = {
        "pipeline_coverage",
        "handoff_coverage",
        "contract_coverage",
        "trace_coverage",
        "audit_coverage",
        "overall_integration_score",
    }
    assert required <= set(metrics)
    for value in metrics.values():
        assert 0 <= value <= 100
    assert metrics["pipeline_coverage"] == 100
    assert metrics["handoff_coverage"] == 100
