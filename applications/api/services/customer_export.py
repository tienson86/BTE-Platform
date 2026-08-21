"""Official customer PDF/DOCX from a selected stored analysis."""

from __future__ import annotations

import logging
import tempfile
import uuid
from pathlib import Path
from typing import Any, Literal, Mapping

from applications.api.exceptions import CustomerExportError
from applications.api.services.customer_contract import (
    CONTRACT_MISMATCH_MESSAGE,
    EMPTY_RESULT_MESSAGE,
    HISTORY_MISMATCH_MESSAGE,
    RENDERER_FAILURE_MESSAGE,
    customer_contract_message,
    customer_contract_status,
    is_compatible_customer_contract,
)
from applications.api.services.customer_report_input import build_customer_report_input
from engines.report_engine.contracts.report_export_result_v1 import ReportExportResultV1
from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.exporting.filename import ascii_slug
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1

logger = logging.getLogger(__name__)

ExportFormat = Literal["pdf", "docx"]

_EXPORT_ROOT = Path(tempfile.gettempdir()) / "bte_customer_export"


def prepare_customer_report_input(
    *,
    analysis_id: str,
    source: str,
    data: Mapping[str, Any],
    birth_input: Mapping[str, Any] | None = None,
) -> ReportInputV1:
    """Validate selected analysis and build the canonical presentation model."""
    selected_id = str(analysis_id or "").strip()
    payload = dict(data or {})
    if not selected_id:
        raise CustomerExportError(EMPTY_RESULT_MESSAGE, code="export_missing_analysis")
    if not payload:
        raise CustomerExportError(EMPTY_RESULT_MESSAGE, code="export_missing_result")
    payload_id = str(payload.get("analysis_id") or payload.get("request_id") or "").strip()
    if payload_id and payload_id != selected_id:
        raise CustomerExportError(
            HISTORY_MISMATCH_MESSAGE,
            status_code=409,
            code="export_history_mismatch",
            details={"analysis_id": selected_id, "payload_id": payload_id, "source": source},
        )
    status = customer_contract_status(payload)
    if status != "ok" or not is_compatible_customer_contract(payload):
        raise CustomerExportError(
            customer_contract_message(status) or CONTRACT_MISMATCH_MESSAGE,
            status_code=409,
            code="export_contract_mismatch",
            details={"status": status, "source": source},
        )
    return build_customer_report_input(
        analysis_id=selected_id,
        data=payload,
        birth_input=birth_input,
    )


def build_customer_export_filename(report_input: ReportInputV1, fmt: str) -> str:
    """Customer download name: slug + birth date + report type. Not the analysis id alone."""
    slug = ascii_slug(report_input.profile.full_name or "KhachHang")
    birth = (report_input.profile.birth_date or "").replace("-", "").replace("/", "")[:8]
    date_token = birth if birth.isdigit() and len(birth) >= 8 else ""
    parts = ["BTE", "BaoCao", slug]
    if date_token:
        parts.append(date_token)
    parts.append("V1")
    extension = fmt.lower().lstrip(".")
    return f"{'_'.join(parts)}.{extension}"


def export_customer_file(
    *,
    report_input: ReportInputV1,
    fmt: ExportFormat,
    service: ReportExportServiceV1 | None = None,
) -> tuple[Path, str, ReportExportResultV1]:
    """Render official PDF or DOCX into a unique temp file."""
    download_name = build_customer_export_filename(report_input, fmt)
    token = uuid.uuid4().hex[:12]
    analysis_token = ascii_slug(report_input.metadata.case_id)[:16] or "analysis"
    _EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    output_path = _EXPORT_ROOT / f"bte_{analysis_token}_{token}_{download_name}"
    exporter = service or ReportExportServiceV1(export_root=_EXPORT_ROOT)
    try:
        if fmt == "pdf":
            result = exporter.export_pdf(report_input, output_path)
        elif fmt == "docx":
            result = exporter.export_docx(report_input, output_path)
        else:
            raise CustomerExportError(RENDERER_FAILURE_MESSAGE, code="export_unsupported_format")
    except CustomerExportError:
        cleanup_export_file(output_path)
        raise
    except Exception:
        logger.exception("customer_export_renderer_failed format=%s", fmt)
        cleanup_export_file(output_path)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_renderer_failed",
        ) from None
    path = Path(result.file_path)
    if not path.is_file() or path.stat().st_size == 0:
        cleanup_export_file(path)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code="export_empty_file",
        )
    return path, download_name, result


def cleanup_export_file(path: Path | str | None) -> None:
    """Delete a temp export artifact after the response is sent."""
    if not path:
        return
    target = Path(path)
    try:
        if target.is_file():
            target.unlink()
    except OSError:
        logger.warning("customer_export_cleanup_failed path=%s", target)
