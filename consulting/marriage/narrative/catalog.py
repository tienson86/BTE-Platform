"""Deterministic TV-01 Vietnamese narrative catalog. Keyed by semantic meaning."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import DomainDecisionState, FindingType, MarriageDomain
from consulting.marriage.models.enums import RecommendationType


@dataclass(frozen=True, slots=True)
class NarrativeEntry:
    """One catalog entry. Text may vary by key; meaning stays bound to the key."""

    key: str
    headline: str
    observation: str
    reason: str
    impact: str
    action_bridge: str


def _e(
    key: str,
    headline: str,
    observation: str,
    reason: str,
    impact: str,
    action_bridge: str,
) -> NarrativeEntry:
    """Build one catalog entry."""
    return NarrativeEntry(key, headline, observation, reason, impact, action_bridge)


_OVERALL: dict[str, NarrativeEntry] = {
    DomainDecisionState.SUPPORTIVE.value: _e(
        "marriage.overall.supportive",
        "Tương hợp tốt về cấu trúc",
        "Cấu trúc hiện cho thấy xu hướng hỗ trợ lẫn nhau ở tầng nền tảng.",
        "Các miền then chốt cùng hướng hỗ trợ hơn là tạo áp lực.",
        "Hai người có cơ sở để phối hợp ổn định khi giữ nhịp trao đổi đều đặn.",
        "Nên củng cố những điểm đang hỗ trợ thay vì thay đổi hướng đột ngột.",
    ),
    DomainDecisionState.BALANCED.value: _e(
        "marriage.overall.balanced",
        "Nền tảng tương đối cân bằng",
        "Cấu trúc hiện cho thấy sự cân bằng, chưa nghiêng rõ về hỗ trợ hay áp lực.",
        "Các tín hiệu then chốt chưa đủ mạnh để kết luận một chiều.",
        "Mối quan hệ có thể vận hành ổn nếu hai người giữ quy ước rõ ràng.",
        "Ưu tiên duy trì nhịp phối hợp hiện có.",
    ),
    DomainDecisionState.MIXED.value: _e(
        "marriage.overall.mixed",
        "Có một số điểm cần điều chỉnh",
        "Cấu trúc hiện cho thấy vừa có điểm hỗ trợ, vừa có điểm tạo áp lực.",
        "Các miền then chốt không cùng một hướng.",
        "Trong những giai đoạn áp lực, hai người có thể cần phối hợp rõ hơn.",
        "Nên xử lý điểm căng trước khi mở rộng các quyết định lớn.",
    ),
    DomainDecisionState.PRESSURED.value: _e(
        "marriage.overall.pressured",
        "Cần lưu ý các điểm áp lực",
        "Đây là điểm cần lưu ý: tầng cấu trúc đang nghiêng về áp lực hơn hỗ trợ.",
        "Các tín hiệu then chốt cho thấy xu hướng căng hơn là nâng đỡ.",
        "Nếu không có quy ước phối hợp, áp lực có thể dễ lộ ra trong sinh hoạt chung.",
        "Ưu tiên giảm xung đột và giữ biên giới trách nhiệm rõ.",
    ),
    DomainDecisionState.CRITICAL.value: _e(
        "marriage.overall.critical",
        "Cần thận trọng với các điểm then chốt",
        "Đây là điểm cần lưu ý ở mức then chốt, không phải lời kết luận tuyệt đối.",
        "Tầng cấu trúc đang cho thấy áp lực tập trung.",
        "Hai người nên chậm lại ở các quyết định lớn cho đến khi có quy ước rõ.",
        "Ưu tiên ổn định giao tiếp và ranh giới trước mọi bước mở rộng.",
    ),
    DomainDecisionState.INSUFFICIENT.value: _e(
        "marriage.overall.insufficient",
        "Chưa đủ dữ liệu để kết luận tổng thể",
        "Hệ thống chưa đủ cơ sở cấu trúc để đưa nhận định tổng thể.",
        "Một số miền then chốt chưa có bằng chứng đủ mạnh.",
        "Thiếu dữ liệu không đồng nghĩa hôn nhân kém tương hợp.",
        "Nên đọc các phần đã đủ dữ liệu và phần giới hạn đi kèm.",
    ),
}

_DOMAIN_TITLE: dict[str, str] = {
    MarriageDomain.FIVE_ELEMENTS.value: "Ngũ hành",
    MarriageDomain.STEM_BRANCH.value: "Can Chi",
    MarriageDomain.TEN_GODS.value: "Thập thần",
    MarriageDomain.INTERACTION.value: "Tương tác",
    MarriageDomain.FINANCE.value: "Tài chính",
    MarriageDomain.FAMILY.value: "Gia đình",
    MarriageDomain.CHILDREN.value: "Con cái",
    MarriageDomain.LUCK.value: "Vận hạn",
}

_DOMAIN_STATE: dict[tuple[str, str], NarrativeEntry] = {}


def _fill_domain(domain: str, stem: str) -> None:
    """Register domain-state entries for one domain."""
    _DOMAIN_STATE[(domain, "supportive")] = _e(
        f"marriage.domain.{stem}.supportive",
        f"{_DOMAIN_TITLE[domain]} đang hỗ trợ",
        f"Ở lớp {_DOMAIN_TITLE[domain].lower()}, cấu trúc hiện cho thấy xu hướng hỗ trợ.",
        "Các tín hiệu cùng miền đang nâng đỡ lẫn nhau.",
        "Điểm này giúp hai người dễ phối hợp hơn trên thực tế.",
        "Nên giữ nhịp đã có hiệu quả.",
    )
    _DOMAIN_STATE[(domain, "balanced")] = _e(
        f"marriage.domain.{stem}.balanced",
        f"{_DOMAIN_TITLE[domain]} tương đối cân",
        f"Lớp {_DOMAIN_TITLE[domain].lower()} đang ở mức cân, chưa nghiêng rõ.",
        "Chưa có tín hiệu then chốt đủ mạnh theo một hướng.",
        "Ảnh hưởng thực tế thường phụ thuộc quy ước hai người tự giữ.",
        "Nên quan sát thêm trước khi đổi hướng lớn.",
    )
    _DOMAIN_STATE[(domain, "mixed")] = _e(
        f"marriage.domain.{stem}.mixed",
        f"{_DOMAIN_TITLE[domain]} vừa hỗ trợ vừa cần điều chỉnh",
        f"Lớp {_DOMAIN_TITLE[domain].lower()} có cả điểm nâng đỡ và điểm tạo áp lực.",
        "Các tín hiệu trong cùng miền không cùng một hướng.",
        "Trong giai đoạn căng, điểm này có thể lộ ra thành khác biệt cách làm.",
        "Nên chốt quy ước cho đúng điểm lệch, không khái quát hóa.",
    )
    _DOMAIN_STATE[(domain, "pressured")] = _e(
        f"marriage.domain.{stem}.pressured",
        f"{_DOMAIN_TITLE[domain]} đang tạo áp lực",
        f"Đây là điểm cần lưu ý ở lớp {_DOMAIN_TITLE[domain].lower()}.",
        "Các tín hiệu cùng miền đang nghiêng về áp lực.",
        "Nếu thiếu quy ước, điểm này dễ thành ma sát trong sinh hoạt chung.",
        "Nên giảm xung đột đúng phần này thay vì kết luận cả mối quan hệ.",
    )
    _DOMAIN_STATE[(domain, "critical")] = _e(
        f"marriage.domain.{stem}.critical",
        f"{_DOMAIN_TITLE[domain]} cần thận trọng",
        f"Lớp {_DOMAIN_TITLE[domain].lower()} đang ở mức then chốt cần lưu ý.",
        "Áp lực tập trung hơn mức thông thường của miền này.",
        "Hai người nên chậm lại ở quyết định liên quan trực tiếp đến miền này.",
        "Ưu tiên ổn định trước, không phóng đại thành kết cục.",
    )


_fill_domain(MarriageDomain.FIVE_ELEMENTS.value, "five_elements")
_fill_domain(MarriageDomain.STEM_BRANCH.value, "stem_branch")
_fill_domain(MarriageDomain.TEN_GODS.value, "ten_gods")
_fill_domain(MarriageDomain.INTERACTION.value, "interaction")
_fill_domain(MarriageDomain.FINANCE.value, "finance")
_fill_domain(MarriageDomain.FAMILY.value, "family")
_fill_domain(MarriageDomain.CHILDREN.value, "children")
_fill_domain(MarriageDomain.LUCK.value, "luck")

_FINDING: dict[tuple[str, str], NarrativeEntry] = {
    (MarriageDomain.FIVE_ELEMENTS.value, FindingType.SUPPORT.value): _e(
        "marriage.finding.five_elements.support",
        "Điểm hỗ trợ nền tảng",
        "Có tín hiệu hỗ trợ ở tầng ngũ hành.",
        "Phần hỗ trợ này xuất phát từ cấu trúc đã được kết luận, không phải suy diễn thêm.",
        "Trên thực tế, hai người dễ nâng đỡ nhau ở nhu cầu cốt lõi.",
        "Nên giữ thói quen phối hợp đang phát huy.",
    ),
    (MarriageDomain.FIVE_ELEMENTS.value, FindingType.RISK.value): _e(
        "marriage.finding.five_elements.risk",
        "Điểm cần lưu ý ở nền tảng",
        "Có tín hiệu áp lực ở tầng ngũ hành.",
        "Đây là kết luận cấu trúc, không phải lời phán về số phận.",
        "Khi căng thẳng, khác biệt nhu cầu có thể lộ rõ hơn.",
        "Nên trao đổi sớm về nhịp sống và cách nâng đỡ lẫn nhau.",
    ),
    (MarriageDomain.STEM_BRANCH.value, FindingType.SUPPORT.value): _e(
        "marriage.finding.stem_branch.support",
        "Điểm phối hợp Can Chi",
        "Có tín hiệu phối hợp ở lớp can chi.",
        "Tín hiệu này thuộc kết luận đã được chốt ở tầng quyết định.",
        "Hai người có thể thấy nhịp ăn khớp dễ hơn ở một số việc chung.",
        "Nên tận dụng nhịp đó cho các việc cần thống nhất.",
    ),
    (MarriageDomain.STEM_BRANCH.value, FindingType.RISK.value): _e(
        "marriage.finding.stem_branch.risk",
        "Điểm ma sát Can Chi",
        "Có tín hiệu căng ở lớp can chi. Đây là điểm cần lưu ý.",
        "Xu hướng này không đồng nghĩa hai người không nên gắn bó.",
        "Trong giai đoạn áp lực, khác biệt nhịp phản ứng có thể tăng.",
        "Nên giảm xung đột bằng quy ước rõ, không bằng kết luận tuyệt đối.",
    ),
    (MarriageDomain.TEN_GODS.value, FindingType.SUPPORT.value): _e(
        "marriage.finding.ten_gods.support",
        "Điểm bổ trợ vai trò",
        "Có tín hiệu bổ trợ ở lớp vai trò.",
        "Phần này phản ánh cách hai người có thể nâng đỡ trách nhiệm của nhau.",
        "Trên thực tế, phân vai rõ sẽ giúp việc chung trôi hơn.",
        "Nên giữ ranh giới trách nhiệm đang hiệu quả.",
    ),
    (MarriageDomain.TEN_GODS.value, FindingType.RISK.value): _e(
        "marriage.finding.ten_gods.risk",
        "Điểm lệch vai trò",
        "Có tín hiệu lệch vai trò cần lưu ý.",
        "Đây là xu hướng cấu trúc, không phải đánh giá phẩm chất.",
        "Nếu không nói rõ trách nhiệm, dễ thành chồng chéo hoặc trống vai.",
        "Nên chốt lại ai giữ phần việc nào trong các quyết định chung.",
    ),
    (MarriageDomain.FINANCE.value, FindingType.SUPPORT.value): _e(
        "marriage.finding.finance.support",
        "Điểm bổ trợ tài chính",
        "Có tín hiệu bổ trợ trong cách phối hợp nguồn lực.",
        "Phần này xuất phát từ kết luận tài chính đã có, không suy ra giàu nghèo.",
        "Hai người có thể phối hợp chi tiêu dễ hơn nếu giữ quy ước chung.",
        "Nên duy trì ranh giới tiền bạc đang rõ.",
    ),
    (MarriageDomain.FINANCE.value, FindingType.RISK.value): _e(
        "marriage.finding.finance.risk",
        "Điểm cần quy ước tài chính",
        "Có tín hiệu cạnh tranh hoặc lệch nhịp về nguồn lực.",
        "Điều này không có nghĩa hôn nhân sẽ thiếu thốn.",
        "Khi có quyết định tiền bạc lớn, khác biệt cách làm có thể lộ ra.",
        "Nên đặt ranh giới chi tiêu chung trước khi quyết định lớn.",
    ),
    (MarriageDomain.LUCK.value, FindingType.TIMING.value): _e(
        "marriage.finding.luck.timing",
        "Điểm về nhịp thời điểm",
        "Có tín hiệu kích hoạt theo thời điểm, không viết lại nền tảng.",
        "Vận hạn chỉ điều chỉnh nhịp, không đổi kết luận nền tảng.",
        "Một số giai đoạn có thể dễ chịu hơn hoặc nhạy hơn.",
        "Nên xem thời điểm như lịch phối hợp, không như lời đoán ngày.",
    ),
}

_MIXED_FINDING = _e(
    "marriage.finding.mixed",
    "Điểm vừa hỗ trợ vừa cần lưu ý",
    "Có tín hiệu trái chiều trong cùng một lớp cấu trúc.",
    "Các tín hiệu không cùng một hướng nên không gộp thành một kết luận tuyệt đối.",
    "Trên thực tế, điểm này thường đòi hỏi quy ước rõ hơn là phán xét.",
    "Nên xử lý đúng phần lệch, không khái quát hóa cả mối quan hệ.",
)

_TIMING_STATE: dict[str, NarrativeEntry] = {
    "supportive": _e(
        "marriage.timing.supportive",
        "Giai đoạn tương đối thuận",
        "Nhịp thời điểm đang nghiêng về hỗ trợ hơn áp lực.",
        "Đây là lớp kích hoạt, không viết lại nền tảng sẵn có.",
        "Hai người có thể thấy phối hợp dễ hơn nếu giữ quy ước sẵn có.",
        "Nên dùng giai đoạn này để củng cố thói quen đang hiệu quả.",
    ),
    "stable": _e(
        "marriage.timing.stable",
        "Giai đoạn tương đối ổn",
        "Nhịp thời điểm chưa nghiêng rõ về thuận hay nhạy.",
        "Ổn định ở lớp kích hoạt không đồng nghĩa không cần phối hợp.",
        "Ảnh hưởng thực tế vẫn phụ thuộc quy ước hai người đang giữ.",
        "Nên duy trì nhịp hiện có.",
    ),
    "mixed": _e(
        "marriage.timing.mixed",
        "Giai đoạn có cả thuận và nhạy",
        "Nhịp thời điểm vừa có phần dễ chịu, vừa có phần cần lưu ý.",
        "Không dùng giai đoạn này để kết luận số phận hôn nhân.",
        "Khi áp lực tăng, nên chậm lại các quyết định lớn.",
        "Nên chọn lúc trao đổi thay vì đẩy quyết định gấp.",
    ),
    "sensitive": _e(
        "marriage.timing.sensitive",
        "Giai đoạn cần lưu ý nhịp",
        "Đây là điểm cần lưu ý về nhịp thời điểm, không phải lời đoán ngày.",
        "Lớp kích hoạt đang nhạy hơn mức thông thường.",
        "Hai người có thể thấy ma sát dễ lộ hơn nếu thiếu quy ước.",
        "Nên chậm quyết định lớn và giữ kênh trao đổi rõ.",
    ),
}

_ACTION: dict[str, NarrativeEntry] = {
    RecommendationType.REINFORCE_STRENGTH.value: _e(
        "marriage.action.reinforce_strength",
        "Củng cố điểm đang hỗ trợ",
        "Hành động này nhằm giữ vững phần đang nâng đỡ.",
        "Nguồn là khuyến nghị đã được kết từ nhận định cấu trúc, không phải lời khuyên chung.",
        "Khi được thực hiện đều, nền tảng hỗ trợ dễ được bảo toàn.",
        "Duy trì thói quen phối hợp đang hiệu quả.",
    ),
    RecommendationType.REDUCE_CONFLICT.value: _e(
        "marriage.action.reduce_conflict",
        "Giảm ma sát khi áp lực tăng",
        "Hành động này nhằm giảm xung đột đúng điểm đang căng.",
        "Mục tiêu là giữ ổn định, không phải kết luận chia tay hay gắn bó.",
        "Trong giai đoạn áp lực, quy ước rõ sẽ giảm ma sát thực tế.",
        "Thống nhất cách trao đổi trước khi quyết định lớn.",
    ),
    RecommendationType.ROLE_BALANCE.value: _e(
        "marriage.action.role_balance",
        "Chốt lại vai trò và ranh giới",
        "Hành động này nhằm làm rõ trách nhiệm của từng người.",
        "Nguồn là kết luận vai trò, không phải đánh giá tính cách.",
        "Phân vai rõ giúp việc chung ít chồng chéo hơn.",
        "Viết ra ai giữ phần nào trong các việc định kỳ.",
    ),
    RecommendationType.FINANCIAL_STRUCTURE.value: _e(
        "marriage.action.financial_structure",
        "Đặt quy ước tiền bạc chung",
        "Hành động này nhằm làm rõ ranh giới chi tiêu và trách nhiệm tài chính.",
        "Mục tiêu là giảm xung đột tiền bạc, không phải hứa hẹn giàu có.",
        "Khi có quyết định tài chính chung, quy ước sẵn sẽ giữ nhịp ổn.",
        "Thống nhất ngân sách và giới hạn chi trước việc lớn.",
    ),
    RecommendationType.TIMING_AWARENESS.value: _e(
        "marriage.action.timing_awareness",
        "Theo dõi nhịp thời điểm",
        "Hành động này nhằm nhận biết giai đoạn nhạy hoặc thuận hơn.",
        "Không đặt ngày cưới hay mốc sinh con mới.",
        "Nhịp thời điểm chỉ giúp chọn lúc trao đổi, không đổi nền tảng.",
        "Dùng giai đoạn nhạy để chậm lại quyết định lớn nếu cần.",
    ),
}

_CONDITION_RESCUED = "Điểm này có thể được giảm nếu các yếu tố hỗ trợ tiếp tục phát huy."
_LIMIT_HOUR = (
    "Giờ sinh chưa rõ nên một số nhận định liên quan trụ giờ được giữ ở mức tham khảo. "
    "Điều này không đồng nghĩa hôn nhân kém tương hợp."
)
_LIMIT_DOMAIN = "Phần này chưa đủ dữ liệu cấu trúc nên không đưa nhận định thay thế."
_CONFIDENCE = {
    "high": "Độ tin cậy của hồ sơ ở mức cao trên dữ liệu hiện có.",
    "medium": "Độ tin cậy ở mức trung bình. Một số phần nên đọc kèm giới hạn.",
    "reference_only": "Một phần kết quả chỉ mang tính tham khảo vì dữ liệu chưa đủ đầy.",
}


def overall_entry(state: str) -> NarrativeEntry:
    """Return the overall catalog entry for a decision state."""
    return _OVERALL[state]


def domain_title(domain: MarriageDomain) -> str:
    """Return the Vietnamese domain title."""
    return _DOMAIN_TITLE[domain.value]


def domain_entry(domain: MarriageDomain, state: str) -> NarrativeEntry | None:
    """Return a domain-state catalog entry when defined."""
    return _DOMAIN_STATE.get((domain.value, state))


def finding_entry(domain: MarriageDomain, finding_type: FindingType) -> NarrativeEntry | None:
    """Return a finding-class catalog entry when defined."""
    mapped = _map_finding_type(finding_type)
    if mapped is FindingType.MIXED:
        return _MIXED_FINDING
    return _FINDING.get((domain.value, mapped.value))


def timing_entry(state: str) -> NarrativeEntry:
    """Return timing-state wording. Never includes calendar dates."""
    return _TIMING_STATE[state]


def _map_finding_type(finding_type: FindingType) -> FindingType:
    """Collapse unused finding types onto catalog classes."""
    if finding_type is FindingType.STRENGTH:
        return FindingType.SUPPORT
    if finding_type is FindingType.BOTTLENECK:
        return FindingType.RISK
    return finding_type


def action_entry(action_type: RecommendationType) -> NarrativeEntry | None:
    """Return an action catalog entry when defined."""
    return _ACTION.get(action_type.value)


def rescued_sentence() -> str:
    """Return the condition-preservation sentence for rescued findings."""
    return _CONDITION_RESCUED


def limitation_hour() -> str:
    """Return the missing-hour limitation wording."""
    return _LIMIT_HOUR


def limitation_domain() -> str:
    """Return the unavailable-domain limitation wording."""
    return _LIMIT_DOMAIN


def confidence_sentence(level: str) -> str:
    """Return confidence wording for a canonical level."""
    return _CONFIDENCE[level]
