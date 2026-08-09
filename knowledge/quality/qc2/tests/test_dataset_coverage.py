"""QC-2 coverage across packages and families."""
from __future__ import annotations

import json
from pathlib import Path

QC2 = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4]
PACKAGES = REPO / "knowledge" / "packages"

REQUIRED_PACKAGES = {
    "bz_01_strength_core",
    "bz_06_useful_god_foundation",
    "bz_09_luck_foundation",
    "bz_16_sentence_library_core",
    "bz_17_explanation_library_core",
    "bz_18_narrative_library_core",
    "bz_19_composition_library_core",
    "bz_20_theme_library_core",
    "bz_21_layout_library_core",
    "bz_22_widget_library_core",
    "bz_23_report_presets_core",
}


def test_coverage_matrix_covers_required_packages() -> None:
    matrix = json.loads((QC2 / "datasets" / "coverage_matrix.json").read_text(encoding="utf-8"))
    by_id = {row["package_id"]: row for row in matrix["rows"]}
    for package_id in REQUIRED_PACKAGES:
        assert by_id[package_id]["covered"] is True
        assert by_id[package_id]["scenario_count"] >= 1
    assert set(matrix["required_families"]) == {"analysis", "decision", "luck", "interpretation", "presentation"}
    assert all(row["covered"] for row in matrix["rows"])


def test_coverage_report_metrics() -> None:
    report = json.loads((QC2 / "reports" / "coverage_report.json").read_text(encoding="utf-8"))
    metrics = json.loads((QC2 / "reports" / "quality_metrics.json").read_text(encoding="utf-8"))
    assert report["scenarios"] == 13
    assert report["snapshots"] == 65
    assert report["interpretation_packages"] == 4
    assert report["presentation_packages"] == 4
    assert report["engines_replayed"] == 0
    assert metrics["metrics"]["engines"] == 0
    assert metrics["metrics"]["snapshots"] == 100
    assert (PACKAGES / "sentence_library" / "core" / "PACKAGE.json").exists()
