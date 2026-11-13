"""Approved customer prose for Day Master, Pattern, Useful God and Shen Sha."""

from __future__ import annotations

from .day_pillar_editorial import day_personality

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
    strength = _map(payload.get("strength"))
    result = day_personality(payload)
    if not result:
        return []
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
    if label and not pattern_copy:
        special = label.split(":", 1)[-1].strip()
        if "Giá Vượng" in special:
            meaning = (
                "Lá số được xếp vào cấu trúc đặc biệt Giá Vượng, "
                "cần phân biệt với một cách cục thông thường lấy tên Thập thần của nguyệt lệnh. "
                "Điểm cần xem là khí nổi trội được nâng đỡ bởi những Can Chi nào, "
                "có thành thế nhất quán hay còn lực khác làm thay đổi hướng vận hành. "
                "Trong đời sống, bạn nên đặt nguồn lực vào công việc có đầu ra rõ, "
                "đồng thời dùng Dụng thần để giữ nhịp và tránh mở rộng quá sức."
            )
        else:
            meaning = (
                "Tên cấu trúc này mô tả cách các nguồn lực kết hợp trong lá số, "
                "không ấn định sẵn một nghề hay một kết quả trong đời. Với bạn, "
                "điều hữu ích là nhận ra hoàn cảnh nào giúp mình làm việc tốt và "
                "phần trách nhiệm nào cần được chia sẻ. Ý nghĩa cụ thể còn phụ thuộc "
                "vào nguyệt lệnh, thế Thân và Dụng thần đã nêu."
            )
        result.append(f"Mệnh cục {special}: {meaning}")
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
            "Ở đây, Chính Tài nói về cách quản lý nguồn lực, làm việc có kết quả và "
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
    day_element = str(bazi.get("day_master_element") or "")
    if not day_element:
        day_element = _STEM_NATURE.get(str(bazi.get("day_master") or ""), ("", ""))[1]
    generates = {"Mộc": "Hỏa", "Hỏa": "Thổ", "Thổ": "Kim", "Kim": "Thủy", "Thủy": "Mộc"}
    controls = {"Mộc": "Thổ", "Thổ": "Thủy", "Thủy": "Hỏa", "Hỏa": "Kim", "Kim": "Mộc"}
    relation = ""
    if day_element in _ELEMENTS:
        if generates[element] == day_element:
            relation = f"{element} sinh {day_element}, tạo nguồn nâng đỡ cho Nhật Chủ. "
        elif controls[element] == day_element:
            relation = f"{element} khắc {day_element}, đặt Nhật Chủ trong quan hệ với sự ràng buộc và trách nhiệm. "
        elif generates[day_element] == element:
            relation = f"Nhật Chủ {day_element} sinh {element}; đây là chiều tiết khí, đưa năng lực ra ngoài qua sự biểu đạt và kết quả. "
        elif controls[day_element] == element:
            relation = f"Nhật Chủ {day_element} khắc {element}; hành này thuộc quan hệ Tài, gắn với việc sử dụng nguồn lực và tạo giá trị. "
        else:
            relation = f"{element} đồng hành với Nhật Chủ, bổ sung lực cùng loại. "
    result.append(f"Dụng thần {display}. {relation}{_catalog()['useful'][element]}")
    if (element == "Hỏa" and day_element == "Kim"
            and str(useful.get("reason_archetype") or "").upper() == "CHẾ"):
        useful_stem = str(useful.get("useful_stem") or "")
        lead = "Hỏa chế Kim giúp điều tiết phần Kim đang mạnh, thay vì tiếp tục tăng thêm lực cùng loại. "
        if useful_stem == "Đinh" and str(bazi.get("day_master") or "") == "Canh":
            lead += "Đinh Hỏa mang vai trò Chính Quan đối với Canh Kim, nhấn vào trách nhiệm, chuẩn mực và sự bền bỉ trong việc giữ lời. "
        result.append(lead + "Khi ứng dụng vào đời sống, bạn có thể bắt đầu từ việc chọn một trách nhiệm vừa sức, làm đến nơi và để kết quả chứng minh năng lực. Sự nghiêm túc có ích khi giúp công việc rõ ràng hơn, không phải khi khiến bạn luôn căng thẳng hoặc khắt khe với mọi người.")
    result.append("Về ứng dụng thực tế: " + _ACTIONS[element] + " Đây là gợi ý điều chỉnh thói quen, không phải bảo đảm rằng chọn một màu sắc, vật phẩm hay nghề cùng hành sẽ thay đổi vận mệnh.")
    hy = useful.get("favorable_roles")
    favorable = {str(item.get("element")) for item in hy if isinstance(item, Mapping)} if isinstance(hy, list) else set()
    if element in favorable and isinstance(hy, list):
        other_stems = [str(item.get("stem")) for item in hy if isinstance(item, Mapping)
                       and item.get("element") == element and item.get("stem") != useful.get("useful_stem")]
        if other_stems:
            result.append(
                f"Hỷ thần còn có {', '.join(other_stems)} {element}, bổ trợ cho sự cân bằng của lá số. "
                f"Dụng thần vẫn là {display}; hai vai trò cùng hành không đồng nghĩa với nhau."
            )
    for support in _ELEMENTS:
        if support in favorable and support != element:
            result.append(
                f"Hỷ thần {support} bổ trợ cho Dụng thần và sự cân bằng chung. "
                f"Bạn có thể tham khảo cách ứng dụng: {_ACTIONS[support]}"
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
    matches = _map(payload.get("bazi")).get("shensha_matches")
    if not isinstance(matches, list):
        return []
    texts = _catalog()["shen_sha"]
    labels = {"year": "năm", "month": "tháng", "day": "ngày", "hour": "giờ"}
    grouped: dict[str, set[str]] = {}
    for match in matches:
        if not isinstance(match, Mapping):
            continue
        name = str(match.get("canonical_name") or match.get("name") or "").strip()
        position = str(match.get("pillar") or "")
        if name and position in labels:
            grouped.setdefault(name, set()).add(position)
    result: list[str] = []
    de_names = ("Thiên Đức Quý Nhân", "Nguyệt Đức Quý Nhân")
    combine_de = all("day" in grouped.get(name, set()) for name in de_names)
    for name, positions in grouped.items():
        # Combine only the shared day occurrence, preserving every other position.
        remaining = positions - {"day"} if combine_de and name in de_names else positions
        if not remaining:
            continue
        places = ", ".join(labels[position] for position in labels if position in remaining)
        meaning = texts.get(name)
        if meaning:
            result.append(f"{name} tại trụ {places}: {meaning}")
        else:
            result.append(f"{name} tại trụ {places}: đây là dấu hiệu bổ sung trong cách luận truyền thống. Riêng dấu hiệu này chưa đủ để kết luận một sự kiện tốt hay xấu trong đời sống của bạn.")
    if combine_de:
        result.append(
            "Thiên Đức và Nguyệt Đức cùng hiện ở trụ ngày: hai dấu này bổ sung chủ đề hòa giải và cách ứng xử trong những quan hệ gần gũi. "
            "Khi bất đồng, việc nói rõ điều mình cần mà vẫn tôn trọng người kia có thể giúp hai bên tìm được cách giải quyết. "
            "Đây không phải bảo đảm mọi mâu thuẫn sẽ tự qua; sự tin cậy vẫn được tạo nên bằng cách hai người đối xử với nhau mỗi ngày."
        )
    return result
