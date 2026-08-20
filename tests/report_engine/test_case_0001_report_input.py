"""CASE-0001 ReportInputV1 snapshot integration tests."""

from __future__ import annotations

import json
from pathlib import Path

from engines.report_engine.adapters.report_input_v1_adapter import ReportInputV1Adapter
from engines.report_engine.adapters.wp6_assembly_bridge import build_report_model_from_input
from tests.report_engine.case_0001_runtime import (
    CASE_0001_CANONICAL,
    build_case_0001_source,
)

_GOLDEN_DIR = (
    Path(__file__).resolve().parents[1]
    / "golden_dataset"
    / "report_v1"
    / "CASE-0001"
)
_EXPECTED_PATH = _GOLDEN_DIR / "expected_report_input.json"


def _normalize_personality_content(content: str) -> str:
    """Stabilize ten-god ordering inside personality section text."""
    marker = "thập thần nổi:"
    lowered = content.lower()
    if marker not in lowered:
        return content
    index = lowered.index(marker)
    before = content[: index + len(marker)]
    after = content[index + len(marker) :]
    names = [part.strip().rstrip(".") for part in after.split(",") if part.strip()]
    names = sorted(name for name in names if name)
    return f"{before} {', '.join(names)}."


def _normalize_snapshot(payload: dict) -> dict:
    """Drop volatile timestamp and normalize known ordering variance."""
    normalized = json.loads(json.dumps(payload, sort_keys=True, ensure_ascii=False))
    metadata = normalized.get("metadata") or {}
    metadata.pop("generated_at", None)
    normalized["metadata"] = metadata
    interpretation = normalized.get("interpretation") or {}
    sections = interpretation.get("sections") or []
    for section in sections:
        if section.get("id") == "personality":
            section["content"] = _normalize_personality_content(
                str(section.get("content") or "")
            )
    interpretation["sections"] = sorted(
        sections,
        key=lambda item: str(item.get("id") or ""),
    )
    normalized["interpretation"] = interpretation
    luck = normalized.get("luck_cycles") or {}
    for key in (
        "current_gan_zhi",
        "current_year_start",
        "current_year_end",
        "current_age_start",
        "current_age_end",
    ):
        luck.pop(key, None)
    normalized["luck_cycles"] = luck
    return normalized


def test_case_0001_pillars_match_canonical() -> None:
    """Runtime pillars match CASE-0001 validation assertions."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    pillars = report_input.pillars
    expected = CASE_0001_CANONICAL["expected_pillars"]
    assert f"{pillars.year.stem} {pillars.year.branch}" == expected["year"]
    assert f"{pillars.month.stem} {pillars.month.branch}" == expected["month"]
    assert f"{pillars.day.stem} {pillars.day.branch}" == expected["day"]
    assert f"{pillars.hour.stem} {pillars.hour.branch}" == expected["hour"]


def test_case_0001_report_input_snapshot() -> None:
    """Pipeline → adapter → ReportInputV1 matches golden snapshot except UG-R2 Overall."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    actual = _normalize_snapshot(report_input.to_dict())
    assert _EXPECTED_PATH.is_file(), f"missing snapshot: {_EXPECTED_PATH}"
    expected = _normalize_snapshot(
        json.loads(_EXPECTED_PATH.read_text(encoding="utf-8"))
    )
    actual_useful = actual.pop("useful_god")
    expected.pop("useful_god")
    actual.pop("interpretation")
    expected.pop("interpretation")
    assert actual == expected
    assert actual_useful["winning_rule_id"] == "str_003"
    assert actual_useful["winning_rule_group"] == "strength"
    assert actual_useful["useful_god"] == "Chính Quan"
    assert actual_useful["useful_display"] == "Hỏa · Đinh · Chính Quan"


def test_case_0001_wp6_assembly_compatibility() -> None:
    """ReportInputV1 can be fed into WP6 ReportBuilder without exception."""
    source = build_case_0001_source()
    report_input = ReportInputV1Adapter().build(source)
    model = build_report_model_from_input(report_input)
    assert model.sections
