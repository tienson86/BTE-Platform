"""
===============================================================================
BTE Platform - Core Exceptions
===============================================================================

Định nghĩa toàn bộ Exception dùng chung cho BTE Platform.

Tất cả Engine đều kế thừa từ BTEError.

Author : BTE Platform
Version: 1.0.0
===============================================================================
"""

# =============================================================================
# Base Exception
# =============================================================================

class BTEError(Exception):
    """Base Exception của toàn bộ BTE Platform."""

    def __init__(self, message="Unknown BTE Error"):
        self.message = message
        super().__init__(message)


# =============================================================================
# Config
# =============================================================================

class ConfigError(BTEError):
    """Lỗi cấu hình hệ thống."""


# =============================================================================
# Validation
# =============================================================================

class ValidationError(BTEError):
    """Lỗi kiểm tra dữ liệu đầu vào."""


class BirthDataError(ValidationError):
    """Sai dữ liệu ngày giờ sinh."""


class DateTimeError(ValidationError):
    """Sai định dạng ngày giờ."""


class LocationError(ValidationError):
    """Sai thông tin vị trí."""


class GenderError(ValidationError):
    """Sai giới tính."""


# =============================================================================
# Database
# =============================================================================

class DatabaseError(BTEError):
    """Lỗi truy cập cơ sở dữ liệu."""


class CSVError(DatabaseError):
    """Lỗi đọc hoặc ghi CSV."""


class JSONError(DatabaseError):
    """Lỗi đọc hoặc ghi JSON."""


class RuleNotFoundError(DatabaseError):
    """Không tìm thấy Rule."""


class DataIntegrityError(DatabaseError):
    """Dữ liệu không nhất quán."""


# =============================================================================
# Calendar Engine
# =============================================================================

class CalendarError(BTEError):
    """Lỗi Calendar Engine."""


class JulianDayError(CalendarError):
    """Lỗi Julian Day."""


class SolarTermError(CalendarError):
    """Lỗi Tiết Khí."""


class NewMoonError(CalendarError):
    """Lỗi Sóc."""


class LunarCalendarError(CalendarError):
    """Lỗi chuyển đổi Âm lịch."""


class TimeZoneError(CalendarError):
    """Lỗi múi giờ."""


# =============================================================================
# Bazi Engine
# =============================================================================

class BaziError(BTEError):
    """Lỗi Bát Tự."""


class StemError(BaziError):
    """Sai Thiên Can."""


class BranchError(BaziError):
    """Sai Địa Chi."""


class HiddenStemError(BaziError):
    """Sai Tàng Can."""


class FiveElementError(BaziError):
    """Sai Ngũ Hành."""


class TenGodError(BaziError):
    """Sai Thập Thần."""


class UsefulGodError(BaziError):
    """Sai Dụng Thần."""


class ChartBuildError(BaziError):
    """Không tạo được lá số."""


# =============================================================================
# Interpretation Engine
# =============================================================================

class InterpretationError(BTEError):
    """Lỗi Engine Diễn Giải."""


class RuleMatchError(InterpretationError):
    """Không match được Rule."""


class RuleScoreError(InterpretationError):
    """Lỗi chấm điểm Rule."""


class TemplateError(InterpretationError):
    """Lỗi Template."""


class SentenceGenerationError(InterpretationError):
    """Lỗi sinh câu."""


# =============================================================================
# Report Engine
# =============================================================================

class ReportError(BTEError):
    """Lỗi Report Engine."""


class ExportError(ReportError):
    """Lỗi xuất báo cáo."""


class PDFError(ReportError):
    """Lỗi PDF."""


class DOCXError(ReportError):
    """Lỗi DOCX."""


class XLSXError(ReportError):
    """Lỗi XLSX."""


class HTMLRenderError(ReportError):
    """Lỗi render HTML."""


class TemplateRenderError(ReportError):
    """Lỗi render Template."""


# =============================================================================
# Engine
# =============================================================================

class EngineError(BTEError):
    """Lỗi Engine chung."""


class EngineNotFoundError(EngineError):
    """Không tìm thấy Engine."""


class EngineInitializeError(EngineError):
    """Khởi tạo Engine thất bại."""


class EngineExecutionError(EngineError):
    """Thực thi Engine thất bại."""


# =============================================================================
# Registry
# =============================================================================

class RegistryError(BTEError):
    """Lỗi Registry."""


class DuplicateRegistrationError(RegistryError):
    """Đăng ký trùng."""


class ComponentNotFoundError(RegistryError):
    """Không tìm thấy Component."""


# =============================================================================
# Cache
# =============================================================================

class CacheError(BTEError):
    """Lỗi Cache."""


# =============================================================================
# Plugin
# =============================================================================

class PluginError(BTEError):
    """Lỗi Plugin."""


# =============================================================================
# Security
# =============================================================================

class PermissionDeniedError(BTEError):
    """Không đủ quyền truy cập."""


class AuthenticationError(BTEError):
    """Xác thực thất bại."""


# =============================================================================
# Unknown
# =============================================================================

class UnknownSystemError(BTEError):
    """Lỗi hệ thống chưa xác định."""
