"""BZ-ID-01 Sprint 01: FourPillarIdentity uses the existing Hạ Nguyên lookup."""

from __future__ import annotations

import inspect

from applications.api.models.analysis_result import AnalysisMeta, AnalysisResult
from applications.api.services.bazi_truth import build_bazi_view
from engines.bazi_engine.engine import BaziEngine
from engines.date_selection.identity import pillar_contract
from engines.identity import canonical_identity_from_bazi, pillar_identity_from_ganzhi
from engines.identity import four_pillars as four_pillars_module

ELEMENTS = {"Mộc", "Hỏa", "Thổ", "Kim", "Thủy"}
FULL_NAP_AM_NAMES = ("Thiên Hà Thủy", "Tuyền Trung Thủy", "Lộ Bàng Thổ", "Sơn Hạ Hỏa")
PILLAR_KEYS = ("year", "month", "day", "hour")
LOOKUP_KEYS = ("can_chi", "nayin_element", "cung_phi")
CELL_KEYS = ("stem", "branch", "can_chi", "nayin_element", "cung_phi", "pillar_type")
PILLAR_TYPES = {"year": "Year", "month": "Month", "day": "Day", "hour": "Hour"}


def test_lookup_is_pillar_contract_not_a_second_table() -> None:
    source = inspect.getsource(four_pillars_module)
    assert "pillar_contract" in source
    assert "DictReader" not in source
    assert "load_nap_am" not in source
    assert "load_ha_nguyen_cung" not in source
    assert "01_nap_am.csv" not in source
    assert "ha_nguyen_cung.csv" not in source


def test_binh_ngo_element_only_not_full_nap_am_name() -> None:
    pillar = pillar_identity_from_ganzhi("Bính Ngọ")
    expected = pillar_contract("Bính Ngọ")
    assert {key: pillar.to_dict()[key] for key in LOOKUP_KEYS} == expected
    assert pillar.can_chi == "Bính Ngọ"
    assert pillar.stem == "Bính"
    assert pillar.branch == "Ngọ"
    assert pillar.nayin_element == "Thủy"
    assert pillar.cung_phi == "Khảm"
    assert pillar.nayin_element not in FULL_NAP_AM_NAMES


def test_four_pillars_all_cells_from_bazi() -> None:
    chart = BaziEngine().build(2026, 8, 28, 12, 0)
    identity = canonical_identity_from_bazi(chart)
    payload = identity.to_dict()
    four = payload["four_pillars"]
    assert set(four) == set(PILLAR_KEYS)
    for key in PILLAR_KEYS:
        cell = four[key]
        assert set(cell) == set(CELL_KEYS)
        assert cell["can_chi"]
        assert cell["stem"]
        assert cell["branch"]
        assert cell["pillar_type"] == PILLAR_TYPES[key]
        assert cell["nayin_element"] in ELEMENTS
        assert cell["cung_phi"]
        assert cell["nayin_element"] not in FULL_NAP_AM_NAMES
        for name in FULL_NAP_AM_NAMES:
            assert name not in cell["nayin_element"]
        assert {item: cell[item] for item in LOOKUP_KEYS} == pillar_contract(cell["can_chi"])
    assert four["year"]["can_chi"] == "Bính Ngọ"
    assert four["month"]["can_chi"] == "Bính Thân"
    assert four["year"]["nayin_element"] == "Thủy"
    assert four["month"]["nayin_element"] == "Hỏa"
    assert four["year"]["cung_phi"] == "Khảm"
    assert four["month"]["cung_phi"] == "Khôn"


def test_analysis_result_exposes_identity_four_pillars() -> None:
    chart = BaziEngine().build(1987, 1, 21, 4, 30, gender="male")
    view = build_bazi_view(chart)
    analysis = AnalysisResult(
        bazi=view,
        identity=canonical_identity_from_bazi(view),
        meta=AnalysisMeta(contract_version="1.0"),
    )
    payload = analysis.identity_dict()
    four = payload["four_pillars"]
    for key in PILLAR_KEYS:
        cell = four[key]
        assert cell["can_chi"]
        assert cell["nayin_element"] in ELEMENTS
        assert cell["cung_phi"]
        assert cell["pillar_type"] == PILLAR_TYPES[key]
        assert {item: cell[item] for item in LOOKUP_KEYS} == pillar_contract(cell["can_chi"])
    assert four["year"]["can_chi"] == "Bính Dần"
    assert four["month"]["can_chi"] == "Tân Sửu"
    assert four["day"]["can_chi"] == "Canh Ngọ"
    assert four["hour"]["can_chi"] == "Mậu Dần"
