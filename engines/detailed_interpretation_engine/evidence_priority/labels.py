"""Customer-safe labels for ranked evidence. No IDs or traces."""

from __future__ import annotations

from engines.detailed_interpretation_engine.shen_sha.constants import (
    CLUSTER_DISPLAY_NAMES,
    STAR_DISPLAY_NAMES,
)
from engines.detailed_interpretation_engine.ten_gods.constants import GOD_ID_TO_LABEL
from engines.detailed_interpretation_engine.ten_gods.presentation import (
    COMBINATION_NAMES,
    SUBJECT_LABELS,
)

DAMAGE_LABELS: dict[str, str] = {
    "resource_overload": "Ấn quá vượng kìm biểu đạt",
    "peer_robs_wealth": "Tỷ Kiếp đoạt Tài",
    "hurting_officer_attacks_officer": "Thương Quan kiến Quan",
    "owl_robs_food": "Kiêu Thần đoạt Thực",
    "wealth_overloads_weak_day_master": "Tài nhiều Thân nhược",
    "killer_overloads_weak_day_master": "Sát mạnh Thân nhược",
    "mixed_officer_killer": "Quan Sát hỗn tạp",
}

RESCUE_LABELS: dict[str, str] = {
    "output_releases_excess": "Thực Thương giải phóng khí thừa",
    "resource_mediates_killer": "Ấn hóa Sát",
    "officer_controls_output": "Quan chế Thương",
    "peer_supports_day_master": "Tỷ Kiếp nâng Nhật Chủ",
}

ACHIEVEMENT_LABELS: dict[str, str] = {
    "academic": "Học thuật",
    "entrepreneurship": "Khởi nghiệp",
    "management": "Quản trị",
    "authority": "Quyền hạn",
    "creative": "Sáng tạo",
}

WEALTH_LABELS: dict[str, str] = {
    "wealth_creation": "Tạo tài",
    "wealth_accumulation": "Tích lũy",
    "wealth_retention": "Giữ tài",
    "wealth_volatility": "Biến động tài",
}

CAREER_LABELS: dict[str, str] = {
    "academic_research": "Nghiên cứu học thuật",
    "managerial": "Quản lý",
    "leadership_command": "Lãnh đạo",
    "entrepreneurship": "Khởi nghiệp",
    "institutional_fit": "Phù hợp tổ chức",
}

CLASSIFICATION_LABELS: dict[str, str] = {
    "very_high": "rất mạnh",
    "high": "mạnh",
    "above_average": "khá",
    "average": "vừa",
    "below_average": "yếu",
    "low": "yếu",
    "very_low": "rất yếu",
}

INTEGRITY_LABELS: dict[str, str] = {
    "complete": "Toàn vẹn",
    "substantially_complete": "Gần toàn vẹn",
    "conditionally_complete": "Toàn vẹn có điều kiện",
    "mixed": "Hỗn hợp",
    "damaged_but_rescued": "Tổn thương đã cứu",
    "damaged": "Tổn thương",
    "failed": "Không giữ được",
}

CONDITION_LABELS: dict[str, str] = {
    "resource_overload": "Cần Thực Thương giải phóng khí thừa",
    "output_releases_excess": "Giữ Thực Thương để giải tỏa Ấn",
    "mixed": "Cần giữ cấu trúc chính, hạn chế pha tạp",
    "integrity_must_hold": "Cần giữ toàn vẹn cấu trúc chính",
    "luck_activation_required": "Cần vận khí kích hoạt đúng chỗ",
}


def god_label(god_id: str, fallback: str = "") -> str:
    """Map a Ten God id or Vietnamese name to a customer label."""
    token = (god_id or "").strip()
    return GOD_ID_TO_LABEL.get(token) or SUBJECT_LABELS.get(token) or fallback or token


def damage_label(damage_type: str, fallback: str = "") -> str:
    """Map an MC-01 damage type to a short customer label."""
    token = (damage_type or "").strip()
    return DAMAGE_LABELS.get(token) or fallback or "Tổn thương cấu trúc"


def rescue_label(rescue_type: str, fallback: str = "") -> str:
    """Map an MC-01 rescue type to a short customer label."""
    token = (rescue_type or "").strip()
    return RESCUE_LABELS.get(token) or fallback or "Cứu giải cấu trúc"


def combination_label(combination_id: str) -> str:
    """Map a combination id to its published Vietnamese name."""
    return COMBINATION_NAMES.get(combination_id, "")


def cluster_label(cluster_id: str) -> str:
    """Map a Shen Sha cluster id to its published name."""
    return CLUSTER_DISPLAY_NAMES.get(cluster_id, "")


def star_label(star_id: str) -> str:
    """Map a Shen Sha star id to its published name."""
    return STAR_DISPLAY_NAMES.get(star_id, "")


def profile_label(dimension: str, classification: str) -> str:
    """Join a profile dimension with its band, without IDs."""
    name = (
        WEALTH_LABELS.get(dimension)
        or CAREER_LABELS.get(dimension)
        or ACHIEVEMENT_LABELS.get(dimension)
        or dimension
    )
    band = CLASSIFICATION_LABELS.get(classification, classification)
    if name and band:
        return f"{name} {band}"
    return name or band
