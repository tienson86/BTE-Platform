"""Evidence Builder tests (N-IMP-02)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from engines.narrative_v2.evidence import (
    EvidenceBuilder,
    EvidenceValidationError,
    NarrativeEvidenceContext,
)
from engines.narrative_v2.evidence.evidence_item import STATUS_AVAILABLE, STATUS_MISSING

EVIDENCE_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_v2" / "evidence"


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_e1_e2_builder_accepts_canonical_and_returns_context(
    case_0001_canonical: dict[str, Any],
) -> None:
    context = EvidenceBuilder().build(case_0001_canonical)
    assert isinstance(context, NarrativeEvidenceContext)
    assert context.items


def test_e3_stable_evidence_ids(case_0001_canonical: dict[str, Any]) -> None:
    context = EvidenceBuilder().build(case_0001_canonical)
    for item in context.items:
        assert item.evidence_id.startswith("evidence.")


def test_e6_missing_fields_are_not_inferred() -> None:
    context = EvidenceBuilder().build({"bazi": {"day_master": "Canh"}})
    strength = context.item("evidence.strength.level")
    assert strength is not None
    assert strength.status == STATUS_MISSING
    assert strength.value is None
    hidden = context.item("evidence.bazi.year_pillar.hidden_stems")
    assert hidden is not None
    assert hidden.status == STATUS_MISSING


def test_e7_no_customer_prose_generated(case_0001_canonical: dict[str, Any]) -> None:
    context = EvidenceBuilder().build(case_0001_canonical)
    blob = " ".join(
        str(item.value)
        for item in context.items
        if item.value is not None
    )
    for marker in (
        "Bạn có nội lực tốt",
        "Bạn làm việc có hệ thống",
        "nên bổ Hỏa",
        "tình duyên tốt",
        "vận thuận lợi",
    ):
        assert marker not in blob


def test_e8_no_astrology_calculations_added() -> None:
    source = (
        EVIDENCE_DIR / "evidence_builder.py"
    ).read_text(encoding="utf-8")
    forbidden = (
        "ten_god_name(",
        "day_master_element(",
        "branch_element(",
        "stem_element(",
        "hidden_stems(",
        "calculate(",
    )
    for token in forbidden:
        assert token not in source


def test_e9_e10_no_pack05_or_portal_imports() -> None:
    forbidden = (
        "engines.narrative_engine",
        "applications.customer_portal",
        "applications.api.services.narrative_result_truth",
    )
    for path in EVIDENCE_DIR.glob("*.py"):
        imported = _imported_modules(path)
        for name in forbidden:
            assert not any(
                item == name or item.startswith(name + ".")
                for item in imported
            ), f"{path} imports {name}"


def test_e14_same_input_identical_output(case_0001_canonical: dict[str, Any]) -> None:
    first = EvidenceBuilder().build(case_0001_canonical)
    second = EvidenceBuilder().build(case_0001_canonical)
    assert first.items == second.items
    assert first.contract_gaps == second.contract_gaps


def test_case_0001_extracts_published_facts(
    case_0001_canonical: dict[str, Any],
) -> None:
    context = EvidenceBuilder().build(case_0001_canonical)
    bazi = case_0001_canonical["bazi"]
    assert context.item("evidence.bazi.day_master").value == bazi["day_master"]
    assert context.item("evidence.bazi.year_pillar.stem").value == bazi["year_pillar"]["stem"]
    assert context.item("evidence.bazi.month_pillar.branch").value == bazi["month_pillar"]["branch"]
    assert context.item("evidence.bazi.day_pillar.stem").value == bazi["day_pillar"]["stem"]
    assert context.item("evidence.bazi.hour_pillar.branch").value == bazi["hour_pillar"]["branch"]
    assert (
        context.item("evidence.strength.level").value
        == case_0001_canonical["strength"]["strength_level"]
    )
    assert (
        context.item("evidence.pattern.primary").value
        == case_0001_canonical["pattern"]["pattern"]
    )
    assert (
        context.item("evidence.useful_god.primary").value
        == case_0001_canonical["useful_god"]["useful_god"]
    )
    wood = context.item("evidence.five_elements.wood.count")
    assert wood is not None
    assert wood.status == STATUS_AVAILABLE
    visible = context.item("evidence.ten_gods.visible_labels")
    assert visible is not None
    assert visible.status == STATUS_AVAILABLE
    names = context.item("evidence.shensha.names")
    assert names is not None
    current = context.item("evidence.luck.current_cycle")
    assert current is not None
    assert current.status == STATUS_AVAILABLE


def test_negative_strength_does_not_become_meaning() -> None:
    context = EvidenceBuilder().build({"strength": {"strength_level": "strong"}})
    values = [str(item.value) for item in context.items if item.value is not None]
    assert "Bạn có nội lực tốt." not in values
    assert context.item("evidence.strength.level").value == "strong"


def test_negative_pattern_does_not_become_meaning() -> None:
    context = EvidenceBuilder().build({"pattern": {"pattern": "Chính Ấn"}})
    blob = " ".join(str(item.value) for item in context.items if item.value is not None)
    assert "Bạn làm việc có hệ thống." not in blob
    assert context.item("evidence.pattern.primary").value == "Chính Ấn"


def test_negative_useful_god_does_not_recommend() -> None:
    context = EvidenceBuilder().build({"useful_god": {"useful_god": "Hỏa"}})
    blob = " ".join(str(item.value) for item in context.items if item.value is not None)
    assert "nên bổ Hỏa." not in blob


def test_negative_shensha_does_not_mean_romance() -> None:
    context = EvidenceBuilder().build(
        {"bazi": {"shensha": ["Hồng Loan"], "shensha_matches": []}}
    )
    blob = " ".join(str(item.value) for item in context.items if item.value is not None)
    assert "tình duyên tốt." not in blob
    assert "Hồng Loan" in blob


def test_negative_luck_does_not_judge_fortune() -> None:
    context = EvidenceBuilder().build(
        {
            "luck": {
                "direction": "forward",
                "current_cycle": {"gan_zhi": "Ất Tỵ", "index": 0},
                "cycles": [{"index": 0, "gan_zhi": "Ất Tỵ"}],
            }
        }
    )
    blob = " ".join(str(item.value) for item in context.items if item.value is not None)
    assert "vận thuận lợi." not in blob


def test_e15_raw_debug_objects_are_rejected() -> None:
    with pytest.raises(EvidenceValidationError, match="debug"):
        EvidenceBuilder().build({"strength": {"strength_level": {"debug": True}}})
