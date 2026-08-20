"""Customer official PDF / DOCX download from a selected analysis."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal
from urllib.parse import quote

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from starlette.background import BackgroundTask

from applications.api.services.customer_export import (
    cleanup_export_file,
    export_customer_file,
    prepare_customer_report_input,
)
from engines.report_engine.contracts.report_export_result_v1 import MEDIA_TYPE_DOCX, MEDIA_TYPE_PDF

logger = logging.getLogger(__name__)

router = APIRouter(tags=["export"])


class CustomerExportRequest(BaseModel):
    """Selected analysis payload already stored by Portal ResultStore."""

    analysis_id: str = Field(..., min_length=1)
    source: Literal["current", "history"] = "current"
    data: dict[str, Any]
    input: dict[str, Any] | None = None


def _content_disposition(filename: str) -> str:
    ascii_name = filename.encode("ascii", "ignore").decode("ascii") or "BTE_BaoCao_V1.bin"
    encoded = quote(filename)
    return f"attachment; filename=\"{ascii_name}\"; filename*=UTF-8''{encoded}"


def _file_response(path: Path, download_name: str, media_type: str, analysis_id: str) -> FileResponse:
    return FileResponse(
        path=str(path),
        media_type=media_type,
        filename=download_name,
        background=BackgroundTask(cleanup_export_file, path),
        headers={
            "Content-Disposition": _content_disposition(download_name),
            "X-BTE-Analysis-Id": analysis_id,
            "X-Content-Type-Options": "nosniff",
        },
    )


@router.post("/export/pdf")
def export_official_pdf(request: Request, body: CustomerExportRequest) -> FileResponse:
    """Official customer PDF — Report V1 Playwright, selected analysis only."""
    del request
    report_input = prepare_customer_report_input(
        analysis_id=body.analysis_id,
        source=body.source,
        data=body.data,
        birth_input=body.input,
    )
    path, download_name, _result = export_customer_file(
        report_input=report_input,
        fmt="pdf",
    )
    logger.info(
        "customer_export_pdf analysis_id=%s source=%s file=%s",
        body.analysis_id,
        body.source,
        download_name,
    )
    return _file_response(path, download_name, MEDIA_TYPE_PDF, body.analysis_id)


@router.post("/export/docx")
def export_official_docx(request: Request, body: CustomerExportRequest) -> FileResponse:
    """Official customer DOCX — existing python-docx renderer, selected analysis only."""
    del request
    report_input = prepare_customer_report_input(
        analysis_id=body.analysis_id,
        source=body.source,
        data=body.data,
        birth_input=body.input,
    )
    path, download_name, _result = export_customer_file(
        report_input=report_input,
        fmt="docx",
    )
    logger.info(
        "customer_export_docx analysis_id=%s source=%s file=%s",
        body.analysis_id,
        body.source,
        download_name,
    )
    return _file_response(path, download_name, MEDIA_TYPE_DOCX, body.analysis_id)
