"""
===============================================================================
Bazi Engine - Configuration
-------------------------------------------------------------------------------
Quản lý toàn bộ cấu hình của Bazi Engine.

Nguyên tắc:
- Không chứa logic nghiệp vụ.
- Không đọc dữ liệu.
- Chỉ khai báo đường dẫn, encoding và tham số hệ thống.
===============================================================================
"""

from pathlib import Path

# =============================================================================
# PROJECT PATH
# =============================================================================

CURRENT_DIR = Path(__file__).resolve().parent

BAZI_ENGINE_DIR = CURRENT_DIR.parent

ENGINE_DIR = BAZI_ENGINE_DIR.parent

PROJECT_ROOT = ENGINE_DIR.parent

# =============================================================================
# DATA DIRECTORIES
# =============================================================================

DATABASE_DIR = PROJECT_ROOT / "database"

RULE_DIR = PROJECT_ROOT / "rules"

ASSETS_DIR = PROJECT_ROOT / "assets"

CACHE_DIR = PROJECT_ROOT / "cache"

TEMP_DIR = PROJECT_ROOT / "temp"

LOG_DIR = PROJECT_ROOT / "logs"

REPORT_DIR = PROJECT_ROOT / "reports"

TEMPLATE_DIR = PROJECT_ROOT / "templates"

EXPORT_DIR = PROJECT_ROOT / "exports"

# =============================================================================
# CALENDAR DATABASE
# =============================================================================

CALENDAR_DATA_DIR = DATABASE_DIR / "calendar"

SOLAR_TERM_DIR = CALENDAR_DATA_DIR / "solar_terms"

MOON_PHASE_DIR = CALENDAR_DATA_DIR / "moon"

EPHEMERIS_DIR = CALENDAR_DATA_DIR / "ephemeris"

# =============================================================================
# BAZI DATABASE
# =============================================================================

BAZI_DATA_DIR = DATABASE_DIR / "bazi"

STEM_DIR = BAZI_DATA_DIR / "heavenly_stems"

BRANCH_DIR = BAZI_DATA_DIR / "earthly_branches"

TEN_GOD_DIR = BAZI_DATA_DIR / "ten_gods"

HIDDEN_STEM_DIR = BAZI_DATA_DIR / "hidden_stems"

NAYIN_DIR = BAZI_DATA_DIR / "nayin"

SHENSHA_DIR = BAZI_DATA_DIR / "shen_sha"

USEFUL_GOD_DIR = BAZI_DATA_DIR / "useful_god"

LUCK_DIR = BAZI_DATA_DIR / "luck"

# =============================================================================
# FILE SETTINGS
# =============================================================================

DEFAULT_ENCODING = "utf-8"

CSV_DELIMITER = ","

CSV_QUOTECHAR = '"'

CSV_NEWLINE = ""

# =============================================================================
# CACHE
# =============================================================================

ENABLE_CACHE = True

CACHE_SIZE = 512

CACHE_EXPIRE_SECONDS = 3600

# =============================================================================
# LOGGING
# =============================================================================

ENABLE_LOG = True

LOG_LEVEL = "INFO"

LOG_FILE = LOG_DIR / "bazi_engine.log"

# =============================================================================
# DEBUG
# =============================================================================

DEBUG = False

STRICT_MODE = True

# =============================================================================
# REPORT
# =============================================================================

DEFAULT_LANGUAGE = "vi"

DEFAULT_TIMEZONE = "Asia/Ho_Chi_Minh"

DEFAULT_DATE_FORMAT = "%d/%m/%Y"

DEFAULT_DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"

# =============================================================================
# EXPORT
# =============================================================================

EXPORT_JSON = True

EXPORT_CSV = False

EXPORT_XML = False

EXPORT_PDF = True

# =============================================================================
# PERFORMANCE
# =============================================================================

MAX_WORKERS = 4

ENABLE_MULTITHREAD = False

ENABLE_MULTIPROCESS = False

# =============================================================================
# VALIDATION
# =============================================================================

MIN_YEAR = 1600

MAX_YEAR = 2300
