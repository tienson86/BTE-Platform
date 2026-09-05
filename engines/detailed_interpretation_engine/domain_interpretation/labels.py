"""Deterministic Domain Interpretation labels. Not DI-19 Narrative Composer."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import DomainState
from engines.detailed_interpretation_engine.evidence_priority.labels import (
    ACHIEVEMENT_LABELS,
    CAREER_LABELS,
    CLASSIFICATION_LABELS,
    DAMAGE_LABELS,
)

UNRESOLVED_COPY: str = "Chưa đủ dữ liệu để kết luận chi tiết"

DOMAIN_TITLES: dict[str, str] = {
    "authority": "Quyền hạn",
    "career": "Sự nghiệp",
    "wealth": "Tài vận",
    "relationship": "Quan hệ",
    "legacy": "Di sản",
    "vitality": "Sinh lực",
    "creative": "Sáng tạo",
    "academic": "Học thuật",
    "leadership": "Lãnh đạo",
    "management": "Quản trị",
    "learning": "Học hỏi",
    "personal_growth": "Phát triển",
}

STATE_LABELS: dict[str, str] = {
    DomainState.VERY_STRONG.value: "Rất mạnh",
    DomainState.STRONG.value: "Mạnh",
    DomainState.MODERATE.value: "Vừa",
    DomainState.WEAK.value: "Yếu",
    DomainState.CONDITIONAL.value: "Có điều kiện",
    DomainState.BLOCKED.value: "Chưa thể luận",
    DomainState.FRAGMENTED.value: "Phân mảnh",
    DomainState.UNRESOLVED.value: "Chưa đủ dữ liệu",
}

DIMENSION_LABELS: dict[str, str] = {
    "formal_authority": "Quyền hạn chính thức",
    "organizational_authority": "Quyền hạn tổ chức",
    "managerial_authority": "Quyền hạn quản trị",
    "command_authority": "Quyền hạn chỉ huy",
    "professional_authority": "Quyền hạn chuyên môn",
    "decision_authority": "Quyền quyết định",
    "authority_stability": "Ổn định quyền hạn",
    "authority_pressure": "Áp lực quyền hạn",
    "organizational_fit": "Phù hợp tổ chức",
    "autonomy_need": "Nhu cầu tự chủ",
    "leadership_fit": "Phù hợp lãnh đạo",
    "management_fit": "Phù hợp quản trị",
    "specialist_fit": "Phù hợp chuyên gia",
    "technical_fit": "Phù hợp kỹ thuật",
    "academic_fit": "Phù hợp học thuật",
    "creative_fit": "Phù hợp sáng tạo",
    "entrepreneurial_fit": "Phù hợp khởi nghiệp",
    "public_facing_fit": "Phù hợp đối ngoại",
    "career_stability": "Ổn định sự nghiệp",
    "career_pressure": "Áp lực sự nghiệp",
    "creation": "Tạo tài",
    "commercialization": "Thương mại hóa",
    "cashflow": "Dòng tiền",
    "retention": "Giữ tài",
    "accumulation": "Tích lũy",
    "expansion": "Mở rộng",
    "capital_discipline": "Kỷ luật vốn",
    "volatility": "Biến động",
    "wealth_sustainability": "Bền vững tài",
    "compatibility": "Tương hợp",
    "communication": "Giao tiếp",
    "trust": "Tin cậy",
    "commitment": "Cam kết",
    "relationship_support": "Năng lực nâng đỡ",
    "relationship_conflict": "Xung đột quan hệ",
    "independence": "Độc lập",
    "dependency": "Phụ thuộc",
    "mutual_growth": "Cùng phát triển",
    "relationship_resilience": "Bền bỉ quan hệ",
    "relationship_sustainability": "Bền vững quan hệ",
    "biological_legacy": "Di sản huyết thống",
    "family_legacy": "Di sản gia tộc",
    "knowledge_legacy": "Di sản tri thức",
    "creative_legacy": "Di sản sáng tạo",
    "business_legacy": "Di sản doanh nghiệp",
    "community_legacy": "Di sản cộng đồng",
    "institutional_legacy": "Di sản tổ chức",
    "spiritual_legacy": "Di sản tinh thần",
    "legacy_sustainability": "Bền vững di sản",
    "legacy_visibility": "Tầm nhìn di sản",
    "capacity": "Sức chứa",
    "stress": "Áp lực",
    "recovery": "Phục hồi",
    "resilience": "Bền bỉ",
    "health_expression": "Biểu hiện sức khỏe",
    "energy_efficiency": "Hiệu suất năng lượng",
    "energy_stability": "Ổn định năng lượng",
    "fatigue_risk": "Rủi ro mệt mỏi",
    "burnout_risk": "Rủi ro kiệt sức",
}

RISK_LABELS: dict[str, str] = {
    "authority_conflict": "Xung đột quyền hạn",
    "pressure_overload": "Quá tải áp lực quyền hạn",
    "role_mismatch": "Lệch vai trò",
    "management_gap": "Thiếu lớp vận hành",
    "poor_retention": "Giữ tài yếu",
    "high_volatility": "Biến động tài cao",
    "communication_gap": "Khe hở giao tiếp",
    "trust_gap": "Khe hở tin cậy",
    "transmission_gap": "Khe hở truyền thừa",
    "poor_recovery": "Phục hồi yếu",
    "stress_overload": "Quá tải căng thẳng",
}

OPPORTUNITY_LABELS: dict[str, str] = {
    "academic_capacity": "Năng lực học thuật",
    "knowledge_conversion": "Chuyển tri thức thành việc",
    "management_capacity": "Năng lực quản trị",
    "leadership_capacity": "Năng lực dẫn dắt",
    "retention_strength": "Năng lực giữ và tích lũy",
    "creation_capacity": "Năng lực tạo giá trị",
    "professional_authority": "Uy tín chuyên môn",
    "knowledge_legacy": "Truyền tri thức",
    "recovery_discipline": "Kỷ luật phục hồi",
}

CONDITION_LABELS: dict[str, str] = {
    "requires_operational_systems": "Cần hệ thống vận hành/hỗ trợ",
    "requires_output_release": "Cần kênh biểu đạt để giải phóng khí thừa",
    "requires_retention_discipline": "Cần kỷ luật giữ tài",
    "requires_structural_integrity": "Cần giữ toàn vẹn cấu trúc chính",
    "requires_communication_support": "Cần khung giao tiếp rõ",
    "requires_recovery_space": "Cần không gian phục hồi",
}

DRIVER_LABELS: dict[str, str] = {
    "zheng_guan_primary": "Chính Quan",
    "qi_sha_yin_chain": "Sát → Ấn",
    "cai_sheng_guan": "Tài sinh Quan",
    "guan_yin_chain": "Quan → Ấn",
    "management_structure": "Cấu trúc quản trị",
    "professional_authority": "Uy tín chuyên môn",
    "mixed": "Cơ chế hỗn hợp",
    "authority_management": "Quản trị / quyền hạn",
    "entrepreneurship": "Khởi nghiệp",
    "technical_specialization": "Chuyên môn kỹ thuật",
    "academic_depth": "Chiều sâu học thuật",
    "creative_output": "Đầu ra sáng tạo",
    "commercial_chain": "Chuỗi thương mại",
    "public_visibility": "Tầm nhìn công chúng",
    "hybrid": "Cơ chế hỗn hợp",
    "output": "Đầu ra tạo tài",
    "commercial": "Thương mại",
    "authority": "Tài từ quyền hạn",
    "technical": "Kỹ thuật",
    "creative": "Sáng tạo",
    "management": "Quản trị",
    "compatibility": "Tương hợp",
    "trust": "Tin cậy",
    "communication": "Giao tiếp",
    "commitment": "Cam kết",
    "shared_growth": "Cùng phát triển",
    "mutual_support": "Nâng đỡ lẫn nhau",
    "teaching": "Dạy học",
    "knowledge": "Tri thức / học thuật",
    "business": "Doanh nghiệp",
    "family": "Gia tộc",
    "community": "Cộng đồng",
    "capacity": "Sức chứa",
    "recovery": "Phục hồi",
    "resilience": "Bền bỉ",
    "energy": "Năng lượng",
}

PRESSURE_LABELS: dict[str, str] = {
    "elevated": "Tăng",
    "moderate": "Vừa",
    "low": "Thấp",
}

SUMMARY_TEMPLATES: dict[tuple[str, str], str] = {
    ("authority", DomainState.MODERATE.value): (
        "Năng lực gánh trách nhiệm khá rõ; điểm cần kiểm soát là áp lực quyền hạn."
    ),
    ("authority", DomainState.CONDITIONAL.value): (
        "Năng lực gánh trách nhiệm khá rõ; điểm cần kiểm soát là áp lực quyền hạn."
    ),
    ("authority", DomainState.STRONG.value): (
        "Năng lực gánh trách nhiệm khá rõ; điểm cần kiểm soát là áp lực quyền hạn."
    ),
    ("wealth", DomainState.FRAGMENTED.value): (
        "Năng lực giữ/tích lũy tốt hơn khả năng tạo tiền nhanh."
    ),
    ("wealth", DomainState.CONDITIONAL.value): (
        "Năng lực giữ/tích lũy tốt hơn khả năng tạo tiền nhanh."
    ),
    ("career", DomainState.CONDITIONAL.value): (
        "Hướng học thuật và quản trị rõ; cần lớp vận hành để trách nhiệm không bị lệch vai."
    ),
    ("career", DomainState.STRONG.value): (
        "Hướng học thuật và quản trị rõ; cần lớp vận hành để trách nhiệm không bị lệch vai."
    ),
    ("career", DomainState.MODERATE.value): (
        "Hướng học thuật và quản trị rõ; cần lớp vận hành để trách nhiệm không bị lệch vai."
    ),
    ("legacy", DomainState.MODERATE.value): (
        "Di sản nghiêng về tri thức và học thuật hơn là truyền huyết thống."
    ),
    ("legacy", DomainState.STRONG.value): (
        "Di sản nghiêng về tri thức và học thuật hơn là truyền huyết thống."
    ),
    ("legacy", DomainState.CONDITIONAL.value): (
        "Di sản nghiêng về tri thức và học thuật hơn là truyền huyết thống."
    ),
    ("vitality", DomainState.CONDITIONAL.value): (
        "Sức chứa còn, nhưng phục hồi và giải tỏa áp lực là điểm cần giữ."
    ),
    ("vitality", DomainState.MODERATE.value): (
        "Sức chứa còn, nhưng phục hồi và giải tỏa áp lực là điểm cần giữ."
    ),
    ("vitality", DomainState.FRAGMENTED.value): (
        "Sức chứa còn, nhưng phục hồi và giải tỏa áp lực là điểm cần giữ."
    ),
}


def classification_label(value: str) -> str:
    """Map an MC-01 band onto a customer word."""
    return CLASSIFICATION_LABELS.get(value, PRESSURE_LABELS.get(value, value))


def capability_label(value: str) -> str:
    """Map an achievement or career code onto a customer word."""
    return ACHIEVEMENT_LABELS.get(value, CAREER_LABELS.get(value, value))


def damage_label(value: str) -> str:
    """Reuse frozen damage labels."""
    return DAMAGE_LABELS.get(value, value)
