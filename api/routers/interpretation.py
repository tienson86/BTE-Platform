"""
BTE Platform

Interpretation Router

File: interpretation.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.request import InterpretationRequest
from api.schemas.response import InterpretationResponse
from api.services.pipeline_service import PipelineService


router = APIRouter()

service = PipelineService()


# ==========================================================
# Interpretation
# ==========================================================

@router.post(
    "/",
    response_model=InterpretationResponse,
    summary="Interpretation",
)
def interpretation(
    request: InterpretationRequest,
) -> InterpretationResponse:
    """
    Luận giải lá số Bát Tự.
    """

    try:

        result = service.interpretation(
            request.model_dump()
        )

        return InterpretationResponse(
            success=True,
            message="Interpretation completed successfully.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Personality
# ==========================================================

@router.post(
    "/personality",
    response_model=InterpretationResponse,
    summary="Personality Analysis",
)
def personality(
    request: InterpretationRequest,
) -> InterpretationResponse:
    """
    Luận giải tính cách.
    """

    try:

        result = service.interpretation(
            request.model_dump()
        )

        return InterpretationResponse(
            success=True,
            message="Personality analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Career
# ==========================================================

@router.post(
    "/career",
    response_model=InterpretationResponse,
    summary="Career Analysis",
)
def career(
    request: InterpretationRequest,
) -> InterpretationResponse:
    """
    Luận giải công danh - sự nghiệp.
    """

    try:

        result = service.interpretation(
            request.model_dump()
        )

        return InterpretationResponse(
            success=True,
            message="Career analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Marriage
# ==========================================================

@router.post(
    "/marriage",
    response_model=InterpretationResponse,
    summary="Marriage Analysis",
)
def marriage(
    request: InterpretationRequest,
) -> InterpretationResponse:
    """
    Luận giải hôn nhân.
    """

    try:

        result = service.interpretation(
            request.model_dump()
        )

        return InterpretationResponse(
            success=True,
            message="Marriage analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Wealth
# ==========================================================

@router.post(
    "/wealth",
    response_model=InterpretationResponse,
    summary="Wealth Analysis",
)
def wealth(
    request: InterpretationRequest,
) -> InterpretationResponse:
    """
    Luận giải tài vận.
    """

    try:

        result = service.interpretation(
            request.model_dump()
        )

        return InterpretationResponse(
            success=True,
            message="Wealth analysis completed.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
