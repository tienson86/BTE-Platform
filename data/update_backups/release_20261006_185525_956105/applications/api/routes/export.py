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

from applications.api.exceptions import CustomerExportError
from applications.api.services.customer_contract import RENDERER_FAILURE_MESSAGE
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


def _export_response(
    body: CustomerExportRequest,
    fmt: Literal["pdf", "docx"],
    media_type: str,
) -> FileResponse:
    try:
        report_input = prepare_customer_report_input(
            analysis_id=body.analysis_id,
            source=body.source,
            data=body.data,
            birth_input=body.input,
        )
        path, download_name, _result = export_customer_file(
            report_input=report_input,
            fmt=fmt,
        )
    except CustomerExportError:
        raise
    except Exception:
        logger.exception("customer_export_unhandled format=%s", fmt)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_renderer_failed",
        ) from None
    logger.info(
        "customer_export format=%s analysis_id=%s source=%s file=%s",
        fmt,
        body.analysis_id,
        body.source,
        download_name,
    )
    return _file_response(path, download_name, media_type, body.analysis_id)


@router.post("/export/pdf")
def export_official_pdf(request: Request, body: CustomerExportRequest) -> FileResponse:
    """Official customer PDF — Report V1 Playwright, selected analysis only."""
    del request
    return _export_response(body, "pdf", MEDIA_TYPE_PDF)


@router.post("/export/docx")
def export_official_docx(request: Request, body: CustomerExportRequest) -> FileResponse:
    """Official customer DOCX — existing python-docx renderer, selected analysis only."""
    del request
    return _export_response(body, "docx", MEDIA_TYPE_DOCX)
