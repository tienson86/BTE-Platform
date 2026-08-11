"""Required/optional/reserved classification tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "required_optional_reserved.json"


def test_classification_counts() -> None:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    counts = data["counts"]
    assert counts["required"] > counts["optional"]
    assert counts["not_supported"] >= 2
    assert any(f["field"].startswith("taxonomy") for f in data["fields"] if f["class"] == "not_supported")


def test_p0_root_and_hidden_pressure_required() -> None:
    data = json.loads(REPORT.read_text(encoding="utf-8"))
    by_field = {f["field"]: f for f in data["fields"]}
    assert by_field["root.root_id_loci"]["class"] == "required"
    assert by_field["root.root_id_loci"]["priority"] == "P0"
    assert by_field["pressure.sitting_hidden"]["class"] == "required"
    assert by_field["structural.clash"]["class"] == "required"
