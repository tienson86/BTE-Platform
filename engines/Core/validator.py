"""
===============================================================================
BTE Platform - Core Validator
===============================================================================

Các hàm kiểm tra dữ liệu dùng chung cho toàn bộ BTE Platform.

Chức năng:
    • Kiểm tra ngày giờ sinh
    • Kiểm tra tọa độ
    • Kiểm tra giới tính
    • Kiểm tra Can Chi
    • Kiểm tra Rule
    • Kiểm tra Score
    • Kiểm tra Engine Input

Author : BTE Platform
Version: 1.0.0
===============================================================================
"""

from datetime import datetime

from .exceptions import (
    ValidationError,
    BirthDataError,
    DateTimeError,
    LocationError,
    GenderError,
)

from .enums import (
    HeavenlyStem,
    EarthlyBranch,
    Gender,
)

from .constants import (
    MAX_RULE_SCORE,
    MIN_RULE_SCORE,
)
# =============================================================================
# Birth Information
# =============================================================================

def validate_birth_datetime(dt: datetime) -> bool:
    """
    Kiểm tra ngày giờ sinh.

    Parameters
    ----------
    dt : datetime

    Returns
    -------
    bool
    """

    if not isinstance(dt, datetime):
        raise DateTimeError("Birth datetime must be datetime object.")

    if dt.year < 1800:
        raise BirthDataError("Birth year is too early.")

    if dt.year > 2200:
        raise BirthDataError("Birth year is too large.")

    return True
  # =============================================================================
# Gender
# =============================================================================

def validate_gender(gender) -> bool:

    if isinstance(gender, Gender):
        return True

    values = [g.value for g in Gender]

    if gender not in values:
        raise GenderError(f"Invalid gender: {gender}")

    return True
  # =============================================================================
# Location
# =============================================================================

def validate_latitude(latitude: float):

    if not isinstance(latitude, (float, int)):
        raise LocationError("Latitude must be numeric.")

    if latitude < -90 or latitude > 90:
        raise LocationError("Latitude out of range.")

    return True


def validate_longitude(longitude: float):

    if not isinstance(longitude, (float, int)):
        raise LocationError("Longitude must be numeric.")

    if longitude < -180 or longitude > 180:
        raise LocationError("Longitude out of range.")

    return True
  # =============================================================================
# Heavenly Stem
# =============================================================================

def validate_stem(stem):

    if isinstance(stem, HeavenlyStem):
        return True

    values = [x.value for x in HeavenlyStem]

    if stem not in values:
        raise ValidationError(f"Invalid Heavenly Stem: {stem}")

    return True
  # =============================================================================
# Earthly Branch
# =============================================================================

def validate_branch(branch):

    if isinstance(branch, EarthlyBranch):
        return True

    values = [x.value for x in EarthlyBranch]

    if branch not in values:
        raise ValidationError(f"Invalid Earthly Branch: {branch}")

    return True
  # =============================================================================
# Rule Score
# =============================================================================

def validate_score(score):

    if not isinstance(score, (int, float)):
        raise ValidationError("Score must be numeric.")

    if score < MIN_RULE_SCORE:
        raise ValidationError("Score too small.")

    if score > MAX_RULE_SCORE:
        raise ValidationError("Score too large.")

    return True
  # =============================================================================
# Rule
# =============================================================================

def validate_rule(rule: dict):

    if not isinstance(rule, dict):
        raise ValidationError("Rule must be dict.")

    required = [
        "rule_id",
        "condition",
        "score",
    ]

    for key in required:

        if key not in rule:
            raise ValidationError(
                f"Missing field: {key}"
            )

    validate_score(rule["score"])

    return True
  # =============================================================================
# Engine Result
# =============================================================================

def validate_engine_result(result):

    if not isinstance(result, dict):
        raise ValidationError("Engine result must be dict.")

    return True
  # =============================================================================
# CSV
# =============================================================================

def validate_csv_row(row):

    if not isinstance(row, dict):
        raise ValidationError("CSV row must be dict.")

    if len(row) == 0:
        raise ValidationError("CSV row is empty.")

    return True
  # =============================================================================
# JSON
# =============================================================================

def validate_json(data):

    if not isinstance(data, dict):
        raise ValidationError("JSON must be dict.")

    return True
  # =============================================================================
# Report
# =============================================================================

def validate_report(report):

    if not isinstance(report, dict):
        raise ValidationError("Report must be dict.")

    return True
  # =============================================================================
# Bazi Chart
# =============================================================================

def validate_bazi_chart(chart):

    if not isinstance(chart, dict):
        raise ValidationError("Bazi chart must be dict.")

    required = [
        "year",
        "month",
        "day",
        "hour",
    ]

    for key in required:

        if key not in chart:
            raise ValidationError(
                f"Missing pillar: {key}"
            )

    return True
  # =============================================================================
# Helper
# =============================================================================

def is_valid(obj, validator):

    try:
        validator(obj)
        return True

    except ValidationError:
        return False
      
