"""
BTE Platform
Calendar Engine Configuration

Quản lý cấu hình cho Calendar Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .constants import (
    DEFAULT_CACHE,
    DEFAULT_COUNTRY,
    DEFAULT_HIGH_PRECISION,
    DEFAULT_LANGUAGE,
    DEFAULT_TIMEZONE,
    DEFAULT_TRUE_SOLAR_TIME,
    ENGINE_NAME,
    ENGINE_VERSION,
)


# ==========================================================
# Data Paths
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"

CACHE_DIR = ROOT_DIR / "__cache__"

LOG_DIR = ROOT_DIR / "__logs__"


# ==========================================================
# Calendar Config
# ==========================================================

@dataclass(slots=True)
class CalendarConfig:
    """
    Cấu hình của Calendar Engine.
    """

    # ------------------------------------------------------
    # Engine
    # ------------------------------------------------------

    engine_name: str = ENGINE_NAME

    engine_version: str = ENGINE_VERSION

    enabled: bool = True

    debug: bool = False

    # ------------------------------------------------------
    # Locale
    # ------------------------------------------------------

    language: str = DEFAULT_LANGUAGE

    country: str = DEFAULT_COUNTRY

    timezone: float = DEFAULT_TIMEZONE

    # ------------------------------------------------------
    # Calculation
    # ------------------------------------------------------

    use_true_solar_time: bool = DEFAULT_TRUE_SOLAR_TIME

    use_high_precision: bool = DEFAULT_HIGH_PRECISION

    use_delta_t: bool = True

    calculate_moon_phase: bool = True

    calculate_solar_term: bool = True

    calculate_four_pillars: bool = True

    # ------------------------------------------------------
    # Cache
    # ------------------------------------------------------

    cache_enabled: bool = DEFAULT_CACHE

    cache_directory: Path = CACHE_DIR

    cache_size: int = 256

    # ------------------------------------------------------
    # Data
    # ------------------------------------------------------

    data_directory: Path = DATA_DIR

    auto_reload_data: bool = False

    validate_data: bool = True

    # ------------------------------------------------------
    # Log
    # ------------------------------------------------------

    log_directory: Path = LOG_DIR

    enable_logging: bool = True

    log_level: str = "INFO"

    # ------------------------------------------------------
    # Extension
    # ------------------------------------------------------

    options: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ======================================================
    # Methods
    # ======================================================

    def update(self, **kwargs: Any) -> None:
        """
        Cập nhật cấu hình.
        """

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> dict[str, Any]:
        """
        Chuyển cấu hình thành dict.
        """

        return {
            "engine_name": self.engine_name,
            "engine_version": self.engine_version,
            "enabled": self.enabled,
            "debug": self.debug,
            "language": self.language,
            "country": self.country,
            "timezone": self.timezone,
            "use_true_solar_time": self.use_true_solar_time,
            "use_high_precision": self.use_high_precision,
            "use_delta_t": self.use_delta_t,
            "calculate_moon_phase": self.calculate_moon_phase,
            "calculate_solar_term": self.calculate_solar_term,
            "calculate_four_pillars": self.calculate_four_pillars,
            "cache_enabled": self.cache_enabled,
            "cache_directory": str(self.cache_directory),
            "cache_size": self.cache_size,
            "data_directory": str(self.data_directory),
            "auto_reload_data": self.auto_reload_data,
            "validate_data": self.validate_data,
            "log_directory": str(self.log_directory),
            "enable_logging": self.enable_logging,
            "log_level": self.log_level,
            "options": self.options,
            "metadata": self.metadata,
        }

    @classmethod
    def default(cls) -> "CalendarConfig":
        """
        Trả về cấu hình mặc định.
        """

        return cls()


# ==========================================================
# Default Config Instance
# ==========================================================

DEFAULT_CONFIG = CalendarConfig()
