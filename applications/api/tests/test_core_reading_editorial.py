"""New customer copy is gated by published chart facts."""

from applications.api.services.core_reading_editorial import (
    _catalog,
    day_master_paragraphs,
    pattern_useful_paragraphs,
    shen_sha_paragraphs,
)
from applications.api.services.orchestrator import OrchestratorService


def test_catalog_covers_five_elements_strength_levels_and_patterns() -> None:
    catalog = _catalog()
    assert len(catalog["day_master"]) == len(catalog["strength"]) == len(catalog["useful"]) == 5
    assert len(catalog["pattern"]) == 10


def test_case_0001_selects_fire_control_and_combines_day_de_stars() -> None:
    payload = OrchestratorService().analyze(
        year=1987, month=1, day=21, hour=4, minute=31,
        gender="male", timezone="Asia/Bangkok",
    )
    day = day_master_paragraphs(payload)
    pattern = pattern_useful_paragraphs(payload)
    stars = shen_sha_paragraphs(payload)
    assert "Canh thuộc Dương Kim" in day[0]
    assert "Thiên Can của trụ ngày" in day[0]
    assert any("Mệnh cục Chính Ấn" in item for item in pattern)
    assert any("Hỏa chế Kim" in item and "Đinh Hỏa" in item for item in pattern)
    assert any("Bính Hỏa" in item and "Hỷ thần" in item for item in pattern)
    assert any("Thiên Đức và Nguyệt Đức cùng hiện" in item for item in stars)
    assert len(stars) == 3
    assert not any("engine" in item.lower() for item in day + pattern + stars)


def test_missing_useful_god_does_not_invent_an_element_or_star() -> None:
    payload = {"bazi": {"day_master": "Ất", "day_master_element": "Mộc"},
               "strength": {"strength_level": "weak"},
               "pattern": {}, "useful_god": {}, "bazi_missing_stars": True}
    assert len(day_master_paragraphs(payload)) == 2
    assert pattern_useful_paragraphs(payload) == []
    assert shen_sha_paragraphs(payload) == []
