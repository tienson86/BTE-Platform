"""QC-3 handoff tests. Read-only over pipeline index and QC-3 reports."""
from __future__ import annotations

import json
from pathlib import Path

QC3 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
INDEX = REPO / "knowledge" / "releases" / "v1.0" / "PIPELINE_INDEX.json"
ORDER = ["AX-2", "AX-3", "AX-4", "IX-1", "RX-1"]


def test_handoff_edges_match_canonical_order() -> None:
    matrix = json.loads((QC3 / "reports" / "integration_matrix.json").read_text(encoding="utf-8"))
    handoff = json.loads((QC3 / "reports" / "handoff_matrix.json").read_text(encoding="utf-8"))
    assert matrix["order"] == ORDER
    producers = [edge["producer"] for edge in matrix["edges"]]
    consumers = [edge["consumer"] for edge in matrix["edges"]]
    assert producers == ORDER[:-1]
    assert consumers == ORDER[1:]
    assert len(matrix["edges"]) == 4
    assert len({edge["edge_id"] for edge in matrix["edges"]}) == 4
    assert all(item["missing_contracts"] == [] for item in handoff["edges"])
    assert handoff["missing_contract_count"] == 0


def test_pipeline_ids_match_release_index() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    status = json.loads((QC3 / "reports" / "pipeline_status.json").read_text(encoding="utf-8"))
    by_id = {item["pipeline_id"]: item for item in index["pipelines"]}
    for row in status["rows"]:
        listed = by_id[row["pipeline_id"]]
        assert listed["version"] == row["version"]
        assert listed["engine"] == row["engine"]
        assert row["index_match"] is True
    assert status["engine_executed"] is False
