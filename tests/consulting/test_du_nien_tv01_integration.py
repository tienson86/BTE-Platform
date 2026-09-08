"""TV-01 consumes the canonical Du Niên matrix. No local override."""

from __future__ import annotations

from consulting.canon.du_nien import lookup
from consulting.marriage.models.enums import CanonicalGender, FiveElement, PersonSide
from consulting.marriage.report.cung_phi import palace_relation, relation_meaning
from tests.consulting.decision_fixtures import build_test_decision, make_snapshot
from tests.consulting.narrative_fixtures import compose_report_bundle


from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot


def _pair(cung_a: str, cung_b: str) -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot]:
    """Snapshots with explicit Canonical Cung Phi. No palace recalculation."""
    snapshot_a = make_snapshot(
        analysis_id="MC-DUNIEN-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        cung_phi=cung_a,
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-DUNIEN-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        cung_phi=cung_b,
    )
    return snapshot_a, snapshot_b


def test_tv01_adapter_reads_canonical_khon_kham() -> None:
    """TV-01 palace_relation is the canonical lookup, not a local exception."""
    canonical = lookup("Khôn", "Khảm")
    assert canonical is not None
    assert palace_relation("Khôn", "Khảm") == canonical.relationship_label
    assert palace_relation("Khôn", "Khảm") == "Tuyệt Mệnh"
    assert palace_relation("Khôn", "Khảm") != "Ngũ Quỷ"
    assert relation_meaning("Tuyệt Mệnh") == canonical.customer_summary


def test_tv01_report_publishes_canonical_tuyet_menh() -> None:
    """Report Cung Phi block shows Tuyệt Mệnh for Khôn → Khảm."""
    decision = build_test_decision(*_pair("Khôn", "Khảm"))
    _, _, _, report = compose_report_bundle(decision)
    section = next(item for item in report.sections if item.section_id == "cung_phi")
    relation = next(block for block in section.blocks if block.block_id == "cung-relation")
    meaning = next(block for block in section.blocks if block.block_id == "cung-meaning")
    limit = next(block for block in section.blocks if block.block_id == "cung-limit")
    assert relation.body == "Tuyệt Mệnh"
    assert "Ngũ Quỷ" not in (meaning.body or "")
    assert "ly hôn" not in (meaning.body or "").lower()
    assert "bằng chứng phụ" in (limit.body or "")


def test_tv01_other_pairs_follow_canonical_matrix() -> None:
    """Representative pairs stay aligned with the canonical source."""
    cases = (
        ("Khôn", "Cấn", "Sinh Khí"),
        ("Khảm", "Khôn", "Tuyệt Mệnh"),
        ("Khảm", "Tốn", "Sinh Khí"),
        ("Khôn", "Chấn", "Ngũ Quỷ"),
    )
    for source, target, label in cases:
        assert palace_relation(source, target) == lookup(source, target).relationship_label
        assert palace_relation(source, target) == label
