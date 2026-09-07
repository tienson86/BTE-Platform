"""Customer-facing labels for report blocks. No new meaning."""

from __future__ import annotations

from consulting.marriage.models.enums import (
    CanonicalGender,
    RecommendationPriority,
    RecommendationUrgency,
)

GENDER_LABEL = {
    CanonicalGender.MALE: "Nam",
    CanonicalGender.FEMALE: "Nữ",
}

PRIORITY_LABEL = {
    RecommendationPriority.CRITICAL: "Then chốt",
    RecommendationPriority.HIGH: "Ưu tiên cao",
    RecommendationPriority.MEDIUM: "Ưu tiên vừa",
    RecommendationPriority.LOW: "Ưu tiên thấp",
    RecommendationPriority.REFERENCE: "Tham khảo",
}

URGENCY_LABEL = {
    RecommendationUrgency.IMMEDIATE: "Cần chú ý sớm",
    RecommendationUrgency.NEAR_TERM: "Trong thời gian gần",
    RecommendationUrgency.LONG_TERM: "Theo lộ trình dài",
    RecommendationUrgency.CONTINUOUS: "Áp dụng đều",
    RecommendationUrgency.EVENT_DRIVEN: "Khi giai đoạn kích hoạt",
}

TIMING_WHEN = {
    "always_applicable": "Áp dụng thường xuyên",
    "sensitive_period": "Khi giai đoạn nhạy",
    "supportive_period": "Khi giai đoạn thuận hơn",
    "timing_finding_activation": "Khi nhịp thời điểm kích hoạt",
}

RENDERER_TOKENS = (
    "css",
    "html",
    "pdf",
    "docx",
    "font-size",
    "margin",
    "padding",
    "layout_x",
    "layout_y",
)
