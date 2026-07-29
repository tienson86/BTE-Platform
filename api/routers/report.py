"""
BTE Platform

Report Router

File: report.py
Version: 1.0
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas.request import ReportRequest
from api.schemas.response import ReportResponse
from api.services.pipeline_service import PipelineService


router = APIRouter()

service = PipelineService()


# ==========================================================
# Generate Report
# ==========================================================

@router.post(
    "/",
    response_model=ReportResponse,
    summary="Generate Report",
)
def generate_report(
    request: ReportRequest,
) -> ReportResponse:
    """
    Sinh báo cáo luận giải.
    """

    try:

        result = service.report(
            request.model_dump()
        )

        return ReportResponse(
            success=True,
            message="Report generated successfully.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# Markdown Report
# ==========================================================

@router.post(
    "/markdown",
    response_model=ReportResponse,
    summary="Generate Markdown Report",
)
def markdown_report(
    request: ReportRequest,
) -> ReportResponse:
    """
    Sinh báo cáo Markdown.
    """

    try:

        result = service.report(
            request.model_dump()
        )

        return ReportResponse(
            success=True,
            message="Markdown report generated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# HTML Report
# ==========================================================

@router.post(
    "/html",
    response_model=ReportResponse,
    summary="Generate HTML Report",
)
def html_report(
    request: ReportRequest,
) -> ReportResponse:
    """
    Sinh báo cáo HTML.
    """

    try:

        result = service.report(
            request.model_dump()
        )

        return ReportResponse(
            success=True,
            message="HTML report generated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )


# ==========================================================
# JSON Report
# ==========================================================

@router.post(
    "/json",
    response_model=ReportResponse,
    summary="Generate JSON Report",
)
def json_report(
    request: ReportRequest,
) -> ReportResponse:
    """
    Sinh báo cáo JSON.
    """

    try:

        result = service.report(
            request.model_dump()
        )

        return ReportResponse(
            success=True,
            message="JSON report generated.",
            data=result,
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
