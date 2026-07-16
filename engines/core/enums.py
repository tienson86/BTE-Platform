"""
BTE Platform
Core Enums

Định nghĩa toàn bộ Enum dùng chung cho các Engine.
"""

from __future__ import annotations

from enum import Enum, IntEnum


# ==========================================================
# Ngũ Hành
# ==========================================================

class Element(str, Enum):

    WOOD = "Mộc"

    FIRE = "Hỏa"

    EARTH = "Thổ"

    METAL = "Kim"

    WATER = "Thủy"


# ==========================================================
# Âm Dương
# ==========================================================

class YinYang(str, Enum):

    YANG = "Dương"

    YIN = "Âm"


# ==========================================================
# Thiên Can
# ==========================================================

class HeavenlyStem(IntEnum):

    GIAP = 1
    AT = 2
    BINH = 3
    DINH = 4
    MAU = 5
    KY = 6
    CANH = 7
    TAN = 8
    NHAM = 9
    QUY = 10


# ==========================================================
# Địa Chi
# ==========================================================

class EarthlyBranch(IntEnum):

    TY = 1
    SUU = 2
    DAN = 3
    MAO = 4
    THIN = 5
    TY_RAN = 6
    NGO = 7
    MUI = 8
    THAN = 9
    DAU = 10
    TUAT = 11
    HOI = 12


# ==========================================================
# Trụ
# ==========================================================

class PillarType(str, Enum):

    YEAR = "year"

    MONTH = "month"

    DAY = "day"

    HOUR = "hour"


# ==========================================================
# Giới tính
# ==========================================================

class Gender(str, Enum):

    MALE = "Nam"

    FEMALE = "Nữ"


# ==========================================================
# Calendar
# ==========================================================

class CalendarType(str, Enum):

    SOLAR = "solar"

    LUNAR = "lunar"


# ==========================================================
# Operation
# ==========================================================

class Operation(str, Enum):

    BUILD_CHART = "build_chart"

    FOUR_PILLARS = "four_pillars"

    HIDDEN_STEMS = "hidden_stems"

    TEN_GODS = "ten_gods"

    STRENGTH = "strength"

    USEFUL_GOD = "useful_god"

    PATTERN = "pattern"

    SHENSHA = "shensha"

    DAI_VAN = "dai_van"

    LUU_NIEN = "luu_nien"

    FULL_ANALYSIS = "full_analysis"


# ==========================================================
# Engine Status
# ==========================================================

class EngineStatus(str, Enum):

    CREATED = "created"

    INITIALIZED = "initialized"

    LOADING = "loading"

    READY = "ready"

    RUNNING = "running"

    FINISHED = "finished"

    ERROR = "error"


# ==========================================================
# Thân Vượng
# ==========================================================

class StrengthLevel(str, Enum):

    VERY_WEAK = "Rất nhược"

    WEAK = "Nhược"

    BALANCED = "Trung hòa"

    STRONG = "Vượng"

    VERY_STRONG = "Rất vượng"


# ==========================================================
# Cách Cục
# ==========================================================

class PatternCategory(str, Enum):

    NORMAL = "Chính cách"

    SPECIAL = "Đặc cách"

    FOLLOW = "Tòng cách"

    TRANSFORM = "Hóa cách"


# ==========================================================
# Dụng Thần
# ==========================================================

class UsefulGodMethod(str, Enum):

    STRENGTH = "strength"

    SEASON = "season"

    TEMPERATURE = "temperature"

    PATTERN = "pattern"

    FOLLOW = "follow"


# ==========================================================
# Thần Sát
# ==========================================================

class ShenShaType(str, Enum):

    AUSPICIOUS = "Cát"

    INAUSPICIOUS = "Hung"

    NEUTRAL = "Trung tính"


# ==========================================================
# Đầu ra Report
# ==========================================================

class ReportFormat(str, Enum):

    PDF = "pdf"

    HTML = "html"

    WORD = "docx"

    EXCEL = "xlsx"

    JSON = "json"


# ==========================================================
# Log Level
# ==========================================================

class LogLevel(str, Enum):

    DEBUG = "DEBUG"

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    CRITICAL = "CRITICAL"
