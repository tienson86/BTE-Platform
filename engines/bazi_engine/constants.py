"""
BTE Platform
Bazi Engine Constants

Định nghĩa toàn bộ hằng số sử dụng trong Bazi Engine.
"""

from __future__ import annotations

# ==========================================================
# Engine
# ==========================================================

ENGINE_NAME = "Bazi Engine"
ENGINE_VERSION = "1.0.0"

# ==========================================================
# Operations
# ==========================================================

OP_BUILD_CHART = "build_chart"

OP_FOUR_PILLARS = "four_pillars"

OP_HIDDEN_STEMS = "hidden_stems"

OP_TEN_GODS = "ten_gods"

OP_STRENGTH = "strength"

OP_USEFUL_GOD = "useful_god"

OP_PATTERN = "pattern"

OP_SHENSHA = "shensha"

OP_DAI_VAN = "dai_van"

OP_LUU_NIEN = "luu_nien"

OP_FULL_ANALYSIS = "full_analysis"

# ==========================================================
# Heavenly Stems
# ==========================================================

HEAVENLY_STEMS = (
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

# ==========================================================
# Earthly Branches
# ==========================================================

EARTHLY_BRANCHES = (
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

# ==========================================================
# Five Elements
# ==========================================================

FIVE_ELEMENTS = (
    "Mộc",
    "Hỏa",
    "Thổ",
    "Kim",
    "Thủy",
)

# ==========================================================
# Yin Yang
# ==========================================================

YIN = "Âm"
YANG = "Dương"

# ==========================================================
# Four Pillars
# ==========================================================

YEAR = "year"

MONTH = "month"

DAY = "day"

HOUR = "hour"

PILLARS = (
    YEAR,
    MONTH,
    DAY,
    HOUR,
)

# ==========================================================
# Ten Gods
# ==========================================================

TEN_GODS_COUNT = 10

# ==========================================================
# Luck
# ==========================================================

DAI_VAN_LENGTH = 10

MAX_DAI_VAN = 12

# ==========================================================
# Cache
# ==========================================================

CACHE_PREFIX = "bazi"

CACHE_TIMEOUT = 3600

# ==========================================================
# Precision
# ==========================================================

DEFAULT_SCORE = 0.0

DEFAULT_WEIGHT = 1.0

FLOAT_PRECISION = 1e-8
