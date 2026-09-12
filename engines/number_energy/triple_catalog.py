"""Frozen triple catalog from knowledge/12_TRIPLE_COMBINATION_CATALOG.md.

Runtime looks up directed A→B by interaction_id. It does not invent meaning.
"""

from __future__ import annotations

from typing import Final, TypedDict

from engines.number_energy.constants import (
    TRIPLE_PRIORITY_COMPACT,
    TRIPLE_PRIORITY_FEATURED,
    TRIPLE_PRIORITY_STANDARD,
)


class TripleCatalogRow(TypedDict):
    """One directed interaction from Knowledge 12."""

    customer_title: str
    customer_summary: str
    domains: tuple[str, ...]
    priority: str


def _row(
    title: str,
    summary: str,
    domains: tuple[str, ...],
    priority: str = TRIPLE_PRIORITY_STANDARD,
) -> TripleCatalogRow:
    """Build one frozen catalog row."""
    return {
        "customer_title": title,
        "customer_summary": summary,
        "domains": domains,
        "priority": priority,
    }


# Keys are interaction_id (canonical_meaning_key). Copy is Knowledge 12;
# customer_title for Golden phone interactions matches 01_GOLDEN_PHONE_FIXTURE.
TRIPLE_CATALOG: Final[dict[str, TripleCatalogRow]] = {
    "SK_TO_SK": _row(
        "Quý nhân và cơ hội được tăng cường",
        "Năng lượng Sinh Khí được tiếp nối, làm nổi bật khả năng gặp người hỗ trợ, cơ hội và các mối quan hệ thuận lợi.",
        ("Quý nhân", "Quan hệ", "Cơ hội", "Công việc"),
    ),
    "TY_TO_SK": _row(
        "Hiếu bằng hữu, nhân duyên tốt",
        "Có tình nghĩa, coi trọng bạn bè và dễ tạo thiện cảm trong quan hệ; đồng thời cũng dễ dành nhiều tiền bạc hoặc nguồn lực cho các mối quan hệ.",
        ("Quan hệ", "Tài chính", "Nhân duyên"),
    ),
    "DN_TO_SK": _row(
        "Công việc vui vẻ, lợi cho học hành",
        "Công việc có xu hướng thuận hơn, tinh thần làm việc thoải mái; đồng thời hỗ trợ khả năng học hỏi và phát triển chuyên môn.",
        ("Công việc", "Học tập", "Tinh thần"),
    ),
    "PV_TO_SK": _row(
        "Sinh Khí được tăng cường",
        "Sinh Khí được gia tăng và kéo dài, làm rõ hơn yếu tố quý nhân, cơ hội và sự hỗ trợ.",
        ("Quý nhân", "Cơ hội", "Quan hệ"),
    ),
    "LS_TO_SK": _row(
        "Nhân duyên tốt, giao tiếp tích cực",
        "Khả năng giao tiếp và xây dựng quan hệ được phát huy theo hướng tích cực; dễ tạo thiện cảm và kết nối với người khác.",
        ("Giao tiếp", "Nhân duyên", "Quan hệ xã hội"),
    ),
    "HH_TO_SK": _row(
        "Khẩu tài tốt",
        "Khả năng giao tiếp và diễn đạt là điểm mạnh. Lời nói có sức thuyết phục và dễ được người khác tiếp nhận.",
        ("Giao tiếp", "Nghề nghiệp", "Kinh doanh"),
    ),
    "NQ_TO_SK": _row(
        "Động não, ý tưởng hữu dụng",
        "Khả năng suy nghĩ nhanh và sáng tạo được dẫn theo hướng hữu ích, dễ hình thành ý tưởng hoặc phương án mới.",
        ("Trí tuệ", "Sáng tạo", "Công việc"),
    ),
    "TM_TO_SK": _row(
        "Hành động chuyển sang cởi mở",
        "Năng lượng hành động mạnh được nối sang Sinh Khí, làm trạng thái trở nên cởi mở và tích cực hơn.",
        ("Tinh thần", "Hành động"),
    ),
    "SK_TO_TY": _row(
        "Quý nhân mang đến Tài vận",
        "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận.",
        ("Tài vận", "Quý nhân", "Cơ hội"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "TY_TO_TY": _row(
        "Tài vận được tăng cường",
        "Thiên Y được tăng cường, làm nổi bật tài vận và tín hiệu tình cảm/hôn nhân.",
        ("Tài vận", "Tình cảm", "Hôn nhân"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "DN_TO_TY": _row(
        "Năng lực nghề nghiệp tạo Tài",
        "Tài vận chủ yếu đến từ năng lực nghề nghiệp và sức làm việc. Hiệu quả tài chính còn phụ thuộc cường độ tương đối giữa Diên Niên và Thiên Y.",
        ("Tài vận", "Nghề nghiệp", "Năng lực"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "PV_TO_TY": _row(
        "Tài vận từ kiên trì",
        "Tài vận thiên về tích lũy theo thời gian; kiên trì và ổn định quan trọng hơn việc nóng vội.",
        ("Tài vận", "Tích lũy", "Kiên trì"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "LS_TO_TY": _row(
        "Tài từ ngành dịch vụ",
        "Tài vận phù hợp với các lĩnh vực dịch vụ, giao tiếp, chăm sóc khách hàng hoặc công việc cần sự tinh tế.",
        ("Tài vận", "Dịch vụ", "Giao tiếp"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "HH_TO_TY": _row(
        "Tài từ khẩu tài",
        "Khả năng nói, tư vấn, bán hàng hoặc thuyết phục có thể trở thành công cụ tạo thu nhập.",
        ("Tài vận", "Bán hàng", "Tư vấn", "Giao tiếp"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "NQ_TO_TY": _row(
        "Tài từ trí tuệ",
        "Trí tuệ, sáng tạo, ý tưởng, khả năng phân tích hoặc công việc dùng nhiều chất xám có thể trở thành nguồn tạo tài.",
        ("Tài vận", "Trí tuệ", "Sáng tạo"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "TM_TO_TY": _row(
        "Tài từ hành động và đầu tư",
        "Tài vận gắn với hành động, nỗ lực, kinh doanh, đầu tư hoặc quản lý tài sản.",
        ("Tài vận", "Đầu tư", "Kinh doanh", "Quản lý tài sản"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "SK_TO_DN": _row(
        "Quý nhân mang đến công việc",
        "Quý nhân và cơ hội hỗ trợ rõ cho công việc, học tập, chuyên môn và khả năng thăng tiến.",
        ("Công việc", "Quý nhân", "Lãnh đạo", "Học tập"),
    ),
    "TY_TO_DN": _row(
        "Tài đi vào sự nghiệp",
        "Có xu hướng chủ động xây dựng sự nghiệp, phù hợp kinh doanh hoặc tự mình làm chủ.",
        ("Sự nghiệp", "Kinh doanh", "Đầu tư"),
        TRIPLE_PRIORITY_FEATURED,
    ),
    "DN_TO_DN": _row(
        "Năng lực nghề nghiệp được tăng cường",
        "Khả năng làm việc, trách nhiệm và năng lực quản lý được tăng cường.",
        ("Công việc", "Lãnh đạo", "Quản lý"),
        TRIPLE_PRIORITY_COMPACT,
    ),
    "PV_TO_DN": _row(
        "Diên Niên được tăng cường",
        "Diên Niên được tăng cường, làm nổi bật năng lực công việc, trách nhiệm và quyền hạn.",
        ("Công việc", "Quản lý", "Quyền hạn"),
    ),
    "LS_TO_DN": _row(
        "Công tác hành chính hoặc phục vụ",
        "Phù hợp công việc hành chính, dịch vụ hoặc môi trường cần xử lý quan hệ xã hội tinh tế.",
        ("Nghề nghiệp", "Dịch vụ", "Quan hệ xã hội"),
    ),
    "HH_TO_DN": _row(
        "Khẩu tài làm nghề",
        "Khả năng giao tiếp, nói, giảng giải, tư vấn hoặc bán hàng có thể trở thành năng lực nghề nghiệp chính.",
        ("Nghề nghiệp", "Giao tiếp", "Bán hàng", "Tư vấn"),
    ),
    "NQ_TO_DN": _row(
        "Công việc dùng trí tuệ",
        "Phù hợp công việc cần tư duy nhanh, sáng tạo, phân tích và xử lý vấn đề liên tục.",
        ("Nghề nghiệp", "Trí tuệ", "Sáng tạo"),
    ),
    "TM_TO_DN": _row(
        "Công việc dám hành động",
        "Khả năng hành động và quyết đoán được đưa vào công việc; phù hợp môi trường kinh doanh, đầu tư hoặc quản lý tài sản.",
        ("Nghề nghiệp", "Kinh doanh", "Đầu tư", "Quản lý tài sản"),
    ),
    "SK_TO_PV": _row(
        "Sinh Khí được kéo dài",
        "Từ trường Sinh Khí được kéo dài.",
        ("Quý nhân", "Cơ hội"),
    ),
    "TY_TO_PV": _row(
        "Thiên Y được kéo dài",
        "Từ trường Thiên Y được kéo dài.",
        ("Tài vận",),
    ),
    "DN_TO_PV": _row(
        "Diên Niên được kéo dài",
        "Từ trường Diên Niên được kéo dài.",
        ("Công việc",),
    ),
    "PV_TO_PV": _row(
        "Phục Vị được tăng cường",
        "Từ trường Phục Vị được tăng cường, vận sức chờ phát động.",
        ("Ổn định",),
    ),
}


def lookup_triple(interaction_id: str) -> TripleCatalogRow | None:
    """Return the frozen catalog row, or None when UNDEFINED."""
    return TRIPLE_CATALOG.get(interaction_id)
