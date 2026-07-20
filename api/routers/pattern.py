"""
BTE Platform

Pattern Router

File: pattern.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.request import PatternRequest
from api.schemas.response import PatternResponse
from api.services.pipeline_service import PipelineService


router = APIRouter()

service = PipelineService()


# ==========================================================
# Pattern
# ==========================================================

@router.post(
    "/",
    response_model=PatternResponse,
    summary="Pattern Analysis",
)
def pattern(
    request: PatternRequest,
) -> PatternResponse:
    """
    Phân tích Cách Cục.
    """

    try:

        result = service.pattern(
            request.model_dump()
        )

        return PatternResponse(
            success=True,
            message="Pattern analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Strength
# ==========================================================

@router.post(
    "/strength",
    response_model=PatternResponse,
    summary="Body Strength",
)
def strength(
    request: PatternRequest,
) -> PatternResponse:
    """
    Đánh giá Thân Vượng/Nhược.
    """

    try:

        result = service.pattern(
            request.model_dump()
        )

        return PatternResponse(
            success=True,
            message="Strength analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Useful God
# ==========================================================

@router.post(
    "/useful-god",
    response_model=PatternResponse,
    summary="Useful God",
)
def useful_god(
    request: PatternRequest,
) -> PatternResponse:
    """
    Phân tích Dụng Thần.
    """

    try:

        result = service.pattern(
            request.model_dump()
        )

        return PatternResponse(
            success=True,
            message="Useful God analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Favorable Elements
# ==========================================================

@router.post(
    "/favorable-elements",
    response_model=PatternResponse,
    summary="Favorable Elements",
)
def favorable_elements(
    request: PatternRequest,
) -> PatternResponse:
    """
    Phân tích Hỷ Thần - Kỵ Thần.
    """

    try:

        result = service.pattern(
            request.model_dump()
        )

        return PatternResponse(
            success=True,
            message="Favorable elements analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
