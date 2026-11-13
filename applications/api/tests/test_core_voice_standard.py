"""Chart-grounded voice regressions; no changes to calculation contracts."""
from copy import deepcopy
from applications.api.services.core_reading_editorial import pattern_useful_paragraphs, shen_sha_paragraphs
from applications.api.services.day_pillar_editorial import day_personality


def test_star_groups_all_positions_and_removes_exact_duplicates():
    payload = {"bazi": {"shensha_matches": [
        {"name": "Thiên Ất Quý Nhân", "pillar": "year"},
        {"name": "Thiên Ất Quý Nhân", "pillar": "month"},
        {"name": "Thiên Ất Quý Nhân", "pillar": "year"},
        {"name": "Văn Xương", "pillar": "year"},
    ]}}
    before = deepcopy(payload)
    result = shen_sha_paragraphs(payload)
    assert len(result) == 2
    assert "trụ năm, tháng:" in result[0]
    assert "Văn Xương tại trụ năm:" in result[1]
    assert "học hỏi" in result[1]
    assert payload == before


def test_combined_day_de_preserves_other_occurrences():
    rows = [{"name": name, "pillar": pillar}
            for name in ("Thiên Đức Quý Nhân", "Nguyệt Đức Quý Nhân")
            for pillar in ("day", "month")]
    result = shen_sha_paragraphs({"bazi": {"shensha_matches": rows}})
    assert len(result) == 3
    assert sum("tại trụ tháng:" in line for line in result) == 2
    assert "cùng hiện ở trụ ngày" in result[-1]


def test_useful_relation_comes_from_day_element_not_son():
    payload = {"bazi": {"day_master": "Quý", "day_master_element": "Thủy"},
               "useful_god": {"useful_element": "Kim", "useful_stem": "Tân",
                              "useful_display": "Kim · Tân · Thiên Ấn"}}
    result = " ".join(pattern_useful_paragraphs(payload))
    assert "Kim sinh Thủy" in result
    assert "khả năng nói một lời" not in result
    assert "Đinh" not in result


def test_fire_control_does_not_invent_dinh_for_other_metal_day_master():
    payload = {"bazi": {"day_master": "Tân", "day_master_element": "Kim"},
               "useful_god": {"useful_element": "Hỏa", "useful_stem": "Bính",
                              "useful_display": "Hỏa · Bính · Chính Quan", "reason_archetype": "CHẾ"}}
    result = " ".join(pattern_useful_paragraphs(payload))
    assert "Đinh" not in result
    assert "Hỏa chế Kim" in result


def test_day_reading_uses_own_hidden_stems_without_inventing_son():
    payload = {"bazi": {"day_master": "Quý", "day_pillar": {"stem": "Quý", "branch": "Hợi"}},
               "ten_gods": {"hidden": [
                   {"pillar": "day", "branch": "Hợi", "stem": "Nhâm", "ten_god": "Kiếp Tài"},
                   {"pillar": "day", "branch": "Hợi", "stem": "Giáp", "ten_god": "Thương Quan"}]}}
    before = deepcopy(payload)
    result = " ".join(day_personality(payload))
    assert "Quý Hợi" in result and "Nhâm Kiếp Tài" in result and "Giáp Thương Quan" in result
    assert "Canh" not in result and "Đinh" not in result
    assert payload == before


def test_no_hidden_data_does_not_create_a_personality_detail():
    result = day_personality({"bazi": {"day_master": "Bính", "day_pillar": {"branch": "Tý"}}})
    assert len(result) == 1
    assert "Thiên Can của trụ ngày" in result[0]


def test_five_element_counts_do_not_become_strength_or_health_claims():
    from applications.api.services.bazi_analysis_contract import _five_elements_chapter_paragraphs
    payload = {"five_elements": {"counts": {"wood": 7, "fire": 3, "earth": 2, "metal": 2, "water": 3},
                                  "dominant": ["wood"], "missing": ["metal"]},
               "useful_god": {"useful_element": "metal"}}
    before = deepcopy(payload)
    result = " ".join(_five_elements_chapter_paragraphs(payload, {}))
    assert "Mộc 7" in result and "Kim 2" in result
    assert "số lần xuất hiện" in result
    assert "Mộc vượng sinh" not in result
    assert "Hành yếu/thiếu" not in result
    assert "Kim không xuất hiện" not in result
    assert payload == before


def test_equal_counts_do_not_select_a_dominant_element():
    from applications.api.services.bazi_analysis_contract import _five_elements_chapter_paragraphs
    result = " ".join(_five_elements_chapter_paragraphs(
        {"five_elements": {"counts": dict.fromkeys(("wood", "fire", "earth", "metal", "water"), 2)}}, {}))
    assert "cao nhất" not in result and "mạnh khắc" not in result


def test_strength_prose_leaves_scores_in_original_technical_data():
    from applications.api.services.bazi_analysis_contract import _strength_summary
    strength = {"strength_level": "weak", "strength_score": 0.23,
                "evidence_compact": "Tù khí theo tháng -10 · Có căn khí +12", "reasoning": "score=0.23"}
    before = deepcopy(strength)
    result = _strength_summary(strength, {})
    assert "Thân nhược" in result and "mùa sinh không tạo ưu thế" in result
    assert "-10" not in result and "+12" not in result and "0.23" not in result
    assert strength == before
