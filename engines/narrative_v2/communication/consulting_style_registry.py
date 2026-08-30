"""Approved consulting frames. Discourse structure only. No astrology meaning."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.communication.consulting_style_profile import DEFAULT_PROFILE_ID


@dataclass(frozen=True, slots=True)
class ConsultingFrame:
    """One approved language frame."""

    frame_id: str
    text: str
    role: str


APPROVED_FRAMES: tuple[ConsultingFrame, ...] = (
    ConsultingFrame("frame.observation.highlight", "Điểm nổi bật ở đây là", "observation"),
    ConsultingFrame("frame.observation.notable", "Điều đáng chú ý là", "observation"),
    ConsultingFrame("frame.reasoning.shows", "Điều này cho thấy", "reasoning"),
    ConsultingFrame("frame.meaning.practice", "Trong thực tế", "meaning"),
    ConsultingFrame("frame.impact.when", "Điểm này thường thể hiện rõ khi", "impact"),
    ConsultingFrame("frame.recommendation.note", "Tuy nhiên, cũng cần lưu ý", "recommendation"),
    ConsultingFrame("frame.positive.side", "Ở mặt tích cực", "meaning"),
    ConsultingFrame("frame.closing.overall", "Ở góc nhìn tổng thể", "closing"),
)

LANGUAGE_ISSUE_APPROVED = "approved_customer_safe"
LANGUAGE_ISSUE_SHORTHAND = "technical_consultant_shorthand"
LANGUAGE_ISSUE_SENTENCE_GAP = "sentence_library_gap"
LANGUAGE_ISSUE_UNSAFE_TO_POLISH = "unsafe_without_language_asset"

FRAGMENT_OPENERS: tuple[str, ...] = ("Hữu ích khi",)

ESCALATION_TERMS: tuple[str, ...] = (
    "thành công",
    "giàu",
    "may mắn",
    "thăng tiến",
    "hôn nhân tốt",
    "sức khỏe tốt",
    "quý nhân bảo vệ",
    "đường tình duyên",
    "màu đỏ",
    "hướng Nam",
)


class ConsultingStyleRegistry:
    """Deterministic frame lookup. No random choice. No LLM."""

    def __init__(self, frames: tuple[ConsultingFrame, ...] = APPROVED_FRAMES) -> None:
        self._frames = {frame.frame_id: frame for frame in frames}

    def frame(self, frame_id: str) -> ConsultingFrame:
        """Return one approved frame."""
        if frame_id not in self._frames:
            raise KeyError(f"Unknown consulting frame: {frame_id}")
        return self._frames[frame_id]

    def frames_for_role(self, role: str) -> tuple[ConsultingFrame, ...]:
        """Return approved frames for one formula role."""
        return tuple(frame for frame in self._frames.values() if frame.role == role)

    def profile_id(self) -> str:
        """Canonical profile this registry serves."""
        return DEFAULT_PROFILE_ID
