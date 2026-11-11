"""Stateless current-name reading from curated meanings and year-only references."""

from __future__ import annotations

import json
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

from consulting.marriage.models.enums import FiveElement
from consulting.marriage.runtime.canonical_labels import try_map_five_element
from consulting.naming.models import CurrentNameRequest, normalize_name
from consulting.naming.service import (
    CONTROLS, ELEMENT_LABELS, GENERATES, describe_element_relation, load_catalog,
)
from engines.calendar_engine.cung_phi import (
    element_label_for_cung,
    personal_cung_phi_from_year_ganzhi,
)
from engines.calendar_engine.tam_nguyen_dataset import CALENDAR_RULE_VERSION, jiazi_row_for_year

_COMPOUND_FAMILY_NAMES = frozenset({"âu dương", "tôn thất", "tôn nữ", "hoàng phủ"})


@lru_cache(maxsize=1)
def load_name_library() -> dict[str, Any]:
    return json.loads(Path(__file__).with_name("name_library.json").read_text(encoding="utf-8"))


def _word_key(value: str) -> str:
    key = normalize_name(value).casefold()
    return load_name_library()["aliases"].get(key, key)


@lru_cache(maxsize=1)
def load_name_words() -> dict[str, dict[str, Any]]:
    data = json.loads(Path(__file__).with_name("name_words.json").read_text(encoding="utf-8"))
    words = {}
    for entry in data["words"] + load_name_library()["words"]:
        key = _word_key(entry["word"])
        if not key or key in words or not entry.get("meaning"):
            raise ValueError("name_word_catalog_invalid")
        if entry.get("element"):
            FiveElement(entry["element"].lower())
            if not entry.get("basis"):
                raise ValueError("name_word_element_basis_missing")
        words[key] = entry
    if any(target not in words for target in load_name_library()["aliases"].values()):
        raise ValueError("name_word_alias_target_missing")
    return words


@lru_cache(maxsize=1)
def load_han_viet() -> dict[str, Any]:
    data = json.loads(Path(__file__).with_name("han_viet.json").read_text(encoding="utf-8"))
    words = {}
    for entry in data["words"] + load_name_library()["words"]:
        key = _word_key(entry["word"])
        if key in words or key not in load_name_words() or not entry.get("interpretation"):
            raise ValueError("han_viet_word_invalid")
        if any(not item.get("character") or not item.get("meaning") for item in entry["characters"]):
            raise ValueError("han_viet_character_invalid")
        words[key] = entry
    phrases = {}
    for entry in data["phrases"] + load_name_library()["phrases"]:
        key = " ".join(_word_key(word) for word in entry["name"].split())
        if key in phrases or not entry["paragraphs"] or not all(entry["paragraphs"]):
            raise ValueError("han_viet_phrase_invalid")
        if any(word not in words for word in key.split()):
            raise ValueError("han_viet_phrase_word_missing")
        phrases[key] = entry
    return {"words": words, "phrases": phrases, "note": data["note"], "version": data["version"]}


def analyze_current_name(request: CurrentNameRequest) -> dict[str, Any]:
    words = request.full_name.split()
    family_size = 0 if len(words) == 1 else 1
    if len(words) >= 3 and " ".join(words[:2]).casefold() in _COMPOUND_FAMILY_NAMES:
        family_size = 2
    name_words = words[family_size:]
    given_part = " ".join(name_words)
    dictionary = load_name_words()
    parts = [_word_reading(word, dictionary) for word in name_words]
    for index, part in enumerate(parts):
        part["role"] = "Tên chính" if index == len(parts) - 1 else "Tên đệm"
    catalog_match = _match_name(given_part)
    main_entry = dictionary.get(_word_key(name_words[-1]))
    combined = _combined_reading(parts, catalog_match)
    element = None
    basis = None
    if catalog_match:
        element = FiveElement(catalog_match["element"].lower())
        basis = catalog_match["basis"]
        meaning = catalog_match["meaning"]
    elif main_entry:
        meaning = f"Tên gọi chính “{name_words[-1]}”: {main_entry['meaning']}"
        if main_entry.get("element"):
            element = FiveElement(main_entry["element"].lower())
            basis = main_entry["basis"]
    else:
        meaning = f"“{name_words[-1]}” là tên chính. Bạn có thể đối chiếu thêm chữ gốc hoặc câu chuyện gia đình gửi trong tiếng tên này để đọc sâu hơn."
    if combined.get("summary"):
        meaning = combined["summary"]

    # The form supplies an already determined lunar year, never a Gregorian year.
    year = jiazi_row_for_year(request.lunar_birth_year)
    cung = personal_cung_phi_from_year_ganzhi(
        year_ganzhi=year.ganzhi, tam_nguyen=year.tam_nguyen,
        reference_year=request.lunar_birth_year, gender=request.gender,
    )
    if cung is None:
        raise ValueError("current_name_cung_phi_missing")
    nap_element = try_map_five_element(year.nap_am.rsplit(" ", 1)[-1])
    cung_element = try_map_five_element(element_label_for_cung(cung.cung_phi))
    unknown = list(dict.fromkeys(part["word"] for part in parts if not part["known"]))
    notes = [
        "Can Chi, Nạp Âm và Cung Phi được đối chiếu theo năm sinh âm lịch bạn đã nhập.",
        "Muốn xét Bát Tự và Dụng/Hỷ thần, cần ngày và giờ sinh đầy đủ.",
    ]
    if unknown:
        notes.append("Chưa có diễn giải cho các tiếng: " + ", ".join(unknown) + ". Không tự gán hành cho những tiếng này.")
    return {
        "module_version": "naming.current-name.v0.3",
        "basis": "lunar_birth_year_only",
        "full_name": request.full_name,
        "gender": request.gender,
        "lunar_birth_year": request.lunar_birth_year,
        "name_reading": {
            "family_part": " ".join(words[:family_size]) or None,
            "given_part": given_part,
            "middle_part": " ".join(name_words[:-1]) or None,
            "main_part": name_words[-1],
            "meaning": meaning,
            "parts": parts,
            "family_reading": _family_reading(" ".join(words[:family_size])),
            "rhythm": _name_rhythm(words),
            "han_viet": {
                "note": load_han_viet()["note"],
                **combined,
            },
            "element": ELEMENT_LABELS.get(element),
            "element_basis": basis,
            "match_source": "catalog_name" if catalog_match else "main_word" if main_entry else "unresolved",
        },
        "year_reference": {
            "calendar": "vietnamese_lunar_year",
            "lunar_birth_year": request.lunar_birth_year,
            "can_chi": year.ganzhi,
            "nap_am": year.nap_am,
            "nap_am_element": ELEMENT_LABELS.get(nap_element),
            "cung_phi": cung.cung_phi,
            "cung_phi_element": ELEMENT_LABELS.get(cung_element),
            "house_group": cung.house_group,
            "source_version": CALENDAR_RULE_VERSION,
        },
        "comparisons": [
            _comparison(element, nap_element, "Nạp Âm theo năm âm lịch"),
            _comparison(element, cung_element, "Cung Phi theo năm âm lịch"),
        ],
        "notes": notes,
        "notice": "Ý nghĩa và hành tên là cách diễn giải tham khảo, không quyết định tính cách, thành công hay danh tiếng của một người.",
    }


def _match_name(given_part: str) -> dict[str, Any] | None:
    key = given_part.casefold()
    candidates = []
    for entry in load_catalog()["names"]:
        name = normalize_name(entry["name"]).casefold()
        if key == name or key.endswith(" " + name):
            candidates.append(entry)
    return max(candidates, key=lambda entry: len(entry["name"])) if candidates else None


def _word_reading(word: str, dictionary: dict[str, dict[str, Any]]) -> dict[str, Any]:
    entry = dictionary.get(_word_key(word))
    han_viet = load_han_viet()["words"].get(_word_key(word), {})
    element = FiveElement(entry["element"].lower()) if entry and entry.get("element") else None
    return {
        "word": word,
        "known": entry is not None,
        "meaning": entry["meaning"] if entry else "Tiếng tên này có thể gắn với một cách đặt riêng. Hãy đối chiếu chữ gốc hoặc ý nghĩa người đặt tên gửi gắm.",
        "element": ELEMENT_LABELS.get(element),
        "han_characters": han_viet.get("characters", []),
        "interpretation": han_viet.get("interpretation"),
    }


def _combined_reading(parts: list[dict[str, Any]], catalog_match: dict[str, Any] | None) -> dict[str, Any]:
    # Select only a documented suffix; do not infer Chinese spelling for the full name.
    key = " ".join(_word_key(part["word"]) for part in parts)
    matches = [entry for phrase, entry in load_han_viet()["phrases"].items()
               if key == phrase or key.endswith(" " + phrase)]
    if matches:
        selected = max(matches, key=lambda entry: len(entry["name"]))
        return {"phrase": selected["name"], "paragraphs": selected["paragraphs"], "summary": selected.get("summary"), "source": "curated_phrase"}
    if any(not part["known"] for part in parts):
        return {"phrase": None, "paragraphs": [
            "Có thể bắt đầu đọc tên từ những tiếng đã rõ nghĩa ở bên dưới. Phần tên mang cách đặt riêng nên được giữ theo lời giải thích của gia đình, để câu chuyện của tên được đọc đúng và đầy đủ hơn."
        ], "source": "partial"}
    if len(parts) == 1:
        return {"phrase": None, "paragraphs": [], "source": "single_word"}
    pair = parts[-2:]
    glosses = [part["han_characters"][0]["meaning"] if part["han_characters"] else part["meaning"].rstrip(".") for part in pair]
    paragraphs = [
        f"Trong tên này, “{pair[0]['word']}” có thể được đọc theo nghĩa {glosses[0]}, còn “{pair[1]['word']}” gợi {glosses[1]}. Tiếng đệm tạo nền cho hình ảnh của tên chính; khi gọi trọn tên, hai lớp nghĩa cùng tạo nên lời gửi gắm riêng của gia đình.",
    ]
    if catalog_match:
        paragraphs.append(f"Với cụm “{catalog_match['name']}”, cách hiểu đang được dùng là: {catalog_match['meaning']} Có thể cảm nhận đây là một lời gửi gắm yêu thương của người đặt tên; cách viết chữ Hán và ý nghĩa cụ thể vẫn có thể khác giữa các gia đình.")
    return {"phrase": " ".join(part["word"] for part in pair), "paragraphs": paragraphs, "source": "word_meanings"}


def _family_reading(family: str) -> dict[str, Any] | None:
    if not family:
        return None
    characters = next((script for word, script in load_name_library()["families"].items()
                       if word.casefold() == family.casefold()), None)
    return {
        "word": family,
        "characters": characters,
        "paragraph": f"{family} là phần họ, giữ dấu nối với gia đình trong cấu trúc tên. Phần tên đệm và tên chính đi sau tạo nét nghĩa riêng cho người mang tên; không dùng nghĩa chữ của họ để suy ra tính cách hay quan hệ họ hàng.",
    }


def _name_rhythm(words: list[str]) -> dict[str, Any]:
    marks = {"\u0300": "huyền", "\u0301": "sắc", "\u0309": "hỏi", "\u0303": "ngã", "\u0323": "nặng"}
    tones = []
    for word in words:
        tone = next((marks[mark] for mark in unicodedata.normalize("NFD", word) if mark in marks), "ngang")
        tones.append({"word": word, "tone": tone, "group": "Bằng" if tone in {"ngang", "huyền"} else "Trắc"})
    pattern = " – ".join(item["group"] for item in tones)
    return {"syllable_count": len(words), "tones": tones, "pattern": pattern,
            "paragraph": f"Tên gồm {len(words)} tiếng, có chuỗi thanh {pattern.lower()}. Tên chính “{words[-1]}” mang thanh {tones[-1]['tone']}. Đây là một cách nhìn nhịp đọc qua dấu viết; bạn có thể đọc liền cả họ tên để cảm nhận sự nối âm trong cách gọi hằng ngày."}


def _comparison(
    element: FiveElement | None, reference: FiveElement | None, label: str,
) -> dict[str, Any]:
    if element is None or reference is None:
        return {"label": label, "relation": "unresolved", "title": "Chưa đủ cơ sở đối chiếu", "explanation": "Chưa xác định được đầy đủ hành tên để đối chiếu trong mục này."}
    if element == reference:
        relation, title = "same", f"Cùng hành {ELEMENT_LABELS[element]}"
    elif GENERATES[element] == reference:
        relation, title = "name_generates_reference", f"Tương sinh: {ELEMENT_LABELS[element]} sinh {ELEMENT_LABELS[reference]}"
    elif GENERATES[reference] == element:
        relation, title = "reference_generates_name", f"Tương sinh: {ELEMENT_LABELS[reference]} sinh {ELEMENT_LABELS[element]}"
    elif CONTROLS[element] == reference:
        relation, title = "name_controls_reference", f"Tương khắc: {ELEMENT_LABELS[element]} khắc {ELEMENT_LABELS[reference]}"
    else:
        relation, title = "reference_controls_name", f"Tương khắc: {ELEMENT_LABELS[reference]} khắc {ELEMENT_LABELS[element]}"
    _, explanation = describe_element_relation(element, reference, label, include_priority_note=False)
    return {"label": label, "relation": relation, "title": title, "explanation": explanation}
