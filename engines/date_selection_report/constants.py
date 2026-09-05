"""PACK 06 Date Selection report foundation constants.

Presentation enums only. Analytical values remain owned by Date Selection.
"""

from __future__ import annotations

from engines.report_engine.foundation_constants import (
    REPORT_CONTRACT_ID,
    REPORT_VERSION as PACK05_REPORT_VERSION,
)

REPORT_TYPE = "date_selection"
REPORT_SCHEMA_VERSION = "1.0"
LOCALE = "vi-VN"
TITLE = "BÁO CÁO CHỌN NGÀY TỐT"
GENERATOR = "pack_06.date_selection_report"
SOURCE = "date_selection"
ENGINE_VERSION = "1.0.0"

DAY_RESULTS: frozenset[str] = frozenset(
    {"Đại An", "Lưu Niên", "Tốc Hỷ", "Xích Khẩu", "Tiểu Cát", "Không Vong"}
)
POSITIVE_KE_RESULTS: frozenset[str] = frozenset({"Đại An", "Tốc Hỷ", "Tiểu Cát"})
# Lưu Liên is a legacy misspelling; keep it rejected so old payloads cannot leak.
NEGATIVE_KE_RESULTS: frozenset[str] = frozenset(
    {"Lưu Niên", "Lưu Liên", "Xích Khẩu", "Không Vong"}
)
ALLOWED_CUNG: frozenset[str] = frozenset(
    {"Khảm", "Ly", "Chấn", "Tốn", "Càn", "Khôn", "Cấn", "Đoài"}
)
ALLOWED_ELEMENTS: frozenset[str] = frozenset({"Mộc", "Hỏa", "Thổ", "Kim", "Thủy"})
ALLOWED_TRACH: frozenset[str] = frozenset({"Đông Tứ Trạch", "Tây Tứ Trạch"})
TRACH_CODE_TO_LABEL: dict[str, str] = {
    "dong": "Đông Tứ Trạch",
    "tay": "Tây Tứ Trạch",
    "Đông Tứ Trạch": "Đông Tứ Trạch",
    "Tây Tứ Trạch": "Tây Tứ Trạch",
}

GUIDANCE_TITLE = "Hướng dẫn tham khảo"
GUIDANCE_ITEMS: tuple[tuple[str, str], ...] = (
    ("Đại An", "Thiên về sự ổn định, bền vững và yên định."),
    ("Tốc Hỷ", "Thiên về sự nhanh chóng, thuận lợi và tin vui."),
    ("Tiểu Cát", "Thiên về sự thuận lợi, phát triển và cầu tài."),
)
