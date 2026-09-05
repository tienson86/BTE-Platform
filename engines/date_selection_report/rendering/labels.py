"""Vietnamese customer-facing labels for Date Selection reports.

Presentation copy only. Never English algorithm terminology.
"""

from __future__ import annotations

LABELS: dict[str, str] = {
    "report_title": "BÁO CÁO CHỌN NGÀY TỐT",
    "subtitle": "BTE Platform",
    "section_person": "THÔNG TIN NGƯỜI XEM",
    "section_search": "THÔNG TIN TÌM NGÀY TỐT",
    "section_recommendations": "CÁC NGÀY ĐỀ XUẤT",
    "compatible_hours": "Giờ phù hợp Nhóm Trạch của bạn",
    "positive_times": "Các thời điểm đẹp",
    "section_guidance": "HƯỚNG DẪN THAM KHẢO",
    "full_name": "Họ và tên",
    "gender": "Giới tính",
    "birth_solar": "Ngày sinh dương",
    "birth_lunar": "Ngày sinh âm",
    "year_ganzhi": "Can Chi năm",
    "month_ganzhi": "Can Chi tháng",
    "day_ganzhi": "Can Chi ngày",
    "nayin": "Nạp âm",
    "cung_phi": "Cung Phi",
    "trach_group": "Nhóm Trạch",
    "solar_date": "Ngày dương",
    "lunar_date": "Ngày âm",
    "day_result": "Kết quả ngày",
    "search_month": "Tháng tìm ngày tốt",
    "recommendation_count": "Số ngày đề xuất",
    "search_explanation": (
        "Các ngày dưới đây được hệ thống lựa chọn dựa trên dữ liệu cá nhân của bạn."
    ),
    "empty_recommendations": (
        "Không tìm thấy ngày phù hợp trong khoảng thời gian đã chọn."
    ),
    "lunar_suffix": "âm",
    "hour_prefix": "Giờ",
    "footer_generated_by": "Tạo bởi",
    "footer_product": "Báo cáo chọn ngày tốt",
}

FORBIDDEN_PUBLIC_TERMS: frozenset[str] = frozenset(
    {
        "Kết quả giờ",
        "Year Ganzhi",
        "Month Ganzhi",
        "Hour Result",
        "hour_result",
        "Lưu Liên",
    }
)

POSITIVE_GROUP_ORDER: tuple[str, ...] = ("Đại An", "Tốc Hỷ", "Tiểu Cát")
EMPTY_STATE_MESSAGE = LABELS["empty_recommendations"]
# P6-01 validate_report_model rejects zero recommendations.
EMPTY_STATE_DORMANT = True
