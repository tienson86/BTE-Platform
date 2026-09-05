"""MC-01 identifiers, aliases, and documented V1 scoring constants.

Numeric weights are provisional ruleset values. They are explicit and
deterministic. They are not frozen scientific coefficients.
"""

from __future__ import annotations

from engines.ten_gods_engine.constants import GOD_ID_TO_FAMILY, GOD_ID_TO_LABEL, LABEL_TO_GOD_ID

SCHEMA_DECISION: str = "bte.mingju.decision.v1"
SCHEMA_CONTEXT: str = "bte.mingju.context.v1"
SCHEMA_COMPOSER: str = "bte.mingju.composer.v1"
RULESET_VERSION: str = "bte.mingju.rules.v1"

PATTERN_FAMILY_BY_ID: dict[str, str] = {
    "zheng_guan": "standard",
    "qi_sha": "standard",
    "zheng_cai": "standard",
    "pian_cai": "standard",
    "zheng_yin": "standard",
    "pian_yin": "standard",
    "shi_shen": "standard",
    "shang_guan": "standard",
    "bi_jian": "standard",
    "jie_cai": "standard",
    "jian_lu": "root_prosperity",
    "yang_ren": "root_prosperity",
    "cong_cai": "follow",
    "cong_guan_sha": "follow",
    "cong_er": "follow",
    "cong_wang": "follow",
    "cong_yin": "follow",
    "hua_qi": "transformation",
}

PATTERN_LABEL_BY_ID: dict[str, str] = {
    **GOD_ID_TO_LABEL,
    "jian_lu": "Kiến Lộc",
    "yang_ren": "Dương Nhẫn",
    "cong_cai": "Tòng Tài",
    "cong_guan_sha": "Tòng Quan Sát",
    "cong_er": "Tòng Nhi",
    "cong_wang": "Tòng Vượng",
    "cong_yin": "Tòng Ấn",
    "hua_qi": "Hóa Khí",
}

# Pattern Engine Vietnamese codes → MC-01 canonical IDs.
PATTERN_CODE_ALIASES: dict[str, str] = {
    "chinh_quan": "zheng_guan",
    "thien_quan": "zheng_guan",
    "that_sat": "qi_sha",
    "thien_sat": "qi_sha",
    "chinh_tai": "zheng_cai",
    "thien_tai": "pian_cai",
    "chinh_an": "zheng_yin",
    "thien_an": "pian_yin",
    "thuc_than": "shi_shen",
    "thuong_quan": "shang_guan",
    "thien_thuong": "shang_guan",
    "ty_kien": "bi_jian",
    "kiep_tai": "jie_cai",
    "kien_loc": "jian_lu",
    "duong_nhan": "yang_ren",
    "tong_tai": "cong_cai",
    "tong_quan": "cong_guan_sha",
    "tong_sat": "cong_guan_sha",
    "tong_nhi": "cong_er",
    "tong_vuong": "cong_wang",
    "tong_an": "cong_yin",
    "hoa_khi": "hua_qi",
}

PATTERN_LABEL_ALIASES: dict[str, str] = {
    **LABEL_TO_GOD_ID,
    "Kiến Lộc": "jian_lu",
    "Dương Nhẫn": "yang_ren",
    "Tòng Tài": "cong_cai",
    "Tòng Quan": "cong_guan_sha",
    "Tòng Sát": "cong_guan_sha",
    "Tòng Quan Sát": "cong_guan_sha",
    "Tòng Nhi": "cong_er",
    "Tòng Vượng": "cong_wang",
    "Tòng Ấn": "cong_yin",
    "Hóa Khí": "hua_qi",
    "Thiên Quan": "zheng_guan",
    "Thiên Sát": "qi_sha",
    "Thiên Thương": "shang_guan",
}

COUNTERPART_PAIRS: tuple[tuple[str, str], ...] = (
    ("zheng_guan", "qi_sha"),
    ("zheng_cai", "pian_cai"),
    ("zheng_yin", "pian_yin"),
    ("shi_shen", "shang_guan"),
    ("bi_jian", "jie_cai"),
)

FAMILY_CONTROLS: dict[str, str] = {
    "officer": "companion",
    "companion": "wealth",
    "wealth": "resource",
    "resource": "output",
    "output": "officer",
}

FAMILY_GENERATES: dict[str, str] = {
    "resource": "companion",
    "companion": "output",
    "output": "wealth",
    "wealth": "officer",
    "officer": "resource",
}

GOD_FAMILY: dict[str, str] = dict(GOD_ID_TO_FAMILY)

PILLAR_EXPOSURE_WEIGHT: dict[str, float] = {
    "month": 4.0,
    "hour": 3.0,
    "day": 2.0,
    "year": 2.0,
}

LAYER_WEIGHT: dict[str, float] = {
    "visible": 3.0,
    "main_qi": 2.0,
    "middle_qi": 1.0,
    "residual_qi": 0.4,
    "branch_hidden": 0.8,
}

MATERIAL_ACTIVATION_THRESHOLD: float = 2.0
STRONG_ACTIVATION_THRESHOLD: float = 4.0

PURITY_BASE_SCORE: float = 72.0
PURITY_POSITIVE_MINOR: float = 6.0
PURITY_POSITIVE_MODERATE: float = 10.0
PURITY_NEGATIVE_MINOR: float = 8.0
PURITY_NEGATIVE_MODERATE: float = 14.0
PURITY_NEGATIVE_MAJOR: float = 22.0
PURITY_NEGATIVE_CRITICAL: float = 32.0

STRENGTH_DIMENSION_WEIGHTS: dict[str, float] = {
    "season_power": 0.24,
    "root_power": 0.22,
    "exposure_power": 0.18,
    "generation_power": 0.14,
    "continuity_power": 0.12,
    "position_power": 0.10,
}

INTEGRITY_WEIGHTS: dict[str, float] = {
    "purity": 0.22,
    "pattern_strength": 0.22,
    "support": 0.10,
    "damage": 0.22,
    "rescue": 0.10,
    "useful_god": 0.07,
    "climate": 0.07,
}

DAMAGE_SEVERITY_POINTS: dict[str, float] = {
    "negligible": 4.0,
    "minor": 12.0,
    "moderate": 24.0,
    "major": 40.0,
    "critical": 58.0,
}

RESCUE_OFFSET_POINTS: dict[str, float] = {
    "minor": 8.0,
    "moderate": 16.0,
    "strong": 28.0,
    "critical": 40.0,
}

PURITY_BANDS: tuple[tuple[float, str], ...] = (
    (90.0, "very_pure"),
    (75.0, "pure"),
    (60.0, "moderately_pure"),
    (40.0, "mixed"),
    (20.0, "heavily_mixed"),
    (0.0, "structurally_impure"),
)

PATTERN_STRENGTH_BANDS: tuple[tuple[float, str], ...] = (
    (80.0, "very_strong"),
    (60.0, "strong"),
    (40.0, "moderate"),
    (20.0, "weak"),
    (0.0, "very_weak"),
)

GRADE_BANDS: tuple[tuple[float, str], ...] = (
    (90.0, "SS"),
    (82.0, "S"),
    (72.0, "A"),
    (60.0, "B"),
    (45.0, "C"),
    (0.0, "D"),
)

ACHIEVEMENT_BANDS: tuple[tuple[float, str], ...] = (
    (85.0, "very_high"),
    (70.0, "high"),
    (60.0, "above_average"),
    (45.0, "moderate"),
    (30.0, "below_average"),
    (15.0, "low"),
    (0.0, "very_low"),
)

WEAK_DM_LEVELS: frozenset[str] = frozenset(
    {"extremely_weak", "very_weak", "weak", "than_nhuoc", "nhược", "nhuoc"}
)
STRONG_DM_LEVELS: frozenset[str] = frozenset(
    {"strong", "very_strong", "extremely_strong", "than_vuong", "vượng", "vuong"}
)

SCORE_GRADE_LETTERS: frozenset[str] = frozenset(
    {"S+", "S", "A+", "A", "B+", "B", "C+", "C", "D+", "D", "E"}
)
MC01_GRADE_LETTERS: frozenset[str] = frozenset({"SS", "S", "A", "B", "C", "D", "UNRESOLVED"})
