"""Customer contract gate for official PDF/DOCX. Presentation/routing only."""

from __future__ import annotations

from typing import Any, Literal, Mapping

from applications.api.services.result_identity import CUSTOMER_USEFUL_GOD_CONTRACT

CustomerContractStatus = Literal["ok", "mismatch", "unversioned", "incomplete"]

EMPTY_RESULT_MESSAGE = (
    "Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu."
)
CONTRACT_MISMATCH_MESSAGE = (
    "Kết quả này được tạo bởi phiên bản dữ liệu cũ. Vui lòng phân tích lại để cập nhật kết quả."
)
CONTRACT_INCOMPLETE_MESSAGE = (
    "Kết quả phân tích chưa đủ hợp đồng hiển thị. Vui lòng phân tích lại."
)
HISTORY_MISMATCH_MESSAGE = (
    "Kết quả lịch sử không khớp với mã phân tích đang chọn. Vui lòng mở lại kết quả đã lưu."
)
RENDERER_FAILURE_MESSAGE = "Không tạo được tệp xuất. Vui lòng thử lại."


def _mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def read_customer_contract(data: Mapping[str, Any] | None) -> str:
    """Return published UsefulGodView contract string, if any."""
    payload = _mapping(data)
    source = _mapping(payload.get("useful_god_source"))
    meta = _mapping(payload.get("result_meta"))
    return _text(source.get("contract")) or _text(meta.get("customer_contract"))


def customer_contract_status(data: Mapping[str, Any] | None) -> CustomerContractStatus:
    """Classify a stored analysis payload against UsefulGodView@1.5."""
    if not isinstance(data, Mapping) or not data:
        return "incomplete"
    contract = read_customer_contract(data)
    if not contract:
        if data.get("useful_god") or data.get("pattern") or data.get("bazi"):
            return "unversioned"
        return "incomplete"
    if contract != CUSTOMER_USEFUL_GOD_CONTRACT:
        return "mismatch"
    useful = _mapping(data.get("useful_god"))
    if useful.get("overall_incomplete"):
        return "ok"
    display = _text(useful.get("useful_display")) or _text(useful.get("favorable_display"))
    if not display:
        return "incomplete"
    return "ok"


def customer_contract_message(status: CustomerContractStatus) -> str:
    """Customer-safe notice for a contract status."""
    if status == "ok":
        return ""
    if status == "incomplete":
        return CONTRACT_INCOMPLETE_MESSAGE
    return CONTRACT_MISMATCH_MESSAGE


def is_compatible_customer_contract(data: Mapping[str, Any] | None) -> bool:
    """True when official PDF/DOCX may be generated."""
    return customer_contract_status(data) == "ok"
