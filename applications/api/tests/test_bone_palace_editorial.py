from applications.api.services.bazi_analysis_contract import (
    _bone_weight_paragraphs,
    _palace_feng_shui_paragraphs,
    build_report_chapters,
)


def test_bone_weight_keeps_rating_distinct_from_day_master_strength():
    payload = {"can_xuong": {"display_weight": "2 lượng 7 chỉ", "classification": "Hạ cách"},
               "strength": {"strength_level": "strong"}}
    prose = " ".join(_bone_weight_paragraphs(payload))
    assert "Hạ cách" in prose and "Thân vượng" in prose
    assert "không có nghĩa Nhật Chủ yếu" in prose


def test_palace_keeps_birth_period_and_report_period_separate():
    payload = {"calendar": {"solar_year": 1987, "cung_phi": "Khôn", "hanh_cung": "Thổ",
                            "nhom_trach": "Tây Tứ Trạch", "tam_nguyen": "Hạ Nguyên", "cuu_van": 7},
               "result_meta": {"created_at": "2026-09-27T12:00:00+00:00"}}
    prose = " ".join(_palace_feng_shui_paragraphs(payload))
    assert "1987 thuộc Hạ Nguyên, Vận 7" in prose
    assert "2026 đang thuộc Hạ Nguyên, Vận 9 (2024–2043)" in prose
    assert "không làm Cung Phi Khôn đổi" in prose


def test_report_drops_duplicate_opening_chapters():
    chapters = build_report_chapters({}, {})
    keys = [chapter.get("chapter_key") for chapter in chapters]
    assert "overview" not in keys and "four_pillars" not in keys
    assert len(chapters) == 11
