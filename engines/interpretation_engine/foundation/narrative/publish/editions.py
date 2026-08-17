"""Publication editions — policy only. Does not compose or rewrite prose."""

from __future__ import annotations

from typing import Final, Mapping

EDITION_EXECUTIVE: Final[str] = "executive"
EDITION_PROFESSIONAL: Final[str] = "professional"
EDITION_APPENDIX: Final[str] = "technical_appendix"

PROFESSIONAL_REPORT_PUBLISHER_ID: Final[str] = "professional_report_publisher_v1"

# Professional consultation pages. Appendix is a separate edition.
PROFESSIONAL_PAGE_ORDER: Final[tuple[str, ...]] = (
    "sec-executive_summary",
    "sec-chart",
    "sec-core_interpretation",
    "sec-ten_gods",
    "sec-shen_sha",
    "sec-luck",
    "sec-career",
    "sec-life_areas",
    "sec-professional_recommendation",
    "sec-professional_conclusion",
)

PROFESSIONAL_PAGE_TITLES: Final[Mapping[str, str]] = {
    "sec-executive_summary": "Tóm tắt",
    "sec-chart": "Lá số",
    "sec-core_interpretation": "Luận giải cốt lõi",
    "sec-ten_gods": "Thập thần",
    "sec-shen_sha": "Thần sát",
    "sec-luck": "Đại vận hiện tại",
    "sec-career": "Sự nghiệp",
    "sec-life_areas": "Tài chính · Quan hệ · Sức khỏe · Học hỏi",
    "sec-professional_recommendation": "Khuyến nghị",
    "sec-professional_conclusion": "Kết luận",
}

# Professional may publish more of the same narrative. Not a second composer.
PROFESSIONAL_SECTION_LIMITS: Final[Mapping[str, int]] = {
    "sec-executive_summary": 6,
    "sec-chart": 8,
    "sec-core_interpretation": 8,
    "sec-ten_gods": 6,
    "sec-shen_sha": 4,
    "sec-luck": 7,
    "sec-career": 8,
    "sec-life_areas": 8,
    "sec-professional_recommendation": 5,
    "sec-professional_conclusion": 1,
}

APPENDIX_SECTION_ID: Final[str] = "sec-technical_appendix"
APPENDIX_TITLE: Final[str] = "Phụ lục kỹ thuật"
APPENDIX_LIMIT: Final[int] = 12

MIN_CONSULTING_WORDS: Final[int] = 8
MIN_ROLE_WHY_WORDS: Final[int] = 12

CORE_DOMAINS: Final[frozenset[str]] = frozenset({"Pattern", "Strength", "UsefulGod"})
TEN_GOD_DOMAIN: Final[str] = "TenGods"
SHEN_SHA_DOMAIN: Final[str] = "ShenSha"

LUCK_MARKERS: Final[tuple[str, ...]] = (
    "đại vận",
    "khung thời gian",
    "vận hiện tại",
)

CAREER_MARKERS: Final[tuple[str, ...]] = (
    "sự nghiệp",
    "hợp môi trường",
    "phong cách",
    "không suy ra một nghề",
    "không suy ra nghề",
)

ROLE_WHY_MARKERS: Final[tuple[str, ...]] = (
    "dụng thần",
    "hỷ thần",
    "kỵ thần",
    "khi được chọn",
    "gia cố",
    "vai trò",
    "kênh",
)
