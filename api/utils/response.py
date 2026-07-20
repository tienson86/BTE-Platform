"""
BTE Platform

Response Utilities

File: response.py
Version: 1.0
"""

from __future__ import annotations

from typing import Any

from fastapi.responses import JSONResponse


# ==========================================================
# Success Response
# ==========================================================

def success_response(
    data: Any = None,
    message: str = "Success.",
    status_code: int = 200,
) -> JSONResponse:
    """
    Trả về Response thành công.
    """

    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )


# ==========================================================
# Error Response
# ==========================================================

def error_response(
    message: str,
    *,
    error: str | None = None,
    errors: Any = None,
    status_code: int = 400,
) -> JSONResponse:
    """
    Trả về Response lỗi.
    """

    content = {
        "success": False,
        "message": message,
    }

    if error is not None:
        content["error"] = error

    if errors is not None:
        content["errors"] = errors

    return JSONResponse(
        status_code=status_code,
        content=content,
    )


# ==========================================================
# Created Response
# ==========================================================

def created_response(
    data: Any = None,
    message: str = "Created.",
) -> JSONResponse:
    """
    Response tạo mới thành công.
    """

    return success_response(
        data=data,
        message=message,
        status_code=201,
    )


# ==========================================================
# No Content Response
# ==========================================================

def no_content_response() -> JSONResponse:
    """
    Response không có nội dung.
    """

    return JSONResponse(
        status_code=204,
        content=None,
    )


# ==========================================================
# Accepted Response
# ==========================================================

def accepted_response(
    data: Any = None,
    message: str = "Accepted.",
) -> JSONResponse:
    """
    Response đã tiếp nhận yêu cầu.
    """

    return success_response(
        data=data,
        message=message,
        status_code=202,
    )


# ==========================================================
# Pagination Response
# ==========================================================

def paged_response(
    items: list[Any],
    total: int,
    page: int,
    page_size: int,
    message: str = "Success.",
) -> JSONResponse:
    """
    Response phân trang.
    """

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": items,
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "pages": (
                    (total + page_size - 1) // page_size
                    if page_size > 0
                    else 0
                ),
            },
        },
    )
