"""
BTE Platform
Interpretation Engine Configuration
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

TEMPLATE_DIR = ROOT_DIR / "templates"

ASSET_DIR = ROOT_DIR / "assets"

CACHE_DIR = ROOT_DIR / "__cache__"


@dataclass(slots=True)
class InterpretationConfig:

    engine_name: str = ENGINE_NAME

    engine_version: str = ENGINE_VERSION

    debug: bool = False

    language: str = "vi"

    template_name: str = "default"

    output_format: str = "markdown"

    template_directory: Path = TEMPLATE_DIR

    asset_directory: Path = ASSET_DIR

    data_directory: Path = DATA_DIR

    cache_directory: Path = CACHE_DIR

    cache_enabled: bool = True

    enable_logging: bool = True

    options: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs):

        for k, v in kwargs.items():

            if hasattr(self, k):

                setattr(self, k, v)


DEFAULT_CONFIG = InterpretationConfig()
