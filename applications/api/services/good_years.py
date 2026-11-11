"""Select favorable lunar periods using the existing Bát Tự and Du Niên evidence."""

SCOPE = (
    "Một thời điểm được chọn khi Can hoặc Chi của chính thời điểm gặp Dụng/Hỷ thần, "
    "Cung Phi thuận, và kết quả đối chiếu không ghi nhận Kỵ thần, lục xung hay vướng mốc đại vận. "
    "Kỵ thần được xét ở thời điểm, đại vận và Can Chi năm khi đánh giá tháng. "
    "Tháng được xét riêng, kể cả trong năm không đạt tiêu chí. "
    "Phạm vi chưa xét hình, hại, phá hoặc điều kiện hợp hóa."
)


def assess(period):
    bazi = period["bazi"]
    evidence = bazi["evidence"]
    # The core always emits the period's own stem and branch before contextual evidence.
    supports = [entry["text"] for entry in evidence[:2] if entry["type"] == "support"]
    reasons = []
    if not supports:
        reasons.append("Can và Chi của thời điểm chưa gặp Dụng thần hoặc Hỷ thần.")
    if not period["cung_phi"]["favorable"]:
        reasons.append(f"Cung Phi gặp {period['cung_phi']['relationship']}, thuộc nhóm cần lưu ý.")
    if any(entry["type"] == "pressure" for entry in evidence):
        reasons.append("Có yếu tố thuộc Kỵ thần khi đối chiếu Can Chi và đại vận.")
    if any(entry.get("relation") == "xung" for entry in evidence):
        reasons.append("Địa Chi thời điểm lục xung với một trụ của lá số.")
    reasons.extend(bazi["missing_context"])
    return {
        "favorable": not reasons,
        "narrative": " ".join(reasons or [period["cung_phi"]["note"], *supports]),
    }


def select_good_periods(result):
    years = []
    for year in result["years"]:
        assessment = assess(year)
        months = []
        for month in year["months"]:
            month_assessment = assess(month)
            if month_assessment["favorable"]:
                months.append({**month, **month_assessment})
        years.append({**year, **assessment, "months": months})
    return {**result, "kind": "good_years", "version": "GOOD-YEARS-01", "scope_note": SCOPE, "years": years}
