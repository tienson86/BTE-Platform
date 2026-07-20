"""
BTE Platform

Score Router

File: score.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.request import ScoreRequest
from api.schemas.response import ScoreResponse
from api.services.pipeline_service import PipelineService


router = APIRouter()

service = PipelineService()


# ==========================================================
# Score Analysis
# ==========================================================

@router.post(
    "/",
    response_model=ScoreResponse,
    summary="Calculate Score",
)
def calculate_score(
    request: ScoreRequest,
) -> ScoreResponse:
    """
    Chấm điểm tổng hợp lá số.
    """

    try:

        result = service.score(
            request.model_dump()
        )

        return ScoreResponse(
            success=True,
            message="Score calculated successfully.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Five Elements
# ==========================================================

@router.post(
    "/five-elements",
    response_model=ScoreResponse,
    summary="Five Elements Score",
)
def five_elements(
    request: ScoreRequest,
) -> ScoreResponse:
    """
    Chấm điểm Ngũ Hành.
    """

    try:

        result = service.score(
            request.model_dump()
        )

        return ScoreResponse(
            success=True,
            message="Five Elements score calculated.",
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
    response_model=ScoreResponse,
    summary="Ten Gods Score",
)
def ten_gods(
    request: ScoreRequest,
) -> ScoreResponse:
    """
    Chấm điểm Thập Thần.
    """

    try:

        result = service.score(
            request.model_dump()
        )

        return ScoreResponse(
            success=True,
            message="Ten Gods score calculated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Overall Score
# ==========================================================

@router.post(
    "/overall",
    response_model=ScoreResponse,
    summary="Overall Score",
)
def overall(
    request: ScoreRequest,
) -> ScoreResponse:
    """
    Chấm điểm tổng thể.
    """

    try:

        result = service.score(
            request.model_dump()
        )

        return ScoreResponse(
            success=True,
            message="Overall score calculated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
