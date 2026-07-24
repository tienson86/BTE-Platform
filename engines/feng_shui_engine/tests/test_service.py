"""Service-level smoke for FengShuiService."""

from __future__ import annotations

from engines.feng_shui_engine import FengShuiService


def test_service_calculate_dict_shape() -> None:
    result = FengShuiService().calculate(year=1990, gender="male")
    data = result.to_dict()
    assert data["gua_number"] == 1
    assert data["gua_name"] == "Khảm"
    assert data["group"] == "Đông Tứ Trạch"
    assert data["cung_phi"] == "Khảm"
    assert data["menh_quai"] == "Khảm"
    assert data["nhom_trach"] == "Đông Tứ Trạch"
