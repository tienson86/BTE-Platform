"""
===============================================================================
Bazi Engine - Custom Exceptions
-------------------------------------------------------------------------------
Định nghĩa các ngoại lệ (Exception) dùng chung cho toàn bộ Bazi Engine.

Nguyên tắc:
- Không chứa logic nghiệp vụ.
- Chỉ định nghĩa các Exception.
- Tất cả module trong Engine đều sử dụng các Exception này.
===============================================================================
"""

from __future__ import annotations


# =============================================================================
# BASE
# =============================================================================

class BaziEngineError(Exception):
    """
    Ngoại lệ gốc của Bazi Engine.
    """
    pass


# =============================================================================
# CONFIG
# =============================================================================

class ConfigurationError(BaziEngineError):
    """
    Lỗi cấu hình hệ thống.
    """
    pass


# =============================================================================
# DATA
# =============================================================================

class DataError(BaziEngineError):
    """
    Lỗi dữ liệu.
    """
    pass


class DataNotFoundError(DataError):
    """
    Không tìm thấy dữ liệu.
    """
    pass


class InvalidDataError(DataError):
    """
    Dữ liệu không hợp lệ.
    """
    pass


class DuplicateDataError(DataError):
    """
    Dữ liệu bị trùng.
    """
    pass


# =============================================================================
# INPUT
# =============================================================================

class InvalidInputError(BaziEngineError):
    """
    Dữ liệu đầu vào không hợp lệ.
    """
    pass


class InvalidDateError(InvalidInputError):
    """
    Ngày tháng không hợp lệ.
    """
    pass


class InvalidTimeError(InvalidInputError):
    """
    Giờ phút không hợp lệ.
    """
    pass


class InvalidGenderError(InvalidInputError):
    """
    Giới tính không hợp lệ.
    """
    pass


# =============================================================================
# CALCULATION
# =============================================================================

class CalculationError(BaziEngineError):
    """
    Lỗi trong quá trình tính toán.
    """
    pass


class PillarCalculationError(CalculationError):
    """
    Lỗi tính Tứ Trụ.
    """
    pass


class HiddenStemCalculationError(CalculationError):
    """
    Lỗi tính Tàng Can.
    """
    pass


class TenGodCalculationError(CalculationError):
    """
    Lỗi tính Thập Thần.
    """
    pass


class StrengthCalculationError(CalculationError):
    """
    Lỗi tính Thân Vượng / Thân Nhược.
    """
    pass


class UsefulGodCalculationError(CalculationError):
    """
    Lỗi xác định Dụng Thần.
    """
    pass


class LuckCalculationError(CalculationError):
    """
    Lỗi tính Đại Vận / Lưu Niên.
    """
    pass


class ShenShaCalculationError(CalculationError):
    """
    Lỗi tính Thần Sát.
    """
    pass


# =============================================================================
# EXPORT
# =============================================================================

class ExportError(BaziEngineError):
    """
    Lỗi xuất dữ liệu.
    """
    pass


# =============================================================================
# IMPORT
# =============================================================================

class ImportErrorEngine(BaziEngineError):
    """
    Lỗi nhập dữ liệu.
    """
    pass


# =============================================================================
# CACHE
# =============================================================================

class CacheError(BaziEngineError):
    """
    Lỗi bộ nhớ đệm.
    """
    pass


# =============================================================================
# VALIDATION
# =============================================================================

class ValidationError(BaziEngineError):
    """
    Lỗi kiểm tra dữ liệu.
    """
    pass


# =============================================================================
# RULE ENGINE
# =============================================================================

class RuleError(BaziEngineError):
    """
    Lỗi Rule Engine.
    """
    pass


class RuleNotFoundError(RuleError):
    """
    Không tìm thấy Rule.
    """
    pass


class RuleExecutionError(RuleError):
    """
    Lỗi thực thi Rule.
    """
    pass
