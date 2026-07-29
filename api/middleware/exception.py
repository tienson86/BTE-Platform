"""
BTE Platform

Exception Middleware

File: exception.py
Version: 1.0
"""

from __future__ import annotations

import traceback

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# ==========================================================
# HTTP Exception
# ==========================================================

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """
    Xử lý HTTPException.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error": "HTTPException",
        },
    )


# ==========================================================
# Validation Exception
# ==========================================================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Xử lý lỗi validate Request.
    """

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": exc.errors(),
        },
    )


# ==========================================================
# Unexpected Exception
# ==========================================================

async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Xử lý mọi Exception còn lại.
    """

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
            "error": exc.__class__.__name__,
        },
    )


# ==========================================================
# Register
# ==========================================================

def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Đăng ký toàn bộ Exception Handler.
    """

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        general_exception_handler,
    )
