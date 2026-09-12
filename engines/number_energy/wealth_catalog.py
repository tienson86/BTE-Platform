"""Frozen Phone Wealth Flow labels from Knowledge 13 + Golden fixture.

Copy is catalog/rules only. This module does not score or recommend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from engines.number_energy.constants import TRIPLE_STATUS_DEFINED, TRIPLE_STATUS_UNDEFINED

TIAN_YI_ENERGY_ID: Final[str] = "tian_yi"
TIAN_YI_LABEL: Final[str] = "Thiên Y"
STORY_WEALTH_NODE: Final[str] = "Tài"

WEALTH_ROLE_PRESENCE: Final[str] = "PRESENCE"
WEALTH_ROLE_SOURCE: Final[str] = "SOURCE"
WEALTH_ROLE_DESTINATION: Final[str] = "DESTINATION"
WEALTH_ROLE_LATER_OUTCOME: Final[str] = "LATER_OUTCOME"

REFERENCE_PAIR: Final[str] = "pair"
REFERENCE_TRIPLE: Final[str] = "triple"

WEALTH_STAGE_IDS: Final[tuple[str, ...]] = ("WF-01", "WF-02", "WF-03", "WF-04")
WEALTH_STAGE_LABELS: Final[tuple[str, ...]] = (
    "TÀI VẬN",
    "TÀI TỪ ĐÂU?",
    "TÀI ĐI ĐÂU?",
    "HẬU VẬN",
)

PRESENCE_HEADLINE: Final[str] = "Có Thiên Y"
PRESENCE_SUMMARY_KEY: Final[str] = "WEALTH_PRESENCE"
NO_DIRECT_THIEN_Y_HEADLINE: Final[str] = "Không có Thiên Y trực tiếp"
NO_DIRECT_THIEN_Y_SUMMARY: Final[str] = (
    "Dãy số không xuất hiện trường Thiên Y trực tiếp, "
    "vì vậy tín hiệu tài vận theo trục Thiên Y không nổi bật."
)
PRESENCE_NARRATIVE_ONE: Final[str] = (
    "Dãy xuất hiện một điểm Thiên Y, vì vậy trục tài vận được hình thành."
)
PRESENCE_NARRATIVE_TWO: Final[str] = (
    "Dãy xuất hiện hai điểm Thiên Y, vì vậy trục tài vận được hình thành rõ."
)
PRESENCE_NARRATIVE_MANY: Final[str] = (
    "Dãy xuất hiện nhiều điểm Thiên Y, vì vậy trục tài vận được hình thành rõ."
)

GOLDEN_QUY_NHAN_CAREER_DN_TY_SYNTHESIS: Final[str] = (
    "Dòng tài vận của dãy đi theo hướng: quý nhân và cơ hội mở đường, "
    "nguồn lực được đưa vào sự nghiệp, và phần cuối lại quy về khả năng "
    "tạo Tài từ chính năng lực nghề nghiệp."
)

STATUS_DEFINED: Final[str] = TRIPLE_STATUS_DEFINED
STATUS_UNDEFINED: Final[str] = TRIPLE_STATUS_UNDEFINED


@dataclass(frozen=True, slots=True)
class WealthSourceRule:
    """SOURCE → Thiên Y customer labels from Knowledge 13 §9."""

    key: str
    customer_label: str
    customer_wording: str
    later_followup: str
    story_node: str


@dataclass(frozen=True, slots=True)
class WealthDestinationRule:
    """Thiên Y → TARGET customer labels from Knowledge 13 §11."""

    key: str
    customer_label: str
    customer_wording: str
    story_node: str


WEALTH_SOURCE_BY_LEFT_CODE: Final[dict[str, WealthSourceRule]] = {
    "SK": WealthSourceRule(
        key="QUY_NHAN",
        customer_label="Quý nhân & cơ hội",
        customer_wording=(
            "Quý nhân, quan hệ hoặc cơ hội có khả năng dẫn tới tài vận."
        ),
        later_followup=(
            "Sinh Khí đứng trước cho thấy quý nhân hoặc cơ hội "
            "tiếp tục là nguồn dẫn tới tài vận."
        ),
        story_node="Quý nhân & cơ hội",
    ),
    "TY": WealthSourceRule(
        key="REINFORCED_WEALTH",
        customer_label="Tài khí tăng cường",
        customer_wording=(
            "Trường Thiên Y được tiếp nối, làm tín hiệu tài vận trở nên nổi bật hơn."
        ),
        later_followup=(
            "Thiên Y đứng trước cho thấy tài khí tiếp tục được tăng cường "
            "ở phần cuối dãy."
        ),
        story_node="Tài khí tăng cường",
    ),
    "DN": WealthSourceRule(
        key="CAREER_ABILITY",
        customer_label="Năng lực nghề nghiệp",
        customer_wording=(
            "Tài vận chủ yếu đến từ năng lực làm việc, chuyên môn và sự nghiệp."
        ),
        later_followup=(
            "Diên Niên đứng trước cho thấy năng lực và công việc "
            "tiếp tục là nguồn dẫn tới tài vận."
        ),
        story_node="Năng lực nghề nghiệp",
    ),
    "PV": WealthSourceRule(
        key="PATIENCE_ACCUMULATION",
        customer_label="Kiên trì & tích lũy",
        customer_wording=(
            "Tài vận thiên về tích lũy theo thời gian, cần sự kiên trì và ổn định."
        ),
        later_followup=(
            "Phục Vị đứng trước cho thấy kiên trì và tích lũy "
            "tiếp tục là nguồn dẫn tới tài vận."
        ),
        story_node="Kiên trì & tích lũy",
    ),
    "LS": WealthSourceRule(
        key="SERVICE",
        customer_label="Dịch vụ & quan hệ",
        customer_wording=(
            "Nguồn tài phù hợp với dịch vụ, giao tiếp, "
            "chăm sóc khách hàng hoặc công việc cần sự tinh tế."
        ),
        later_followup=(
            "Lục Sát đứng trước cho thấy dịch vụ và quan hệ "
            "tiếp tục là nguồn dẫn tới tài vận."
        ),
        story_node="Dịch vụ & quan hệ",
    ),
    "HH": WealthSourceRule(
        key="COMMUNICATION",
        customer_label="Khẩu tài",
        customer_wording=(
            "Khả năng nói, bán hàng, tư vấn hoặc thuyết phục "
            "có thể trở thành công cụ tạo thu nhập."
        ),
        later_followup=(
            "Họa Hại đứng trước cho thấy khẩu tài tiếp tục là nguồn dẫn tới tài vận."
        ),
        story_node="Khẩu tài",
    ),
    "NQ": WealthSourceRule(
        key="INTELLECT_CREATIVITY",
        customer_label="Trí tuệ & sáng tạo",
        customer_wording=(
            "Tài vận gắn với trí tuệ, ý tưởng, khả năng phân tích, "
            "sáng tạo hoặc công việc dùng nhiều chất xám."
        ),
        later_followup=(
            "Ngũ Quỷ đứng trước cho thấy trí tuệ và sáng tạo "
            "tiếp tục là nguồn dẫn tới tài vận."
        ),
        story_node="Trí tuệ & sáng tạo",
    ),
    "TM": WealthSourceRule(
        key="ACTION_INVESTMENT",
        customer_label="Hành động & đầu tư",
        customer_wording=(
            "Tài vận gắn với hành động, nỗ lực, kinh doanh, "
            "đầu tư hoặc quản lý tài sản."
        ),
        later_followup=(
            "Tuyệt Mệnh đứng trước cho thấy hành động và nỗ lực "
            "tiếp tục là nguồn dẫn tới tài vận."
        ),
        story_node="Hành động & đầu tư",
    ),
}

WEALTH_DESTINATION_BY_RIGHT_CODE: Final[dict[str, WealthDestinationRule]] = {
    "SK": WealthDestinationRule(
        key="RELATIONSHIP_NETWORK",
        customer_label="Quan hệ & bằng hữu",
        customer_wording=(
            "Sau khi có tài, nguồn lực có xu hướng được sử dụng "
            "cho quan hệ, bạn bè hoặc việc mở rộng nhân duyên."
        ),
        story_node="Quan hệ",
    ),
    "TY": WealthDestinationRule(
        key="REINFORCED_WEALTH",
        customer_label="Tài khí tiếp nối",
        customer_wording=(
            "Tài khí được tiếp tục tăng cường, làm chủ đề tài vận nổi bật trong dãy số."
        ),
        story_node="Tài",
    ),
    "DN": WealthDestinationRule(
        key="CAREER_BUSINESS",
        customer_label="Sự nghiệp & lập nghiệp",
        customer_wording=(
            "Nguồn lực có xu hướng được đưa vào công việc, kinh doanh "
            "hoặc phát triển sự nghiệp."
        ),
        story_node="Sự nghiệp",
    ),
    "PV": WealthDestinationRule(
        key="EXTENDED_WEALTH",
        customer_label="Tài khí kéo dài",
        customer_wording=(
            "Thiên Y được Phục Vị kéo dài, vì vậy ảnh hưởng của tài khí "
            "có xu hướng tiếp tục sang đoạn sau của dãy số."
        ),
        story_node="Tài khí",
    ),
    "LS": WealthDestinationRule(
        key="SERVICE_RELATIONSHIP_EXPENSE",
        customer_label="Quan hệ & tiêu dùng",
        customer_wording=(
            "Tài khí phía trước dễ chuyển thành chi tiêu "
            "cho quan hệ, gia đình, dịch vụ hoặc nhu cầu đời sống."
        ),
        story_node="Quan hệ",
    ),
    "HH": WealthDestinationRule(
        key="COMMUNICATION_SOCIAL_EXPENSE",
        customer_label="Xã giao & chi tiêu",
        customer_wording=(
            "Dòng tài dễ chuyển sang các khoản chi cho giao tiếp, "
            "xã giao hoặc những nhu cầu phát sinh."
        ),
        story_node="Xã giao",
    ),
    "NQ": WealthDestinationRule(
        key="VOLATILE_FLOW",
        customer_label="Dòng tiền biến động",
        customer_wording=(
            "Tài khí có nhưng dòng tiền dễ biến động, "
            "vào ra nhanh và khó duy trì trạng thái ổn định."
        ),
        story_node="Dòng tiền",
    ),
    "TM": WealthDestinationRule(
        key="INVESTMENT_ACTION_OUTFLOW",
        customer_label="Đầu tư & hành động",
        customer_wording=(
            "Nguồn tài có xu hướng được đưa vào đầu tư, "
            "hành động hoặc những quyết định tài chính mạnh."
        ),
        story_node="Đầu tư",
    ),
}
