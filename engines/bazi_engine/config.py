"""
BTE Platform
Bazi Engine Configuration
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .constants import (
    ENGINE_NAME,
    ENGINE_VERSION,
)


ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"

CACHE_DIR = ROOT_DIR / "__cache__"

LOG_DIR = ROOT_DIR / "__logs__"


@dataclass(slots=True)
class BaziConfig:
    """
    Cấu hình của Bazi Engine.
    """

    # Engine

    engine_name: str = ENGINE_NAME

    engine_version: str = ENGINE_VERSION

    enabled: bool = True

    debug: bool = False

    # Data

    data_directory: Path = DATA_DIR

    validate_data: bool = True

    auto_reload: bool = False

    # Cache

    cache_enabled: bool = True

    cache_directory: Path = CACHE_DIR

    cache_size: int = 512

    # Logging

    enable_logging: bool = True

    log_directory: Path = LOG_DIR

    log_level: str = "INFO"

    # Calculation

    calculate_strength: bool = True

    calculate_pattern: bool = True

    calculate_useful_god: bool = True

    calculate_shensha: bool = True

    calculate_luck: bool = True

    # Extension

    options: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------

    def update(self, **kwargs: Any) -> None:

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> dict[str, Any]:

        return {
            "engine_name": self.engine_name,
            "engine_version": self.engine_version,
            "enabled": self.enabled,
            "debug": self.debug,
            "data_directory": str(self.data_directory),
            "validate_data": self.validate_data,
            "auto_reload": self.auto_reload,
            "cache_enabled": self.cache_enabled,
            "cache_directory": str(self.cache_directory),
            "cache_size": self.cache_size,
            "enable_logging": self.enable_logging,
            "log_directory": str(self.log_directory),
            "log_level": self.log_level,
            "calculate_strength": self.calculate_strength,
            "calculate_pattern": self.calculate_pattern,
            "calculate_useful_god": self.calculate_useful_god,
            "calculate_shensha": self.calculate_shensha,
            "calculate_luck": self.calculate_luck,
            "options": self.options,
            "metadata": self.metadata,
        }

    @classmethod
    def default(cls) -> "BaziConfig":
        return cls()


DEFAULT_CONFIG = BaziConfig()
