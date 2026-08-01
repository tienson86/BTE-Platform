"""Constants for Ten Gods Interpreter business logic."""

from __future__ import annotations

TEN_GODS_MODULE_IDS: tuple[str, ...] = (
    "ten_gods",
    "ten_gods_engine",
    "10_ten_gods",
    "thap_than",
)

TEN_GODS_SECTION_TYPE = "ten_gods"
TEN_GODS_INTERPRETER_ID = "ten_gods_interpreter"
TEN_GODS_INTERPRETER_VERSION = "1.0.0"

PRESENCE_KEYS: tuple[str, ...] = (
    "presence",
    "ten_gods",
    "thap_than",
    "gods",
)
RELATIONSHIP_KEYS: tuple[str, ...] = (
    "relationships",
    "relations",
    "quan_he",
)
INTERACTION_KEYS: tuple[str, ...] = (
    "interactions",
    "tuong_tac",
)
FAVORABILITY_KEYS: tuple[str, ...] = (
    "favorability",
    "favorabilities",
)
DISTRIBUTION_KEYS: tuple[str, ...] = (
    "distribution",
    "summary",
)
SCORE_KEYS: tuple[str, ...] = (
    "ten_gods_score",
    "score",
)

# Analysis god_id -> Vietnamese display label (Pack 01 thap_than).
GOD_ID_TO_LABEL: dict[str, str] = {
    "bi_jian": "Tỷ Kiên",
    "jie_cai": "Kiếp Tài",
    "shi_shen": "Thực Thần",
    "shang_guan": "Thương Quan",
    "pian_cai": "Thiên Tài",
    "zheng_cai": "Chính Tài",
    "qi_sha": "Thất Sát",
    "zheng_guan": "Chính Quan",
    "pian_yin": "Thiên Ấn",
    "zheng_yin": "Chính Ấn",
}

# Pack 01 ma_thap_than / ASCII ten -> Vietnamese label.
GOD_CODE_TO_LABEL: dict[str, str] = {
    "tt01": "Tỷ Kiên",
    "ty_kien": "Tỷ Kiên",
    "tt02": "Kiếp Tài",
    "kiep_tai": "Kiếp Tài",
    "tt03": "Thực Thần",
    "thuc_than": "Thực Thần",
    "tt04": "Thương Quan",
    "thuong_quan": "Thương Quan",
    "tt05": "Thiên Tài",
    "thien_tai": "Thiên Tài",
    "tt06": "Chính Tài",
    "chinh_tai": "Chính Tài",
    "tt07": "Thất Sát",
    "that_sat": "Thất Sát",
    "tt08": "Chính Quan",
    "chinh_quan": "Chính Quan",
    "tt09": "Thiên Ấn",
    "thien_an": "Thiên Ấn",
    "tt10": "Chính Ấn",
    "chinh_an": "Chính Ấn",
}

FAVORABLE_TOKENS: frozenset[str] = frozenset(
    {
        "favorable",
        "huu_dung",
        "hữu_dụng",
        "hy_than",
        "hỷ",
        "dung_than",
        "dụng",
        "positive",
        "good",
    }
)
UNFAVORABLE_TOKENS: frozenset[str] = frozenset(
    {
        "unfavorable",
        "vo_dung",
        "vô_dụng",
        "ky_than",
        "kỵ",
        "negative",
        "bad",
    }
)

STRENGTH_DIMENSIONS: frozenset[str] = frozenset(
    {"strength", "than_vuong", "than_nhuoc", "day_master_strength"}
)
