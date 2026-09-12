"""Frozen domain / finding copy from Golden fixture and Knowledge 10/13.

Resolver selects templates. It does not invent spiritual copy or score.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

SOURCE_PAIR_OCCURRENCES: Final[str] = "pair_occurrences"
SOURCE_PAIR_SUMMARY: Final[str] = "pair_summary"
SOURCE_ENERGY_DISTRIBUTION: Final[str] = "energy_distribution"
SOURCE_TRIPLE_OCCURRENCES: Final[str] = "triple_occurrences"
SOURCE_CHAIN: Final[str] = "chain"
SOURCE_WEALTH_FLOW: Final[str] = "wealth_flow"
SOURCE_LATER_OUTCOME: Final[str] = "later_outcome"

ALLOWED_EVIDENCE_SOURCES: Final[frozenset[str]] = frozenset(
    {
        SOURCE_PAIR_OCCURRENCES,
        SOURCE_PAIR_SUMMARY,
        SOURCE_ENERGY_DISTRIBUTION,
        SOURCE_TRIPLE_OCCURRENCES,
        SOURCE_CHAIN,
        SOURCE_WEALTH_FLOW,
        SOURCE_LATER_OUTCOME,
    }
)

DOMAIN_TITLES: Final[tuple[str, ...]] = (
    "Tài vận",
    "Công việc & sự nghiệp",
    "Tình cảm & quan hệ",
    "Tính cách & năng lực",
    "Cân bằng trường khí",
)

INTERACTION_SK_TY: Final[str] = "Sinh Khí → Thiên Y"
INTERACTION_TY_DN: Final[str] = "Thiên Y → Diên Niên"
INTERACTION_DN_TY: Final[str] = "Diên Niên → Thiên Y"
INTERACTION_HH_SK: Final[str] = "Họa Hại → Sinh Khí"
INTERACTION_DN_DN: Final[str] = "Diên Niên → Diên Niên"

LABEL_TIAN_YI: Final[str] = "Thiên Y"
LABEL_SHENG_QI: Final[str] = "Sinh Khí"
LABEL_YAN_NIAN: Final[str] = "Diên Niên"
LABEL_HUO_HAI: Final[str] = "Họa Hại"


@dataclass(frozen=True, slots=True)
class DomainTemplate:
    """One frozen domain card."""

    domain: str
    conclusion: str
    narrative: str
    caution: str
    conclusion_key: str
    narrative_key: str
    caution_key: str | None


@dataclass(frozen=True, slots=True)
class FindingTemplate:
    """One frozen strength or caution."""

    semantic_key: str
    title: str
    summary: str


GOLDEN_DOMAINS: Final[tuple[DomainTemplate, ...]] = (
    DomainTemplate(
        domain="Tài vận",
        conclusion="Có đường Tài tương đối rõ",
        narrative=(
            "Dãy có hai trường Thiên Y. Điểm Thiên Y đầu được Sinh Khí dẫn vào, "
            "cho thấy quý nhân, quan hệ và cơ hội có thể hỗ trợ việc hình thành tài vận. "
            "Phần cuối Diên Niên → Thiên Y nhấn mạnh khả năng tạo Tài thông qua chuyên môn, "
            "năng lực làm việc và sự nghiệp."
        ),
        caution=(
            "Tài vận vẫn cần được nhìn trong toàn bộ cách sử dụng dãy số, "
            "không nên hiểu Thiên Y như một cam kết tài chính."
        ),
        conclusion_key="DOM-WEALTH-CLEAR-PATH",
        narrative_key="NAR-WEALTH-GOLDEN-001",
        caution_key="CAU-WEALTH-NO-GUARANTEE",
    ),
    DomainTemplate(
        domain="Công việc & sự nghiệp",
        conclusion="Đây là một trong những điểm mạnh nhất của dãy",
        narrative=(
            "Diên Niên xuất hiện ba lần liên tiếp ở phần sau của thân số, "
            "cho thấy công việc, trách nhiệm và năng lực nghề nghiệp là chủ đề nổi bật. "
            "Tổ hợp Thiên Y → Diên Niên cho thấy nguồn lực có xu hướng được đưa vào "
            "công việc hoặc lập nghiệp."
        ),
        caution="",
        conclusion_key="DOM-CAREER-STRONGEST",
        narrative_key="NAR-CAREER-GOLDEN-001",
        caution_key=None,
    ),
    DomainTemplate(
        domain="Tình cảm & quan hệ",
        conclusion="Quan hệ xã hội có yếu tố hỗ trợ",
        narrative=(
            "Sinh Khí xuất hiện hai lần và được tiếp nối ở đoạn đầu, "
            "làm nổi bật yếu tố nhân duyên, quý nhân và khả năng nhận được hỗ trợ. "
            "Tuy nhiên, dãy này không lấy trường tình cảm làm trục nổi bật nhất; "
            "trọng tâm vẫn nghiêng nhiều hơn về công việc và tài vận."
        ),
        caution="",
        conclusion_key="DOM-REL-SUPPORTIVE",
        narrative_key="NAR-REL-GOLDEN-001",
        caution_key=None,
    ),
    DomainTemplate(
        domain="Tính cách & năng lực",
        conclusion="Trách nhiệm và năng lực làm việc khá rõ",
        narrative=(
            "Diên Niên giữ vai trò chủ đạo, vì vậy dãy thiên về tính trách nhiệm, "
            "khả năng làm việc, tổ chức và xu hướng muốn tạo kết quả rõ ràng. "
            "Sinh Khí phía trước giúp cấu trúc bớt khô cứng, tăng yếu tố kết nối và hỗ trợ."
        ),
        caution="",
        conclusion_key="DOM-PERSONALITY-DUTY",
        narrative_key="NAR-PER-GOLDEN-001",
        caution_key=None,
    ),
    DomainTemplate(
        domain="Cân bằng trường khí",
        conclusion="Cát tinh giữ vai trò chủ đạo",
        narrative=(
            "Toàn thân số có Sinh Khí, Thiên Y và Diên Niên chiếm ưu thế. "
            "Họa Hại chỉ xuất hiện ở đầu thân số và ngay sau đó đi vào tổ hợp "
            "Họa Hại → Sinh Khí. Cấu trúc tổng thể không nên được đọc theo cách "
            "đơn giản là “có một Hung tinh”."
        ),
        caution="",
        conclusion_key="DOM-BALANCE-CAT-LEAD",
        narrative_key="NAR-BAL-GOLDEN-001",
        caution_key=None,
    ),
)

STRENGTH_QUY_NHAN: Final[FindingTemplate] = FindingTemplate(
    semantic_key="ST-QUY-NHAN-TAI",
    title="Quý nhân có thể mở đường cho Tài",
    summary=(
        "Quan hệ, người hỗ trợ hoặc những cơ hội thuận lợi "
        "có thể trở thành một trong những con đường hình thành Tài."
    ),
)
STRENGTH_CAREER_REPEAT: Final[FindingTemplate] = FindingTemplate(
    semantic_key="ST-CAREER-REPEAT",
    title="Năng lực nghề nghiệp nổi bật",
    summary=(
        "Diên Niên được lặp lại liên tiếp, làm công việc, trách nhiệm "
        "và năng lực nghề nghiệp trở thành chủ đề mạnh của dãy."
    ),
)
STRENGTH_CAREER_RESULT: Final[FindingTemplate] = FindingTemplate(
    semantic_key="ST-CAREER-RESULT",
    title="Công việc có khả năng tạo thành quả",
    summary=(
        "Phần cuối dãy tiếp tục đưa năng lực nghề nghiệp về Thiên Y, "
        "làm rõ hơn con đường tạo Tài bằng chuyên môn và công việc."
    ),
)
STRENGTH_KHAU_TAI: Final[FindingTemplate] = FindingTemplate(
    semantic_key="ST-KHAU-TAI",
    title="Khẩu tài có thể phát huy tích cực",
    summary=(
        "Khả năng nói và diễn đạt có giá trị khi được sử dụng đúng cách, "
        "đặc biệt trong giao tiếp và công việc với con người."
    ),
)

CAUTION_SPEECH: Final[FindingTemplate] = FindingTemplate(
    semantic_key="CA-SPEECH",
    title="Cần chú ý cách sử dụng lời nói",
    summary=(
        "Họa Hại xuất hiện ở đầu thân số, vì vậy lời nói và cách phản ứng "
        "vẫn là một điểm cần tiết chế. Khi dùng tốt, bộ 328 lại phát huy thành khẩu tài."
    ),
)
CAUTION_CAT_COUNT: Final[FindingTemplate] = FindingTemplate(
    semantic_key="CA-CAT-COUNT",
    title="Không nên chỉ nhìn số lượng Cát tinh",
    summary=(
        "Dãy có nhiều Cát tinh, nhưng giá trị thực tế vẫn nằm ở cách "
        "các trường khí nối tiếp và vận động với nhau."
    ),
)

# Fallback domain copy from Knowledge 13 / Knowledge 10 when Golden pattern is absent.
WEALTH_NO_TIAN_YI: Final[DomainTemplate] = DomainTemplate(
    domain="Tài vận",
    conclusion="Tín hiệu tài vận theo trục Thiên Y không nổi bật",
    narrative=(
        "Dãy số không xuất hiện trường Thiên Y trực tiếp, "
        "vì vậy tín hiệu tài vận theo trục Thiên Y không nổi bật."
    ),
    caution="Không nên hiểu việc vắng Thiên Y như kết luận không có tài.",
    conclusion_key="DOM-WEALTH-NO-DIRECT-TY",
    narrative_key="NAR-WEALTH-NO-DIRECT-TY",
    caution_key="CAU-WEALTH-NO-POVERTY-CLAIM",
)
WEALTH_HAS_TIAN_YI: Final[DomainTemplate] = DomainTemplate(
    domain="Tài vận",
    conclusion="Có Thiên Y",
    narrative=(
        "Dãy xuất hiện trường Thiên Y, vì vậy trục tài vận được hình thành. "
        "Kết luận cuối cùng vẫn cần nhìn nguồn vào, hướng đi và phần cuối dãy."
    ),
    caution=(
        "Không nên hiểu Thiên Y như một cam kết tài chính."
    ),
    conclusion_key="DOM-WEALTH-HAS-TY",
    narrative_key="NAR-WEALTH-HAS-TY",
    caution_key="CAU-WEALTH-NO-GUARANTEE",
)
WEALTH_SK_TY: Final[DomainTemplate] = DomainTemplate(
    domain="Tài vận",
    conclusion="Quý nhân, quan hệ hoặc cơ hội có thể hỗ trợ tài vận",
    narrative=(
        "Tài vận của dãy nghiêng về khả năng nhận cơ hội thông qua quý nhân, "
        "quan hệ hoặc môi trường hỗ trợ."
    ),
    caution=(
        "Không nên hiểu Thiên Y như một cam kết tài chính."
    ),
    conclusion_key="DOM-WEALTH-SQ-TY",
    narrative_key="NAR-WEALTH-SQ-TY-001",
    caution_key="CAU-WEALTH-NO-GUARANTEE",
)
WEALTH_DN_TY: Final[DomainTemplate] = DomainTemplate(
    domain="Tài vận",
    conclusion="Tài vận thiên về năng lực nghề nghiệp",
    narrative=(
        "Dòng tài vận thiên về kiếm tiền bằng năng lực, chuyên môn và kinh nghiệm thực tế."
    ),
    caution=(
        "Không nên hiểu Thiên Y như một cam kết tài chính."
    ),
    conclusion_key="DOM-WEALTH-YN-TY",
    narrative_key="NAR-WEALTH-YN-TY-001",
    caution_key="CAU-WEALTH-NO-GUARANTEE",
)

CAREER_TY_DN: Final[DomainTemplate] = DomainTemplate(
    domain="Công việc & sự nghiệp",
    conclusion="Nguồn lực có xu hướng được đưa vào công việc hoặc lập nghiệp",
    narrative=(
        "Dãy số cho thấy xu hướng đưa tài nguyên vào sự nghiệp, "
        "phù hợp với việc xây dựng công việc hoặc tự mình làm chủ."
    ),
    caution="",
    conclusion_key="DOM-CAREER-TY-YN",
    narrative_key="NAR-CAREER-TY-YN-001",
    caution_key=None,
)
CAREER_HAS_DN: Final[DomainTemplate] = DomainTemplate(
    domain="Công việc & sự nghiệp",
    conclusion="Năng lực nghề nghiệp có mặt trong dãy",
    narrative=(
        "Diên Niên xuất hiện trong dãy, làm nổi bật trách nhiệm, "
        "khả năng làm việc và xu hướng tạo kết quả."
    ),
    caution="",
    conclusion_key="DOM-CAREER-HAS-DN",
    narrative_key="NAR-PER-YN-001",
    caution_key=None,
)
CAREER_QUIET: Final[DomainTemplate] = DomainTemplate(
    domain="Công việc & sự nghiệp",
    conclusion="Công việc chưa phải trục nổi bật nhất",
    narrative=(
        "Diên Niên không chiếm ưu thế trên dãy, vì vậy chủ đề sự nghiệp "
        "không nổi bật như các miền khác."
    ),
    caution="",
    conclusion_key="DOM-CAREER-QUIET",
    narrative_key="NAR-CAREER-QUIET",
    caution_key=None,
)

REL_HAS_SK: Final[DomainTemplate] = DomainTemplate(
    domain="Tình cảm & quan hệ",
    conclusion="Quan hệ xã hội có yếu tố hỗ trợ",
    narrative=(
        "Sinh Khí làm nổi bật yếu tố nhân duyên, quý nhân và khả năng nhận được hỗ trợ. "
        "Dãy này không lấy trường tình cảm làm trục duy nhất."
    ),
    caution="",
    conclusion_key="DOM-REL-HAS-SK",
    narrative_key="NAR-REL-SQ-TY-001",
    caution_key=None,
)
REL_QUIET: Final[DomainTemplate] = DomainTemplate(
    domain="Tình cảm & quan hệ",
    conclusion="Quan hệ chưa phải trục nổi bật nhất",
    narrative=(
        "Sinh Khí không chiếm ưu thế, vì vậy dãy không lấy trường tình cảm "
        "làm trục nổi bật nhất."
    ),
    caution="",
    conclusion_key="DOM-REL-QUIET",
    narrative_key="NAR-REL-QUIET",
    caution_key=None,
)

PERSONALITY_DN: Final[DomainTemplate] = DomainTemplate(
    domain="Tính cách & năng lực",
    conclusion="Trách nhiệm và năng lực làm việc khá rõ",
    narrative=(
        "Diên Niên tạo tính trách nhiệm, chủ kiến và khả năng chịu áp lực. "
        "Đây là trường khí phù hợp với người cần tổ chức hoặc đứng ra gánh trách nhiệm."
    ),
    caution="",
    conclusion_key="DOM-PERSONALITY-YN",
    narrative_key="NAR-PER-YN-001",
    caution_key=None,
)
PERSONALITY_SK: Final[DomainTemplate] = DomainTemplate(
    domain="Tính cách & năng lực",
    conclusion="Sự cởi mở và khả năng hòa nhập",
    narrative=(
        "Sinh Khí làm nổi bật sự cởi mở, lạc quan và khả năng hòa nhập."
    ),
    caution="",
    conclusion_key="DOM-PERSONALITY-SQ",
    narrative_key="NAR-PER-SQ-001",
    caution_key=None,
)
PERSONALITY_TY: Final[DomainTemplate] = DomainTemplate(
    domain="Tính cách & năng lực",
    conclusion="Sự thiện lương và khả năng tạo niềm tin",
    narrative=(
        "Thiên Y làm nổi bật sự thiện lương, rộng rãi và khả năng cảm nhận người khác."
    ),
    caution="",
    conclusion_key="DOM-PERSONALITY-TY",
    narrative_key="NAR-PER-TY-001",
    caution_key=None,
)
PERSONALITY_GENERIC: Final[DomainTemplate] = DomainTemplate(
    domain="Tính cách & năng lực",
    conclusion="Tính cách đi theo năng lượng chủ đạo của dãy",
    narrative=(
        "Tính cách và năng lực được đọc theo trường khí chủ đạo của toàn dãy, "
        "không kết luận từ một cặp số đơn lẻ."
    ),
    caution="",
    conclusion_key="DOM-PERSONALITY-GENERIC",
    narrative_key="NAR-PER-GENERIC",
    caution_key=None,
)

BALANCE_CAT_LEAD: Final[DomainTemplate] = DomainTemplate(
    domain="Cân bằng trường khí",
    conclusion="Cát tinh giữ vai trò chủ đạo",
    narrative=(
        "Các trường thuận giữ vai trò chủ, trong khi những trường có tính thử thách "
        "không nên được đọc tách rời khỏi toàn chuỗi."
    ),
    caution="",
    conclusion_key="DOM-BALANCE-CAT-LEAD",
    narrative_key="NAR-BAL-WELL-001",
    caution_key=None,
)
BALANCE_MIXED: Final[DomainTemplate] = DomainTemplate(
    domain="Cân bằng trường khí",
    conclusion="Cấu trúc có cả thuận và thử thách",
    narrative=(
        "Dãy có cả trường thuận và trường thử thách. "
        "Giá trị nằm ở cách các trường khí nối tiếp, không chỉ ở số lượng Cát hay Hung."
    ),
    caution="",
    conclusion_key="DOM-BALANCE-MIXED",
    narrative_key="NAR-BAL-PARTIAL-001",
    caution_key=None,
)
