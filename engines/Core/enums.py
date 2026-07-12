"""
===============================================================================
BTE Platform - Core Enums
===============================================================================

Định nghĩa các Enum dùng chung cho toàn bộ Framework.

Không chứa dữ liệu nghiệp vụ chi tiết.
Chỉ định nghĩa các kiểu dữ liệu chuẩn.

Author : BTE Platform
Version: 1.0.0
===============================================================================
"""

from enum import Enum, IntEnum, auto


# =============================================================================
# Framework
# =============================================================================

class EngineType(Enum):
    CALENDAR = "calendar"
    BAZI = "bazi"
    INTERPRETATION = "interpretation"
    REPORT = "report"
    EXPORT = "export"
    FENGSHUI = "fengshui"


class Status(Enum):
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PENDING = "PENDING"


# =============================================================================
# Basic
# =============================================================================

class Gender(Enum):
    MALE = "Nam"
    FEMALE = "Nữ"


class YinYang(Enum):
    YANG = "Dương"
    YIN = "Âm"


# =============================================================================
# Five Elements
# =============================================================================

class Element(Enum):
    WOOD = "Mộc"
    FIRE = "Hỏa"
    EARTH = "Thổ"
    METAL = "Kim"
    WATER = "Thủy"


# =============================================================================
# Heavenly Stem
# =============================================================================

class HeavenlyStem(Enum):
    GIAP = "Giáp"
    AT = "Ất"
    BINH = "Bính"
    DINH = "Đinh"
    MAU = "Mậu"
    KY = "Kỷ"
    CANH = "Canh"
    TAN = "Tân"
    NHAM = "Nhâm"
    QUY = "Quý"


# =============================================================================
# Earthly Branch
# =============================================================================

class EarthlyBranch(Enum):
    TY = "Tý"
    SUU = "Sửu"
    DAN = "Dần"
    MAO = "Mão"
    THIN = "Thìn"
    TY2 = "Tỵ"
    NGO = "Ngọ"
    MUI = "Mùi"
    THAN = "Thân"
    DAU = "Dậu"
    TUAT = "Tuất"
    HOI = "Hợi"


# =============================================================================
# Ten Gods
# =============================================================================

class TenGod(Enum):
    BIEN_TAI = "Thiên Tài"
    CHINH_TAI = "Chính Tài"

    THAT_SAT = "Thất Sát"
    CHINH_QUAN = "Chính Quan"

    THUC_THAN = "Thực Thần"
    THUONG_QUAN = "Thương Quan"

    THIEN_AN = "Thiên Ấn"
    CHINH_AN = "Chính Ấn"

    TY_KIEN = "Tỷ Kiên"
    KIEP_TAI = "Kiếp Tài"


# =============================================================================
# Luck
# =============================================================================

class LuckType(Enum):
    NATAL = "Mệnh Cục"
    MAJOR = "Đại Vận"
    YEAR = "Lưu Niên"
    MONTH = "Lưu Nguyệt"
    DAY = "Lưu Nhật"
    HOUR = "Lưu Thời"


# =============================================================================
# Direction
# =============================================================================

class Direction(Enum):
    NORTH = "Bắc"
    SOUTH = "Nam"
    EAST = "Đông"
    WEST = "Tây"

    NORTHEAST = "Đông Bắc"
    NORTHWEST = "Tây Bắc"

    SOUTHEAST = "Đông Nam"
    SOUTHWEST = "Tây Nam"


# =============================================================================
# Season
# =============================================================================

class Season(Enum):
    SPRING = "Xuân"
    SUMMER = "Hạ"
    AUTUMN = "Thu"
    WINTER = "Đông"


# =============================================================================
# Moon Phase
# =============================================================================

class MoonPhase(Enum):
    NEW_MOON = "Sóc"
    FIRST_QUARTER = "Thượng Huyền"
    FULL_MOON = "Vọng"
    LAST_QUARTER = "Hạ Huyền"


# =============================================================================
# Report
# =============================================================================

class ReportFormat(Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    HTML = "html"
    JSON = "json"


# =============================================================================
# Rule
# =============================================================================

class RuleCategory(Enum):
    BASIC = "basic"

    DAY_MASTER = "day_master"

    FIVE_ELEMENTS = "five_elements"

    TEN_GODS = "ten_gods"

    USEFUL_GOD = "useful_god"

    CAREER = "career"

    WEALTH = "wealth"

    MARRIAGE = "marriage"

    HEALTH = "health"

    LUCK = "luck"

    FENGSHUI = "fengshui"


# =============================================================================
# Relationship
# =============================================================================

class RelationType(Enum):
    GENERATE = "Sinh"

    CONTROL = "Khắc"

    COMBINATION = "Hợp"

    CLASH = "Xung"

    HARM = "Hại"

    PUNISHMENT = "Hình"

    DESTRUCTION = "Phá"


# =============================================================================
# Calendar
# =============================================================================

class CalendarType(Enum):
    SOLAR = "Dương lịch"
    LUNAR = "Âm lịch"


# =============================================================================
# Score
# =============================================================================

class ScoreLevel(IntEnum):
    VERY_LOW = 20
    LOW = 40
    NORMAL = 60
    HIGH = 80
    EXCELLENT = 100


# =============================================================================
# Log
# =============================================================================

class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
