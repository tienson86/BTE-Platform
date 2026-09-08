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

FORBIDDEN_CUSTOMER_PHRASES: Final[tuple[str, ...]] = (
    "chắc chắn gây bệnh",
    "chắc chắn phá sản",
    "chắc chắn ly hôn",
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
