"""
BTE Platform

Calendar Router

File: calendar.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.request import CalendarRequest
from api.schemas.response import CalendarResponse, ErrorResponse
from api.services.pipeline_service import PipelineService


router = APIRouter()

service = PipelineService()


# ==========================================================
# Calendar Engine
# ==========================================================

@router.post(
    "/",
    response_model=CalendarResponse,
    summary="Calculate Calendar",
)
def calculate_calendar(
    request: CalendarRequest,
) -> CalendarResponse:
    """
    Tính toán dữ liệu lịch âm dương.
    """

    try:

        result = service.calendar(
            request.model_dump()
        )

        return CalendarResponse(
            success=True,
            message="Calendar calculation completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Solar -> Lunar
# ==========================================================

@router.post(
    "/solar-to-lunar",
    response_model=CalendarResponse,
    summary="Solar to Lunar",
)
def solar_to_lunar(
    request: CalendarRequest,
) -> CalendarResponse:
    """
    Chuyển đổi Dương lịch sang Âm lịch.
    """

    try:

        result = service.calendar(
            request.model_dump()
        )

        return CalendarResponse(
            success=True,
            message="Solar to Lunar conversion completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Lunar -> Solar
# ==========================================================

@router.post(
    "/lunar-to-solar",
    response_model=CalendarResponse,
    summary="Lunar to Solar",
)
def lunar_to_solar(
    request: CalendarRequest,
) -> CalendarResponse:
    """
    Chuyển đổi Âm lịch sang Dương lịch.
    """

    try:

        result = service.calendar(
            request.model_dump()
        )

        return CalendarResponse(
            success=True,
            message="Lunar to Solar conversion completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Four Pillars
# ==========================================================

@router.post(
    "/pillars",
    response_model=CalendarResponse,
    summary="Calculate Four Pillars",
)
def calculate_pillars(
    request: CalendarRequest,
) -> CalendarResponse:
    """
    Tính Can Chi năm, tháng, ngày, giờ.
    """

    try:

        result = service.calendar(
            request.model_dump()
        )

        return CalendarResponse(
            success=True,
            message="Four Pillars calculated successfully.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
