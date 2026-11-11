"""Select favorable lunar periods using the existing Bát Tự and Du Niên evidence."""

SCOPE = (
    "Cung Phi – Du Niên và Bát Tự có kết quả thuận riêng. Bát Tự đối chiếu Can Chi với "
    "Dụng/Hỷ/Kỵ thần, Nhật chủ và bối cảnh đại vận. Quan hệ hợp được ghi nhận, chưa xét hóa. "
    "Tháng được xét riêng trong năm âm lịch. Số năm thuận theo Cung Phi thay đổi theo khoảng xét."
)

DU_NIEN_LEVELS = {
    "sinh_khi": "Ưu tiên · Khởi sắc, còn cần xét Bát Tự",
    "thien_y": "Ưu tiên · Có trợ lực",
    "dien_nien": "Thuận · Ổn định",
    "phuc_vi": "Thuận · Duy trì",
    "tuyet_menh": "Cần lưu ý cao nhất",
    "luc_sat": "Cần lưu ý cao",
    "ngu_quy": "Cần lưu ý",
    "hoa_hai": "Cần lưu ý",
}
STEM_HARMONY = {"Giáp": "Kỷ", "Ất": "Canh", "Bính": "Tân", "Đinh": "Nhâm", "Mậu": "Quý"}
DOMAINS = {
    "Thiên Tài": "tài lộc và cơ hội kinh doanh",
    "Chính Tài": "tài lộc và nguồn thu ổn định",
    "Chính Quan": "công việc và trách nhiệm",
    "Chính Ấn": "học hành và trợ lực",
    "Thiên Ấn": "học hỏi và chuyên môn",
}


def assess(period):
    bazi = period["bazi"]
    direct = bazi["evidence"][:2]  # Can và Chi của chính năm/tháng.
    context = bazi["evidence"][2:]
    supports = [entry["text"] for entry in direct if entry["type"] == "support"]
    direct_pressure = [entry["text"] for entry in direct if entry["type"] == "pressure"]
    cautions = [entry["text"] for entry in context
                if entry["type"] == "pressure" or entry.get("relation") == "xung"]
    palace = period["cung_phi"]
    palace_favorable = palace["favorable"]
    palace_label = DU_NIEN_LEVELS.get(palace.get("relationship_id"), palace["relationship"])
    stem = period["ganzhi"].split()[0]
    day_master = bazi["day_master"]
    notes = []
    if STEM_HARMONY.get(stem) == day_master or STEM_HARMONY.get(day_master) == stem:
        notes.append(f"Can {stem} hợp Nhật chủ {day_master}; cần xét điều kiện hợp hóa.")
    if bazi["exact_useful_stem"]:
        notes.append(f"Can {stem} trùng đúng can Dụng thần.")
    god = bazi["ten_god"]
    if direct[0]["type"] == "support" and god in DOMAINS:
        notes.append(f"{stem} là {god}, có dấu hiệu trợ lực về {DOMAINS[god]}.")
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
    bazi_favorable = label in ("Thuận", "Thuận có lưu ý")
    if palace_favorable and bazi_favorable:
        combined = "Thuận theo cả hai cách"
    elif palace_favorable:
        combined = "Thuận theo Cung Phi"
    elif bazi_favorable:
        combined = "Thuận theo Bát Tự"
    else:
        combined = label
    return {
        "favorable": palace_favorable or bazi_favorable,
        "bazi_favorable": bazi_favorable,
        "bazi_assessment_label": label,
        "palace_assessment_label": palace_label,
        "assessment_label": combined,
        "assessment": " ".join([*reasons, *notes, *direct_pressure, *cautions, *gaps]),
    }


def select_good_periods(result):
    years = []
    for year in result["years"]:
        assessment = assess(year)
        months = [{**month, **assess(month)} for month in year["months"]]
        years.append({**year, **assessment, "months": months})
    return {**result, "kind": "good_years", "version": "GOOD-YEARS-04", "scope_note": SCOPE, "years": years}


def expand_legacy_row(row):
    """Recalculate older results using the profile frozen in the saved report."""
    result = row["result"]
    if result["version"] not in {"GOOD-YEARS-01", "GOOD-YEARS-02", "GOOD-YEARS-03"}:
        return row
    from applications.api.services.van_han_core import build

    years = result["years"]
    full = build(result["profile"], years[0]["year"], years[-1]["year"])
    return {**row, "result": select_good_periods({**result, "years": full["years"]})}
