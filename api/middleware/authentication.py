"""
BTE Platform

Authentication Middleware

File: authentication.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import Header
from fastapi import HTTPException


# ==========================================================
# API Key
# ==========================================================

API_KEY_HEADER = "X-API-Key"


def verify_api_key(
    api_key: str | None = Header(
        default=None,
        alias=API_KEY_HEADER,
    ),
) -> str:
    """
    Kiểm tra API Key.
    """

    if api_key is None:

        raise HTTPException(
            status_code=401,
            detail="Missing API Key.",
        )

    #
    # TODO:
    # Sau này đọc từ Config hoặc Database.
    #

    if api_key != "BTE_PLATFORM":

        raise HTTPException(
            status_code=401,
            detail="Invalid API Key.",
        )

    return api_key
