"""
===============================================================================
Bazi Engine - Core Constants
-------------------------------------------------------------------------------
Các hằng số dùng chung cho toàn bộ hệ thống Bát Tự.

Nguyên tắc:
- Không chứa thuật toán.
- Không chứa logic nghiệp vụ.
- Chỉ khai báo hằng số.
- Toàn bộ Engine chỉ sử dụng dữ liệu từ file này.
===============================================================================
"""

from typing import Final

# =============================================================================
# VERSION
# =============================================================================

ENGINE_NAME: Final = "Bazi Engine"

ENGINE_VERSION: Final = "1.0.0"

ENGINE_AUTHOR: Final = "Phong Thuy AI"

# =============================================================================
# YIN / YANG
# =============================================================================

YANG: Final = "Dương"
YIN: Final = "Âm"

YIN_YANG = (
    YANG,
    YIN,
)

# =============================================================================
# FIVE ELEMENTS
# =============================================================================

WOOD: Final = "Mộc"
FIRE: Final = "Hỏa"
EARTH: Final = "Thổ"
METAL: Final = "Kim"
WATER: Final = "Thủy"

FIVE_ELEMENTS = (
    WOOD,
    FIRE,
    EARTH,
    METAL,
    WATER,
)

# =============================================================================
# HEAVENLY STEMS
# =============================================================================

JIA = "Giáp"
YI = "Ất"
BING = "Bính"
DING = "Đinh"
WU = "Mậu"
JI = "Kỷ"
GENG = "Canh"
XIN = "Tân"
REN = "Nhâm"
GUI = "Quý"

HEAVENLY_STEMS = (
    JIA,
    YI,
    BING,
    DING,
    WU,
    JI,
    GENG,
    XIN,
    REN,
    GUI,
)

# =============================================================================
# EARTHLY BRANCHES
# =============================================================================

ZI = "Tý"
CHOU = "Sửu"
YIN_BRANCH = "Dần"
MAO = "Mão"
CHEN = "Thìn"
SI = "Tỵ"
WU_BRANCH = "Ngọ"
WEI = "Mùi"
SHEN = "Thân"
YOU = "Dậu"
XU = "Tuất"
HAI = "Hợi"

EARTHLY_BRANCHES = (
    ZI,
    CHOU,
    YIN_BRANCH,
    MAO,
    CHEN,
    SI,
    WU_BRANCH,
    WEI,
    SHEN,
    YOU,
    XU,
    HAI,
)

# =============================================================================
# TEN GODS
# =============================================================================

DIRECT_RESOURCE = "Chính Ấn"
INDIRECT_RESOURCE = "Thiên Ấn"

FRIEND = "Tỷ Kiên"
ROBBING_WEALTH = "Kiếp Tài"

EATING_GOD = "Thực Thần"
HURTING_OFFICER = "Thương Quan"

INDIRECT_WEALTH = "Thiên Tài"
DIRECT_WEALTH = "Chính Tài"

SEVEN_KILLINGS = "Thất Sát"
DIRECT_OFFICER = "Chính Quan"

TEN_GODS = (
    FRIEND,
    ROBBING_WEALTH,
    EATING_GOD,
    HURTING_OFFICER,
    INDIRECT_WEALTH,
    DIRECT_WEALTH,
    SEVEN_KILLINGS,
    DIRECT_OFFICER,
    INDIRECT_RESOURCE,
    DIRECT_RESOURCE,
)

# =============================================================================
# TEN DAY MASTERS
# =============================================================================

DAY_MASTERS = HEAVENLY_STEMS

# =============================================================================
# TWELVE STAGES OF GROWTH
# =============================================================================

TWELVE_STAGES = (
    "Trường Sinh",
    "Mộc Dục",
    "Quan Đới",
    "Lâm Quan",
    "Đế Vượng",
    "Suy",
    "Bệnh",
    "Tử",
    "Mộ",
    "Tuyệt",
    "Thai",
    "Dưỡng",
)

# =============================================================================
# FOUR PILLARS
# =============================================================================

YEAR = "Năm"
MONTH = "Tháng"
DAY = "Ngày"
HOUR = "Giờ"

FOUR_PILLARS = (
    YEAR,
    MONTH,
    DAY,
    HOUR,
)

# =============================================================================
# GENDER
# =============================================================================

MALE = "Nam"
FEMALE = "Nữ"

GENDERS = (
    MALE,
    FEMALE,
)

# =============================================================================
# LUCK CYCLE
# =============================================================================

FORWARD = "Thuận"
BACKWARD = "Nghịch"

LUCK_DIRECTIONS = (
    FORWARD,
    BACKWARD,
)

# =============================================================================
# SEASONS
# =============================================================================

SPRING = "Xuân"
SUMMER = "Hạ"
AUTUMN = "Thu"
WINTER = "Đông"

SEASONS = (
    SPRING,
    SUMMER,
    AUTUMN,
    WINTER,
)

# =============================================================================
# TWENTY-FOUR SOLAR TERMS
# =============================================================================

SOLAR_TERMS = (
    "Lập Xuân",
    "Vũ Thủy",
    "Kinh Trập",
    "Xuân Phân",
    "Thanh Minh",
    "Cốc Vũ",
    "Lập Hạ",
    "Tiểu Mãn",
    "Mang Chủng",
    "Hạ Chí",
    "Tiểu Thử",
    "Đại Thử",
    "Lập Thu",
    "Xử Thử",
    "Bạch Lộ",
    "Thu Phân",
    "Hàn Lộ",
    "Sương Giáng",
    "Lập Đông",
    "Tiểu Tuyết",
    "Đại Tuyết",
    "Đông Chí",
    "Tiểu Hàn",
    "Đại Hàn",
)

# =============================================================================
# MONTH BRANCH ORDER
# =============================================================================

MONTH_BRANCH_ORDER = (
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
    "Tý",
    "Sửu",
)

# =============================================================================
# DEFAULT VALUES
# =============================================================================

DEFAULT_ENCODING = "utf-8"

DEFAULT_DECIMAL = 2

DEFAULT_CACHE_SIZE = 256

DEFAULT_TIMEZONE = "Asia/Ho_Chi_Minh"

# =============================================================================
# FILE EXTENSIONS
# =============================================================================

CSV = ".csv"
JSON = ".json"
YAML = ".yaml"

SUPPORTED_DATA_FILES = (
    CSV,
    JSON,
    YAML,
)
