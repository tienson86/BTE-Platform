"""Select favorable lunar periods using the existing Bát Tự and Du Niên evidence."""

SCOPE = (
    "Xếp mức thuận dựa trước hết vào Can và Chi của chính thời điểm. "
    "Kỵ thần ở đại vận hoặc ở năm, Cung Phi và lục xung là các điểm lưu ý. "
    "Tháng được xét riêng trong bối cảnh năm và đại vận. "
    "Phạm vi chưa xét hình, hại, phá hoặc điều kiện hợp hóa."
)


def assess(period):
    bazi = period["bazi"]
    direct = bazi["evidence"][:2]  # Can và Chi của chính năm/tháng.
    context = bazi["evidence"][2:]
    supports = [entry["text"] for entry in direct if entry["type"] == "support"]
    direct_pressure = [entry["text"] for entry in direct if entry["type"] == "pressure"]
    cautions = [entry["text"] for entry in context
                if entry["type"] == "pressure" or entry.get("relation") == "xung"]
    palace = period["cung_phi"]
    if not palace["favorable"]:
        cautions.append(f"Cung Phi gặp {palace['relationship']}, thuộc nhóm cần lưu ý.")
    gaps = bazi["missing_context"]
    if gaps:
        label = "Chưa đủ căn cứ"
    elif supports and direct_pressure:
        label = "Thuận nghịch đan xen"
    elif supports:
        label = "Thuận có lưu ý" if cautions else "Thuận"
    elif direct_pressure or cautions:
        label = "Cần thận trọng"
    else:
        label = "Chưa có trợ lực nổi bật"
    reasons = supports or ["Can và Chi của thời điểm chưa gặp Dụng thần hoặc Hỷ thần."]
    return {
        "favorable": label in ("Thuận", "Thuận có lưu ý"),
        "assessment_label": label,
        "assessment": " ".join([*reasons, *direct_pressure, *cautions, *gaps]),
    }


def select_good_periods(result):
    years = []
    for year in result["years"]:
        assessment = assess(year)
        months = [{**month, **assess(month)} for month in year["months"]]
        years.append({**year, **assessment, "months": months})
    return {**result, "kind": "good_years", "version": "GOOD-YEARS-03", "scope_note": SCOPE, "years": years}


def expand_legacy_row(row):
    """Recalculate older results using the profile frozen in the saved report."""
    result = row["result"]
    if result["version"] not in {"GOOD-YEARS-01", "GOOD-YEARS-02"}:
        return row
    from applications.api.services.van_han_core import build

    years = result["years"]
    full = build(result["profile"], years[0]["year"], years[-1]["year"])
    return {**row, "result": select_good_periods({**result, "years": full["years"]})}
