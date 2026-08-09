"""QC-2 pipeline regression: deterministic snapshot reload, no engine run."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

QC2 = Path(__file__).resolve().parents[1]
LAYERS = ("analysis", "decision", "luck", "interpretation", "report")


def _digest(obj: dict) -> str:
    payload = {key: value for key, value in obj.items() if key != "content_digest"}
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def test_snapshot_self_hash_stable() -> None:
    report = json.loads((QC2 / "reports" / "snapshot_report.json").read_text(encoding="utf-8"))
    for layer in LAYERS:
        for path in (QC2 / "snapshots" / layer).glob("*.json"):
            first = json.loads(path.read_text(encoding="utf-8"))
            second = json.loads(path.read_text(encoding="utf-8"))
            assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
            assert first["content_digest"] == _digest(first)
            assert report["digests"][first["snapshot_id"]] == first["content_digest"]


def test_regression_report_flags() -> None:
    report = json.loads((QC2 / "reports" / "regression_report.json").read_text(encoding="utf-8"))
    assert report["snapshot_stability"] is True
    assert report["contract_stability"] is True
    assert report["trace_stability"] is True
    assert report["audit_stability"] is True
    assert report["renderer_independence"] is True
    assert report["knowledge_independence"] is True
    assert report["engine_replay"] is False
    assert report["compared_against_released_snapshots"] is False


def test_pipeline_layers_complete() -> None:
    pipeline = json.loads((QC2 / "reports" / "pipeline_validation.json").read_text(encoding="utf-8"))
    assert pipeline["pipeline"] == list(LAYERS)
    assert pipeline["scenarios_with_all_layers"] == 13
    assert pipeline["engine_wired"] is False
