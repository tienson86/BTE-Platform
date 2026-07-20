"""
BTE Platform

Analysis Router

File: analysis.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.request import AnalysisRequest
from api.schemas.response import AnalysisResponse
from api.services.pipeline_service import PipelineService


router = APIRouter()

service = PipelineService()


# ==========================================================
# Full Analysis Pipeline
# ==========================================================

@router.post(
    "/",
    response_model=AnalysisResponse,
    summary="Run Full Analysis",
)
def analyze(
    request: AnalysisRequest,
) -> AnalysisResponse:
    """
    Chạy toàn bộ Pipeline:
    Calendar → Bazi → Pattern → Score → Interpretation → Report.
    """

    try:

        result = service.analyze(
            request.model_dump()
        )

        return AnalysisResponse(
            success=True,
            message="Analysis completed successfully.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Quick Analysis
# ==========================================================

@router.post(
    "/quick",
    response_model=AnalysisResponse,
    summary="Quick Analysis",
)
def quick_analysis(
    request: AnalysisRequest,
) -> AnalysisResponse:
    """
    Chạy phân tích nhanh.
    """

    try:

        result = service.analyze(
            request.model_dump()
        )

        return AnalysisResponse(
            success=True,
            message="Quick analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Complete Analysis
# ==========================================================

@router.post(
    "/complete",
    response_model=AnalysisResponse,
    summary="Complete Analysis",
)
def complete_analysis(
    request: AnalysisRequest,
) -> AnalysisResponse:
    """
    Chạy phân tích đầy đủ.
    """

    try:

        result = service.analyze(
            request.model_dump()
        )

        return AnalysisResponse(
            success=True,
            message="Complete analysis finished.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
