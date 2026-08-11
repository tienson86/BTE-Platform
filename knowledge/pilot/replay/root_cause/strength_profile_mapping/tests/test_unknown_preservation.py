"""Unknown / not_available preservation tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def test_seasonal_strength_state_not_inferred() -> None:
    for path in RESULTS.glob("*.json"):
        seasonal = json.loads(path.read_text(encoding="utf-8"))["profile"]["seasonal_state"]
        assert seasonal["seasonal_strength_state"] == "unknown"


def test_root_loci_unknown() -> None:
    for path in RESULTS.glob("*.json"):
        rooting = json.loads(path.read_text(encoding="utf-8"))["profile"]["rooting_state"]
        assert rooting["day_branch_root"] == "unknown"
        assert rooting["month_branch_root"] == "unknown"
        assert rooting["root_distribution"] == []


def test_structural_unavailable_marked() -> None:
    for path in RESULTS.glob("SYN-STR-*.json"):
        structural = json.loads(path.read_text(encoding="utf-8"))["profile"]["structural_state"]
        assert structural["clash"]["status"] == "not_available"
        assert structural["follow_pattern"]["status"] == "not_available"


def test_no_missing_to_neutral_conversion_for_absent_support() -> None:
    # SYN-STR-000001 has support_type null and support bucket 0 — summary should not invent strong/weak labels.
    data = json.loads((RESULTS / "SYN-STR-000001.json").read_text(encoding="utf-8"))
    support = data["profile"]["support_state"]
    assert support["summary"] == "unknown"
    assert support["bucket_total"] == 0.0
