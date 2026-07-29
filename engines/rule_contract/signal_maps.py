"""
Static signal maps for RuleContext Builder (WP2D).

Lookup-only tables. No engine calls. No CSV writes.
Used to map already-available chart pillars into RuleContext signals.
"""

from __future__ import annotations

# Stem → five element + polarity (yang=True)
STEM_META: dict[str, tuple[str, bool]] = {
    "Giáp": ("wood", True),
    "Ất": ("wood", False),
    "Bính": ("fire", True),
    "Đinh": ("fire", False),
    "Mậu": ("earth", True),
    "Kỷ": ("earth", False),
    "Canh": ("metal", True),
    "Tân": ("metal", False),
    "Nhâm": ("water", True),
    "Quý": ("water", False),
}

BRANCH_HIDDEN: dict[str, list[str]] = {
    "Tý": ["Quý"],
    "Sửu": ["Kỷ", "Quý", "Tân"],
    "Dần": ["Giáp", "Bính", "Mậu"],
    "Mão": ["Ất"],
    "Thìn": ["Mậu", "Ất", "Quý"],
    "Tỵ": ["Bính", "Mậu", "Canh"],
    "Ngọ": ["Đinh", "Kỷ"],
    "Mùi": ["Kỷ", "Đinh", "Ất"],
    "Thân": ["Canh", "Nhâm", "Mậu"],
    "Dậu": ["Tân"],
    "Tuất": ["Mậu", "Tân", "Đinh"],
    "Hợi": ["Nhâm", "Giáp"],
}

# Day-master element → ten-god name for target element + same/opposite polarity
# Order: same, output, wealth, officer, resource
TEN_GOD_MATRIX: dict[str, dict[str, tuple[str, str]]] = {
    # element → {role: (yang_name, yin_name)} relative to yang day master naming
    "wood": {
        "same": ("Tỷ Kiên", "Kiếp Tài"),
        "output": ("Thực Thần", "Thương Quan"),
        "wealth": ("Thiên Tài", "Chính Tài"),
        "officer": ("Thất Sát", "Chính Quan"),
        "resource": ("Thiên Ấn", "Chính Ấn"),
    },
    "fire": {
        "same": ("Tỷ Kiên", "Kiếp Tài"),
        "output": ("Thực Thần", "Thương Quan"),
        "wealth": ("Thiên Tài", "Chính Tài"),
        "officer": ("Thất Sát", "Chính Quan"),
        "resource": ("Thiên Ấn", "Chính Ấn"),
    },
    "earth": {
        "same": ("Tỷ Kiên", "Kiếp Tài"),
        "output": ("Thực Thần", "Thương Quan"),
        "wealth": ("Thiên Tài", "Chính Tài"),
        "officer": ("Thất Sát", "Chính Quan"),
        "resource": ("Thiên Ấn", "Chính Ấn"),
    },
    "metal": {
        "same": ("Tỷ Kiên", "Kiếp Tài"),
        "output": ("Thực Thần", "Thương Quan"),
        "wealth": ("Thiên Tài", "Chính Tài"),
        "officer": ("Thất Sát", "Chính Quan"),
        "resource": ("Thiên Ấn", "Chính Ấn"),
    },
    "water": {
        "same": ("Tỷ Kiên", "Kiếp Tài"),
        "output": ("Thực Thần", "Thương Quan"),
        "wealth": ("Thiên Tài", "Chính Tài"),
        "officer": ("Thất Sát", "Chính Quan"),
        "resource": ("Thiên Ấn", "Chính Ấn"),
    },
}

GENERATES: dict[str, str] = {
    "wood": "fire",
    "fire": "earth",
    "earth": "metal",
    "metal": "water",
    "water": "wood",
}

CONTROLS: dict[str, str] = {
    "wood": "earth",
    "earth": "water",
    "water": "fire",
    "fire": "metal",
    "metal": "wood",
}

# Pattern name → useful ten-god family (for presence mapping only)
PATTERN_USEFUL_GOD: dict[str, str] = {
    "chinh_quan": "Chính Quan",
    "that_sat": "Thất Sát",
    "chinh_tai": "Chính Tài",
    "thien_tai": "Thiên Tài",
    "chinh_an": "Chính Ấn",
    "thien_an": "Thiên Ấn",
    "thuc_than": "Thực Thần",
    "thuong_quan": "Thương Quan",
}

# Classical Thiên Ất Quý Nhân: day-master stem → noble branches
TIAN_YI_BRANCHES: dict[str, tuple[str, ...]] = {
    "Giáp": ("Sửu", "Mùi"),
    "Mậu": ("Sửu", "Mùi"),
    "Canh": ("Sửu", "Mùi"),
    "Ất": ("Tý", "Thân"),
    "Kỷ": ("Tý", "Thân"),
    "Bính": ("Hợi", "Dậu"),
    "Đinh": ("Hợi", "Dậu"),
    "Nhâm": ("Mão", "Tỵ"),
    "Quý": ("Mão", "Tỵ"),
}

# Văn Xương: day master → branch
WEN_CHANG_BRANCH: dict[str, str] = {
    "Giáp": "Tỵ",
    "Ất": "Ngọ",
    "Bính": "Thân",
    "Đinh": "Dậu",
    "Mậu": "Thân",
    "Kỷ": "Dậu",
    "Canh": "Hợi",
    "Tân": "Tý",
    "Nhâm": "Dần",
    "Quý": "Mão",
}

# Lộc Thần
LU_SHEN_BRANCH: dict[str, str] = {
    "Giáp": "Dần",
    "Ất": "Mão",
    "Bính": "Tỵ",
    "Đinh": "Ngọ",
    "Mậu": "Tỵ",
    "Kỷ": "Ngọ",
    "Canh": "Thân",
    "Tân": "Dậu",
    "Nhâm": "Hợi",
    "Quý": "Tý",
}

# Hồng Loan (by year branch — simplified year-branch table)
HONG_LUAN_OPPOSITE: dict[str, str] = {
    "Tý": "Mão",
    "Sửu": "Dần",
    "Dần": "Sửu",
    "Mão": "Tý",
    "Thìn": "Hợi",
    "Tỵ": "Tuất",
    "Ngọ": "Dậu",
    "Mùi": "Thân",
    "Thân": "Mùi",
    "Dậu": "Ngọ",
    "Tuất": "Tỵ",
    "Hợi": "Thìn",
}

# Hoa Cái — day branch in earth group
HUA_GAI_BRANCHES: frozenset[str] = frozenset({"Thìn", "Tuất", "Sửu", "Mùi"})

# Dương Nhẫn
YANG_REN_BRANCH: dict[str, str] = {
    "Giáp": "Mão",
    "Bính": "Ngọ",
    "Mậu": "Ngọ",
    "Canh": "Dậu",
    "Nhâm": "Tý",
}

# Thiên Đức — by solar/lunar month branch (month branch key)
TIAN_DE_BRANCH: dict[str, str] = {
    "Dần": "Đinh",
    "Mão": "Thân",
    "Thìn": "Nhâm",
    "Tỵ": "Tân",
    "Ngọ": "Hợi",
    "Mùi": "Giáp",
    "Thân": "Quý",
    "Dậu": "Dần",
    "Tuất": "Bính",
    "Hợi": "Ất",
    "Tý": "Tỵ",
    "Sửu": "Canh",
}

# Nguyệt Đức — by month branch
YUE_DE_STEM: dict[str, str] = {
    "Dần": "Bính",
    "Mão": "Giáp",
    "Thìn": "Nhâm",
    "Tỵ": "Canh",
    "Ngọ": "Bính",
    "Mùi": "Giáp",
    "Thân": "Nhâm",
    "Dậu": "Canh",
    "Tuất": "Bính",
    "Hợi": "Giáp",
    "Tý": "Nhâm",
    "Sửu": "Canh",
}

# Score CSV star_name → detector key
SHENSHA_DETECTORS: tuple[tuple[str, str], ...] = (
    ("Thiên Ất Quý Nhân", "tian_yi"),
    ("Thiên Ất", "tian_yi"),
    ("Văn Xương", "wen_chang"),
    ("Văn Khúc", "wen_chang"),  # approximate map when Wen Qu table absent
    ("Lộc Thần", "lu_shen"),
    ("Hồng Loan", "hong_luan"),
    ("Thiên Hỷ", "tian_xi"),
)

ROOT_LEVEL_LABELS: tuple[tuple[int, str], ...] = (
    (3, "Thông căn 3 chi trở lên"),
    (2, "Thông căn 2 chi"),
    (1, "Thông căn 1 chi"),
)

SUPPORT_LABELS = {
    "same": "Đồng hành trợ thân",
    "resource": "Ấn tinh sinh thân",
    "stem": "Thiên Can trợ lực",
    "branch": "Địa Chi trợ lực",
}

CONTROL_LABELS = {
    "officer": "Bị Quan Sát khắc",
    "output": "Bị Thực Thương tiết",
    "wealth": "Bị Tài tinh hao",
}
