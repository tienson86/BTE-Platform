"""Deterministic customer labels. Presentation mapping only. No new decisions."""

from __future__ import annotations

from consulting.marriage.models.enums import (
    CanonicalGender,
    ConfidenceLevel,
    DomainDecisionState,
    MarriageDomain,
    RecommendationPriority,
)

GENDER_DISPLAY = {
    CanonicalGender.MALE: "Nam",
    CanonicalGender.FEMALE: "Nữ",
}

OVERALL_STATE_LABEL = {
    DomainDecisionState.SUPPORTIVE: "Tương hợp tốt",
    DomainDecisionState.BALANCED: "Cân bằng",
    DomainDecisionState.MIXED: "Hỗn hợp",
    DomainDecisionState.PRESSURED: "Có nhiều điểm cần lưu ý",
    DomainDecisionState.CRITICAL: "Cần thận trọng",
    DomainDecisionState.INSUFFICIENT: "Chưa đủ dữ liệu",
}

OVERALL_STATE_HEADLINE = {
    DomainDecisionState.SUPPORTIVE: "Tương hợp tốt",
    DomainDecisionState.BALANCED: "Nền tảng tương đối cân bằng",
    DomainDecisionState.MIXED: "Có điểm thuận và điểm cần điều chỉnh",
    DomainDecisionState.PRESSURED: "Có nhiều điểm cần lưu ý",
    DomainDecisionState.CRITICAL: "Cần thận trọng với các điểm then chốt",
    DomainDecisionState.INSUFFICIENT: "Chưa đủ dữ liệu để kết luận tổng thể",
}

CONFIDENCE_LABEL = {
    ConfidenceLevel.HIGH: "Độ tin cậy cao",
    ConfidenceLevel.MEDIUM: "Khá tin cậy",
    ConfidenceLevel.REFERENCE_ONLY: "Mang tính tham khảo",
}

PRIORITY_LABEL = {
    RecommendationPriority.CRITICAL: "Then chốt",
    RecommendationPriority.HIGH: "Ưu tiên cao",
    RecommendationPriority.MEDIUM: "Nên thực hiện",
    RecommendationPriority.LOW: "Tham khảo / bổ trợ",
    RecommendationPriority.REFERENCE: "Tham khảo / bổ trợ",
}

DOMAIN_TITLE = {
    MarriageDomain.FIVE_ELEMENTS: "Ngũ hành",
    MarriageDomain.STEM_BRANCH: "Can Chi",
    MarriageDomain.TEN_GODS: "Thập thần",
    MarriageDomain.INTERACTION: "Tương tác",
    MarriageDomain.FINANCE: "Tài chính",
    MarriageDomain.FAMILY: "Gia đình",
    MarriageDomain.CHILDREN: "Con cái",
    MarriageDomain.LUCK: "Nhịp thời điểm",
    MarriageDomain.OVERALL: "Tổng thể",
}

OPTIONAL_DOMAINS = (
    MarriageDomain.INTERACTION,
    MarriageDomain.FAMILY,
    MarriageDomain.CHILDREN,
)

SEMANTIC_UNAVAILABLE = ""
