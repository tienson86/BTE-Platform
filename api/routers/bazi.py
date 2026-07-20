"""
BTE Platform

Bazi Router

File: bazi.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.request import BaziRequest
from api.schemas.response import BaziResponse
from api.services.pipeline_service import PipelineService


router = APIRouter()

service = PipelineService()


# ==========================================================
# Calculate Bazi
# ==========================================================

@router.post(
    "/",
    response_model=BaziResponse,
    summary="Calculate Bazi",
)
def calculate_bazi(
    request: BaziRequest,
) -> BaziResponse:
    """
    Lập Tứ Trụ Bát Tự.
    """

    try:

        result = service.bazi(
            request.model_dump()
        )

        return BaziResponse(
            success=True,
            message="Bazi calculated successfully.",
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
    response_model=BaziResponse,
    summary="Four Pillars",
)
def pillars(
    request: BaziRequest,
) -> BaziResponse:
    """
    Tính Tứ Trụ.
    """

    try:

        result = service.bazi(
            request.model_dump()
        )

        return BaziResponse(
            success=True,
            message="Four Pillars calculated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Ten Gods
# ==========================================================

@router.post(
    "/ten-gods",
    response_model=BaziResponse,
    summary="Ten Gods",
)
def ten_gods(
    request: BaziRequest,
) -> BaziResponse:
    """
    Tính Thập Thần.
    """

    try:

        result = service.bazi(
            request.model_dump()
        )

        return BaziResponse(
            success=True,
            message="Ten Gods calculated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Hidden Stems
# ==========================================================

@router.post(
    "/hidden-stems",
    response_model=BaziResponse,
    summary="Hidden Stems",
)
def hidden_stems(
    request: BaziRequest,
) -> BaziResponse:
    """
    Tính Tàng Can.
    """

    try:

        result = service.bazi(
            request.model_dump()
        )

        return BaziResponse(
            success=True,
            message="Hidden Stems calculated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
