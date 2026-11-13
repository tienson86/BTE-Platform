import pytest
from applications.api.services import bazi_analysis_contract as contract
from applications.api.services.day_pillar_editorial import day_personality

KEYS = ("health", "wealth", "career", "marriage", "children", "parents", "siblings", "ancestry", "property")

@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("payload", [{}, {"bazi": {}}, {"bazi": {"day_master": "unknown"}}])
def test_missing_chart_never_reuses_legacy_prose(key, payload, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("legacy or unsupported editorial path used")
    monkeypatch.setattr(contract, "life_domain_prose", forbidden)
    monkeypatch.setattr(contract, "customer_wealth_paragraphs", forbidden)
    lines = contract._life_domain_detail_paragraphs(key, payload, "Legacy inference that must not leak")
    assert len(lines) == 1
    assert lines[0].startswith("Chưa đủ dữ liệu")
    assert "Legacy inference" not in lines[0]

@pytest.mark.parametrize("key", KEYS)
def test_no_approved_copy_uses_clear_missing_notice(key, monkeypatch):
    monkeypatch.setattr(contract, "life_domain_prose", lambda *_: [])
    monkeypatch.setattr(contract, "customer_wealth_paragraphs", lambda *_: [])
    lines = contract._life_domain_detail_paragraphs(key, {"bazi": {"day_master": "Giáp"}}, "old claim")
    assert lines[0].startswith("Chưa đủ dữ liệu")

@pytest.mark.parametrize("god", ["Chính Tài", "Thiên Tài", "Chính Ấn", "Thiên Ấn", "Thực Thần", "Thương Quan", "Tỷ Kiên", "Kiếp Tài"])
def test_other_hidden_day_role_families_get_personal_synthesis(god):
    payload={"bazi": {"day_master": "Giáp", "day_pillar": {"stem": "Giáp", "branch": "Tý"}}, "ten_gods": {"hidden": [{"pillar": "day", "branch": "Tý", "stem": "Quý", "ten_god": god}]}}
    lines=day_personality(payload)
    assert len(lines)==3
    assert god in lines[1]
    assert "Canh Ngọ" not in " ".join(lines)


def test_canonical_subtitle_has_no_numbered_editorial_placeholder():
    assert contract._life_domain_subtitle("Một câu không có từ khóa nhận diện.", 3) == "Điều đáng suy ngẫm"

def test_unknown_pattern_stays_customer_facing():
    from applications.api.services.core_reading_editorial import pattern_useful_paragraphs
    lines=pattern_useful_paragraphs({"pattern": {"cach_cuc": "Cấu trúc khác"}})
    assert lines and "Với bạn" in lines[0]
    assert "Khi đọc cần" not in lines[0]

def test_strong_day_has_no_editor_instruction():
    from applications.api.services.core_reading_editorial import day_master_paragraphs
    lines=day_master_paragraphs({"bazi": {"day_master": "Giáp"}, "strength": {"strength_level": "strong"}})
    assert "hướng luận" not in " ".join(lines)
