"""Intake specification and template tests."""

from __future__ import annotations

from .helpers import REQUIRED_DOCS, ROOT, TEMPLATES, load_json


def test_required_docs_exist() -> None:
    missing = [n for n in REQUIRED_DOCS if not (ROOT / n).is_file()]
    assert missing == []


def test_intake_template_required_fields() -> None:
    data = load_json(TEMPLATES / "intake_record.json")
    for field in (
        "acquisition_id",
        "source_type",
        "source_reference",
        "received_at",
        "consent_status",
        "privacy_status",
        "birth_date",
        "birth_time",
        "birth_place",
        "timezone",
        "gender",
        "calendar_type",
        "data_precision",
        "verification_status",
        "case_status",
    ):
        assert field in data
    assert data["cal_id"] is None
    assert data["case_status"] == "intake_pending"


def test_intake_spec_documents_cal_rule() -> None:
    text = (ROOT / "INTAKE_SPECIFICATION.md").read_text(encoding="utf-8")
    assert "cal_id" in text
    assert "eligibility" in text.lower()
