"""Unit tests for ReportInputV1 contract."""

from __future__ import annotations

import json

from engines.report_engine.contracts.report_input_v1 import (
    REPORT_INPUT_VERSION,
    ReportInputV1,
    ReportInterpretationSectionV1,
    ReportInterpretationV1,
    ReportMetadataV1,
    ReportProfileV1,
    missing_data_message,
)


def test_report_input_v1_construction_defaults() -> None:
    """ReportInputV1 can be constructed with defaults."""
    report_input = ReportInputV1()
    assert report_input.metadata.report_version == REPORT_INPUT_VERSION
    assert report_input.profile.timezone == "Asia/Bangkok"
    assert report_input.interpretation.sections == []


def test_report_input_v1_optional_fields() -> None:
    """Optional nested fields remain None-safe in serialization."""
    report_input = ReportInputV1(
        profile=ReportProfileV1(full_name="Nguyễn Tiến Sơn"),
        interpretation=ReportInterpretationV1(
            sections=[
                ReportInterpretationSectionV1(
                    id="overview",
                    title="Tổng quan",
                    content="Nội dung thử.",
                )
            ],
            confidence=0.8,
        ),
    )
    payload = report_input.to_dict()
    assert payload["profile"]["full_name"] == "Nguyễn Tiến Sơn"
    assert payload["interpretation"]["sections"][0]["id"] == "overview"
    assert payload["interpretation"]["confidence"] == 0.8


def test_report_input_v1_serialization_deterministic() -> None:
    """to_dict output is stable across repeated calls."""
    report_input = ReportInputV1(
        metadata=ReportMetadataV1(
            case_id="CASE-0001",
            generated_at="2026-08-12T10:00:00Z",
            engine_version="1.0.0",
        ),
        profile=ReportProfileV1(full_name="Test"),
    )
    first = json.dumps(report_input.to_dict(), sort_keys=True, ensure_ascii=False)
    second = json.dumps(report_input.to_dict(), sort_keys=True, ensure_ascii=False)
    assert first == second


def test_missing_data_message_vietnamese() -> None:
    """Fallback message is neutral Vietnamese."""
    assert "Chưa đủ dữ liệu" in missing_data_message()
