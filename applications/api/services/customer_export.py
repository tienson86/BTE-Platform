"""Customer PDF/DOCX export from a stored canonical analysis.

Does not re-run Calendar / BaZi / Strength / Pattern / Useful God engines.
"""

from __future__ import annotations

import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from applications.api.exceptions import ApplicationsAPIError
from applications.api.services.customer_report_adapter import build_customer_report_input
from applications.api.services.result_identity import CUSTOMER_USEFUL_GOD_CONTRACT
from engines.report_engine.contracts.report_export_result_v1 import ReportExportResultV1
from engines.report_engine.contracts.report_input_v1 import ReportInputV1
from engines.report_engine.exporting.filename import ascii_slug
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1

logger = logging.getLogger(__name__)

EMPTY_RESULT_MESSAGE = (
    "Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu."
)
CONTRACT_MISMATCH_MESSAGE = (
    "Kết quả này được tạo bởi phiên bản dữ liệu cũ. "
    "Vui lòng phân tích lại để cập nhật kết quả."
)
CONTRACT_INCOMPLETE_MESSAGE = (
    "Kết quả phân tích chưa đủ hợp đồng hiển thị. Vui lòng phân tích lại."
)
HISTORY_MISMATCH_MESSAGE = (
    "Bản xuất không khớp kết quả đang xem. Vui lòng mở lại kết quả rồi tải file."
)
RENDERER_FAILURE_MESSAGE = "Không thể tạo file xuất. Vui lòng thử lại."

EXPORT_EMPTY = "export_empty"
EXPORT_CONTRACT = "export_contract_mismatch"
EXPORT_HISTORY = "export_history_mismatch"
EXPORT_RENDERER = "export_renderer_failed"


class CustomerExportError(ApplicationsAPIError):
    """Recoverable customer export failure."""


def customer_contract_status(data: Mapping[str, Any] | None) -> str:
    """Classify stored Analyze data against UsefulGodView@1.5."""
    if not data or not isinstance(data, Mapping):
        return "incomplete"
    source = dict(data.get("useful_god_source") or {})
    meta = dict(data.get("result_meta") or {})
    contract = str(source.get("contract") or meta.get("customer_contract") or "").strip()
    if not contract:
        if data.get("useful_god") or data.get("pattern") or data.get("bazi") or data.get("calendar"):
            return "unversioned"
        return "incomplete"
    if contract != CUSTOMER_USEFUL_GOD_CONTRACT:
        return "mismatch"
    useful = dict(data.get("useful_god") or {})
    if useful.get("overall_incomplete"):
        return "ok"
    display = str(useful.get("useful_display") or useful.get("favorable_display") or "").strip()
    if display:
        return "ok"
    return "incomplete"


def contract_customer_message(status: str) -> str:
    """Customer-facing contract notice."""
    if status == "incomplete":
        return CONTRACT_INCOMPLETE_MESSAGE
    return CONTRACT_MISMATCH_MESSAGE


def build_customer_download_filename(report_input: ReportInputV1, fmt: str) -> str:
    """Safe ASCII download name: slug + date + report type. Not analysis-id-only."""
    slug = ascii_slug(report_input.profile.full_name or "BaoCao")
    generated = report_input.metadata.generated_at or datetime.now(timezone.utc).isoformat()
    day = generated[:10].replace("-", "")
    if len(day) != 8 or not day.isdigit():
        day = datetime.now(timezone.utc).strftime("%Y%m%d")
    extension = fmt.lower().lstrip(".")
    return f"BTE_{slug}_{day}_BaoCao_V1.{extension}"


def prepare_customer_report_input(
    *,
    analysis_id: str | None,
    source: str | None,
    data: Mapping[str, Any] | None,
    birth_input: Mapping[str, Any] | None,
) -> ReportInputV1:
    """Validate identity/contract and build the canonical presentation model."""
    payload = dict(data or {})
    if not payload:
        raise CustomerExportError(
            EMPTY_RESULT_MESSAGE,
            status_code=422,
            code=EXPORT_EMPTY,
        )
    requested_id = str(analysis_id or "").strip()
    stored_id = str(payload.get("analysis_id") or payload.get("request_id") or "").strip()
    meta = dict(payload.get("result_meta") or {})
    if not stored_id:
        stored_id = str(meta.get("analysis_id") or "").strip()
    if not requested_id or not stored_id:
        raise CustomerExportError(
            EMPTY_RESULT_MESSAGE,
            status_code=422,
            code=EXPORT_EMPTY,
        )
    if requested_id != stored_id:
        raise CustomerExportError(
            HISTORY_MISMATCH_MESSAGE,
            status_code=422,
            code=EXPORT_HISTORY,
            details={"requested_id": requested_id, "stored_id": stored_id},
        )
    status = customer_contract_status(payload)
    if status != "ok":
        raise CustomerExportError(
            contract_customer_message(status),
            status_code=422,
            code=EXPORT_CONTRACT,
            details={"contract_status": status, "source": source or "current"},
        )
    return build_customer_report_input(
        data=payload,
        analysis_id=stored_id,
        birth_input=birth_input,
        source=str(source or "current"),
    )


def export_customer_file(
    *,
    report_input: ReportInputV1,
    fmt: str,
    export_service: ReportExportServiceV1 | None = None,
) -> tuple[Path, str, ReportExportResultV1]:
    """Render official PDF or DOCX into a unique temp file."""
    service = export_service or ReportExportServiceV1()
    extension = fmt.lower().lstrip(".")
    temp_dir = Path(tempfile.gettempdir())
    temp_path = temp_dir / f"bte_export_{uuid4().hex}.{extension}"
    download_name = build_customer_download_filename(report_input, extension)
    try:
        if extension == "pdf":
            result = service.export_pdf(report_input, temp_path)
        elif extension == "docx":
            result = service.export_docx(report_input, temp_path)
        else:
            raise CustomerExportError(
                RENDERER_FAILURE_MESSAGE,
                status_code=400,
                code=EXPORT_RENDERER,
            )
    except CustomerExportError:
        _safe_unlink(temp_path)
        raise
    except Exception:
        _safe_unlink(temp_path)
        logger.exception(
            "customer_export_renderer_failed analysis_id=%s format=%s",
            report_input.metadata.case_id,
            extension,
        )
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code=EXPORT_RENDERER,
        ) from None
    if not temp_path.is_file() or temp_path.stat().st_size <= 0:
        _safe_unlink(temp_path)
        raise CustomerExportError(
            RENDERER_FAILURE_MESSAGE,
            status_code=500,
            code=EXPORT_RENDERER,
        )
    return temp_path, download_name, result


def cleanup_export_file(path: Path) -> None:
    """Delete a one-shot export temp file."""
    _safe_unlink(path)


def _safe_unlink(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        logger.warning("customer_export_temp_cleanup_failed path=%s", path)
