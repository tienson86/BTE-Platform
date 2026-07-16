"""
BTE Platform
Calendar Engine Constants

Toàn bộ hằng số dùng trong Calendar Engine.
"""

from __future__ import annotations

# ==========================================================
# Version
# ==========================================================

ENGINE_NAME = "Calendar Engine"
ENGINE_VERSION = "1.0.0"

# ==========================================================
# Calendar
# ==========================================================

SOLAR_CALENDAR = "solar"
LUNAR_CALENDAR = "lunar"

DEFAULT_TIMEZONE = 7.0

MIN_YEAR = 1
MAX_YEAR = 9999

MIN_MONTH = 1
MAX_MONTH = 12

MIN_DAY = 1
MAX_DAY = 31

# ==========================================================
# Geographic
# ==========================================================

MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0

MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0

MIN_TIMEZONE = -12
MAX_TIMEZONE = 14

# ==========================================================
# Astronomy
# ==========================================================

J2000 = 2451545.0

JULIAN_DAY_OFFSET = 1721425.5

TROPICAL_YEAR = 365.242189

SIDEREAL_YEAR = 365.256363004

SYNODIC_MONTH = 29.530588853

ANOMALISTIC_MONTH = 27.55454988

DRACONIC_MONTH = 27.212220817

EARTH_OBLIQUITY = 23.439291111

SUN_FULL_CIRCLE = 360.0

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
# Zodiac
# ==========================================================

ZODIAC = (
    "Chuột",
    "Trâu",
    "Hổ",
    "Mèo",
    "Rồng",
    "Rắn",
    "Ngựa",
    "Dê",
    "Khỉ",
    "Gà",
    "Chó",
    "Lợn",
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
# 24 Solar Terms
# ==========================================================

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

SOLAR_TERM_COUNT = 24

SOLAR_TERM_INTERVAL = 15.0

# ==========================================================
# Moon Phase
# ==========================================================

NEW_MOON = "New Moon"
WAXING_CRESCENT = "Waxing Crescent"
FIRST_QUARTER = "First Quarter"
WAXING_GIBBOUS = "Waxing Gibbous"
FULL_MOON = "Full Moon"
WANING_GIBBOUS = "Waning Gibbous"
LAST_QUARTER = "Last Quarter"
WANING_CRESCENT = "Waning Crescent"

# ==========================================================
# Operation
# ==========================================================

OP_FULL_CALENDAR = "full_calendar"

OP_SOLAR_TO_LUNAR = "solar_to_lunar"

OP_LUNAR_TO_SOLAR = "lunar_to_solar"

OP_SOLAR_TERM = "solar_term"

OP_YEAR_PILLAR = "year_pillar"

OP_MONTH_PILLAR = "month_pillar"

OP_DAY_PILLAR = "day_pillar"

OP_HOUR_PILLAR = "hour_pillar"

# ==========================================================
# Cache
# ==========================================================

CACHE_PREFIX = "calendar"

CACHE_TIMEOUT = 3600

# ==========================================================
# Data Files
# ==========================================================

SOLAR_TERM_FILE = "solar_terms.csv"

NEWMOON_FILE = "newmoon.csv"

DELTA_T_FILE = "delta_t.csv"

PERIODIC_LONGITUDE_FILE = "periodic_longitude.csv"

PERIODIC_LATITUDE_FILE = "periodic_latitude.csv"

PERIODIC_DISTANCE_FILE = "periodic_distance.csv"

LEAP_MONTH_FILE = "leap_month.json"

# ==========================================================
# Precision
# ==========================================================

FLOAT_PRECISION = 1e-8

ANGLE_PRECISION = 1e-10

TIME_PRECISION = 1e-6

# ==========================================================
# Default Config
# ==========================================================

DEFAULT_LANGUAGE = "vi"

DEFAULT_COUNTRY = "VN"

DEFAULT_CACHE = True

DEFAULT_TRUE_SOLAR_TIME = True

DEFAULT_HIGH_PRECISION = True
