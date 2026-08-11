"""Unknown / missing data policy tests."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_unknown_policy_doc_forbids_conversions() -> None:
    text = (ROOT / "UNKNOWN_AND_MISSING_DATA_POLICY.md").read_text(encoding="utf-8")
    assert "unknown -> neutral" in text
    assert "not_available -> false" in text
    assert "missing -> zero" in text


def test_unknown_example_preserves_unknown() -> None:
    import json

    data = json.loads((ROOT / "examples" / "unknown_output.json").read_text(encoding="utf-8"))
    assert data["score_reference"]["current_v1_band"] == "unknown"
    assert data["score_reference"]["saturation_detected"] == "unknown"
    assert data["completeness"]["overall"] == "unknown"
    assert data["evidence"]["seasonal"] is None
