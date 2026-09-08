"""Customer-visible copy helpers. Presentation only. No new consulting advice."""

from __future__ import annotations

import re

_LIMITATION_CUSTOMER = {
    "birth_time_unknown": "Chưa có giờ sinh của một người. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
    "timezone_unspecified": "Múi giờ chưa được ghi nhận. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
    "birth_place_unknown": "Nơi sinh chưa được ghi nhận. Đây là giới hạn dữ liệu, không phải nhận định về hôn nhân.",
    "children_unsupported": "Hiện chưa đủ dữ liệu để kết luận về việc nuôi dạy con chung.",
    "insufficient_comparison_evidence": "Một số phần so sánh chưa đủ dữ liệu nên được giữ ở mức tham khảo.",
}

_TECHNICAL = re.compile(
    r"\b(?:timezone_unspecified|birth_time_unknown|birth_place_unknown|"
    r"semantic_key|language_key|mixed|insufficient|structure)\b",
    re.IGNORECASE,
)
_ID_LEAK = re.compile(r"\b(?:EV|F|RC|CF|MC)-\w+\b")

_CONFIDENCE_CUSTOMER = {
    "high": "Độ tin cậy cao",
    "medium": "Khá tin cậy",
    "reference_only": "Mang tính tham khảo",
}


def customer_limitation(code: str) -> str | None:
    """Map an internal limitation code to customer Vietnamese. Drop unknown codes."""
    text = (code or "").strip()
    if not text:
        return None
    if text in _LIMITATION_CUSTOMER:
        return _LIMITATION_CUSTOMER[text]
    if " " in text or any(ord(ch) > 127 for ch in text):
        if _TECHNICAL.search(text) or _ID_LEAK.search(text):
            return None
        return text
    return None


def customer_limitations(codes: list[str]) -> list[str]:
    """Deduplicated customer limitation sentences."""
    seen: set[str] = set()
    items: list[str] = []
    for code in codes:
        text = customer_limitation(code)
        if not text or text in seen:
            continue
        seen.add(text)
        items.append(text)
    return items


def customer_confidence(level: str) -> str:
    """Map an internal confidence enum to customer Vietnamese."""
    return _CONFIDENCE_CUSTOMER.get((level or "").strip(), "Mang tính tham khảo")


def customerize(text: str) -> str:
    """Soften internal phrasing without inventing a new conclusion."""
    cleaned = text.replace("Cấu trúc hiện cho thấy", "Trong thực tế,")
    cleaned = cleaned.replace("Tầng cấu trúc đang", "Nền tảng đang")
    cleaned = cleaned.replace("tầng cấu trúc đang", "nền tảng đang")
    cleaned = cleaned.replace("tầng cấu trúc", "nền tảng")
    cleaned = cleaned.replace("Hệ thống chưa đủ", "Hiện chưa đủ")
    cleaned = cleaned.replace("Hệ thống hiện chưa", "Hiện chưa")
    cleaned = cleaned.replace("cơ sở cấu trúc", "cơ sở")
    cleaned = cleaned.replace("dữ liệu cấu trúc", "dữ liệu")
    cleaned = cleaned.replace("kết luận cấu trúc", "kết luận đã chốt")
    cleaned = cleaned.replace(" về cấu trúc", "")
    cleaned = cleaned.replace("của hồ sơ ở mức cao trên dữ liệu hiện có", "cao trên dữ liệu hiện có")
    return " ".join(cleaned.split()).strip()
