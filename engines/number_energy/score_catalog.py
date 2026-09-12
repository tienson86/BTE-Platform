"""Frozen Phone Score labels, bands, and reason copy from Knowledge 14 + Golden fixture."""

from __future__ import annotations

from typing import Final

SCORE_MAX: Final[int] = 100
DIM_STRUCTURE_MAX: Final[int] = 25
DIM_WEALTH_MAX: Final[int] = 25
DIM_CAREER_MAX: Final[int] = 20
DIM_STABILITY_MAX: Final[int] = 15
DIM_TAIL_MAX: Final[int] = 15

DIM_STRUCTURE_LABEL: Final[str] = "Cấu trúc năng lượng"
DIM_WEALTH_LABEL: Final[str] = "Dòng tài vận"
DIM_CAREER_LABEL: Final[str] = "Công việc & trợ lực"
DIM_STABILITY_LABEL: Final[str] = "Ổn định & rủi ro"
DIM_TAIL_LABEL: Final[str] = "Năng lượng kết"

GRADE_BANDS: Final[tuple[tuple[int, int, str], ...]] = (
    (85, 100, "RẤT TỐT"),
    (70, 84, "TỐT"),
    (55, 69, "KHÁ"),
    (40, 54, "TRUNG BÌNH"),
    (25, 39, "CẦN CÂN NHẮC"),
    (0, 24, "NHIỀU ĐIỂM CẦN LƯU Ý"),
)

REASON_CAT_LEAD: Final[tuple[str, str, str]] = (
    "SCR-CAT-LEAD",
    "Cấu trúc Cát giữ vai trò chủ đạo",
    "Sinh Khí, Thiên Y và Diên Niên chiếm phần lớn thân số.",
)
REASON_WEALTH_SOURCE: Final[tuple[str, str, str]] = (
    "SCR-WEALTH-SOURCE",
    "Dòng Tài có nguồn rõ",
    "Sinh Khí → Thiên Y cho thấy quý nhân và cơ hội có khả năng dẫn tới Tài.",
)
REASON_CAREER_AXIS: Final[tuple[str, str, str]] = (
    "SCR-CAREER-AXIS",
    "Công việc là trục mạnh",
    "Diên Niên xuất hiện liên tiếp và tiếp tục dẫn tới Thiên Y ở phần cuối dãy.",
)
REASON_HUO_HAI_USE: Final[tuple[str, str, str]] = (
    "SCR-HUO-HAI-USE",
    "Họa Hại cần được sử dụng đúng cách",
    "Họa Hại xuất hiện ở đầu thân số, nhưng tổ hợp tiếp theo là Họa Hại → Sinh Khí, "
    "giúp khả năng giao tiếp có hướng phát huy tích cực.",
)
