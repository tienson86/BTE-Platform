"""Deterministic plain-language mappings — translate concepts, invent no doctrine."""

from __future__ import annotations

# Theme / concept → lived customer concept (not BaZi teaching).
THEME_TO_PLAIN: dict[str, str] = {
    "OPERATING_OUTPUT": "cần nhìn thấy đầu ra và kết quả rõ ràng",
    "OPERATING_SELF_CARRY": "dễ tự gánh và tự đẩy tiến độ",
    "OPERATING_STANDARDS": "nhạy với phạm vi trách nhiệm và kỳ vọng rõ ràng",
    "FOLLOW_STRUCTURE": "vận hành theo khung dài hạn riêng, không ép theo khuôn thường",
    "STANDARD_STRUCTURE": "cần nhất quán với khung dài hạn đã xác định",
    "CAPACITY_STRONG": "có nền chịu tải rõ",
    "CAPACITY_BALANCED": "cần nhịp tải và phục hồi cân bằng",
    "CAPACITY_WEAK": "cần bảo toàn năng lượng trước khi mở rộng",
    "BALANCE_DIRECTION": "cần một hướng điều tiết rõ trong tuần",
    "OVERLOAD_RISK": "rủi ro nhận thêm việc khi hệ đã căng",
}

# Operating role labels → work/life language.
STYLE_TO_PLAIN: dict[str, str] = {
    "Thương Quan": "kênh biểu đạt và tạo ra kết quả nhìn thấy được",
    "Thực Thần": "kênh làm ra / thể hiện năng lực qua sản phẩm cụ thể",
    "Thất Sát": "nhịp quyết nhanh dưới áp lực và tiêu chuẩn cao",
    "Chính Quan": "nhịp trách nhiệm và phạm vi quyết định rõ",
    "Tỷ Kiên": "tự lực và đồng hành ngang hàng",
    "Kiếp Tài": "chia sẻ tải và cạnh tranh tài nguyên trong nhóm",
    "Chính Ấn": "học hỏi, chuẩn bị và khung hỗ trợ dài hạn",
    "Thiên Ấn": "không gian suy nghĩ và chất lượng nội tại",
    "Chính Tài": "quản lý nguồn lực có kiểm soát",
    "Thiên Tài": "linh hoạt với cơ hội và nguồn lực biến động",
}

# Capacity cues from claim plan body:* fragments.
CAPACITY_TO_PLAIN: dict[str, str] = {
    "balanced": "nền năng lượng trung hòa — mạnh khi giữ nhịp, yếu khi ép quá sức",
    "strong": "nền chịu tải vững — mạnh khi chuyển tải thành đầu ra có định nghĩa",
    "very_strong": "nền chịu tải rất vững — rủi ro chính là ôm thêm vô hạn",
    "weak": "nền cần bảo toàn — ưu tiên phục hồi trước mở rộng",
    "very_weak": "nền cần bảo vệ chặt — tránh mở rộng tải sớm",
}

# Priority keys → concrete action sentences.
PRIORITY_TO_ACTION: dict[str, str] = {
    "align_operating_role": (
        "Điều phối tuần làm việc quanh kênh vận hành đã rõ — "
        "đừng nhận việc trái nhịp chỉ vì đang trống lịch."
    ),
    "apply_balance": (
        "Giữ hướng điều tiết như thói quen tuần: làm dịu cường độ khi hệ nóng, "
        "không chờ đến lúc kiệt mới nghỉ."
    ),
    "keep_load_recovery_rhythm": (
        "Xen nhịp tải và phục hồi trong tuần; trước khi nhận thêm việc, "
        "xác định việc nào tự quyết và việc nào giao lại."
    ),
    "convert_load_to_defined_output": (
        "Chuyển việc đang mang thành đầu ra có định nghĩa rõ trong tuần — "
        "không chỉ giữ việc trên vai."
    ),
    "keep_structure_consistency": (
        "Giữ nhất quán khung dài hạn; đừng đổi khung mỗi khi áp lực ngắn hạn tăng."
    ),
}

# Avoidance keys → concrete don'ts.
AVOID_TO_ACTION: dict[str, str] = {
    "avoid_reflex_extra_load": (
        "Đừng nhận thêm đầu việc theo phản xạ khi hệ đã căng."
    ),
    "avoid_forcing_ordinary_daymaster_frame": (
        "Đừng ép mình vào khuôn ‘làm việc như mọi người’ nếu khung dài hạn của bạn là kiểu riêng."
    ),
    "avoid_suppressing_expression_channel": (
        "Đừng dập tắt kênh biểu đạt và tạo ra kết quả — đó là mạch vận hành, không phải phần thêm."
    ),
    "avoid_overexertion_cycles": (
        "Đừng ép chu kỳ làm việc quá sức khi nền đang cần cân bằng."
    ),
    "avoid_claims_beyond_published_data": (
        "Đừng kết luận ngoài phạm vi dữ liệu đã có."
    ),
}

# Relation / constraint ids → limitation language (customer-safe).
CONSTRAINT_TO_PLAIN: dict[str, str] = {
    "follow_qualifies_strength": (
        "Khung dài hạn riêng định hình cách đọc nền năng lượng thường — "
        "hai tín hiệu đều đúng trong phạm vi của chúng, không chọn một cái xóa cái kia."
    ),
    "str_pattern_scope": (
        "Nội lực thân và khung cấu trúc dài hạn là hai khía cạnh khác nhau — cần đọc cùng nhau."
    ),
    "follow_strength_nuance": (
        "Nền năng lượng công bố và khung riêng cùng đúng trong phạm vi của chúng."
    ),
    "OVERLOAD_RISK": (
        "Rủi ro chính là ôm thêm tải khi vẫn còn làm được — sức mạnh dễ thành gánh quá."
    ),
    "tg_vs_pattern_scope": (
        "Cách vận hành hàng ngày và khung dài hạn là hai lớp — không gộp thành một nhãn."
    ),
}

# Stems used only as balance pivots → lived cooling/support language (no doctrine).
STEM_BALANCE_HINT: dict[str, str] = {
    "Nhâm": "làm dịu cường độ, tạo khoảng nghỉ và dòng chảy ổn định hơn",
    "Quý": "giữ mềm mại và phục hồi tinh tế",
    "Canh": "cắt giảm phần thừa, làm rõ biên",
    "Thực Thần": "nhả tải bằng cách tạo ra sản phẩm / kết quả cụ thể",
    "Thương Quan": "nhả tải bằng biểu đạt và đầu ra nhìn thấy được",
}

FORBIDDEN_CUSTOMER_TOKENS: tuple[str, ...] = (
    "claim_id",
    "TRUE_CONFLICT",
    "DEPENDENCY_OVERRIDE",
    "CONDITIONAL_NUANCE",
    "DIFFERENT_SCOPE",
    "UNRESOLVED",
    "theme_id",
    "align_operating_role:",
    "apply_balance:",
    "keep_load_recovery_rhythm",
    "convert_load_to_defined_output",
    "keep_structure_consistency:",
    "avoid_reflex_extra_load",
    "avoid_forcing_ordinary_daymaster_frame",
    "avoid_suppressing_expression_channel",
    "avoid_overexertion_cycles",
    "avoid_claims_beyond_published_data",
    "balance:",
    "body:",
    "structure:",
    "OPERATING_OUTPUT",
    "OPERATING_SELF_CARRY",
    "FOLLOW_STRUCTURE",
    "CAPACITY_STRONG",
    "CAPACITY_BALANCED",
    "DRAFT_KNOWLEDGE",
)


def plain_theme(theme_id: str) -> str:
    """Map theme id to plain concept."""
    return THEME_TO_PLAIN.get(theme_id, "")


def plain_style(style: str) -> str:
    """Map operating style label to plain language."""
    style = (style or "").strip()
    if not style:
        return ""
    if style in STYLE_TO_PLAIN:
        return STYLE_TO_PLAIN[style]
    # Multi-label "A, B"
    parts = [p.strip() for p in style.replace("·", ",").split(",") if p.strip()]
    mapped = [STYLE_TO_PLAIN.get(p, "") for p in parts]
    mapped = [m for m in mapped if m]
    if mapped:
        return mapped[0] if len(mapped) == 1 else " và ".join(mapped[:2])
    return f"vai trò vận hành {style}"


def plain_capacity(cue: str) -> str:
    """Map body capacity cue."""
    key = (cue or "").strip().lower()
    if key.startswith("body:"):
        key = key.split(":", 1)[1]
    return CAPACITY_TO_PLAIN.get(key, "")


def plain_balance(cue: str) -> str:
    """Map balance direction to lived guidance."""
    raw = (cue or "").strip()
    if raw.lower().startswith("balance:"):
        raw = raw.split(":", 1)[1].strip()
    hint = STEM_BALANCE_HINT.get(raw, "")
    if hint:
        return f"hướng điều tiết nghiêng về {hint}"
    if raw:
        return f"hướng điều tiết đã công bố ({raw}) — ưu tiên nhịp làm dịu và làm rõ biên"
    return ""


def plain_priority(item: str) -> str:
    """Map priority key or key:value to action sentence."""
    item = (item or "").strip()
    if not item:
        return ""
    key, _, rest = item.partition(":")
    base = PRIORITY_TO_ACTION.get(key, "")
    if not base:
        return item if " " in item else ""
    if rest and key == "align_operating_role":
        style = plain_style(rest)
        return (
            f"Điều phối tuần làm việc quanh {style} — "
            "đừng nhận việc trái nhịp chỉ vì đang trống lịch."
        )
    if rest and key == "apply_balance":
        bal = plain_balance(rest)
        return (
            f"Giữ {bal} như thói quen tuần, không chờ đến lúc kiệt mới điều chỉnh."
        )
    if rest and key == "keep_structure_consistency":
        return (
            "Giữ nhất quán khung dài hạn đã xác định; "
            "đừng đổi khung mỗi khi áp lực ngắn hạn tăng."
        )
    return base


def plain_avoid(item: str) -> str:
    """Map avoidance key to action sentence."""
    item = (item or "").strip()
    return AVOID_TO_ACTION.get(item, item if " " in item and "avoid_" not in item else "")


def plain_constraint(key: str) -> str:
    """Map constraint / relation id to limitation prose."""
    return CONSTRAINT_TO_PLAIN.get((key or "").strip(), "")


def parse_identity_core(identity_core: str) -> tuple[str, str, str]:
    """Extract theme-ish, capacity, structure cues from plan identity_core."""
    text = identity_core or ""
    capacity = ""
    structure = ""
    theme_hint = ""
    for part in text.split("|"):
        part = part.strip()
        low = part.lower()
        if low.startswith("body:"):
            capacity = part.split(":", 1)[1].strip()
        elif low.startswith("structure:"):
            structure = part.split(":", 1)[1].strip()
        elif part and not theme_hint:
            theme_hint = part
    return theme_hint, capacity, structure


def structure_to_plain(structure: str) -> str:
    """Lived framing for structure labels without teaching theory."""
    s = (structure or "").strip()
    if not s:
        return ""
    low = s.lower()
    if "tòng" in low or "tong" in low:
        return (
            "khung dài hạn kiểu riêng (không ép theo khuôn thông thường) — "
            "cần được tôn trọng khi tự đánh giá bản thân"
        )
    if "ấn" in low:
        return "khung dài hạn nghiêng về chuẩn bị, hỗ trợ và ổn định nền"
    if "tài" in low:
        return "khung dài hạn nghiêng về quản lý nguồn lực và cơ hội"
    if "quan" in low or "sát" in low:
        return "khung dài hạn nghiêng về trách nhiệm, ranh giới và chuẩn"
    if "thương" in low or "thực" in low:
        return "khung dài hạn nghiêng về làm ra và thể hiện"
    return "khung dài hạn cần giữ nhất quán — không đổi mỗi khi áp lực ngắn hạn tăng"


def contains_forbidden_leak(text: str) -> list[str]:
    """Return forbidden tokens found in customer text."""
    found: list[str] = []
    for token in FORBIDDEN_CUSTOMER_TOKENS:
        if token in text:
            found.append(token)
    return found
