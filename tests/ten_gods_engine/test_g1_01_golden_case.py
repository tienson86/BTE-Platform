"""G1-01 Golden CASE: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần, Day Master Canh."""

from __future__ import annotations

from applications.api.services.ten_gods_truth import shape_ten_gods_payload
from engines.ten_gods_engine import run_case_0001

VISIBLE_EXPECTED = (
    ("year", "Bính", "Thất Sát"),
    ("month", "Tân", "Kiếp Tài"),
    ("day", "Canh", "Nhật Chủ"),
    ("hour", "Mậu", "Thiên Ấn"),
)

HIDDEN_EXPECTED = (
    ("year", "Dần", "Giáp", "Thiên Tài"),
    ("year", "Dần", "Bính", "Thất Sát"),
    ("year", "Dần", "Mậu", "Thiên Ấn"),
    ("month", "Sửu", "Kỷ", "Chính Ấn"),
    ("month", "Sửu", "Quý", "Thương Quan"),
    ("month", "Sửu", "Tân", "Kiếp Tài"),
    ("day", "Ngọ", "Đinh", "Chính Quan"),
    ("day", "Ngọ", "Kỷ", "Chính Ấn"),
    ("hour", "Dần", "Giáp", "Thiên Tài"),
    ("hour", "Dần", "Bính", "Thất Sát"),
    ("hour", "Dần", "Mậu", "Thiên Ấn"),
)


def test_golden_case_visible_and_hidden() -> None:
    """CASE-0001 visible 4/4 and hidden 11/11 with provenance fields."""
    result = run_case_0001()
    visible = [(item.pillar, item.stem, item.ten_god) for item in result.visible]
    hidden = [
        (item.pillar, item.branch, item.hidden_stem, item.ten_god)
        for item in result.hidden
    ]
    assert visible == list(VISIBLE_EXPECTED)
    assert hidden == list(HIDDEN_EXPECTED)
    assert all(item.element for item in result.visible)
    assert all(item.element for item in result.hidden)


def test_public_payload_keeps_hidden_ten_gods() -> None:
    """Public adapter copies mapped hidden Ten Gods, not tàng-can names only."""
    payload = shape_ten_gods_payload(run_case_0001())
    hidden_stems = {item["hidden_stem"] for item in payload["hidden"]}
    hidden_gods = [item["ten_god"] for item in payload["hidden"]]
    assert len(payload["visible"]) == 4
    assert len(payload["hidden"]) == 11
    assert hidden_stems == {"Giáp", "Bính", "Mậu", "Kỷ", "Quý", "Tân", "Đinh"}
    assert "Thiên Tài" in hidden_gods
    assert "Chính Quan" in hidden_gods
    assert payload["hidden"] != payload["visible"]
    assert all(item.get("pillar") for item in payload["hidden"])
    assert all(item.get("branch") for item in payload["hidden"])
    assert all(item.get("visibility") == "hidden" for item in payload["hidden"])
    assert all(item.get("display") for item in payload["hidden"])
    assert payload["note"] == "Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ."
    assert payload["visible_labels"] == [
        "Thất Sát",
        "Kiếp Tài",
        "Nhật Chủ",
        "Thiên Ấn",
    ]
