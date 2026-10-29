import json
import unicodedata

import pytest

from consulting.naming.current_name import analyze_current_name, load_han_viet, load_name_library, load_name_words
from consulting.naming.models import CurrentNameRequest


def analyze(name, gender="female"):
    return analyze_current_name(CurrentNameRequest(full_name=name, gender=gender, lunar_birth_year=1986))


@pytest.mark.parametrize("name, phrase, family, middle, main", [
    ("Đặng Thị Dung", "Thị Dung", "Đặng", "Thị", "Dung"),
    ("Lương Ngọc Huỳnh", "Ngọc Huỳnh", "Lương", "Ngọc", "Huỳnh"),
])
def test_requested_names_have_full_word_and_composed_readings(name, phrase, family, middle, main):
    reading = analyze(name)["name_reading"]
    assert (reading["family_part"], reading["middle_part"], reading["main_part"]) == (family, middle, main)
    assert reading["han_viet"]["source"] == "curated_phrase"
    assert reading["han_viet"]["phrase"] == phrase
    assert len(reading["han_viet"]["paragraphs"]) >= 3
    assert len(" ".join(reading["han_viet"]["paragraphs"])) > 650
    assert all(part["known"] and part["interpretation"] for part in reading["parts"])
    assert [part["role"] for part in reading["parts"]] == ["Tên đệm", "Tên chính"]
    assert "chưa có đủ dữ liệu" not in json.dumps(reading, ensure_ascii=False).casefold()
    assert reading["family_reading"]["characters"] == ("鄧" if family == "Đặng" else "梁")


def test_dung_has_distinct_alternative_meanings_not_a_personality_prediction():
    reading = analyze("Đặng Thị Dung")["name_reading"]
    dung = reading["parts"][-1]
    assert {entry["character"] for entry in dung["han_characters"]} == {"容", "融", "蓉"}
    assert "bao dung" in dung["meaning"]
    assert reading["element"] is None
    assert "tiếng đệm" in reading["han_viet"]["paragraphs"][0]


def test_similar_sounding_names_keep_their_own_letters_and_meanings():
    dung = analyze("Nguyễn Dung")["name_reading"]["parts"][-1]
    dung_other = analyze("Nguyễn Dũng")["name_reading"]["parts"][-1]
    assert dung["han_characters"][0]["character"] == "容"
    assert dung_other["han_characters"][0]["character"] == "勇"
    huynh = analyze("Lương Ngọc Huỳnh")["name_reading"]["parts"][-1]
    huyen = analyze("Lương Ngọc Huyền")["name_reading"]["parts"][-1]
    quynh = analyze("Lương Ngọc Quỳnh")["name_reading"]["parts"][-1]
    assert [part["han_characters"][0]["character"] for part in (huynh, huyen, quynh)] == ["黃", "玄", "瓊"]
    thi = analyze("Đặng Thị Dung")["name_reading"]["parts"][0]
    thi_other = analyze("Đặng Thi Dung")["name_reading"]["parts"][0]
    assert thi["han_characters"][0]["character"] == "氏"
    assert thi_other["han_characters"][0]["character"] == "詩"


@pytest.mark.parametrize("name", [
    "Nguyễn Thùy Linh", "Trần Minh Khôi", "Lê Hoàng Phúc", "Phạm Anh Dũng",
    "Võ Ngọc Quỳnh", "Đỗ Thị Duyên", "Bùi Gia Hân", "Nguyễn Văn Tài",
    "Phan Bảo Trân", "Nguyễn Cao Kỳ Duyên", "Hoàng Thanh Hương", "Lý Như Ý",
    "Trương Minh Tú", "Ngô Anh Tuệ", "Phạm Cát Tường", "Lê Duy Phát",
    "Trần Mỹ Loan", "Bùi Ngọc Trà", "Nguyễn Thị Tuyết", "Nguyễn Văn Lương",
])
def test_broader_common_names_do_not_stop_at_missing_data(name):
    reading = analyze(name)["name_reading"]
    assert all(part["known"] for part in reading["parts"])
    assert all(part["interpretation"] for part in reading["parts"])
    assert reading["han_viet"]["source"] in {"curated_phrase", "word_meanings", "single_word"}


@pytest.mark.parametrize("name, expected", [
    ("Đặng Thị Dung", ["nặng", "nặng", "ngang"]),
    ("Lương Ngọc Huỳnh", ["ngang", "nặng", "huyền"]),
    ("NGUYỄN TIẾN SƠN", ["ngã", "sắc", "ngang"]),
])
def test_rhythm_uses_actual_diacritics_in_nfc_and_nfd(name, expected):
    for value in (name, unicodedata.normalize("NFD", name)):
        rhythm = analyze(value)["name_reading"]["rhythm"]
        assert [tone["tone"] for tone in rhythm["tones"]] == expected
        assert rhythm["syllable_count"] == 3


def test_limited_spelling_aliases_preserve_meaningful_tone_differences():
    for value in ("Nguyễn Thuỳ Dung", "Nguyễn Thuý Dung", "Nguyễn Hoà Bình"):
        assert all(part["known"] for part in analyze(value)["name_reading"]["parts"])
    assert analyze("Nguyễn Dung")["name_reading"]["parts"][-1]["meaning"] != analyze("Nguyễn Dũng")["name_reading"]["parts"][-1]["meaning"]


def test_unknown_names_still_do_not_get_fabricated_characters_or_elements():
    reading = analyze("Đặng Thị Xyza")["name_reading"]
    assert reading["parts"][-1]["known"] is False
    assert reading["parts"][-1]["han_characters"] == []
    assert reading["element"] is None
    assert reading["han_viet"]["source"] == "partial"
    unknown_family = analyze("Zyza Ngọc Huỳnh")["name_reading"]["family_reading"]
    assert unknown_family["characters"] is None


def test_expanded_data_is_unique_and_complete_without_changing_existing_elements():
    words, han_viet = load_name_words(), load_han_viet()
    assert len(words) >= 180
    assert set(words) == set(han_viet["words"])
    assert len(han_viet["phrases"]) >= 30
    assert len(load_name_library()["families"]) >= 30
    assert words["sơn"]["element"] == "EARTH"
    assert words["ngọc"]["element"] == "EARTH"
    assert words["huỳnh"].get("element") is None
    assert words["dung"].get("element") is None


def test_family_reading_does_not_assign_a_given_name_meaning_or_element():
    family = analyze("Lương Ngọc Huỳnh")["name_reading"]["family_reading"]
    main = analyze("Nguyễn Văn Lương")["name_reading"]["parts"][-1]
    assert family["characters"] == "梁"
    assert main["han_characters"][0]["character"] == "良"
    assert analyze("Kim Thị Dung")["name_reading"]["element"] is None
