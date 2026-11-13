from copy import deepcopy

from applications.api.services.pillar_life_editorial import pillar_domain, pillar_recommendations
from applications.api.services.family_property_editorial import run_family_property_editorial


def _pillars():
    return {"bazi": {"day_master": "Canh", "day_pillar": {"branch": "Ngọ"},
        "year_pillar": {"stem": "Bính", "branch": "Dần", "ten_god": "Thất Sát", "truong_sinh": "Tuyệt"},
        "month_pillar": {"stem": "Tân", "branch": "Sửu", "ten_god": "Kiếp Tài", "truong_sinh": "Mộ"},
        "hour_pillar": {"stem": "Mậu", "branch": "Dần", "ten_god": "Thiên Ấn", "truong_sinh": "Tuyệt"}}}


def test_canh_ngo_recommendations_are_reachable_and_chart_gated():
    payload = _pillars()
    assert len(pillar_recommendations(payload)) == 2
    payload["bazi"]["year_pillar"]["stem"] = "Giáp"
    assert not any("Trong nghề, hãy giữ một hướng" in line for line in pillar_recommendations(payload))


def test_generic_parents_and_ancestry_do_not_share_paragraphs():
    payload = _pillars()
    payload["bazi"]["day_master"] = "Quý"
    payload["bazi"]["year_pillar"].update(stem="Ất", branch="Mão", ten_god="Thực Thần", truong_sinh="Trường Sinh")
    parents = pillar_domain("parents", payload)
    ancestry = pillar_domain("ancestry", payload)
    assert parents and ancestry
    assert not set(parents) & set(ancestry)
    assert "trụ năm Ất Mão" in parents[0]
    assert all("Hãy bắt đầu bằng một việc nhỏ có người cùng thử" not in line for line in parents)


def test_family_no_duplicate_bridge_no_unconditional_child_character():
    payload = {"bazi": {"day_master": "Quý", "day_pillar": {"branch": "Hợi"}, "hour_pillar": {"branch": "Dần"}},
        "ten_gods": {"visible": [{"ten_god": "Chính Ấn"}, {"ten_god": "Thực Thần"}],
        "hidden": [{"ten_god": "Chính Ấn"}, {"ten_god": "Chính Tài"}, {"pillar": "hour", "ten_god": "Chính Quan"}]}}
    before = deepcopy(payload)
    sections = run_family_property_editorial(payload)["sections"]
    all_lines = [line for lines in sections.values() for line in lines]
    assert len(all_lines) == len(set(all_lines))
    assert not any("trẻ dễ có cá tính" in line or "Cách diễn đạt phù hợp" in line for line in all_lines)
    assert not any("Ấn tinh nằm trong Tàng Can, không lộ" in line for line in sections["parents"])
    assert not any("Thương Quan hoặc Kiếp Tài trong trụ giờ" in line for line in sections["children"])
    assert payload == before
