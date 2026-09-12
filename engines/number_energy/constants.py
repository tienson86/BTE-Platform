"""Frozen V1 constants from NUMBER_ENERGY_MASTER_KNOWLEDGE_V1.

Do not add pair groups, control relations, or meanings beyond the canonical files.
"""

from __future__ import annotations

from typing import Final

KNOWLEDGE_VERSION: Final[str] = "1.0"
SYSTEM_NAME: Final[str] = "Bát Cực Linh Số"
SYSTEM_SHORT_NAME: Final[str] = "Năng lượng số"
UNKNOWN_REASON_NOT_FROZEN: Final[str] = (
    "rule not frozen in NUMBER_ENERGY_INTERACTION_RULES_V1"
)
CONSECUTIVE_MODIFIER_REASON: Final[str] = (
    "consecutive modifiers are not frozen in V1"
)
UNUSED_MODIFIER_REASON: Final[str] = (
    "edge or unused modifier 0/5 without a frozen A-M-B window"
)
APPROVED_SUPPORTIVE_CHAIN_SEQUENCE: Final[str] = "141319"
APPROVED_SUPPORTIVE_CHAIN_ID: Final[str] = "approved_supportive_chain"
HEALTH_DISCLAIMER: Final[str] = (
    "Phần này chỉ mang ý nghĩa tham khảo theo hệ thống Năng lượng số, "
    "không phải chẩn đoán y khoa."
)
COMPATIBILITY_NOTE: Final[str] = (
    "Không kết luận tương hợp cuối cùng với chủ số khi chưa có dữ liệu "
    "Cung Phi hoặc Bát Tự."
)
CHALLENGING_CUSTOMER_LABEL: Final[str] = "trường khí cần kiểm soát"
CLASSIFICATION_CUSTOMER_LABELS: Final[dict[str, str]] = {
    "supportive": "trường khí hỗ trợ",
    "supportive_stabilizing": "trường khí ổn định",
    "challenging": CHALLENGING_CUSTOMER_LABEL,
}
PATTERN_CUSTOMER_LABELS: Final[dict[str, str]] = {
    APPROVED_SUPPORTIVE_CHAIN_ID: (
        "Chuỗi hỗ trợ đã khóa: Sinh Khí → Thiên Y → Diên Niên"
    ),
}
UNDEFINED_REASON_CUSTOMER_VI: Final[dict[str, str]] = {
    UNKNOWN_REASON_NOT_FROZEN: (
        "Đoạn này chưa được khóa trong quy tắc tương tác V1."
    ),
    CONSECUTIVE_MODIFIER_REASON: (
        "Các số 0 hoặc 5 đứng liền nhau chưa được khóa trong V1, "
        "nên không suy diễn thêm quy tắc."
    ),
    UNUSED_MODIFIER_REASON: (
        "Số 0 hoặc 5 ở mép dãy chưa tạo cửa sổ A-M-B đã khóa trong V1."
    ),
}

# Operational input bound for phone / plate / ID / account strings. Not a V2 rule.
MAX_INPUT_DIGITS: Final[int] = 128


def is_ascii_digit_string(value: str) -> bool:
    """Return True if ``value`` is a non-empty ASCII ``0-9`` string."""
    return bool(value) and value.isascii() and value.isdigit()


ORDINARY_GUA_DIGITS: Final[frozenset[int]] = frozenset({1, 2, 3, 4, 6, 7, 8, 9})
MODIFIER_DIGITS: Final[frozenset[int]] = frozenset({0, 5})

LINE_DIA: Final[str] = "dia"
LINE_NHAN: Final[str] = "nhan"
LINE_THIEN: Final[str] = "thien"
LINE_ORDER: Final[tuple[str, str, str]] = (LINE_DIA, LINE_NHAN, LINE_THIEN)

# Vector order is [Địa, Nhân, Thiên] and must not be reordered.
TRIGRAM_VECTORS: Final[dict[int, tuple[int, int, int]]] = {
    6: (1, 1, 1),
    7: (1, 1, 0),
    9: (1, 0, 1),
    3: (1, 0, 0),
    4: (0, 1, 1),
    1: (0, 1, 0),
    8: (0, 0, 1),
    2: (0, 0, 0),
}

LINE_DIFF_TO_ENERGY: Final[dict[frozenset[str], str]] = {
    frozenset(): "fu_wei",
    frozenset({LINE_THIEN}): "sheng_qi",
    frozenset({LINE_NHAN}): "jue_ming",
    frozenset({LINE_DIA}): "huo_hai",
    frozenset({LINE_THIEN, LINE_NHAN}): "wu_gui",
    frozenset({LINE_NHAN, LINE_DIA}): "tian_yi",
    frozenset({LINE_THIEN, LINE_DIA}): "liu_sha",
    frozenset({LINE_THIEN, LINE_NHAN, LINE_DIA}): "yan_nian",
}

ENERGY_DISPLAY_NAMES: Final[dict[str, str]] = {
    "sheng_qi": "Sinh Khí",
    "tian_yi": "Thiên Y",
    "yan_nian": "Diên Niên",
    "fu_wei": "Phục Vị",
    "huo_hai": "Họa Hại",
    "wu_gui": "Ngũ Quỷ",
    "liu_sha": "Lục Sát",
    "jue_ming": "Tuyệt Mệnh",
}
ENERGY_INTERACTION_CODES: Final[dict[str, str]] = {
    "sheng_qi": "SK",
    "tian_yi": "TY",
    "yan_nian": "DN",
    "fu_wei": "PV",
    "liu_sha": "LS",
    "huo_hai": "HH",
    "wu_gui": "NQ",
    "jue_ming": "TM",
}
TRIPLE_PRIORITY_FEATURED: Final[str] = "FEATURED"
TRIPLE_PRIORITY_STANDARD: Final[str] = "STANDARD"
TRIPLE_PRIORITY_COMPACT: Final[str] = "COMPACT"
TRIPLE_STATUS_DEFINED: Final[str] = "DEFINED"
TRIPLE_STATUS_UNDEFINED: Final[str] = "UNDEFINED"

ENERGY_CLASSIFICATION: Final[dict[str, str]] = {
    "sheng_qi": "supportive",
    "tian_yi": "supportive",
    "yan_nian": "supportive",
    "fu_wei": "supportive_stabilizing",
    "huo_hai": "challenging",
    "wu_gui": "challenging",
    "liu_sha": "challenging",
    "jue_ming": "challenging",
}
SUPPORTIVE_ENERGY_IDS: Final[frozenset[str]] = frozenset(
    {
        "sheng_qi",
        "tian_yi",
        "yan_nian",
        "fu_wei",
    }
)
CHALLENGING_ENERGY_IDS: Final[frozenset[str]] = frozenset(
    {
        "huo_hai",
        "wu_gui",
        "liu_sha",
        "jue_ming",
    }
)
# Canonical catalog order for P-S05 (Golden §19). Includes zero-count rows.
ENERGY_DISTRIBUTION_ORDER: Final[tuple[str, ...]] = tuple(ENERGY_DISPLAY_NAMES)
CUSTOMER_CATEGORY_CAT: Final[str] = "CAT"
CUSTOMER_CATEGORY_HUNG: Final[str] = "HUNG"
CUSTOMER_CATEGORY_LABELS: Final[dict[str, str]] = {
    CUSTOMER_CATEGORY_CAT: "Cát",
    CUSTOMER_CATEGORY_HUNG: "Hung",
}
CUSTOMER_STRENGTH_LIGHT: Final[str] = "Nhẹ"
CUSTOMER_STRENGTH_STRONG: Final[str] = "Mạnh"
STRENGTH_SLOT_COUNT: Final[int] = 4
# Knowledge 03 tiers T1–T2 → Mạnh; T3–T4 → Nhẹ. Rank 1 is strongest.
RANK_TO_STRENGTH_LABEL: Final[dict[int, str]] = {
    1: CUSTOMER_STRENGTH_STRONG,
    2: CUSTOMER_STRENGTH_STRONG,
    3: CUSTOMER_STRENGTH_LIGHT,
    4: CUSTOMER_STRENGTH_LIGHT,
}
RANK_TO_STRENGTH_SLOTS: Final[dict[int, int]] = {
    1: 4,
    2: 3,
    3: 2,
    4: 1,
}
FORCE_LABELS: Final[dict[int, str]] = {
    1: "lực rất mạnh",
    2: "lực mạnh",
    3: "lực vừa",
    4: "lực nhẹ",
}
STATE_CUSTOMER_LABELS: Final[dict[str, str]] = {
    "HIDDEN": "Bị che bởi số 0",
    "AMPLIFIED": "Được kích hoạt",
    "REPEATED": "Lặp lại",
    "CONTROLLED": "Được cát tinh nâng đỡ",
    "NORMAL": "",
    "NEUTRALIZED": "Được cát tinh nâng đỡ",
    "UNKNOWN_OR_NOT_DEFINED": "Chưa đủ dữ liệu V1 để luận phần này",
}
PHONE_LEADING_ZERO_NOTE: Final[str] = "Sim này có đầu số 0 hợp lệ."
PHONE_INTERIOR_ZERO_NOTE: Final[str] = (
    "Số 0 chỉ nên xuất hiện ở đầu số điện thoại. "
    "Khi xuất hiện trong thân số, năng lượng dễ bị che hoặc đứt mạch."
)
PHONE_SUPPORTIVE_BALANCED: Final[str] = "Cấu trúc cát tinh khá cân bằng."
PHONE_SUPPORTIVE_FEW: Final[str] = "Cần thêm trường hỗ trợ để dãy số vững hơn."
PHONE_SUPPORTIVE_SKEWED: Final[str] = (
    "Cát tinh có lực nhưng cần xem có bị lệch về một nhóm năng lượng hay không."
)
PHONE_CONSECUTIVE_CHALLENGING: Final[str] = (
    "Dãy số có nhiều trường khí cần kiểm soát đứng liền nhau, "
    "dễ tạo cảm giác bất ổn nếu không có cát tinh đủ lực cân bằng."
)
PHONE_CONSECUTIVE_CHALLENGING_SOFT: Final[str] = (
    "Có chuỗi trường khí cần kiểm soát, nhưng dãy vẫn có cát tinh "
    "đủ lực để cân bằng một phần."
)
PHONE_LIFTED_NOTE: Final[str] = (
    "Hung tinh được cát tinh phía sau nâng đỡ, nên ảnh hưởng bất lợi "
    "có cơ hội được kéo về hướng tốt hơn."
)
PHONE_FORCE_WINS: Final[str] = "Cát tinh đủ lực áp chế/chuyển hóa phần bất lợi."
PHONE_FORCE_SHORT: Final[str] = (
    "Cát tinh có hỗ trợ nhưng chưa đủ lực áp chế hoàn toàn."
)
PHONE_ENDING_SUPPORTIVE: Final[str] = "Năng lượng kết là cát tinh, hướng kết dãy thuận."
PHONE_ENDING_CHALLENGING: Final[str] = (
    "Năng lượng kết là trường khí cần kiểm soát, nên xem lại bộ số cuối."
)
PHONE_ENDING_UNKNOWN: Final[str] = (
    "Chưa đủ dữ liệu V1 để kết luận năng lượng kết."
)
PHONE_PURPOSE_NOTE: Final[str] = (
    "Không phải sim nào nhiều cát tinh cũng phù hợp với mọi người. "
    "Cần xét mục đích sử dụng và căn mệnh ở lớp phân tích sau."
)
PHONE_CCCD_NOTE: Final[str] = (
    "Lớp hóa giải theo CCCD chưa chạy trong phiên bản này. "
    "Khi có dữ liệu định danh, sẽ xét năng lượng kết và khí lực sim "
    "so với từ trường CCCD."
)
INCOMPLETE_CUSTOMER_NOTICE: Final[str] = "Chưa đủ dữ liệu V1 để luận phần này."
SUPPORTIVE_THEME_SHORT: Final[dict[str, str]] = {
    "sheng_qi": "quý nhân",
    "tian_yi": "tài khí",
    "yan_nian": "ổn định, trách nhiệm",
    "fu_wei": "duy trì",
}

# Rank 1 is strongest expression; do not convert to numeric scores in V1.
ENERGY_PAIR_RANKS: Final[dict[str, dict[int, tuple[str, str]]]] = {
    "sheng_qi": {
        1: ("14", "41"),
        2: ("67", "76"),
        3: ("39", "93"),
        4: ("28", "82"),
    },
    "tian_yi": {
        1: ("13", "31"),
        2: ("68", "86"),
        3: ("49", "94"),
        4: ("27", "72"),
    },
    "yan_nian": {
        1: ("19", "91"),
        2: ("78", "87"),
        3: ("34", "43"),
        4: ("26", "62"),
    },
    "fu_wei": {
        1: ("11", "22"),
        2: ("88", "99"),
        3: ("66", "77"),
        4: ("33", "44"),
    },
    "huo_hai": {
        1: ("17", "71"),
        2: ("89", "98"),
        3: ("46", "64"),
        4: ("23", "32"),
    },
    "wu_gui": {
        1: ("18", "81"),
        2: ("79", "97"),
        3: ("36", "63"),
        4: ("24", "42"),
    },
    "liu_sha": {
        1: ("16", "61"),
        2: ("47", "74"),
        3: ("38", "83"),
        4: ("29", "92"),
    },
    "jue_ming": {
        1: ("12", "21"),
        2: ("69", "96"),
        3: ("48", "84"),
        4: ("37", "73"),
    },
}

DIGIT_PROFILES: Final[dict[int, dict[str, str | None]]] = {
    1: {
        "internal_type": "gua",
        "gua_or_field": "Khảm",
        "direction": "Bắc",
        "element": "Thủy",
        "group": "Đông tứ",
        "pair_role": "normal pair digit",
    },
    2: {
        "internal_type": "gua",
        "gua_or_field": "Khôn",
        "direction": "Tây Nam",
        "element": "Thổ",
        "group": "Tây tứ",
        "pair_role": "normal pair digit",
    },
    3: {
        "internal_type": "gua",
        "gua_or_field": "Chấn",
        "direction": "Đông",
        "element": "Mộc",
        "group": "Đông tứ",
        "pair_role": "normal pair digit",
    },
    4: {
        "internal_type": "gua",
        "gua_or_field": "Tốn",
        "direction": "Đông Nam",
        "element": "Mộc",
        "group": "Đông tứ",
        "pair_role": "normal pair digit",
    },
    5: {
        "internal_type": "modifier",
        "gua_or_field": "Dương trường / Trung cung Dương",
        "direction": "Trung cung",
        "element": "Thổ",
        "group": "Trung",
        "pair_role": "modifier only",
    },
    6: {
        "internal_type": "gua",
        "gua_or_field": "Càn",
        "direction": "Tây Bắc",
        "element": "Kim",
        "group": "Tây tứ",
        "pair_role": "normal pair digit",
    },
    7: {
        "internal_type": "gua",
        "gua_or_field": "Đoài",
        "direction": "Tây",
        "element": "Kim",
        "group": "Tây tứ",
        "pair_role": "normal pair digit",
    },
    8: {
        "internal_type": "gua",
        "gua_or_field": "Cấn",
        "direction": "Đông Bắc",
        "element": "Thổ",
        "group": "Tây tứ",
        "pair_role": "normal pair digit",
    },
    9: {
        "internal_type": "gua",
        "gua_or_field": "Ly",
        "direction": "Nam",
        "element": "Hỏa",
        "group": "Đông tứ",
        "pair_role": "normal pair digit",
    },
    0: {
        "internal_type": "modifier",
        "gua_or_field": "Âm trường / Trung cung Âm",
        "direction": "Trung cung",
        "element": None,
        "group": "Trung",
        "pair_role": "modifier only",
    },
}

# Challenging energy -> controlling supportive energy. Họa Hại has no direct pair.
CONTROL_RELATIONS: Final[dict[str, str]] = {
    "wu_gui": "sheng_qi",
    "jue_ming": "tian_yi",
    "liu_sha": "yan_nian",
}

FU_WEI_SUPPORT_ENERGIES: Final[frozenset[str]] = frozenset({"sheng_qi", "tian_yi"})
HUO_HAI_ID: Final[str] = "huo_hai"
FU_WEI_ID: Final[str] = "fu_wei"

PURPOSE_FOCUS: Final[dict[str, str]] = {
    "phone_number": "communication, relationship, wealth, career flow, daily use",
    "car_plate": (
        "movement, safety symbolism, work mobility, asset stability, financial flow"
    ),
    "motorbike_plate": (
        "mobility, daily movement, personal rhythm, practical safety symbolism"
    ),
    "id_number": "long-term identity imprint, life themes, owner compatibility",
    "bank_account": "wealth flow, retention, risk, transaction stability",
    "house_number": (
        "family stability, rest, health symbolism, long-term field"
    ),
    "generic_number": "only intrinsic number-energy unless owner/context supplied",
}

CUSTOMER_PRESENTATION_CONTEXTS: Final[frozenset[str]] = frozenset(
    {"phone_number", "car_plate", "motorbike_plate", "id_number"}
)

FORBIDDEN_CUSTOMER_PHRASES: Final[tuple[str, ...]] = (
    "chắc chắn gây bệnh",
    "chắc chắn phá sản",
    "chắc chắn ly hôn",
    "chắc chắn phát tài",
    "chắc chắn giữ được tiền",
    "về già chắc chắn",
    "đổi số ngay",
    "mua số ngay",
    "mua sim",
    "0 triệt tiêu hoàn toàn nên không còn tác động",
    "5 biến thành quái số bình thường",
)


def build_pair_lookup() -> dict[str, tuple[str, int]]:
    """Build pair-digit lookup: ``'14' -> ('sheng_qi', 1)``."""
    lookup: dict[str, tuple[str, int]] = {}
    for energy_id, ranks in ENERGY_PAIR_RANKS.items():
        for rank, pairs in ranks.items():
            for pair in pairs:
                lookup[pair] = (energy_id, rank)
    return lookup


PAIR_LOOKUP: Final[dict[str, tuple[str, int]]] = build_pair_lookup()


def is_ordinary_gua(digit: int) -> bool:
    """Return True if ``digit`` is an ordinary pair gua."""
    return digit in ORDINARY_GUA_DIGITS


def is_modifier(digit: int) -> bool:
    """Return True if ``digit`` is modifier ``0`` or ``5``."""
    return digit in MODIFIER_DIGITS
