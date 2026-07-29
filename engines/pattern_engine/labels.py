"""Display labels for pattern codes (portal-compatible Vietnamese)."""

from __future__ import annotations

PATTERN_LABELS: dict[str, str] = {
    "chinh_quan": "Chính Quan",
    "thien_quan": "Thiên Quan",
    "thien_tai": "Thiên Tài",
    "chinh_tai": "Chính Tài",
    "thien_an": "Thiên Ấn",
    "chinh_an": "Chính Ấn",
    "thien_thuong": "Thiên Thương",
    "thuc_than": "Thực Thần",
    "thuong_quan": "Thương Quan",
    "thien_sat": "Thiên Sát",
    "that_sat": "Thất Sát",
    "kien_loc": "Kiến Lộc",
    "duong_nhan": "Dương Nhẫn",
    "ty_kien": "Tỷ Kiên",
    "kiep_tai": "Kiếp Tài",
}

STRENGTH_LEVEL_LABELS: dict[str, str] = {
    "strong": "Vượng",
    "weak": "Nhược",
    "balanced": "Trung hòa",
    "unknown": "",
}


def pattern_display_label(code: str | None, description: str | None = None) -> str:
    """Resolve Vietnamese Cách cục label from rule code or CSV description."""
    key = str(code or "").strip().lower()
    if key in PATTERN_LABELS:
        return PATTERN_LABELS[key]
    if description and str(description).strip():
        text = str(description).strip()
        return text.replace("cach", "cách").replace("Cach", "Cách")
    if key:
        return " ".join(part.capitalize() for part in key.split("_") if part)
    return ""
