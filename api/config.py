"""
BTE Platform

API Configuration

File: api/config.py
Version: 1.0
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


# ==========================================================
# Paths
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = ROOT_DIR / "database"

ENGINE_DIR = ROOT_DIR / "engines"

REPORT_DIR = ROOT_DIR / "reports"

LOG_DIR = ROOT_DIR / "logs"

TEMP_DIR = ROOT_DIR / "temp"


# ==========================================================
# API Config
# ==========================================================

@dataclass(slots=True)
class ApiConfig:

    title: str = "BTE Platform API"

    version: str = "1.0.0"

    description: str = (
        "Bazi & Feng Shui Engine Platform"
    )

    host: str = os.getenv(
        "BTE_HOST",
        "0.0.0.0",
    )

    port: int = int(
        os.getenv(
            "BTE_PORT",
            "8000",
        )
    )

    reload: bool = os.getenv(
        "BTE_RELOAD",
        "true",
    ).lower() == "true"

    debug: bool = os.getenv(
        "BTE_DEBUG",
        "false",
    ).lower() == "true"


# ==========================================================
# Engine Config
# ==========================================================

@dataclass(slots=True)
class EngineConfig:

    calendar: bool = True

    bazi: bool = True

    pattern: bool = True

    score: bool = True

    interpretation: bool = True

    report: bool = True


# ==========================================================
# Report Config
# ==========================================================

@dataclass(slots=True)
class ReportConfig:

    output_dir: Path = REPORT_DIR

    default_format: str = "markdown"

    template_dir: Path = (
        ROOT_DIR
        / "engines"
        / "report_engine"
        / "templates"
    )


# ==========================================================
# Log Config
# ==========================================================

@dataclass(slots=True)
class LogConfig:

    level: str = "INFO"

    directory: Path = LOG_DIR

    filename: str = "bte.log"


# ==========================================================
# Global Config
# ==========================================================

@dataclass(slots=True)
class Config:

    api: ApiConfig = ApiConfig()

    engine: EngineConfig = EngineConfig()

    report: ReportConfig = ReportConfig()

    log: LogConfig = LogConfig()


config = Config()


# ==========================================================
# Helpers
# ==========================================================

def ensure_directories() -> None:
    """
    Tạo các thư mục cần thiết.
    """

    for directory in (

        DATABASE_DIR,

        REPORT_DIR,

        LOG_DIR,

        TEMP_DIR,

    ):

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
