"""
BTE Platform
Bazi Engine Exceptions
"""

from __future__ import annotations


class BaziError(Exception):
    """Base Exception của Bazi Engine."""
    pass


# ==========================================================
# Validation
# ==========================================================

class BaziValidationError(BaziError):
    pass


class InvalidBirthDataError(BaziValidationError):
    pass


class InvalidCalendarError(BaziValidationError):
    pass


class InvalidPillarError(BaziValidationError):
    pass


class InvalidStemError(BaziValidationError):
    pass


class InvalidBranchError(BaziValidationError):
    pass


# ==========================================================
# Data
# ==========================================================

class BaziDataError(BaziError):
    pass


class RuleNotFoundError(BaziDataError):
    pass


class DataLoadError(BaziDataError):
    pass


class DatabaseError(BaziDataError):
    pass


# ==========================================================
# Calculation
# ==========================================================

class BaziCalculationError(BaziError):
    pass


class FourPillarsError(BaziCalculationError):
    pass


class HiddenStemError(BaziCalculationError):
    pass


class TenGodError(BaziCalculationError):
    pass


class StrengthCalculationError(BaziCalculationError):
    pass


class UsefulGodCalculationError(BaziCalculationError):
    pass


class PatternCalculationError(BaziCalculationError):
    pass


class ShenShaCalculationError(BaziCalculationError):
    pass


class LuckCalculationError(BaziCalculationError):
    pass


# ==========================================================
# Engine
# ==========================================================

class BaziEngineError(BaziError):
    pass


class EngineInitializeError(BaziEngineError):
    pass


class EngineExecutionError(BaziEngineError):
    pass


class EngineConfigurationError(BaziEngineError):
    pass
