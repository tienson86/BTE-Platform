"""
===============================================================================
Bazi Engine - Logger
-------------------------------------------------------------------------------
Ghi log cho toàn bộ Bazi Engine.

Chức năng:
- Ghi log Console.
- Ghi log File.
- Chuẩn hóa định dạng log.
- Có thể dùng chung cho toàn bộ Engine.
===============================================================================
"""

from __future__ import annotations

import logging
from pathlib import Path

from .config import LOG_DIR, LOG_FILE, LOG_LEVEL


# =============================================================================
# CREATE LOG DIRECTORY
# =============================================================================

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)


# =============================================================================
# LOGGER
# =============================================================================

LOGGER_NAME = "BaziEngine"

logger = logging.getLogger(LOGGER_NAME)


# Tránh tạo nhiều handler khi import nhiều lần
if not logger.handlers:

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -------------------------------------------------------------------------
    # Console
    # -------------------------------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # -------------------------------------------------------------------------
    # File
    # -------------------------------------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    # -------------------------------------------------------------------------
    # Add handlers
    # -------------------------------------------------------------------------

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def debug(message: str) -> None:
    logger.debug(message)


def info(message: str) -> None:
    logger.info(message)


def warning(message: str) -> None:
    logger.warning(message)


def error(message: str) -> None:
    logger.error(message)


def critical(message: str) -> None:
    logger.critical(message)


def exception(message: str) -> None:
    logger.exception(message)


# =============================================================================
# STARTUP LOG
# =============================================================================

logger.info("==============================================")
logger.info("Bazi Engine Logger initialized successfully.")
logger.info("==============================================")
