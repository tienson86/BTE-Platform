"""HK-R1H: same-element static sibling is not customer Hỷ; Dụng reason is published."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from engines.useful_god_engine.presentation import (
    HY_ROLE_STATIC_OTHER,
    HY_ROLE_STATIC_SAME_ELEMENT,
    HY_ROLE_SUPPORTED_INDEPENDENT,
    INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
    classify_hy_role,
)
from engines.useful_god_engine.reasoning import ARCHETYPE_TIET


def _analyze(**kwargs):
    return OrchestratorService().analyze(**kwargs)


def test_same_element_output_sibling_is_static_not_independent() -> None:
    status = classify_hy_role(
        {"element": "Thủy", "stem": "Nhâm", "ten_god": "Thực Thần"},
        {"element": "Thủy", "stem": "Quý", "ten_god": "Thương Quan"},
        winning_rule_id="str_004",
    )
    assert status == HY_ROLE_STATIC_SAME_ELEMENT


def test_peer_on_weak_path_is_independent() -> None:
    status = classify_hy_role(
        {"element": "Kim", "stem": "Tân", "ten_god": "Chính Ấn"},
        {"element": "Thủy", "stem": "Nhâm", "ten_god": "Tỷ Kiên"},
        winning_rule_id="str_001",
    )
    assert status == HY_ROLE_SUPPORTED_INDEPENDENT


def test_dung_customer_hy_is_neutral_and_reason_is_visible() -> None:
    payload = _analyze(
        year=1985,
        month=9,
        day=18,
        hour=8,
        minute=0,
        gender="male",
        timezone="Asia/Bangkok",
    )
    useful = payload["useful_god"]
    assert useful["useful_display"] == "Thủy · Nhâm · Thực Thần"
    assert useful["favorable_gods"] == ["Thực Thần", "Thương Quan"]
    assert useful["canonical_favorable_display"].startswith("Thủy · Nhâm · Thực Thần")
    assert useful["favorable_display"] == INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    assert useful["hy_role_status"] == HY_ROLE_STATIC_SAME_ELEMENT
    assert "Quý" not in useful["favorable_display"]
    assert "Thủy" not in useful["favorable_display"]
    reason = useful["short_reason"]
    assert useful["reason_archetype"] == ARCHETYPE_TIET
    assert "str_004" not in reason
    assert "Canh" in reason
    assert "thân vượng" in reason
    assert "Tiết" in reason
    assert "Kim sinh Thủy" in reason
    assert "Nhâm" in reason
    assert "Thực Thần" in reason
    assert "mô hình cân bằng V1.0" in reason
    assert useful["unfavorable_display"].startswith("Kim · Canh · Tỷ Kiên")
    assert useful["climate_display"].startswith("Hỏa")


def test_huyen_same_element_output_sibling_is_neutral() -> None:
    payload = _analyze(
        year=1987,
        month=9,
        day=7,
        hour=2,
        minute=0,
        gender="female",
        timezone="Asia/Bangkok",
    )
    useful = payload["useful_god"]
    assert useful["useful_display"] == "Kim · Tân · Thực Thần"
    assert useful["favorable_gods"] == ["Thực Thần", "Thương Quan"]
    assert useful["favorable_display"] == INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    assert useful["hy_role_status"] == HY_ROLE_STATIC_SAME_ELEMENT
    assert "Canh" not in useful["favorable_display"]
    assert "Thổ sinh Kim" in useful["short_reason"]


def test_truong_keeps_peer_drops_same_element_resource_sibling() -> None:
    payload = _analyze(
        year=1989,
        month=7,
        day=21,
        hour=15,
        minute=45,
        gender="male",
        timezone="Asia/Bangkok",
    )
    useful = payload["useful_god"]
    assert useful["useful_display"] == "Kim · Tân · Chính Ấn"
    assert useful["favorable_gods"] == ["Chính Ấn", "Thiên Ấn", "Tỷ Kiên"]
    assert useful["hy_role_status"] == HY_ROLE_SUPPORTED_INDEPENDENT
    assert useful["favorable_display"] == "Thủy · Nhâm · Tỷ Kiên"
    assert "Thiên Ấn" not in useful["favorable_display"]
    assert "Canh" not in useful["favorable_display"]
    assert "Kim sinh Thủy" in useful["short_reason"]


def test_tuyen_output_leftover_stays_neutral() -> None:
    payload = _analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    useful = payload["useful_god"]
    assert useful["useful_display"] == "Mộc · Ất · Chính Quan"
    assert useful["favorable_gods"] == ["Chính Quan", "Thực Thần"]
    assert useful["favorable_display"] == INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    assert useful["hy_role_status"] == HY_ROLE_STATIC_OTHER
    assert "Mộc khắc Thổ" in useful["short_reason"]
    assert "str_003" not in useful["short_reason"]
