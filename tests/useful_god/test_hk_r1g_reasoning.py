"""HK-R1G: Dụng reasoning chain + Hỷ independent-role gate."""

from __future__ import annotations

from applications.api.services.orchestrator import OrchestratorService
from engines.useful_god_engine.presentation import (
    HY_ROLE_STATIC,
    HY_ROLE_STATIC_SAME_ELEMENT,
    HY_ROLE_SUPPORTED_INDEPENDENT,
    INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY,
)
from engines.useful_god_engine.reasoning import (
    ARCHETYPE_BALANCED_WEALTH,
    ARCHETYPE_CHE,
    ARCHETYPE_SINH_TRO,
    ARCHETYPE_TIET,
)


def _analyze(**kwargs):
    return OrchestratorService().analyze(**kwargs)


def test_dung_reason_is_tiet_chain_without_rule_id() -> None:
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
    assert useful["reason_archetype"] == ARCHETYPE_TIET
    reason = useful["short_reason"]
    assert "str_004" not in reason
    assert "Canh" in reason
    assert "thân vượng" in reason
    assert "Tiết" in reason
    assert "Kim sinh Thủy" in reason
    assert "Nhâm" in reason
    assert "Thực Thần" in reason
    assert "mô hình cân bằng V1.0" in reason
    assert useful["favorable_gods"] == ["Thực Thần", "Thương Quan"]
    assert useful["favorable_display"] == INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    assert useful["hy_role_status"] == HY_ROLE_STATIC_SAME_ELEMENT
    assert "Nhâm" not in useful["favorable_display"]
    assert "Quý" not in useful["favorable_display"]
    assert useful["unfavorable_display"].startswith("Kim · Canh · Tỷ Kiên")
    assert useful["climate_display"].startswith("Hỏa")


def test_tuyen_reason_is_che_and_static_hy_is_insufficient() -> None:
    payload = _analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    useful = payload["useful_god"]
    assert useful["useful_display"] == "Mộc · Ất · Chính Quan"
    assert useful["reason_archetype"] == ARCHETYPE_CHE
    reason = useful["short_reason"]
    assert "str_003" not in reason
    assert "Mậu" in reason
    assert "Chế" in reason
    assert "Mộc khắc Thổ" in reason
    assert "Ất" in reason
    assert useful["favorable_gods"] == ["Chính Quan", "Thực Thần"]
    assert useful["favorable_display"] == INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    assert useful["hy_role_status"] == HY_ROLE_STATIC


def test_truong_reason_is_sinh_tro() -> None:
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
    assert useful["reason_archetype"] == ARCHETYPE_SINH_TRO
    reason = useful["short_reason"]
    assert "thân nhược" in reason
    assert "Kim sinh Thủy" in reason
    assert "Tân" in reason
    assert "Chính Ấn" in reason
    assert useful["hy_role_status"] == HY_ROLE_SUPPORTED_INDEPENDENT
    assert "Chính Ấn" not in useful["favorable_display"]
    assert useful["favorable_display"] == "Thủy · Nhâm · Tỷ Kiên"
    assert "Thiên Ấn" not in useful["favorable_display"]


def test_balanced_wealth_reason_is_honest() -> None:
    payload = _analyze(
        year=1996,
        month=11,
        day=29,
        hour=17,
        minute=20,
        gender="male",
        timezone="Asia/Bangkok",
    )
    useful = payload["useful_god"]
    assert useful["winning_rule_id"] == "str_005"
    assert useful["reason_archetype"] == ARCHETYPE_BALANCED_WEALTH
    assert "không đối chiếu sâu toàn cục" in useful["short_reason"]
    assert useful["favorable_gods"] == ["Chính Tài", "Thực Thần"]
    assert useful["favorable_display"] == INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
