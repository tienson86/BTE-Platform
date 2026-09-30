"""Customer prose grounded in published life-domain and Đại vận facts.

The approved Sơn drafts are editorial examples. Only predicates on published
facts select these paragraphs; they are never copied wholesale to other charts.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.ten_gods_engine.mapper import day_master_info, map_stem_to_ten_god
from engines.ten_gods_engine.exceptions import TenGodsValidationError


def _map(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _pill(payload: Mapping[str, Any], position: str) -> Mapping[str, Any]:
    return _map(_map(payload.get("bazi")).get(position + "_pillar"))


def _god_entries(payload: Mapping[str, Any], position: str | None = None) -> list[Mapping[str, Any]]:
    gods = _map(payload.get("ten_gods"))
    return [entry for visibility in ("visible", "hidden")
            for entry in (gods.get(visibility) or [])
            if isinstance(entry, Mapping) and (position is None or entry.get("pillar") == position)]


def _has(payload: Mapping[str, Any], *names: str, position: str | None = None) -> bool:
    return any(_text(entry.get("ten_god")) in names for entry in _god_entries(payload, position))


def _where(payload: Mapping[str, Any], name: str) -> list[str]:
    return list(dict.fromkeys(_text(entry.get("pillar")) for entry in _god_entries(payload)
                              if entry.get("ten_god") == name and entry.get("pillar")))


def _wealth_prose(payload: Mapping[str, Any]) -> list[str]:
    """Explain possible income channels from natal evidence and the current cycle."""
    entries = _god_entries(payload)
    labels = {"year": "năm", "month": "tháng", "day": "ngày", "hour": "giờ"}

    def evidence(name: str) -> str:
        matches = [entry for entry in entries if entry.get("ten_god") == name]
        facts = []
        for entry in matches:
            place = labels.get(_text(entry.get("pillar")))
            stem = _text(entry.get("hidden_stem") or entry.get("stem"))
            if not place:
                continue
            hidden = entry.get("visibility") == "hidden" or bool(entry.get("hidden_stem"))
            fact = f"{stem} tàng ở trụ {place}" if hidden and stem else (
                f"lộ ở trụ {place}" if not hidden else f"tàng ở trụ {place}")
            if fact not in facts:
                facts.append(fact)
        return ", ".join(facts)

    indirect, direct = evidence("Thiên Tài"), evidence("Chính Tài")
    resources = [name for name in ("Chính Ấn", "Thiên Ấn") if _has(payload, name)]
    outputs = [name for name in ("Thực Thần", "Thương Quan") if _has(payload, name)]
    authority = [name for name in ("Chính Quan", "Thất Sát") if _has(payload, name)]
    cycle = _map(_map(payload.get("luck")).get("current_cycle"))
    cycle_stem = _text(cycle.get("stem"))
    day_master = _text(_map(payload.get("bazi")).get("day_master"))
    try:
        cycle_role = map_stem_to_ten_god(day_master, cycle_stem)[0] if cycle_stem else ""
    except (ValueError, TenGodsValidationError):
        cycle_role = ""
    channels = []
    if indirect:
        channels.append("cơ hội qua quan hệ và dự án có người mua")
    if direct:
        channels.append("công việc hoặc hợp đồng có dòng thu kiểm soát được")
    if resources:
        channels.append("kiến thức và phương pháp được chuyển thành giá trị")
    if outputs:
        channels.append("sản phẩm hoặc lời giải có đầu ra cụ thể")
    if authority:
        channels.append("uy tín được xây bằng trách nhiệm và chuẩn bàn giao")
    paragraphs = [
        "Tiền đến từ đâu?: " + (
            "Lá số gợi những cửa tạo giá trị sau: " + "; ".join(channels) + ". "
            "Đây là đường hình thành thu nhập cần đối chiếu với năng lực, người mua và kết quả thực tế; "
            "không khẳng định bạn đã có những khoản thu ấy."
            if channels else "Chưa đủ dấu hiệu đã công bố để chỉ một nguồn thu cụ thể. "
            "Cần đối chiếu năng lực, sản phẩm, người mua và thu chi thực tế trước khi kết luận."
        ),
        "Cửa Thiên Tài: " + (
            f"Thiên Tài {indirect} gợi cơ hội từ việc kết nối nhu cầu, gặp đối tác hoặc nhận dự án mới. "
            "Nếu nằm ở can tàng, cơ hội cần được nhận ra và chuyển thành thỏa thuận, kết quả giao được và khoản thu thực; "
            "không thể coi là tiền may rủi hay lợi nhuận đầu cơ."
            if indirect else "Không thấy Thiên Tài trong các can đã công bố của lá số gốc; "
            "điều đó không cấm bạn làm kinh doanh hoặc có nguồn thu theo dự án. "
            "Cần xem vận, kỹ năng và nhu cầu thật trước khi nhận định một cơ hội."
        ),
        "Cửa Chính Tài: " + (
            f"Chính Tài {direct} gợi đường thu từ công việc, dịch vụ hoặc hợp đồng có phạm vi và cách thanh toán rõ. "
            "Can tàng cho biết một khả năng trong cấu trúc, không bảo đảm thu nhập cố định; "
            "việc lặp lại phụ thuộc chất lượng bàn giao và quản lý chi phí."
            if direct else "Không thấy Chính Tài trong các can đã công bố của lá số gốc; "
            "đây không phải kết luận bạn thiếu lương hay không giữ được tiền. "
            "Nguồn thu đều có thể được xây bằng hợp đồng, định giá và kiểm soát chi phí."
        ),
    ]
    if cycle_role in ("Chính Tài", "Thiên Tài"):
        paragraphs.append(
            f"Cửa Tài trong Đại vận: Can {cycle_stem} của vận đang đi mang vai trò {cycle_role}; "
            + ("đây là lớp tác động của vận, không phải Chính Tài có sẵn trong lá số gốc. "
               if cycle_role == "Chính Tài" and not direct else
               "đây là lớp tác động của vận, không phải Thiên Tài có sẵn trong lá số gốc. "
               if cycle_role == "Thiên Tài" and not indirect else
               "cần đọc cùng các dấu Tài ở lá số gốc. ")
            + "Muốn biết tiền đến từ kênh nào, hãy kiểm tra công việc, người trả tiền, hợp đồng và phần còn lại sau chi phí."
        )
    if resources or outputs:
        paragraphs.append(
            "Kiến thức thành nguồn thu: "
            + (f"{', '.join(resources)} cho nền học hỏi và xây phương pháp. " if resources else "")
            + (f"{', '.join(outputs)} gợi bước diễn đạt hoặc tạo sản phẩm từ điều đã học. " if outputs else "")
            + "Tri thức chỉ tạo thu nhập khi giải đúng nhu cầu, có người nhận đầu ra và một cách định giá rõ."
        )
    if authority:
        paragraphs.append(
            f"Uy tín thành nguồn thu: {', '.join(authority)} hiện trong lá số gợi việc được nhìn nhận qua trách nhiệm "
            "và khả năng giữ lời hứa. Chính Quan và Thất Sát là hai vai trò khác nhau; "
            "uy tín chỉ có thể giữ khách khi chuẩn làm việc, kết quả và trách nhiệm được kiểm chứng."
        )
    if indirect and resources and authority:
        paragraphs.append(
            "Khách giới thiệu và tích lũy: Thiên Tài mở khả năng gặp người và dự án; Ấn giúp hình thành "
            "phương pháp, Quan hoặc Sát đặt câu hỏi về độ tin cậy. Từ đó có thể suy luận khả năng khách cũ giới thiệu "
            "khách mới khi họ thực sự hài lòng; lá số không xác nhận việc giới thiệu đã xảy ra. "
            "Giữ được tiền lâu dài còn cần ghi chép, tái đầu tư có kiểm soát và dòng tiền được kiểm chứng; "
            "không suy ra lợi nhuận của một khoản đầu tư tài chính."
        )
    paragraphs.append(
        "Ranh giới và kiểm chứng: " + (
            "Kiếp Tài hiện rõ ở trụ tháng: khi làm với người ngang vai, hãy ghi rõ vốn, quyền quyết định "
            "và cách chia phần còn lại. "
            if _text(_pill(payload, "month").get("ten_god")) == "Kiếp Tài" else
            "Nếu làm chung, hãy ghi rõ vốn, quyền quyết định và trách nhiệm. "
        ) + "Tách chi phí sinh hoạt, dự phòng và vận hành; theo dõi khách trả tiền cho điều gì, "
        "tần suất quay lại và số tiền còn sau chi phí trước khi mở rộng."
    )
    return paragraphs


# Pattern suggests a way to work; the actual profession still depends on training and opportunity.
_CAREER_PATHS = {
    "Chính Ấn": (
        "chuyên gia tư vấn, giảng viên hoặc người đào tạo nội bộ, người thiết kế quy trình, "
        "người kiểm tra chất lượng và hướng dẫn đội ngũ",
        "đào tạo, dịch vụ tư vấn dựa trên chuyên môn, nghiên cứu ứng dụng, quản lý chất lượng "
        "hoặc bộ phận xây dựng tiêu chuẩn trong tổ chức",
    ),
    "Thiên Ấn": (
        "chuyên gia phân tích vấn đề khó, cố vấn giải pháp, người nghiên cứu và thử nghiệm phương pháp",
        "nghiên cứu ứng dụng, thiết kế sản phẩm chuyên môn, phân tích dữ liệu hoặc tư vấn chuyên sâu",
    ),
    "Chính Tài": (
        "người quản lý vận hành, kế hoạch và ngân sách; người kiểm soát chi phí, hợp đồng "
        "hoặc chuỗi cung ứng",
        "vận hành doanh nghiệp, kế toán và quản trị tài chính khi có chuyên môn, thu mua, "
        "quản lý hợp đồng hoặc dịch vụ có quy trình bàn giao rõ",
    ),
    "Thiên Tài": (
        "người phát triển thị trường, quản lý danh mục khách hàng hoặc điều phối dự án mới",
        "kinh doanh dịch vụ, phát triển đối tác, thương mại hoặc tổ chức dự án theo cơ hội",
    ),
    "Chính Quan": (
        "người quản lý tiêu chuẩn, điều hành nhóm hoặc giám sát trách nhiệm và chất lượng",
        "quản trị vận hành, hành chính chuyên môn, kiểm soát chất lượng hoặc đào tạo quản lý",
    ),
    "Thất Sát": (
        "người xử lý tình huống khó, quản lý dự án chịu áp lực hoặc điều phối đội phản ứng nhanh",
        "quản trị rủi ro, vận hành dự án, kỹ thuật hiện trường hoặc dịch vụ cần quyết định có trách nhiệm",
    ),
    "Thực Thần": (
        "người làm sản phẩm, đào tạo thực hành hoặc phụ trách trải nghiệm khách hàng",
        "sản phẩm và dịch vụ sáng tạo, giáo dục thực hành hoặc phát triển nội dung chuyên môn",
    ),
    "Thương Quan": (
        "người cải tiến quy trình, thiết kế giải pháp hoặc truyền đạt kiến thức theo cách mới",
        "thiết kế sản phẩm, truyền thông chuyên môn, công nghệ ứng dụng hoặc tư vấn cải tiến",
    ),
    "Tỷ Kiên": (
        "chuyên gia độc lập, trưởng nhóm chuyên môn hoặc người xây dựng một chuẩn nghề riêng",
        "dịch vụ chuyên môn độc lập, quản lý đội nhỏ hoặc sản xuất theo một tay nghề vững",
    ),
    "Kiếp Tài": (
        "người kết nối đội ngũ, quản lý quan hệ đối tác hoặc điều phối nhiều bên cùng làm",
        "kinh doanh theo nhóm, phát triển đối tác, tổ chức sự kiện hoặc vận hành mạng lưới dịch vụ",
    ),
}

_CAREER_USEFUL_STYLES = {
    "Mộc": "nuôi một hướng sản phẩm hoặc đội ngũ theo từng chặng, có người hướng dẫn và mốc đánh giá",
    "Hỏa": "đứng ra giải thích kết quả, đặt chuẩn giao việc và nhận trách nhiệm trước người sử dụng",
    "Thổ": "lập lịch, giữ hồ sơ và tạo điểm bàn giao để công việc có nền vận hành bền",
    "Kim": "làm rõ tiêu chí chọn lựa, phạm vi trách nhiệm và bước kiểm tra chất lượng",
    "Thủy": "mở kênh khảo sát, lắng nghe phản hồi và chuyển thông tin thành quyết định có căn cứ",
}

_HEALTH_ELEMENT_NOTES = {
    "metal": ("Kim", "Phế – Đại trường, mũi và da", "mũi họng, nhịp thở, ho hoặc tình trạng khô nếu thực tế xuất hiện"),
    "fire": ("Hỏa", "Tâm – Tiểu trường", "giấc ngủ, cảm giác hồi hộp và nhịp hoạt động nếu thực tế xuất hiện"),
    "wood": ("Mộc", "Can – Đởm", "mắt, gân cơ và cảm giác căng thẳng nếu thực tế xuất hiện"),
    "water": ("Thủy", "Thận – Bàng quang", "thay đổi tiểu tiện hoặc cảm giác giữ nước nếu thực tế xuất hiện"),
    "earth": ("Thổ", "Tỳ – Vị", "ăn uống, đầy bụng và nhịp tiêu hóa nếu thực tế xuất hiện"),
}
_HEALTH_ELEMENT_KEYS = {"Mộc": "wood", "Hỏa": "fire", "Thổ": "earth", "Kim": "metal", "Thủy": "water"}
_HEALTH_CONTROLS = {"fire": "metal", "wood": "earth", "earth": "water", "water": "fire", "metal": "wood"}
_HEALTH_PAIR_NOTES = {
    ("fire", "metal"): "để ý liệu những đợt công việc căng kéo có đi cùng khô họng, ho hoặc khó chịu hô hấp",
    ("wood", "earth"): "để ý liệu căng thẳng có đi cùng đầy bụng, ăn kém hoặc thay đổi đại tiện",
    ("earth", "water"): "để ý liệu có cảm giác nặng người, phù hoặc thay đổi tiểu tiện",
    ("water", "fire"): "để ý giấc ngủ, cảm giác hồi hộp hoặc lo âu khi nhịp sinh hoạt thay đổi",
    ("metal", "wood"): "để ý đau đầu, chóng mặt, căng cơ hoặc mắt khó chịu khi công việc dồn dập",
}


def _health_prose(payload: Mapping[str, Any], day_master: str) -> list[str]:
    bazi, strength = _map(payload.get("bazi")), _map(payload.get("strength"))
    counts = _map(_map(payload.get("five_elements")).get("counts"))
    useful = _map(payload.get("useful_god"))
    month = _pill(payload, "month")
    season = _text(month.get("branch"))
    day_element = _HEALTH_ELEMENT_KEYS.get(_text(bazi.get("day_master_element")))
    present = {key: float(value) for key, value in counts.items()
               if key in _HEALTH_ELEMENT_NOTES and isinstance(value, (int, float)) and value >= 0}
    strong = _text(strength.get("strength_level")) in ("strong", "very_strong")
    overview = (
        f"Nhật Chủ {day_master} " + ("ở thế Thân vượng" if strong else "cần được đặt trong thế vượng nhược của toàn cục")
        + (f", sinh vào tháng {season}" if season else "")
        + ". Các hành cần được đọc cùng mùa sinh và vị trí Can Chi để thấy nhịp vận hành của toàn lá số."
    )
    paragraphs = ["Cách đọc sức khỏe: " + overview]
    if present:
        ranked = sorted(present, key=lambda key: (-present[key], key))
        selected = [day_element] if day_element in present else []
        selected.extend(key for key in ranked[:2] if key not in selected)
        low = min(present, key=lambda key: (present[key], key))
        if low not in selected:
            selected.append(low)
        for key in selected:
            name, organs, signs = _HEALTH_ELEMENT_NOTES[key]
            prominence = (
                "xuất hiện ít nhất trong bảng đếm" if key == low and present[key] < max(present.values()) else
                "nằm trong nhóm xuất hiện nhiều trong bảng đếm" if key in ranked[:2] else
                "cần được đọc theo sức của Nhật Chủ, không chỉ theo số lần xuất hiện"
            )
            role = " của Nhật Chủ" if key == day_element else ""
            paragraphs.append(
                f"{name} và hướng theo dõi: {name}{role} {prominence} ({present[key]:g} vị trí). "
                f"Trong cách nhìn của Đông y, {name} gắn với {organs}; bạn nên để ý {signs}."
            )
    else:
        paragraphs.append("Dữ liệu ngũ hành: Chưa có bảng phân bố để chọn hành nổi bật; "
                          "không suy tên bệnh hoặc mức vượng từ riêng Nhật Chủ.")
    useful_key = _HEALTH_ELEMENT_KEYS.get(_text(useful.get("useful_element")))
    pair = None
    if useful_key and day_element and _HEALTH_CONTROLS.get(useful_key) == day_element:
        pair = useful_key, day_element
    elif len(present) == 5:
        candidates = [(a, b) for a, b in _HEALTH_CONTROLS.items()
                      if present[a] == max(present.values()) and present[b] == min(present.values())]
        pair = candidates[0] if candidates else None
    if pair:
        a, b = pair
        a_name, b_name = _HEALTH_ELEMENT_NOTES[a][0], _HEALTH_ELEMENT_NOTES[b][0]
        note = _HEALTH_PAIR_NOTES[pair]
        if a == useful_key and b == day_element:
            useful_stem = _text(useful.get("useful_stem"))
            paragraphs.append(
                f"Quan hệ {a_name} khắc {b_name}: {useful_stem or a_name} {a_name} là hướng Dụng thần "
                f"đã chọn để điều tiết Nhật Chủ {b_name}. Trong nhịp sống, bạn có thể {note}."
            )
        else:
            paragraphs.append(
                f"Quan hệ {a_name} khắc {b_name}: Bảng đếm cho thấy {a_name} nhiều và {b_name} ít; "
                "mối quan hệ này cần được đọc cùng mùa sinh và các Can Chi khác. "
                f"Trong đời sống, bạn có thể {note}."
            )
    paragraphs.extend([
        "Chăm sóc hằng ngày: Giữ giờ ngủ và giờ làm tương đối đều, nghỉ giữa những việc đòi hỏi tập trung, "
        "ăn uống và vận động phù hợp; quan sát khả năng hồi phục sau giai đoạn bận rộn.",
        "Khi cần kiểm tra sức khỏe: Nếu một biểu hiện kéo dài hoặc nặng lên, hãy thăm khám để xác định nguyên nhân "
        "và chọn cách chăm sóc phù hợp."
    ])
    return paragraphs


def life_domain_prose(key: str, payload: Mapping[str, Any]) -> list[str]:
    """Return prose only when a natal Day Master and relevant evidence exist."""
    bazi = _map(payload.get("bazi"))
    day_master = _text(bazi.get("day_master"))
    if not day_master:
        return []
    useful = _map(payload.get("useful_god"))
    strength = _map(payload.get("strength"))
    pattern = _map(payload.get("pattern"))
    calendar = _map(payload.get("calendar"))
    year, month, day, hour = (_pill(payload, name) for name in ("year", "month", "day", "hour"))
    strong = _text(strength.get("strength_level")) in ("strong", "very_strong")
    useful_stem = _text(useful.get("useful_stem"))
    useful_element = _text(useful.get("useful_element"))
    use = f"{useful_stem} {useful_element}".strip()
    pattern_name = _text(pattern.get("cach_cuc"))

    if key == "health":
        return _health_prose(payload, day_master)

    if key == "wealth":
        return _wealth_prose(payload)

    if key == "career":
        sát = _has(payload, "Thất Sát", position="year")
        quan = _has(payload, "Chính Quan")
        hour_resource = _text(hour.get("stem")) if _text(hour.get("ten_god")) == "Thiên Ấn" else ""
        roles, industries = _CAREER_PATHS.get(pattern_name, ("người làm chuyên môn có đầu ra rõ và được kiểm tra", "lĩnh vực đã có kinh nghiệm, khách hàng và nhu cầu thực"))
        combination = (
            "Ấn tinh đi cùng Quan hoặc Sát: học sâu rồi dùng phương pháp để giữ chuẩn và xử lý việc khó. "
            "Bạn có thể bắt đầu ở vai trò chuyên gia, sau đó phụ trách đào tạo hoặc chất lượng khi đã có thành quả để dẫn chứng."
            if _has(payload, "Chính Ấn", "Thiên Ấn") and _has(payload, "Chính Quan", "Thất Sát") else
            "Tài tinh đi cùng Thực Thần hoặc Thương Quan: cần biến hiểu biết hay đầu ra thành sản phẩm có người mua, "
            "mức giá, chi phí và trách nhiệm giao hàng rõ ràng."
            if _has(payload, "Chính Tài", "Thiên Tài") and _has(payload, "Thực Thần", "Thương Quan") else
            "Trước khi mở rộng, hãy xem kỹ năng nào đang tạo kết quả và ai là người nhận kết quả đó."
        )
        return [
            "Nền nghề: " + (
                f"Mệnh cục {pattern_name} cho bạn lợi thế học sâu và hệ thống hóa tri thức. "
                + (f"Thiên Ấn {hour_resource} ở trụ giờ nhắc đến cách tìm lời giải riêng. " if hour_resource else "")
                +
                "Giá trị của phần nền ấy rõ nhất khi người nhận hiểu mình sẽ được giải quyết việc gì, vì sao và theo quy trình nào."
                if pattern_name == "Chính Ấn" else
                f"Mệnh cục {pattern_name or 'đang được xem xét'} cần đi cùng công việc có đầu ra kiểm chứng được. "
                "Lá số không tự ấn định một nghề duy nhất."),
            "Chuẩn và áp lực: " + (
                f"Thất Sát ở trụ năm nhắc tới cách bạn đón việc khó; hướng Dụng thần {use}"
                " đặt chuẩn chất lượng và trách nhiệm lên trước nhịp đối đầu. "
                "Áp lực Thất Sát không được gọi thành Chính Quan chỉ vì cả hai liên quan Hỏa."
                if sát and quan and use else
                f"Hướng Dụng thần {use} giúp bạn chọn cách tổ chức công việc có phương pháp. "
                "Mỗi Thập thần có vai trò riêng; cần xem trụ và can cụ thể trước khi kết luận." if use else
                "Khi gặp việc khó, hãy tách yêu cầu, nguồn lực và người chịu trách nhiệm trước khi nhận thêm."),
            "Việc có thể làm: Chọn một dạng công việc, viết câu hỏi đầu vào, mẫu bàn giao và cách kiểm tra kết quả. "
            "Thử giải thích cho người chưa học chuyên môn; khi họ hiểu và dùng được kết quả, tri thức mới có đường thành dịch vụ bền.",
            f"Vị trí có thể phát huy: Với Mệnh cục {pattern_name or 'đã công bố'}, "
            f"bạn có thể cân nhắc vai trò {roles}. {combination}",
            f"Nhóm nghề nên khảo sát: {industries}. Đây là nhóm môi trường để thử năng lực, "
            "không phải kết luận rằng chỉ một ngành sẽ thành công; các vị trí đòi bằng cấp hoặc giấy phép "
            "vẫn cần đáp ứng điều kiện nghề nghiệp thực tế.",
            "Cách chọn và tiến nghề: " + (
                f"Dụng thần {use} gợi cách làm việc: {_CAREER_USEFUL_STYLES[useful_element]}. "
                if use and useful_element in _CAREER_USEFUL_STYLES else "Hãy đặt cách làm phù hợp vào công việc bạn đang có. "
            ) + "Chọn hai vị trí gần chuyên môn sẵn có, thử bằng một dự án nhỏ trong vài tháng; "
            "so sánh chất lượng đầu ra, nhu cầu khách hàng, chi phí học thêm và sức bền của bản thân trước khi chuyển nghề."
        ]

    if key == "marriage":
        branch = _text(day.get("branch"))
        hidden = list(dict.fromkeys(_text(e.get("ten_god")) for e in _god_entries(payload, "day")
                                    if e.get("visibility") == "hidden" or e.get("hidden_stem")))
        return [
            "Ở gần nhau: " + (f"Trụ ngày {day_master} {branch} đặt Nhật Chủ cạnh cung quan hệ thân thiết. "
                + (f"Trong chi ngày có {', '.join(hidden)}; đây là các lớp để hỏi về trách nhiệm và nhu cầu được nâng đỡ, " if hidden else "Cần đọc cả các trụ và đời sống thật, ")
                + "không đủ để kết luận tính cách người phối ngẫu hoặc hôn nhân sẽ thuận hay khó."
                if branch else "Thiếu chi ngày nên chưa thể luận riêng về cung quan hệ thân thiết."),
            "Cách chăm mối quan hệ: Khi bất đồng về tiền, thời gian hoặc gia đình hai bên, "
            "hãy hỏi người kia đang lo điều gì rồi mới đề xuất giải pháp. Giữ lời hứa nhỏ về phần việc đã nhận và thời gian dành cho nhau.",
            "Giới hạn: Muốn luận cho một cặp đôi cụ thể cần lá số người còn lại và hoàn cảnh hai người. "
            "Lá số của một người không thể phán thay quyết định chung của họ."
        ]

    if key == "children":
        branch = _text(hour.get("branch"))
        return [
            "Trụ giờ và hậu vận: " + (f"Trụ giờ {hour.get('stem', '')} {branch} gợi câu hỏi về những điều bạn muốn trao lại: "
                "tri thức, cách làm và một nền đủ vững để người đến sau tự bước tiếp. "
                "Trụ này không tiên đoán số con, giới tính hay khả năng sinh sản."
                if branch else "Thiếu giờ sinh đáng tin cậy; chưa nên đưa ra lời luận riêng về trụ giờ hay chuyện con cái."),
            "Cách chuẩn bị: Nếu có kế hoạch nuôi dạy con, hãy dành nguồn lực cho sức khỏe, "
            "thời gian có mặt và ngân sách nhiều năm. Cho trẻ được học, được hỏi và thử cách riêng thay vì phải thành bản sao của mình.",
            "Thời điểm: Chọn lúc sinh con cần xem nguyện vọng của cả hai, sức khỏe thực tế và Đại vận nếu muốn tham khảo thêm; "
            "không dùng riêng trụ giờ để định một năm sinh."
        ]

    if key == "parents":
        branch = _text(month.get("branch"))
        month_gods = list(dict.fromkeys(_text(e.get("ten_god")) for e in _god_entries(payload, "month")
                                         if e.get("ten_god") and e.get("ten_god") != "Nhật Chủ"))
        return [
            "Nền trưởng thành: " + (f"Trụ tháng {month.get('stem', '')} {branch} có "
                + (f"các dấu {', '.join(month_gods)}. " if month_gods else "một vai trò trong nền khí của lá số. ")
                + "Bạn có thể nhìn lại điều mình nhận từ gia đình: sự nâng đỡ, kỳ vọng và những quy tắc đã thành thói quen. "
                "Các dấu này không kể thay cuộc đời của cha mẹ."
                if branch else "Thiếu dữ liệu trụ tháng để nói về nền gia đình trong lá số này."),
            "Giữ kết nối: Khi chăm sóc người thân, hãy nói cụ thể lịch thăm hỏi, mức hỗ trợ và ai cùng chia trách nhiệm. "
            "Sự quan tâm đều đặn thường bền hơn việc một người âm thầm gánh hết rồi kiệt sức.",
            "Phần được chọn: Bạn có thể giữ lòng biết ơn với điều được dạy và vẫn đặt giới hạn lành mạnh "
            "với những kỳ vọng không còn hợp hoàn cảnh hiện tại."
        ]

    if key == "siblings":
        peer = _text(month.get("ten_god"))
        return [
            "Quan hệ ngang vai: " + (f"{peer} lộ ở trụ tháng, gợi nơi anh em, bạn bè hoặc cộng sự có thể cùng góp sức "
                "nhưng cũng cần minh bạch lợi ích. Sao này không khẳng định một ai sẽ tranh tiền hay phản bội bạn."
                if peer in ("Kiếp Tài", "Tỷ Kiên") else
                "Anh em và người đồng hành phải được đọc cùng các dấu ở trụ tháng, "
                "không gán sẵn người nào giúp hoặc cản bạn."),
            "Khi làm chung: Thống nhất ai chịu trách nhiệm trước khách hàng, ai quyết định chi tiêu "
            "và khi dừng việc chung sẽ bàn giao tài liệu, khách hàng, tiền ra sao. Viết được điều ấy ngắn gọn là cách giữ cả công việc lẫn tình thân.",
            "Trong giao tiếp: Giữ chuẩn chất lượng, cho người khác quyền góp ý vào cách làm và hẹn thời điểm đánh giá lại. "
            "Ranh giới rõ không đồng nghĩa thiếu tin nhau."
        ]

    if key == "ancestry":
        branch = _text(year.get("branch"))
        god = _text(year.get("ten_god"))
        return [
            "Gốc nhà: " + (f"Trụ năm {year.get('stem', '')} {branch}" + (f" với {god}" if god else "")
                + " là một cửa nhìn về nếp nhà và những điều được truyền qua các thế hệ. "
                "Nó không chứng minh tổ tiên từng gặp biến cố hay đo được phúc họa của cả dòng họ."
                if branch else "Thiếu dữ liệu trụ năm nên chưa luận riêng về gốc gia đình."),
            "Điều nên tiếp nối: Chọn một giá trị đã thực sự giúp bạn sống tốt, giữ nó bằng hành động trong gia đình hiện tại. "
            "Những kỳ vọng khiến mình nặng lòng có thể được nhìn lại và trao đổi với người thân.",
            "Khi cần hiểu sâu hơn: Hãy lắng nghe lịch sử thật của gia đình và hoàn cảnh từng thế hệ. "
            "Một trụ năm không thể thay lời kể của những người đã sống trong câu chuyện ấy."
        ]

    if key == "property":
        palace = _text(calendar.get("cung_phi"))
        group = _text(calendar.get("nhom_trach"))
        avoid = {_text(item.get("element")) for item in useful.get("unfavorable_roles") or [] if isinstance(item, Mapping)}
        return [
            "Không gian hợp cách sống: " + (f"Cung Phi {palace} thuộc {group} là dữ kiện để khảo sát phương vị. "
                "Hướng trên giấy không thể bù cho nơi ở thiếu sáng, nóng bí hoặc không đủ chỗ làm việc."
                if palace and group else "Chưa có đủ Cung Phi và nhóm trạch để gợi ý nhóm phương vị cho nhà ở."),
            "Đối chiếu Tứ trụ: " + (f"Dụng thần {use} và nhóm Kỵ có {_text(calendar.get('hanh_cung'))}; "
                "đừng vì hành Cung Phi mà tăng vô hạn màu sắc hay vật liệu cùng hành. "
                if use and _text(calendar.get("hanh_cung")) in avoid else
                f"Hướng Dụng thần {use} cần được đặt cạnh Cung Phi, " if use else
                "Bố trí nhà cần dựa trên nhu cầu sử dụng thực, ")
            + "Ưu tiên ánh sáng, lối đi, thông gió, ngân sách và nơi bạn thực sự làm việc hoặc nghỉ ngơi.",
            "Tam Nguyên Cửu Vận: Để luận một căn nhà cần hướng đo, năm xây hoặc thời điểm vào ở cùng mặt bằng. "
            "Vận của thời điểm xem nhà không tự làm Cung Phi của người sống trong nhà thay đổi."
        ]
    return []


_GOD_THEMES = {
    "Thực Thần": ("học qua trải nghiệm rồi diễn đạt thành kỹ năng", "ghi điều đã thử và chia sẻ lại bằng một kết quả có thể kiểm chứng"),
    "Thương Quan": ("thử cách làm riêng và đặt câu hỏi với quy tắc quen", "đưa đề xuất kèm lý do và kết quả thử nghiệm"),
    "Thiên Tài": ("nhìn ra cơ hội, dự án hoặc nhu cầu mới", "thử quy mô nhỏ và đo phần tiền còn lại sau chi phí"),
    "Chính Tài": ("xây dòng thu đều từ giá trị rõ ràng", "chuẩn hóa sản phẩm, hợp đồng và cách quản lý thu chi"),
    "Thất Sát": ("đón áp lực, thử thách và kỳ vọng cao", "đặt người chịu trách nhiệm, quy trình và điểm dừng trước khi nhận thêm việc"),
    "Chính Quan": ("xây uy tín bằng chuẩn và lời hứa có thể giao", "kiểm soát chất lượng và trao quyền theo tiêu chuẩn dễ hiểu"),
    "Thiên Ấn": ("tìm hiểu theo một lối riêng, tích lũy kinh nghiệm sâu", "ghi lại kiến thức và cho người khác thử, sửa, góp ý"),
    "Chính Ấn": ("giữ nền tri thức, sự nâng đỡ và phương pháp", "chuyển kinh nghiệm thành tài liệu và quy trình người khác dùng được"),
    "Tỷ Kiên": ("giữ bản sắc và quyền tự chủ", "nêu rõ tiêu chuẩn cốt lõi nhưng để người khác chọn cách thực hiện"),
    "Kiếp Tài": ("cân nhắc nguồn lực và quan hệ ngang vai", "làm rõ phần đóng góp, quyết định và quyền lợi trong việc chung"),
}

_GOD_LONG_VIEW = {
    "Thực Thần": "Một điều học được chỉ thật sự có sức sống khi bạn thử lại, nói ra và để người khác dùng được.",
    "Thương Quan": "Sự độc lập hữu ích nhất khi đi cùng bằng chứng và một cách trình bày mà người khác có thể kiểm tra.",
    "Thiên Tài": "Cơ hội đáng giữ là cơ hội có người nhận kết quả, chi phí rõ ràng và còn phần để tái đầu tư.",
    "Chính Tài": "Đường thu nhập bền cần ranh giới giữa tiền sinh hoạt, vốn vận hành và phần còn lại thực sự tích lũy.",
    "Thất Sát": "Sức ép có thể rèn nghề, nhưng chỉ bền khi có đội ngũ, quyền quyết định và cách bàn giao tương xứng.",
    "Chính Quan": "Một chuẩn làm việc có giá trị khi người khác hiểu được, thực hiện được và biết ai chịu trách nhiệm nếu cần sửa.",
    "Thiên Ấn": "Điều bạn hiểu theo lối riêng sẽ trở thành di sản khi được viết ra, thử lại và để người khác góp ý.",
    "Chính Ấn": "Giữ nền tri thức có ích; giữ tất cả trong đầu một mình sẽ làm nền ấy khó truyền đi.",
    "Tỷ Kiên": "Bản sắc nghề không cần buộc người đi sau phải chọn đúng một cách làm như bạn.",
    "Kiếp Tài": "Trong việc chung, phần việc và quyền lợi càng rõ thì sự tin cậy càng có chỗ đứng lâu dài.",
}


def luck_cycle_prose(payload: Mapping[str, Any], cycles: Mapping[str, Any]) -> list[str]:
    """Describe every published cycle, separating stem role from branch climate."""
    day_master = _text(_map(payload.get("bazi")).get("day_master"))
    items = [item for item in cycles.get("cycles") or [] if isinstance(item, Mapping)]
    if not day_master or not items:
        return []
    useful = _map(payload.get("useful_god"))
    use_stem = _text(useful.get("useful_stem"))
    use_element = _text(useful.get("useful_element"))
    favorable = {_text(item.get("element")) for item in useful.get("favorable_roles") or [] if isinstance(item, Mapping)}
    unfavorable = {_text(item.get("element")) for item in useful.get("unfavorable_roles") or [] if isinstance(item, Mapping)}
    current = _map(cycles.get("current_cycle"))
    paragraphs = [
        f"Cách đọc Đại vận: Đại vận khởi khoảng {cycles.get('start_age')} tuổi và đi {cycles.get('direction_label') or cycles.get('direction') or 'theo chiều đã tính'}. "
        "Mỗi chặng cho biết môi trường tác động lên nền lá số. Khi đọc một vận, cần tách vai trò Thập thần của Thiên Can "
        "và khí của Địa Chi, sau đó mới đặt chúng bên cạnh Dụng thần."
    ]
    for item in items:
        stem = _text(item.get("stem"))
        branch = _text(item.get("branch"))
        if not stem or not branch:
            continue
        try:
            god, _ = map_stem_to_ten_god(day_master, stem)
        except (ValueError, TenGodsValidationError):
            continue
        theme, action = _GOD_THEMES.get(god, ("nhìn lại cách sử dụng nguồn lực", "đối chiếu công việc và hoàn cảnh thực tế"))
        label = _text(item.get("gan_zhi")) or f"{stem} {branch}"
        start, end = item.get("year_start"), item.get("year_end")
        age_start, age_end = item.get("age_start"), item.get("age_end")
        context = f"{start}–{end}, khoảng {age_start}–{age_end} tuổi" if None not in (start, end, age_start, age_end) else "một chặng Đại vận"
        element = _text(item.get("branch_element"))
        climate = (
            f"Chi {branch} thuộc {element}, chạm tới hướng ngũ hành cần bồi trong lá số. "
            if element and element in favorable else
            f"Chi {branch} thuộc {element}, cần xem liệu nó có làm phần khí vốn đã mạnh thêm quá mức. "
            if element and element in unfavorable else
            f"Chi {branch} thuộc {element}; riêng hành của chi chưa đủ để gọi cả vận là tốt hoặc xấu. "
            if element else "Cần đặt địa chi cạnh toàn cục trước khi đánh giá vận. "
        )
        if stem == use_stem:
            nuance = f"Can {stem} chính là can Dụng thần đã chọn; địa chi và lưu niên vẫn cần xét riêng. "
        elif _text(item.get("stem_element")) == use_element and use_stem:
            nuance = f"Can {stem} cùng hành {use_element} với Dụng thần {use_stem} nhưng mang vai trò {god} riêng; không đồng nhất hai can. "
        else:
            nuance = ""
        if god == "Chính Tài" and element in favorable and use_stem:
            nuance += "Đây là dịp xem cách chuyển chuyên môn thành dòng thu có chuẩn, không phải lời hứa riêng cho từng năm trong vận. "
        elif god == "Chính Quan" and element in unfavorable:
            nuance += "Hành của chi cần được giữ vừa sức để chuẩn mực không biến thành thêm tầng nghĩa vụ. "
        elif god == "Thiên Ấn" and branch == "Thân" and _text(_pill(payload, "year").get("branch")) == "Dần":
            nuance += "Thân và Dần có quan hệ xung; chỉ luận thành sự kiện khi có thêm toàn cục và thời điểm kích hoạt. "
        if god == "Chính Tài":
            nuance += (
                f"Can {stem} đặt trọng tâm vào việc tạo nguồn thu từ giá trị có người nhận: "
                "cần làm rõ sản phẩm, giá bán, chi phí và phần tiền giữ lại. "
                f"Khí {element or 'của chi'} ở chi {branch} chỉ là bối cảnh thúc đẩy hoặc thử thách "
                "cách quản lý ấy, không biến Chính Tài thành Quan hay Sát. "
            )
        elif god == "Thất Sát":
            nuance += (
                f"Can {stem} đưa thử thách, áp lực cạnh tranh và trách nhiệm xử lý việc khó "
                "ra phía trước; cần xác định quyền quyết định và sức của đội ngũ trước khi nhận việc. "
                + (f"Dù cùng hành {use_element}, {stem} là Thất Sát, còn {use_stem} là can Dụng thần; "
                   "không thể đọc hai can như cùng một vai trò. "
                   if use_stem and _text(item.get('stem_element')) == use_element and stem != use_stem else "")
            )
        is_current = bool(current and item.get("index") == current.get("index"))
        prefix = "Vận đang đi qua" if is_current else "Đại vận"
        paragraphs.append(f"{prefix} {label} ({context}): {stem} là {god} của Nhật Chủ {day_master}, gợi chủ đề {theme}. "
                          f"{climate}{nuance}{_GOD_LONG_VIEW.get(god, '')} Bạn có thể {action}.")
    paragraphs.append("Khi chọn thời điểm: Muốn biết năm nào nên mở rộng hoặc giảm tải, hãy đọc thêm lưu niên "
                      "cùng sức khỏe, dòng tiền, gia đình và nguồn lực thực tế. Đại vận không tự ấn định chức vụ, tài sản, bệnh hay tuổi thọ.")
    return paragraphs


def synthesis_prose(payload: Mapping[str, Any]) -> list[str]:
    """Connect the approved chapters without asserting life events."""
    bazi = _map(payload.get("bazi"))
    stem = _text(bazi.get("day_master"))
    if not stem:
        return []
    try:
        stem_info = day_master_info(stem)
        stem_nature = f"{stem} thuộc {stem_info['yin_yang']} {stem_info['element']}"
    except TenGodsValidationError:
        stem_nature = stem
    strength = _text(_map(payload.get("strength")).get("strength_level"))
    pattern = _text(_map(payload.get("pattern")).get("cach_cuc"))
    useful = _map(payload.get("useful_god"))
    use_stem, use_element = _text(useful.get("useful_stem")), _text(useful.get("useful_element"))
    year, month, day, hour = (_pill(payload, key) for key in ("year", "month", "day", "hour"))
    cycle = _map(_map(payload.get("luck")).get("current_cycle"))
    title = f"{use_stem} {use_element}".strip()
    strong = strength in ("strong", "very_strong")
    paragraphs = [
        "Trục mệnh: " + (f"Nhật Chủ {stem_nature} ở thế Thân vượng" if strong else f"Nhật Chủ {stem_nature} với thế Thân đã công bố")
        + (f", mang Mệnh cục {pattern}" if pattern else "")
        + (f" và lấy {title} làm Dụng thần" if title else "")
        + ". Điều đáng giữ ở đây là năng lực học, chọn và theo đuổi việc khó; "
        "điều làm năng lực ấy đáng tin là một tiêu chuẩn có thể giải thích và giao kết quả cho người khác."
        if strong and pattern == "Chính Ấn" else
        "Trục mệnh: " + f"Nhật Chủ {stem_nature}" + (f", Mệnh cục {pattern}" if pattern else "")
        + (f", hướng Dụng thần {title}" if title else "")
        + ". Đây là ba dữ kiện cần đọc cùng nhau khi lựa chọn công việc và nhịp sống, "
        "không suy ra sẵn một nghề hay kết quả duy nhất."
    ]
    tai = _has(payload, "Chính Tài", "Thiên Tài")
    peer = _text(month.get("ten_god"))
    if tai or peer:
        paragraphs.append("Đường nghề và tiền: "
            + ("Tài tinh có mặt trong lá số gợi đường biến chuyên môn thành việc có người nhận và sẵn lòng trả tiền. " if tai else
               "Thu nhập cần được kiểm chứng bằng sản phẩm, khách hàng và phần tiền giữ lại. ")
            + (f"{peer} ở trụ tháng nhắc bạn định rõ việc chung, vốn góp và quyền quyết định khi làm với người ngang vai. "
               if peer in ("Kiếp Tài", "Tỷ Kiên") else "")
            + "Một doanh thu lớn nhưng luôn phải dùng hết sức mình để tạo lại chưa hẳn là một nền tài chính bền.")
    day_branch = _text(day.get("branch"))
    hour_branch = _text(hour.get("branch"))
    if day_branch or hour_branch:
        paragraphs.append("Người thân và sức bền: "
            + (f"Trụ ngày {stem} {day_branch} nhắc đặt lời hứa, thời gian và cách lắng nghe vào quan hệ gần gũi. " if day_branch else "")
            + (f"Trụ giờ {hour.get('stem', '')} {hour_branch} gợi câu hỏi bạn muốn trao lại điều gì cho người đến sau. " if hour_branch else "")
            + "Giữ lịch nghỉ và chia trách nhiệm rõ sẽ giúp bạn theo đường dài; một trụ riêng không kết luận hôn nhân, số con hay sức khỏe.")
    current_name = _text(cycle.get("gan_zhi"))
    if current_name:
        start, end = cycle.get("year_start"), cycle.get("year_end")
        window = f" ({start}–{end})" if start and end else ""
        paragraphs.append(f"Chặng hiện tại: Đại vận {current_name}{window} là bối cảnh để xem "
            "chuyên môn, trách nhiệm và dòng thu đang gặp thời như thế nào. "
            + (f"{_text(cycle.get('stem'))} của vận không tự đồng nhất với Dụng thần {use_stem}; "
               if _text(cycle.get("stem")) and use_stem and cycle.get("stem") != use_stem else "")
            + "khi chọn một năm hay quyết định lớn, hãy đặt thêm lưu niên và điều kiện thực tế cạnh Đại vận.")
    paragraphs.append("Điểm chốt: Lá số đưa ra một cách nhìn về nguồn lực và thời điểm. "
                      "Điều có thể thay đổi bằng tay bạn là cách làm việc, giữ tiền, chăm quan hệ và giữ sức; "
                      "mỗi bước nên có tiêu chí kiểm tra được trong đời sống thực.")
    return paragraphs


def recommendation_prose(payload: Mapping[str, Any]) -> list[str]:
    """Actionable steps selected from the same published facts as the synthesis."""
    bazi = _map(payload.get("bazi"))
    if not _text(bazi.get("day_master")):
        return []
    useful = _map(payload.get("useful_god"))
    pattern = _text(_map(payload.get("pattern")).get("cach_cuc"))
    cycle = _map(_map(payload.get("luck")).get("current_cycle"))
    use_stem, use_element = _text(useful.get("useful_stem")), _text(useful.get("useful_element"))
    current_name = _text(cycle.get("gan_zhi"))
    peer = _text(_pill(payload, "month").get("ten_god")) in ("Kiếp Tài", "Tỷ Kiên")
    palace = _text(_map(payload.get("calendar")).get("cung_phi"))
    paragraphs = [
        "Việc làm trong tháng tới: Chọn một công việc hoặc dịch vụ có thể bàn giao; "
        "viết đầu vào cần có, kết quả sẽ giao, thời hạn và cách kiểm tra chất lượng. "
        + (f"Mệnh cục {pattern} giúp bạn xây phương pháp, " if pattern == "Chính Ấn" else "Hãy dùng thế mạnh của bạn để làm ra đầu ra rõ, ")
        + (f"còn Dụng thần {use_stem} {use_element} nhắc giữ trách nhiệm với lời đã hứa." if use_stem and use_element else
           "và nói rõ ai chịu trách nhiệm khi kết quả cần sửa."),
        "Tiền giữ được: Mỗi tháng tách số tiền thu về, chi phí để giao dịch vụ và phần còn lại. "
        "Giữ quỹ sinh hoạt, dự phòng và khoản tái đầu tư thành các phần riêng. "
        "Khi một ý tưởng cần thêm vốn, thử ở quy mô nhỏ và đặt trước mức chi có thể chịu được.",
        "Giữ sức khi mở việc: Chọn giờ làm việc sâu, giờ trả lời khách và một giới hạn nhận việc mỗi tuần. "
        "Nếu luôn phải làm thay người khác để kịp hạn, sửa khâu giao việc trước khi tiếp tục tăng số khách hoặc dự án.",
    ]
    if peer:
        paragraphs.append("Hợp tác có ranh giới: Với người cùng góp sức, hãy ghi rõ ai giữ hồ sơ, "
                          "ai chốt chi phí, ai chịu trách nhiệm trước khách và cách chia phần còn lại. "
                          "Làm rõ từ đầu giúp giữ cả quan hệ lẫn chất lượng công việc.")
    else:
        paragraphs.append("Quan hệ làm việc: Khi cần cộng sự, hãy thống nhất phạm vi, quyền quyết định "
                          "và cách đánh giá kết quả trước khi giao một phần công việc quan trọng.")
    if palace:
        paragraphs.append(f"Không gian dễ sử dụng: Cung Phi {palace} là lớp để khảo sát hướng; "
                          "hãy xem trước ánh sáng, độ thoáng, đường đi và chỗ trao đổi với khách. "
                          "Chỉ luận sâu hướng nhà khi có hướng đo, mặt bằng và năm vào ở; "
                          "không tăng một ngũ hành chỉ vì tên hành của Cung Phi.")
    if current_name:
        paragraphs.append(f"Chọn nhịp trong vận {current_name}: Cuối mỗi quý, nhìn lại "
                          "giá trị khách nhận được, phần tiền giữ lại, số giờ bản thân phải trực tiếp làm "
                          "và mức hồi phục sau công việc. Nếu cả bốn cùng tốt lên, bạn mới có cơ sở mở rộng; "
                          "quyết định năm cụ thể cần thêm lưu niên và hoàn cảnh thực tế.")
    return paragraphs
