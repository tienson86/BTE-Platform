"""Approved customer prose for Day Master, Pattern, Useful God and Shen Sha."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

_FILE = Path(__file__).resolve().parents[3] / "knowledge" / "editorial" / "core_reading_v1.json"
_STRENGTH = {
    "very_weak": "Rất nhược", "weak": "Nhược", "balanced": "Trung hòa",
    "strong": "Vượng", "very_strong": "Rất vượng",
}
_ELEMENTS = ("Mộc", "Hỏa", "Thổ", "Kim", "Thủy")
_STEM_NATURE = {
    "Giáp": ("Dương", "Mộc"), "Ất": ("Âm", "Mộc"),
    "Bính": ("Dương", "Hỏa"), "Đinh": ("Âm", "Hỏa"),
    "Mậu": ("Dương", "Thổ"), "Kỷ": ("Âm", "Thổ"),
    "Canh": ("Dương", "Kim"), "Tân": ("Âm", "Kim"),
    "Nhâm": ("Dương", "Thủy"), "Quý": ("Âm", "Thủy"),
}
_CAUTIONS = {
    "Mộc": "Nếu nhiều hướng phát triển cùng mở, hãy giữ một kế hoạch có đủ sức nuôi rồi mới mở hướng tiếp theo.",
    "Hỏa": "Nếu nhịp làm việc quá gấp hoặc lời hứa vượt sức giao, hãy giảm cam kết và giữ lại tiêu chuẩn quan trọng nhất.",
    "Thổ": "Nếu bạn đang ôm cả việc lẫn quyết định của mọi người, hãy chia trách nhiệm và giải phóng phần nền không còn cần thiết.",
    "Kim": "Nếu sự kiểm soát khiến người khác khó góp ý, hãy giữ chuẩn cốt lõi và chừa chỗ cho cách làm khác đạt cùng kết quả.",
    "Thủy": "Nếu thông tin nhiều hơn quyết định, hãy chọn một nguồn tin cậy và một bước nhỏ có thời hạn.",
}
_ACTIONS = {
    "Mộc": "Nuôi một kỹ năng hoặc dự án theo từng chặng có lịch kiểm tra; tạo môi trường sáng, có sự sống và một nhóm người giúp việc ấy lớn lên.",
    "Hỏa": "Làm việc trong không gian đủ sáng và ấm, tạo dịp trình bày kết quả, nói rõ tiêu chuẩn chất lượng, thời hạn và trách nhiệm với người nhận.",
    "Thổ": "Giữ một nơi làm việc có tài liệu dễ tìm; đặt lịch, điểm bàn giao và người giữ nhịp cho từng đầu việc.",
    "Kim": "Ghi tiêu chí chọn và bỏ việc, chuẩn hóa kiểm tra chất lượng và đặt ranh giới hợp tác rõ ràng.",
    "Thủy": "Mở kênh lắng nghe và phản hồi; chuyển thông tin đang giữ thành lời giải thích hoặc một kết quả người khác dùng được.",
}


@lru_cache(maxsize=1)
def _catalog() -> dict[str, Any]:
    with _FILE.open(encoding="utf-8") as stream:
        result = json.load(stream)
    if result.get("version") != "editorial.core_reading.v1":
        raise ValueError("Unknown core reading editorial version")
    return result


def _map(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def day_master_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    bazi = _map(payload.get("bazi"))
    strength = _map(payload.get("strength"))
    stem, element = str(bazi.get("day_master") or ""), str(bazi.get("day_master_element") or "")
    prose = _catalog()["day_master"].get(element)
    if not stem or not prose:
        return []
    nature = _STEM_NATURE.get(stem)
    if nature and nature[1] == element:
        introduction = (
            f"Nhật Chủ là Thiên Can của trụ ngày, dùng để chỉ chính bạn trong lá số Bát Tự. "
            f"Trong lá số này, {stem} thuộc {nature[0]} {element}. "
            f"Chữ ‘{nature[0]}’ nói về tính âm dương của Thiên Can, còn ‘{element}’ cho biết ngũ hành của Can ấy. "
            "Đây là điểm bắt đầu để đọc cách bạn sử dụng năng lực của mình; "
            "mạnh hay yếu phải xét thêm mùa sinh, các trụ còn lại và toàn cục lá số. "
        )
    else:
        introduction = f"Nhật Chủ {stem} thuộc {element}. "
    result = [introduction + prose]
    label = _STRENGTH.get(str(strength.get("strength_level") or ""))
    if label:
        result.append(f"Xét toàn cục, Nhật Chủ ở thế Thân {label.lower()}. {_catalog()['strength'][label]}")
    return result


def pattern_useful_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    pattern = _map(payload.get("pattern"))
    useful = _map(payload.get("useful_god"))
    bazi = _map(payload.get("bazi"))
    label = str(pattern.get("cach_cuc") or "")
    element = str(useful.get("useful_element") or "")
    display = str(useful.get("useful_display") or "")
    result: list[str] = []
    pattern_copy = _catalog()["pattern"].get(label)
    if pattern_copy:
        month_branch = str(pattern.get("month_branch") or "").strip()
        main_qi = str(pattern.get("month_main_qi") or "").strip()
        main_role = str(pattern.get("month_main_qi_ten_god") or "").strip()
        day_master = str(bazi.get("day_master") or pattern.get("day_master") or "").strip()
        basis = (
            f"Lá số được xếp vào Mệnh cục {label} vì nguyệt lệnh {month_branch} "
            f"có khí chính {main_qi}; xét từ Nhật Chủ {day_master}, "
            f"{main_qi} mang vai trò {main_role}. "
            if month_branch and main_qi and main_role and day_master and main_role == label
            else f"Lá số được xếp vào Mệnh cục {label} khi xét cấu trúc của toàn cục. "
        )
        meaning = (
            "Ở đây, Chính Tài nói về cách quản lý nguồn lực, làm việc có đầu ra và "
            "giữ chữ tín với phần mình nhận; nó không tự khẳng định bạn giàu có. "
            if label == "Chính Tài" else "Tên mệnh cục cho biết cách nguồn lực trong lá số thường vận hành. "
        )
        result.append(f"Mệnh cục {label}: {basis}{meaning}{pattern_copy}")
        if label == "Chính Tài" and month_branch and main_qi and pattern.get("penetration_exact") is False:
            related = pattern.get("penetration_related")
            related = related if isinstance(related, list) else []
            related_text = ""
            for entry in related:
                if not isinstance(entry, Mapping):
                    continue
                stem = str(entry.get("stem") or "").strip()
                role = str(entry.get("ten_god") or "").strip()
                position = str(entry.get("pillar_label") or "").strip()
                if stem and role and position:
                    related_text = f"; {stem} {role} hiện ở trụ {position.lower()}"
                    break
            result.append(
                f"Cách này lấy gốc ở khí của tháng {month_branch}, nhưng {main_qi} "
                f"{label} chưa lộ trực tiếp trên các Thiên Can{related_text}. "
                "Vì vậy, khi đọc về tiền bạc và công việc, hãy nhìn cả khả năng "
                "biến nguồn lực thành kết quả ổn định; không suy từ tên cách cục "
                "thành một lời bảo đảm về tài vận."
            )
    if element not in _ELEMENTS or not display:
        return result
    result.append(f"Dụng thần {display}. {_catalog()['useful'][element]}")
    if (element == "Hỏa" and str(bazi.get("day_master_element") or "") == "Kim"
            and str(useful.get("reason_archetype") or "").upper() == "CHẾ"):
        result.append(
            "Hỏa chế Kim ở đây là cách lá số đặt một chuẩn sáng rõ cho nguồn lực Kim đang mạnh. "
            "Đinh Hỏa nhấn vào kỷ luật nhất quán: xác định kết quả bạn hứa giao, cách kiểm tra "
            "chất lượng và người chịu trách nhiệm khi kết quả cần sửa. Bính Hỏa là lực thử thách "
            "khác; không thay tên Bính cho Đinh chỉ vì cả hai cùng thuộc Hỏa."
        )
        result.append(
            "Trong nhịp sống, hãy tạo chỗ làm việc đủ sáng, ấm và dễ trao đổi; giữ thời gian "
            "nghỉ để sự nhiệt tình không thành hao sức. Trong công việc, chọn một phần chuyên môn "
            "để giảng giải, trình bày hoặc đóng thành quy trình người khác dùng được. Một lịch "
            "công bố kết quả và một kênh nhận phản hồi giúp điều bạn biết bước ra ngoài, thay vì "
            "chỉ được giữ trong đầu. Những vai trò cần giải thích, điều phối hoặc chịu trách nhiệm "
            "về chất lượng có thể là môi trường rèn Hỏa khi phù hợp năng lực thật của bạn."
        )
        result.append(
            "Nếu lịch trình bị lấp kín, lời hứa vượt quá khả năng giao hoặc bạn thúc người khác "
            "liên tục, cách dùng Hỏa đang quá tay. Hãy giảm số cam kết, giữ lại chuẩn quan trọng "
            "nhất và cho mình cùng người làm việc có thời gian phục hồi. Dụng thần là hướng "
            "điều tiết, không phải mệnh lệnh phải luôn sống nhanh và nóng."
        )
    else:
        result.append(_ACTIONS[element])
    hy = useful.get("favorable_roles")
    favorable = {str(item.get("element")) for item in hy if isinstance(item, Mapping)} if isinstance(hy, list) else set()
    if element in favorable and isinstance(hy, list):
        other_stems = [str(item.get("stem")) for item in hy if isinstance(item, Mapping)
                       and item.get("element") == element and item.get("stem") != useful.get("useful_stem")]
        if other_stems:
            result.append(
                f"Trong phần Hỷ thần còn có {', '.join(other_stems)} {element}. Cùng là {element}, "
                "vai trò hỗ trợ này không thay cho can Dụng thần đã chọn; hãy đọc theo việc "
                "nó nâng đỡ trục chính, không gộp hai can thành một kết luận."
            )
    for support in _ELEMENTS:
        if support in favorable and support != element:
            result.append(
                f"Hỷ thần {support} là phần hỗ trợ cho trục Dụng thần trong lá số này. "
                f"{_ACTIONS[support]} Hãy dùng nó vừa đủ để việc chính thông hơn."
            )
    ky = useful.get("unfavorable_roles")
    unfavorable = {str(item.get("element")) for item in ky if isinstance(item, Mapping)} if isinstance(ky, list) else set()
    for caution in _ELEMENTS:
        if caution in unfavorable:
            result.append(
                f"Với Kỵ thần {caution}, điều cần tránh là để đặc tính của hành này trở nên quá mạnh "
                f"trong hoàn cảnh hiện tại, chứ không phải loại bỏ mọi thứ mang tên {caution}. {_CAUTIONS[caution]}"
            )
    return result


def shen_sha_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    bazi = _map(payload.get("bazi"))
    matches = bazi.get("shensha_matches")
    if not isinstance(matches, list):
        return []
    texts = _catalog()["shen_sha"]
    result: list[str] = []
    seen: set[str] = set()
    de_pillars: set[str] = set()
    for match in matches:
        if not isinstance(match, Mapping):
            continue
        name = str(match.get("canonical_name") or match.get("name") or "")
        if name in seen or name not in texts:
            continue
        seen.add(name)
        raw_pillar = str(match.get("pillar") or "")
        if name in ("Thiên Đức Quý Nhân", "Nguyệt Đức Quý Nhân") and raw_pillar == "day":
            de_pillars.add(name)
            continue
        pillar = {"year": "năm", "month": "tháng", "day": "ngày", "hour": "giờ"}.get(raw_pillar)
        if pillar:
            result.append(f"{name} tại trụ {pillar}: {texts[name]}")
    if de_pillars == {"Thiên Đức Quý Nhân", "Nguyệt Đức Quý Nhân"}:
        result.append(
            "Thiên Đức và Nguyệt Đức cùng hiện ở trụ ngày: trong chuyện gần gũi, hai dấu này "
            "cùng nhắc đến một lợi thế của cách ứng xử: giữ lòng tốt mà vẫn giữ ranh giới. "
            "Khi quan hệ gặp điều khó nói, bạn có thêm cơ hội chọn lời vừa thật vừa có đường "
            "cho người kia bước tới. Đây là điểm sáng bổ trợ; độ bền của quan hệ vẫn cần đọc "
            "từ toàn bộ trụ ngày và cuộc sống thực của hai người."
        )
    else:
        for name in ("Thiên Đức Quý Nhân", "Nguyệt Đức Quý Nhân"):
            if name in de_pillars:
                result.append(f"{name} tại trụ ngày: {texts[name]}")
    other_names = []
    for match in matches:
        if isinstance(match, Mapping):
            name = str(match.get("canonical_name") or match.get("name") or "")
            if name and name not in texts and name not in other_names:
                other_names.append(name)
    if result and other_names:
        result.append(
            "Lá số còn ghi nhận " + ", ".join(other_names) +
            ". Những dấu này cần được đọc cùng vị trí trụ và toàn cục trước khi đưa ra lời luận riêng."
        )
    return result
