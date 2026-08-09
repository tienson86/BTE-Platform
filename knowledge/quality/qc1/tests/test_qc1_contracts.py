"""QC-1 contract tests. Read-only."""
from __future__ import annotations

import json
from pathlib import Path

REPORTS = Path(__file__).resolve().parents[1] / "reports"


def test_published_output_names_unique() -> None:
    report = json.loads((REPORTS / "contract_graph.json").read_text(encoding="utf-8"))
    assert report["duplicate_contracts"] == {}


def test_contract_graph_serialization() -> None:
    payload = json.loads((REPORTS / "contract_graph.json").read_text(encoding="utf-8"))
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    loaded = json.loads(encoded)
    assert loaded["duplicate_contracts"] == {}
    assert "producers" in loaded
    assert "consumers" in loaded


def test_publication_matrix_covers_all_packages() -> None:
    matrix = json.loads((REPORTS / "publication_matrix.json").read_text(encoding="utf-8"))
    assert len(matrix["rows"]) == 23
    ids = {row["package_id"] for row in matrix["rows"]}
    assert len(ids) == 23
