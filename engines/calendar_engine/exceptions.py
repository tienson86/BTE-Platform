"""
BTE Platform
Calendar Engine Exceptions

Định nghĩa toàn bộ Exception của Calendar Engine.
"""

from __future__ import annotations


# ==========================================================
# Base Exception
# ==========================================================

class CalendarError(Exception):
    """
    Lớp cha của toàn bộ Calendar Engine Exception.
    """

    def __init__(
        self,
        message: str = "Calendar Engine Error",
    ) -> None:

        super().__init__(message)


# ==========================================================
# Validation
# ==========================================================

class CalendarValidationError(CalendarError):
    """
    Lỗi kiểm tra dữ liệu đầu vào.
    """
    pass


class InvalidDateError(CalendarValidationError):
    """
    Ngày tháng không hợp lệ.
    """
    pass


class InvalidTimezoneError(CalendarValidationError):
    """
    Múi giờ không hợp lệ.
    """
    pass


class InvalidCoordinateError(CalendarValidationError):
    """
    Kinh độ hoặc vĩ độ không hợp lệ.
    """
    pass


class InvalidLocationError(CalendarValidationError):
    """
    Thông tin địa điểm không hợp lệ.
    """
    pass


# ==========================================================
# Data
# ==========================================================

class CalendarDataError(CalendarError):
    """
    Lỗi dữ liệu Calendar.
    """
    pass


class DataFileNotFound(CalendarDataError):
    """
    Không tìm thấy file dữ liệu.
    """
    pass


class DataFormatError(CalendarDataError):
    """
    Sai định dạng dữ liệu.
    """
    pass


class DataLoadError(CalendarDataError):
    """
    Không thể đọc dữ liệu.
    """
    pass


# ==========================================================
# Calculation
# ==========================================================

class CalendarCalculationError(CalendarError):
    """
    Lỗi tính toán.
    """
    pass


class JulianDayError(CalendarCalculationError):
    """
    Lỗi tính Julian Day.
    """
    pass


class SolarTermCalculationError(CalendarCalculationError):
    """
    Lỗi tính Tiết khí.
    """
    pass


class LunarDateCalculationError(CalendarCalculationError):
    """
    Lỗi chuyển đổi âm lịch.
    """
    pass


class LeapMonthCalculationError(CalendarCalculationError):
    """
    Lỗi tính tháng nhuận.
    """
    pass


class MoonPhaseCalculationError(CalendarCalculationError):
    """
    Lỗi tính pha Mặt Trăng.
    """
    pass


class SunLongitudeCalculationError(CalendarCalculationError):
    """
    Lỗi tính kinh độ Mặt Trời.
    """
    pass


class MoonLongitudeCalculationError(CalendarCalculationError):
    """
    Lỗi tính kinh độ Mặt Trăng.
    """
    pass


# ==========================================================
# Ganzhi
# ==========================================================

class GanzhiCalculationError(CalendarCalculationError):
    """
    Lỗi tính Can Chi.
    """
    pass


class YearPillarError(GanzhiCalculationError):
    """
    Lỗi tính Can Chi năm.
    """
    pass


class MonthPillarError(GanzhiCalculationError):
    """
    Lỗi tính Can Chi tháng.
    """
    pass


class DayPillarError(GanzhiCalculationError):
    """
    Lỗi tính Can Chi ngày.
    """
    pass


class HourPillarError(GanzhiCalculationError):
    """
    Lỗi tính Can Chi giờ.
    """
    pass


# ==========================================================
# Engine
# ==========================================================

class CalendarEngineError(CalendarError):
    """
    Lỗi trong quá trình thực thi Engine.
    """
    pass


class CalendarInitializationError(CalendarEngineError):
    """
    Engine khởi tạo thất bại.
    """
    pass


class CalendarExecutionError(CalendarEngineError):
    """
    Engine thực thi thất bại.
    """
    pass


class CalendarConfigurationError(CalendarEngineError):
    """
    Cấu hình Engine không hợp lệ.
    """
    pass


# ==========================================================
# Loader
# ==========================================================

class CalendarLoaderError(CalendarError):
    """
    Lỗi Loader.
    """
    pass


class CacheError(CalendarLoaderError):
    """
    Lỗi bộ nhớ đệm.
    """
    pass


class ResourceNotFoundError(CalendarLoaderError):
    """
    Không tìm thấy tài nguyên.
    """
    pass


# ==========================================================
# Integration
# ==========================================================

class CalendarIntegrationError(CalendarError):
    """
    Lỗi tích hợp với Engine khác.
    """
    pass


class BaziIntegrationError(CalendarIntegrationError):
    """
    Lỗi kết nối với Bazi Engine.
    """
    pass


class ScoreIntegrationError(CalendarIntegrationError):
    """
    Lỗi kết nối với Score Engine.
    """
    pass


class PatternIntegrationError(CalendarIntegrationError):
    """
    Lỗi kết nối với Pattern Engine.
    """
    pass


class InterpretationIntegrationError(CalendarIntegrationError):
    """
    Lỗi kết nối với Interpretation Engine.
    """
    pass


class ReportIntegrationError(CalendarIntegrationError):
    """
    Lỗi kết nối với Report Engine.
    """
    pass
