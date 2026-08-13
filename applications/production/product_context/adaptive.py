"""Adaptive delivery frames — audience packaging only, no claim rewrite."""

from __future__ import annotations

from applications.production.interpretation.cross_domain.models import (
    CrossDomainReasoningResult,
)
from applications.production.product_context.models import (
    ActionProfile,
    LifeStage,
    ProductContextResult,
)

# Frozen replacement table: adult consulting frame → child/parent delivery frame.
REPLACEMENTS: tuple[tuple[str, str, str], ...] = (
    ("adult_consulting", "development_guidance", "Tư vấn nghề người lớn → định hướng phát triển"),
    ("self_language", "parent_language", "Xưng hô 'bạn = chủ thể tự quyết' → phụ huynh / con"),
    ("career", "development", "Career Decision → nuôi dưỡng phát triển"),
    ("business", "learning", "Kinh doanh / mở rộng → học tập"),
    ("leadership", "confidence", "Lãnh đạo / quyền quyết → xây tự tin"),
)


def is_weak_capacity(reasoning: CrossDomainReasoningResult) -> bool:
    """Read published capacity from claim plan — do not infer new truth."""
    core = reasoning.executive_claim_plan.identity_core or ""
    return "weak" in core.lower() or "body:weak" in core.lower()


def development_operating_frame(theme: str) -> str:
    """Map operating theme to child development language."""
    if theme == "OPERATING_OUTPUT":
        return (
            "Con có nhu cầu được làm ra / thể hiện và nhận phản hồi rõ. "
            "Đây là nhu cầu học tập và xây tự tin — không phải áp lực thành tích "
            "hay vai trò lãnh đạo người lớn."
        )
    if theme == "OPERATING_SELF_CARRY":
        return (
            "Con dễ tự nhận việc và tự đẩy. Người lớn nên giúp chia việc nhỏ, "
            "không để con ôm hết để chứng minh."
        )
    return (
        "Nuôi dưỡng đúng kênh vận hành đã công bố, với biên phù hợp độ tuổi — "
        "không dịch thành tư vấn nghề người lớn."
    )


def learning_environment(theme: str) -> str:
    """Business/career environment → learning environment."""
    if theme == "OPERATING_OUTPUT":
        return (
            "Môi trường học tập hợp hơn khi con được làm ra thứ nhỏ, "
            "được phản hồi ấm và đúng việc — không phải sân cạnh tranh người lớn "
            "hay chỗ chỉ đo bằng hiện diện."
        )
    return (
        "Môi trường học tập hợp hơn khi nhịp nhẹ, rõ việc, và người lớn đứng cạnh — "
        "không giao con tự quyết như người lớn."
    )


def confidence_building(theme: str) -> str:
    """Leadership frame → confidence building."""
    if theme == "OPERATING_OUTPUT":
        return (
            "Xây tự tin bằng việc hoàn thành nhỏ rồi được nhìn thấy — "
            "không giao 'vai trò lãnh đạo' hay quyền quyết người lớn."
        )
    if theme == "OPERATING_SELF_CARRY":
        return (
            "Xây tự tin bằng việc con biết khi nào được nhờ người lớn — "
            "không khen việc ôm hết một mình."
        )
    return "Xây tự tin bằng bước nhỏ có người lớn đi cùng."


def conservation_line(weak: bool) -> str:
    """Capacity truth → child conservation, not adult load coaching."""
    if weak:
        return (
            "Nền của con đang cần bảo toàn: ưu tiên nghỉ, lịch nhẹ, "
            "không chất thêm lớp hay hoạt động để 'chứng minh'."
        )
    return (
        "Nền năng lượng cần nhịp đều: giữ học–chơi–nghỉ rõ, "
        "tránh dồn thành tích ngắn hạn."
    )


def parent_actions(
    *,
    theme: str,
    weak: bool,
    action_profile: ActionProfile,
) -> list[str]:
    """Adult self-actions → parent accompaniment actions."""
    actions = [
        "Tạo góc học / chơi có sản phẩm nhỏ và phản hồi ấm — đây là học tập, không phải kinh doanh.",
        confidence_building(theme),
        "Không dùng báo cáo này để chọn nghề, mở hướng kinh doanh, hoặc timing hôn nhân.",
    ]
    if weak:
        actions.insert(
            1,
            "Bảo toàn năng lượng trước khi thêm hoạt động: nghỉ đủ, lịch thưa, không ép tuần làm việc người lớn.",
        )
    else:
        actions.insert(
            1,
            "Giữ biên hoạt động vừa sức độ tuổi — không dịch thành điều phối tuần làm việc người lớn.",
        )
    if action_profile == ActionProfile.PARENT_ACTIONS:
        return [f"Phụ huynh: {item}" for item in actions]
    return actions


def parent_who(context: ProductContextResult) -> str:
    """Self-report opening → parent-reader opening."""
    age = (
        f" (khoảng {context.subject_age} tuổi)"
        if context.subject_age is not None
        else ""
    )
    return (
        f"Phụ huynh đang đọc nhận diện phát triển của con{age}. "
        "Đây không phải tư vấn tự quyết của người lớn."
    )


def conflict_nuance(reasoning: CrossDomainReasoningResult) -> str:
    """Keep unresolved truth, speak to caregiver."""
    if not (reasoning.tensions or reasoning.conflicts):
        return ""
    return (
        "Có điểm cần đọc có điều kiện giữa các lớp phân tích — "
        "phụ huynh giữ cả hai tín hiệu, không gắn một nhãn duy nhất cho con."
    )


def stage_is_adaptive(context: ProductContextResult) -> bool:
    """Whether delivery must adapt (not adult pass-through)."""
    return context.life_stage in {LifeStage.CHILD, LifeStage.TEEN} or not context.pass_through
