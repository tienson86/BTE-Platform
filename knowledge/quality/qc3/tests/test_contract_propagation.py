"""QC-3 contract propagation: required contracts ⊆ producer outputs."""
from __future__ import annotations

import json
from pathlib import Path

QC3 = Path(__file__).resolve().parents[1]


def test_required_contracts_are_published_by_producer() -> None:
    matrix = json.loads((QC3 / "reports" / "integration_matrix.json").read_text(encoding="utf-8"))
    flow = json.loads((QC3 / "reports" / "contract_flow.json").read_text(encoding="utf-8"))
    pipelines = {item["sprint_id"]: item for item in matrix["pipelines"]}
    for edge in matrix["edges"]:
        published = set(pipelines[edge["producer"]]["published_outputs"])
        assert set(edge["contracts"]) <= published
    assert len(flow["flow"]) == 4
    assert flow["flow"][0]["from"] == "AX-2"
    assert flow["flow"][-1]["to"] == "RX-1"


def test_version_pins_are_compatible() -> None:
    flow = json.loads((QC3 / "reports" / "contract_flow.json").read_text(encoding="utf-8"))
    expected = {
        "AX-2": "2.0.0",
        "AX-3": "1.0.0",
        "AX-4": "1.0.0",
        "IX-1": "1.0.0",
        "RX-1": "1.0.0",
    }
    matrix = json.loads((QC3 / "reports" / "integration_matrix.json").read_text(encoding="utf-8"))
    versions = {item["sprint_id"]: item["version"] for item in matrix["pipelines"]}
    assert versions == expected
    for hop in flow["flow"]:
        for pipeline_id, constraint in hop["version_constraint"].items():
            assert constraint.startswith("==")
            sprint = next(item["sprint_id"] for item in matrix["pipelines"] if item["pipeline_id"] == pipeline_id)
            assert versions[sprint] == constraint[2:]
