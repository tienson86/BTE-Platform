"""Customer presentation mapping for Shen Sha. No new analytical conclusions."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.enums import (
    ShenShaClusterState,
    ShenShaModifierState,
)
from engines.detailed_interpretation_engine.shen_sha.constants import (
    CATEGORY_DISPLAY_NAMES,
    CLUSTER_DISPLAY_NAMES,
    CLUSTER_RISK,
    STAR_DISPLAY_NAMES,
)
from engines.detailed_interpretation_engine.shen_sha.models import (
    ShenShaClusterResult,
    ShenShaEcosystemResult,
    ShenShaInterpretationCollection,
    ShenShaInterpretationResult,
)

UNRESOLVED_COPY = "Chưa đủ dữ liệu cấu trúc để kết luận."

STATE_LABELS: dict[str, str] = {
    ShenShaModifierState.APPLIED.value: "Hỗ trợ",
    ShenShaModifierState.WEAK_SUPPORT.value: "Hỗ trợ",
    ShenShaModifierState.QUALIFIED.value: "Điều kiện",
    ShenShaModifierState.WARNING.value: "Cảnh báo",
    ShenShaModifierState.BLOCKED.value: "Chưa đủ dữ liệu",
    ShenShaModifierState.INACTIVE.value: "Chưa đủ dữ liệu",
    ShenShaModifierState.UNRESOLVED.value: "Chưa đủ dữ liệu",
}

STAR_COPY: dict[tuple[str, str], str] = {
    ("hua_gai", "applied"): (
        "Hoa Cái bổ sung tín hiệu cho khuynh hướng sáng tạo/nghiên cứu khi nền tảng cấu trúc tương ứng đã có."
    ),
    ("hua_gai", "qualified"): (
        "Hoa Cái chỉ là tín hiệu hỗ trợ có điều kiện; không tạo phân loại sáng tạo."
    ),
    ("hua_gai", "blocked"): (
        "Hoa Cái không đủ điều kiện cấu trúc để kết luận khuynh hướng nghệ sĩ hay sáng tạo cao."
    ),
    ("hua_gai", "unresolved"): (
        "Hoa Cái hiện chỉ là tín hiệu hỗ trợ; chưa đủ dữ liệu cấu trúc để kết luận khuynh hướng sáng tạo."
    ),
    ("guo_yin", "applied"): (
        "Quốc Ấn bổ sung độ tin cậy cho chủ đề quyền hạn khi nền tảng cấu trúc đã có."
    ),
    ("guo_yin", "blocked"): (
        "Quốc Ấn không nâng kết luận quyền hạn khi nền tảng cấu trúc còn thấp hoặc vắng."
    ),
    ("guo_yin", "unresolved"): (
        "Quốc Ấn hiện chỉ là tín hiệu hỗ trợ; chưa đủ dữ liệu cấu trúc để nâng kết luận về quyền hạn."
    ),
    ("tian_yi", "applied"): (
        "Thiên Ất bổ sung tín hiệu hỗ trợ bên ngoài khi nền tảng quyền hạn/công việc đã có."
    ),
    ("tian_yi", "blocked"): (
        "Thiên Ất không đồng nghĩa luôn có quý nhân; thiếu nền tảng cấu trúc nên không kết luận."
    ),
    ("tian_yi", "unresolved"): (
        "Thiên Ất là tín hiệu hỗ trợ; chưa đủ dữ liệu cấu trúc để khẳng định quý nhân."
    ),
    ("hong_luan", "applied"): (
        "Hồng Loan bổ sung tín hiệu duyên gặp gỡ khi hồ sơ quan hệ cấu trúc đã có."
    ),
    ("hong_luan", "blocked"): (
        "Hồng Loan không đủ điều kiện để kết luận hôn nhân tốt hay chất lượng quan hệ."
    ),
    ("hong_luan", "unresolved"): (
        "Hồng Loan chưa đủ dữ liệu cấu trúc để luận về quan hệ hay hôn nhân."
    ),
    ("tian_xi", "applied"): (
        "Thiên Hỷ bổ sung tín hiệu vui trong quan hệ khi nền tảng cấu trúc đã có."
    ),
    ("tian_xi", "blocked"): (
        "Thiên Hỷ không phải sự kiện hôn nhân; thiếu nền tảng quan hệ nên không kết luận."
    ),
    ("tian_xi", "unresolved"): (
        "Thiên Hỷ chưa đủ dữ liệu cấu trúc; không dùng để đoán sự kiện hôn nhân."
    ),
    ("yang_ren", "warning"): (
        "Dương Nhẫn là tín hiệu cảnh báo cạnh tranh/áp lực, không phải tai họa định sẵn."
    ),
    ("khong_vong", "warning"): (
        "Không Vong là tín hiệu cần thận trọng, không đồng nghĩa tai họa."
    ),
    ("khong_vong", "unresolved"): (
        "Không Vong hiện chỉ là tín hiệu phụ; không kết luận tai họa."
    ),
    ("co_than", "warning"): (
        "Cô Thần là tín hiệu cảnh báo khoảng cách, không kết luận thất bại quan hệ."
    ),
    ("co_than", "unresolved"): (
        "Cô Thần chưa đủ dữ liệu cấu trúc; không kết luận cô độc hay thất bại quan hệ."
    ),
    ("qua_tu", "warning"): (
        "Quả Tú là tín hiệu cảnh báo khoảng cách, không kết luận thất bại quan hệ."
    ),
    ("qua_tu", "unresolved"): (
        "Quả Tú chưa đủ dữ liệu cấu trúc; không kết luận cô độc hay thất bại quan hệ."
    ),
    ("wen_chang", "applied"): (
        "Văn Xương bổ sung tín hiệu học thuật khi nền tảng học/nghiên cứu đã có."
    ),
    ("wen_chang", "unresolved"): (
        "Văn Xương là tín hiệu hỗ trợ học thuật; chưa đủ dữ liệu cấu trúc để kết luận."
    ),
    ("lu_shen", "applied"): (
        "Lộc Thần bổ sung tín hiệu cơ hội nguồn lực khi hồ sơ tài đã có."
    ),
    ("lu_shen", "unresolved"): (
        "Lộc Thần không đồng nghĩa đã giàu; chưa đủ dữ liệu cấu trúc tài."
    ),
    ("tian_de", "applied"): (
        "Thiên Đức bổ sung tín hiệu nâng đỡ khi đã có cấu trúc cần bảo vệ."
    ),
    ("tian_de", "unresolved"): (
        "Thiên Đức là tín hiệu hỗ trợ/phục hồi; chưa đủ dữ liệu cấu trúc để kết luận."
    ),
    ("yue_de", "applied"): (
        "Nguyệt Đức bổ sung tín hiệu nâng đỡ khi đã có cấu trúc cần bảo vệ."
    ),
    ("yue_de", "unresolved"): (
        "Nguyệt Đức là tín hiệu hỗ trợ/phục hồi; chưa đủ dữ liệu cấu trúc để kết luận."
    ),
}

GENERIC_COPY: dict[str, str] = {
    "applied": "Đây là tín hiệu hỗ trợ cho chủ đề cấu trúc đã có, không tạo kết luận mới.",
    "weak_support": "Tín hiệu hỗ trợ yếu; không nâng phân loại cấu trúc.",
    "qualified": "Tín hiệu có điều kiện; cần đủ nền tảng cấu trúc mới được dùng.",
    "warning": "Tín hiệu cảnh báo bổ sung, không phải sự kiện xấu định sẵn.",
    "blocked": "Thiếu nền tảng cấu trúc nên thần sát này không được dùng để kết luận.",
    "inactive": UNRESOLVED_COPY,
    "unresolved": UNRESOLVED_COPY,
}

PILLAR_LABELS: dict[str, str] = {
    "year": "Năm",
    "month": "Tháng",
    "day": "Ngày",
    "hour": "Giờ",
}


def _star_name(star_id: str) -> str:
    return STAR_DISPLAY_NAMES.get(star_id, "")


def _category_label(categories: tuple[str, ...]) -> str:
    labels = [CATEGORY_DISPLAY_NAMES[item] for item in categories if item in CATEGORY_DISPLAY_NAMES]
    return " · ".join(dict.fromkeys(labels))


def _placement(item: ShenShaInterpretationResult) -> str:
    pillars = []
    for position in item.positions:
        label = PILLAR_LABELS.get(position.pillar, "")
        if label and label not in pillars:
            pillars.append(label)
    return " · ".join(f"Trụ {item}" for item in pillars)


def _explanation(item: ShenShaInterpretationResult) -> str:
    key = item.modifier_state.value
    mapped = STAR_COPY.get((item.shen_sha_id, key))
    if mapped:
        return mapped
    if key == "qualified":
        mapped = STAR_COPY.get((item.shen_sha_id, "unresolved"))
        if mapped:
            return mapped
    return GENERIC_COPY.get(key, UNRESOLVED_COPY)


def present_shen_sha_item(item: ShenShaInterpretationResult) -> dict[str, Any]:
    """Customer-safe star row. No IDs or traces."""
    return {
        "name": _star_name(item.shen_sha_id),
        "category": _category_label(item.categories),
        "state_label": STATE_LABELS.get(item.modifier_state.value, "Chưa đủ dữ liệu"),
        "placement": _placement(item),
        "explanation": _explanation(item),
        "unresolved": item.modifier_state.value in {"unresolved", "blocked", "inactive"},
        "warning": item.modifier_state is ShenShaModifierState.WARNING,
    }


def present_shen_sha_customer(collection: ShenShaInterpretationCollection) -> dict[str, Any]:
    """Customer projection of interpreted stars."""
    return {
        "state": collection.state.value,
        "items": [present_shen_sha_item(item) for item in collection.items if item.detected],
    }


def _cluster_blurb(cluster: ShenShaClusterResult) -> str:
    name = CLUSTER_DISPLAY_NAMES.get(cluster.cluster_id, "")
    if cluster.state is ShenShaClusterState.UNRESOLVED:
        return f"{name} chưa đủ dữ liệu cấu trúc để thành nhóm luận giải."
    if cluster.state is ShenShaClusterState.BLOCKED:
        return f"{name} bị chặn vì thiếu nền tảng cấu trúc; không tạo kết luận."
    if cluster.cluster_id == CLUSTER_RISK:
        return f"{name} chỉ là nhóm cảnh báo phụ, không phải sự kiện xấu định sẵn."
    if cluster.state is ShenShaClusterState.CONDITIONAL:
        return f"{name} đang ở trạng thái có điều kiện; không nâng phân loại cấu trúc."
    return f"{name} bổ sung độ tin cậy cho chủ đề đã có, không tạo phân loại mới."


def _present_cluster(cluster: ShenShaClusterResult) -> dict[str, Any]:
    return {
        "name": CLUSTER_DISPLAY_NAMES.get(cluster.cluster_id, ""),
        "state_label": {
            "active": "Hỗ trợ",
            "conditional": "Điều kiện",
            "blocked": "Chưa đủ điều kiện",
            "unresolved": "Chưa đủ dữ liệu",
            "inactive": "Không hiện",
        }.get(cluster.state.value, "Chưa đủ dữ liệu"),
        "explanation": _cluster_blurb(cluster),
        "warning": cluster.cluster_id == CLUSTER_RISK,
        "unresolved": cluster.state.value in {"unresolved", "blocked", "inactive"},
        "prominent": cluster.state in {
            ShenShaClusterState.ACTIVE,
            ShenShaClusterState.CONDITIONAL,
        }
        or cluster.cluster_id == CLUSTER_RISK and bool(cluster.members),
    }


def present_shen_sha_ecosystem_customer(result: ShenShaEcosystemResult) -> dict[str, Any]:
    """Customer projection of Hệ Thần Sát. No IDs or traces."""
    lookup = {item.cluster_id: item for item in result.clusters}
    prominent = [_present_cluster(item) for item in result.clusters if _present_cluster(item)["prominent"]]
    dominant_unresolved = not result.dominant_cluster
    dominant_name = CLUSTER_DISPLAY_NAMES.get(result.dominant_cluster, "")
    supporting_name = CLUSTER_DISPLAY_NAMES.get(result.supporting_cluster, "")
    risk = lookup.get(CLUSTER_RISK)
    return {
        "state": result.state.value,
        "dominant": "Chưa đủ dữ liệu" if dominant_unresolved else dominant_name,
        "dominant_unresolved": dominant_unresolved,
        "supporting": supporting_name,
        "warning": CLUSTER_DISPLAY_NAMES[CLUSTER_RISK] if risk and risk.members else "",
        "unresolved_label": "Chưa đủ điều kiện" if dominant_unresolved else "",
        "clusters": prominent,
    }
