"""Date Selection constants — public labels and canonical mappings."""

from __future__ import annotations

ENGINE_NAME = "Date Selection Engine"
ENGINE_VERSION = "1.0.0"

BRANCHES: tuple[str, ...] = (
    "Tý",
    "Sửu",
    "Dần",
    "Mão",
    "Thìn",
    "Tỵ",
    "Ngọ",
    "Mùi",
    "Thân",
    "Dậu",
    "Tuất",
    "Hợi",
)

# Traditional branch index used by day/hour value (Tý = 1 … Hợi = 12).
BRANCH_INDEX: dict[str, int] = {name: index + 1 for index, name in enumerate(BRANCHES)}

STEMS: tuple[str, ...] = (
    "Giáp",
    "Ất",
    "Bính",
    "Đinh",
    "Mậu",
    "Kỷ",
    "Canh",
    "Tân",
    "Nhâm",
    "Quý",
)

# Date Selection civil-clock convention (not Bazi hour_branch.csv 07:00–08:59).
# Each odd HH:00 is the inclusive close of the previous two-hour branch.
# Tý: 23:01–01:00 (cross midnight). Thìn: 07:01–09:00.
DS_HOUR_WINDOWS: tuple[tuple[str, int, int, int, int, bool], ...] = (
    ("Tý", 23, 1, 1, 0, True),
    ("Sửu", 1, 1, 3, 0, False),
    ("Dần", 3, 1, 5, 0, False),
    ("Mão", 5, 1, 7, 0, False),
    ("Thìn", 7, 1, 9, 0, False),
    ("Tỵ", 9, 1, 11, 0, False),
    ("Ngọ", 11, 1, 13, 0, False),
    ("Mùi", 13, 1, 15, 0, False),
    ("Thân", 15, 1, 17, 0, False),
    ("Dậu", 17, 1, 19, 0, False),
    ("Tuất", 19, 1, 21, 0, False),
    ("Hợi", 21, 1, 23, 0, False),
)

SIX_STATE_BY_REMAINDER: dict[int, tuple[str, str]] = {
    1: ("dai_an", "Đại An"),
    2: ("luu_lien", "Lưu Liên"),
    3: ("toc_hy", "Tốc Hỷ"),
    4: ("xich_khau", "Xích Khẩu"),
    5: ("tieu_cat", "Tiểu Cát"),
    0: ("khong_vong", "Không Vong"),
}

POSITIVE_DAY_CODES = frozenset({"dai_an", "toc_hy", "tieu_cat"})
REJECT_DAY_CODES = frozenset({"xich_khau", "khong_vong"})
POSITIVE_KE_CODES = frozenset({"dai_an", "toc_hy", "tieu_cat"})
REJECT_KE_CODES = frozenset({"xich_khau", "khong_vong"})

DAY_RANK_SCORE: dict[str, int] = {
    "dai_an": 3,
    "tieu_cat": 2,
    "toc_hy": 2,
    "luu_lien": 1,
}

KE_RANK_SCORE: dict[str, int] = {
    "dai_an": 3,
    "tieu_cat": 2,
    "toc_hy": 2,
    "luu_lien": 1,
}

DIVERSITY_ORDER: tuple[str, ...] = ("dai_an", "tieu_cat", "toc_hy")

MAX_RANKED_DATES = 5
KE_COUNT = 6
KE_MINUTES = 20

GENDER_LABELS: dict[str, str] = {"male": "Nam", "female": "Nữ"}
MALE_GENDER_ALIASES = frozenset({"male", "nam", "m", "1", "man", "boy"})
FEMALE_GENDER_ALIASES = frozenset({"female", "nu", "nữ", "f", "woman", "girl"})

CUNG_ELEMENT: dict[str, tuple[str, str]] = {
    "Khảm": ("thuy", "Thủy"),
    "Ly": ("hoa", "Hỏa"),
    "Chấn": ("moc", "Mộc"),
    "Tốn": ("moc", "Mộc"),
    "Càn": ("kim", "Kim"),
    "Khôn": ("tho", "Thổ"),
    "Cấn": ("tho", "Thổ"),
    "Đoài": ("kim", "Kim"),
}

DONG_TU_TRACH = frozenset({"Khảm", "Ly", "Chấn", "Tốn"})
TAY_TU_TRACH = frozenset({"Càn", "Khôn", "Cấn", "Đoài"})

TRACH_DONG = ("dong", "Đông Tứ Trạch")
TRACH_TAY = ("tay", "Tây Tứ Trạch")

HOUR_STEM_GROUPS: dict[str, str] = {
    "Giáp": "Giáp-Kỷ",
    "Kỷ": "Giáp-Kỷ",
    "Ất": "Ất-Canh",
    "Canh": "Ất-Canh",
    "Bính": "Bính-Tân",
    "Tân": "Bính-Tân",
    "Đinh": "Đinh-Nhâm",
    "Nhâm": "Đinh-Nhâm",
    "Mậu": "Mậu-Quý",
    "Quý": "Mậu-Quý",
}

HOUR_BRANCH_CSV = "database/02_quy_tac/hour_branch.csv"
NAP_AM_CSV = "engines/calendar_engine/data/01_nap_am.csv"
HOUR_GANZHI_CSV = "engines/calendar_engine/data/04_hour_ganzhi.csv"
HOA_GIAP_CUNG_PHI_CSV = "engines/date_selection/data/hoa_giap_cung_phi.csv"
HA_NGUYEN_CUNG_CSV = "engines/date_selection/data/ha_nguyen_cung.csv"

VALID_CUNG = frozenset(CUNG_ELEMENT)
JIAZI_LABELS: tuple[str, ...] = tuple(
    f"{STEMS[index % 10]} {BRANCHES[index % 12]}" for index in range(60)
)
