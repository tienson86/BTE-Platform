"""Runtime catalog for Commercial Theme Library V1.0 — read-only hook.

Source of truth remains knowledge/commercial_theme_library/.
This module is the runtime projection used by Report Engine V2.
"""

from __future__ import annotations

from dataclasses import dataclass, field

THEME_LIBRARY_VERSION = "1.0.0"

OPERATING_THEMES = frozenset(
    {
        "OPERATING_SELF_CARRY",
        "OPERATING_OUTPUT",
        "OPERATING_STANDARDS",
        "BALANCE_DIRECTION",
    }
)

OVERLAY_THEMES = frozenset(
    {
        "CONSERVING",
        "TENSION_HOLDER",
        "FOLLOW_FRAME",
        "STABILIZER",
    }
)

ALIASES: dict[str, str] = {
    "CREATOR": "OPERATING_OUTPUT",
    "OVER_CARRIER": "OPERATING_SELF_CARRY",
    "SPECIAL_STRUCTURE": "FOLLOW_FRAME",
    "FOLLOW_STRUCTURE": "FOLLOW_FRAME",
    "CAPACITY_WEAK": "CONSERVING",
    "THEME_CAPACITY_WEAK": "CONSERVING",
    "THEME_FOLLOW_STRUCTURE": "FOLLOW_FRAME",
    "THEME_OPERATING_OUTPUT": "OPERATING_OUTPUT",
    "THEME_OPERATING_SELF_CARRY": "OPERATING_SELF_CARRY",
    "THEME_OPERATING_STANDARDS": "OPERATING_STANDARDS",
    "THEME_BALANCE_DIRECTION": "BALANCE_DIRECTION",
}

BLOCK_IDS: tuple[str, ...] = (
    "identity",
    "career",
    "relationship",
    "growth",
    "stress",
    "leadership",
    "environment",
    "memory",
    "action",
)

# Feature section id → theme block (SECTION_MAPPING.md).
IDENTITY_BLOCK_MAP: dict[str, str] = {
    "WHO": "identity",
    "OPERATING": "identity",
    "STRENGTHS": "growth",
    "BLIND_SPOTS": "stress",
    "PRESSURE": "stress",
    "ENVIRONMENT": "environment",
    "LESSON": "memory",
    "ACTIONS": "action",
    "SUMMARY": "memory",
    "CONDITION": "stress",
}

CAREER_BLOCK_MAP: dict[str, str] = {
    "WORK_STYLE": "career",
    "ENVIRONMENT": "environment",
    "POSTURE": "leadership",
    "PRESSURE": "stress",
    "BALANCE": "action",
    "RISK": "stress",
    "FOCUS": "action",
    "AVOIDS": "action",
    "SUMMARY": "memory",
    "CONDITION": "stress",
}

EXECUTIVE_BLOCK_MAP: dict[str, str] = {
    "WHO": "identity",
    "SYSTEM": "identity",
    "SUPPORTS": "growth",
    "LIMITS": "stress",
    "DIRECTION": "action",
    "INSIGHT": "memory",
    "PRIORITIES": "action",
    "AVOIDS": "action",
    "CONCLUSION": "memory",
    "LEARNING": "growth",
    "CONFIDENCE": "growth",
    "CAPACITY": "stress",
}


@dataclass(slots=True)
class ThemeRecord:
    """One library theme."""

    theme_id: str
    kind: str
    customer_name: str
    job: str
    never: str
    blocks: dict[str, str] = field(default_factory=dict)


def _theme(
    theme_id: str,
    kind: str,
    customer_name: str,
    job: str,
    never: str,
    blocks: dict[str, str],
) -> ThemeRecord:
    return ThemeRecord(
        theme_id=theme_id,
        kind=kind,
        customer_name=customer_name,
        job=job,
        never=never,
        blocks=blocks,
    )


def build_catalog() -> dict[str, ThemeRecord]:
    """Return the frozen V1.0 theme catalog."""
    return {
        "OPERATING_SELF_CARRY": _theme(
            "OPERATING_SELF_CARRY",
            "operating",
            "Người tự gánh",
            "Làm rõ tải tự gánh — và biết dừng nhận thêm.",
            "Không tâng bốc tải. Không nói mạnh hơn khi ôm thêm.",
            {
                "identity": "Bạn ngồi vào ghế khó trước khi việc được chia. Sức mạnh là tải có biên, không phải tải vô hạn.",
                "career": "Việc hợp khi nhiệm vụ rõ và được phép từ chối. Thành công không được biến thành hộp thư mở.",
                "growth": "Lớn lên ở kỹ năng dừng nhận — không phải kỹ năng ôm thêm.",
                "stress": "Phản xạ là nhận thêm một việc. Dừng: quyết / giao trước khi nhận.",
                "leadership": "Uy tín là hoàn thành điều đã nhận — không phải nhận hết.",
                "environment": "Vai tự chủ có biên tải. Không phải chỗ đổ mặc định.",
                "memory": "Bạn mạnh ở chỗ tự gánh — và bền hơn khi biết dừng nhận thêm.",
                "action": "Tuần này: biến một việc đang ôm thành đầu ra có biên. Dừng: nhận thêm theo phản xạ.",
            },
        ),
        "OPERATING_OUTPUT": _theme(
            "OPERATING_OUTPUT",
            "operating",
            "Người ra kết quả",
            "Trả bằng đầu ra nhìn thấy được, không bằng sự có mặt.",
            "Không giảng cày thông thường. Không đo bằng giờ ngồi ghế.",
            {
                "identity": "Bạn được nhận ra khi có thứ ra được — một sản phẩm, một ý, một kết quả — không khi hấp thụ việc của người khác.",
                "career": "Hợp khi được trả và đánh giá theo kết quả nhìn thấy được, với quyền chỉnh chất lượng.",
                "growth": "Tốt hơn = chu kỳ làm → thấy → chỉnh rõ hơn. Không phải thêm chức danh.",
                "stress": "Bạn lấy lại thế bằng một việc đóng được. Chọn một nhịp đóng, không thêm phiếu.",
                "leadership": "Dẫn bằng một kết quả có tên, không bằng giữ phòng.",
                "environment": "Chỗ được làm và nhận phản hồi. Không phải văn hóa chỉ có mặt.",
                "memory": "Bạn rõ khi tạo ra đầu ra trong đúng khung của mình — không khi ép khuôn chung hay ôm thêm cho đủ.",
                "action": "Tuần này: đóng một đầu ra trước khi mở cái tiếp. Dừng: tắt kênh làm.",
            },
        ),
        "OPERATING_STANDARDS": _theme(
            "OPERATING_STANDARDS",
            "operating",
            "Người giữ chuẩn",
            "Phạm vi, kỳ vọng, quyền quyết sạch.",
            "Không làm nhục. Không bịa cấp bậc.",
            {
                "identity": "Bạn chạy trên phạm vi rõ, kỳ vọng rõ, và biết ai quyết. Nhiệm vụ mơ hồ dễ thành thất bại cá nhân.",
                "career": "Vai có nhiệm vụ và vòng review rõ thắng vai ‘cứ phải chịu trách nhiệm’.",
                "growth": "Mài chuẩn giữ được — không phải chuẩn làm nhục.",
                "stress": "Áp lực hiện thành siết luật hoặc đóng băng. Quay về một phạm vi có tên.",
                "leadership": "Giữ đúng brief. Đừng nới brief để chứng minh nghiêm túc.",
                "environment": "Nơi nói được ‘xong’ nghĩa là gì. Không phải việc phụ không tên.",
                "memory": "Bạn làm sạch khi nhiệm vụ được viết — không khi đoán cho đủ.",
                "action": "Tuần này: viết một định nghĩa xong. Dừng: việc phụ chưa từng được giao.",
            },
        ),
        "BALANCE_DIRECTION": _theme(
            "BALANCE_DIRECTION",
            "operating",
            "Người điều tiết",
            "Tuần có hướng làm mát / điều tiết, không thêm tăng tốc.",
            "Không đóng bằng mạnh hơn. Không để dư vòng ra kết quả.",
            {
                "identity": "Tuần của bạn cần hướng điều tiết — mát, nghỉ, hoặc nhịp đều — không thêm tăng tốc.",
                "career": "Quyết định nghề là việc gì ngừng chồng, không phải hệ sản xuất mới.",
                "growth": "Lớn là tuần bền, không phải tuần nặng hơn.",
                "stress": "Nóng lên khi vẫn ‘còn chịu được’. Điều tiết trước khi cạn.",
                "leadership": "Làm mẫu tuần mát hơn. Đừng dẫn bằng luôn sẵn sàng.",
                "environment": "Chỗ cho phép nghỉ giữa vòng. Không phải chứng minh luôn bật.",
                "memory": "Bạn bền khi tuần có hướng làm mát — không khi đợi sụp mới nghỉ.",
                "action": "Tuần này: chèn một nhịp mát sau một vòng đã đóng. Dừng: vòng quá sức.",
            },
        ),
        "CONSERVING": _theme(
            "CONSERVING",
            "overlay",
            "Người cần bảo toàn",
            "Nghỉ và giữ nền là sản phẩm.",
            "Không diễn thuyết động lực. Không ‘bạn mạnh hơn khi…’.",
            {
                "identity": "Đây là mùa mỏng, không phải lỗi tính cách. Bảo toàn là đọc đúng.",
                "career": "Giữ năng lượng. Quyết định là việc gì không nhận. Không khung cày thứ hai.",
                "growth": "Hồi phục trước. Mở rộng sau — và chỉ khi nền cho phép.",
                "stress": "Thêm hoạt động để ‘chứng minh’ là bẫy. Giảm diện.",
                "memory": "Tuần này không cần mạnh hơn. Cần giữ nền còn nguyên.",
                "action": "Tuần này: trả hoặc bỏ một việc. Dừng: chứng minh bằng khối lượng.",
            },
        ),
        "TENSION_HOLDER": _theme(
            "TENSION_HOLDER",
            "overlay",
            "Người giữ hai lớp",
            "Giữ cả hai câu chuyện đã công bố.",
            "Không chọn một nhãn để xóa nhãn kia.",
            {
                "identity": "Cả hai lớp đều đúng. Nêu một lớp không xóa lớp kia.",
                "career": "Đừng thiết kế việc chỉ nuôi một lớp. Nêu đánh đổi.",
                "growth": "Tích hợp, không đổi nhãn.",
                "stress": "Áp lực là cuộc đấu giữa hai lớp. Chậm lựa chọn; đừng giả chắc.",
                "memory": "Hai sự thật đã công bố — tuần này đừng chọn một nhãn để xóa nhãn kia.",
                "action": "Tuần này: viết cả hai lớp trong một câu. Dừng: đóng bằng một nhãn.",
            },
        ),
        "FOLLOW_FRAME": _theme(
            "FOLLOW_FRAME",
            "overlay",
            "Khung riêng",
            "Không ép khuôn thường.",
            "Không giảng nhật chủ thông thường. Không ‘khung lá số’ rỗng.",
            {
                "identity": "Khung dài hạn của bạn không phải khuôn chung. Đo bằng ‘như mọi người’ là bán rẻ.",
                "career": "Hợp khi tổ chức tôn trọng khung riêng cộng cách vận hành — không thang chung.",
                "growth": "Đào sâu khung đang có. Đừng đổi khung vì áp lực ngắn.",
                "stress": "Áp lực bảo ‘hãy bình thường’. Quay về khung đã công bố.",
                "memory": "Bạn không kém vì không khớp khuôn chung. Bạn rõ trong khung của mình.",
                "action": "Tuần này: một việc trong đúng khung thật. Dừng: ép khuôn thường.",
            },
        ),
        "STABILIZER": _theme(
            "STABILIZER",
            "overlay",
            "Người giữ nhịp",
            "Giữ khung; giảm nhiễu; không mở vòng cày mới.",
            "Không ổn định bằng làm thêm.",
            {
                "identity": "Bạn giữ một tuần dùng được: cùng khung, ít nhiễu hơn.",
                "career": "Bảo vệ hệ đang chạy. Đừng mở lại kiến trúc.",
                "growth": "Ổn định chính là phần thắng.",
                "stress": "Áp lực muốn thiết kế lại. Giữ.",
                "memory": "Bạn rõ hơn khi khung đứng — không khi dựng lại dưới nóng.",
                "action": "Tuần này: giữ một nghi thức không đổi. Dừng: thiết kế thêm.",
            },
        ),
    }


CATALOG: dict[str, ThemeRecord] = build_catalog()


def canonical_theme_id(raw: str) -> str:
    """Map alias / CDR id to catalog id."""
    key = (raw or "").strip()
    if not key:
        return ""
    if key in CATALOG:
        return key
    return ALIASES.get(key, key)


def get_theme(theme_id: str) -> ThemeRecord | None:
    """Return catalog theme or None."""
    return CATALOG.get(canonical_theme_id(theme_id))
