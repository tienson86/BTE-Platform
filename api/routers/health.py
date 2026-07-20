"""
BTE Platform

Health Router

File: health.py
Version: 1.0
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter

from api.config import config
from api.schemas.response import HealthResponse


router = APIRouter()


# ==========================================================
# Health Check
# ==========================================================

@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
)
def health() -> HealthResponse:
    """
    Kiểm tra trạng thái của API.
    """

    return HealthResponse(
        success=True,
        message="BTE Platform is running.",
        service=config.api.title,
        version=config.api.version,
        status="healthy",
    )


# ==========================================================
# Ping
# ==========================================================

@router.get(
    "/ping",
    summary="Ping",
)
def ping() -> dict:
    """
    Kiểm tra kết nối.
    """

    return {
        "success": True,
        "message": "pong",
    }


# ==========================================================
# Version
# ==========================================================

@router.get(
    "/version",
)
def version() -> dict:
    """
    Thông tin phiên bản.
    """

    return {
        "name": config.api.title,
        "version": config.api.version,
        "description": config.api.description,
    }


# ==========================================================
# Status
# ==========================================================

@router.get(
    "/status",
)
def status() -> dict:
    """
    Thông tin trạng thái hệ thống.
    """

    return {
        "status": "healthy",
        "time": datetime.now().isoformat(),
        "api": True,
    }
