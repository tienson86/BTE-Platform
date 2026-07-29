"""
BTE Platform

Logging Middleware

File: logging.py
Version: 1.0
"""

from __future__ import annotations

import logging
import time

from fastapi import FastAPI
from fastapi import Request


# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger("bte.api")


def setup_logging() -> None:
    """
    Khởi tạo Logging.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
    )


# ==========================================================
# Middleware
# ==========================================================

def register_logging(app: FastAPI) -> None:
    """
    Đăng ký Logging Middleware.
    """

    @app.middleware("http")
    async def logging_middleware(
        request: Request,
        call_next,
    ):
        start = time.perf_counter()

        response = await call_next(request)

        elapsed = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            "%s %s -> %s (%.2f ms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )

        return response
