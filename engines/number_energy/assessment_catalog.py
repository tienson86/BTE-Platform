"""Frozen assessment / recommendation copy from Golden fixture and Knowledge 10.

Selected by structure from RB05-A/B/C/D. Not derived from score.
"""

from __future__ import annotations

from typing import Final

ASSESSMENT_TITLE: Final[str] = "Đánh giá tổng thể"

GOLDEN_ASSESSMENT_SUMMARY: Final[str] = (
    "Dãy số nổi bật ở Diên Niên, đi cùng Sinh Khí và Thiên Y. "
    "Quý nhân và cơ hội có khả năng dẫn tới Tài, trong khi năng lực nghề nghiệp "
    "tiếp tục đóng vai trò tạo thành quả ở phần cuối dãy."
)
GOLDEN_STORY_NODES: Final[tuple[str, ...]] = ("QUÝ NHÂN", "TÀI", "SỰ NGHIỆP", "TÀI")
GOLDEN_STORY_LINE: Final[str] = "QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI"
GOLDEN_STORY_KEY: Final[str] = "ASM-STORY-GOLDEN-001"

GOLDEN_RECOMMENDATION_LABEL: Final[str] = "PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG"
GOLDEN_RECOMMENDATION_SUMMARY: Final[str] = (
    "Dãy có nhiều yếu tố hỗ trợ, đặc biệt ở công việc, quý nhân và đường tạo Tài."
)
GOLDEN_RECOMMENDATION_KEY: Final[str] = "REC-CONTINUE-USE-GOLDEN-001"

KEEP_COPY_KEY: Final[str] = "NAR-REC-KEEP-001"
KEEP_SUMMARY: Final[str] = (
    "Dãy số hiện tại có cấu trúc tương đối phù hợp với mục đích sử dụng. "
    "Không có dấu hiệu cần thay đổi chỉ vì một cặp số riêng lẻ."
)

BALANCE_COPY_KEY: Final[str] = "NAR-REC-BALANCE-001"
BALANCE_SUMMARY: Final[str] = (
    "Điểm cần ưu tiên không phải là tìm một dãy toàn Cát, "
    "mà là tạo cấu trúc cân bằng hơn."
)

STORY_NODE_MAP: Final[dict[str, str]] = {
    "Quý nhân & cơ hội": "QUÝ NHÂN",
    "Tài": "TÀI",
    "Sự nghiệp": "SỰ NGHIỆP",
}

GOLDEN_STRENGTH_TITLES: Final[tuple[str, ...]] = (
    "Quý nhân có thể mở đường cho Tài",
    "Năng lực nghề nghiệp nổi bật",
    "Công việc có khả năng tạo thành quả",
    "Khẩu tài có thể phát huy tích cực",
)

GENERIC_ASSESSMENT_SUMMARY: Final[str] = (
    "Dãy số được đọc theo toàn bộ cấu trúc cặp, bộ ba và phần cuối, "
    "không kết luận từ một cặp đơn lẻ."
)
