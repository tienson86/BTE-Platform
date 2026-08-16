"""Publication limits and reject markers. Not composition policy."""

from __future__ import annotations

from typing import Final, Mapping

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAIN_CAREER,
    CUSTOMER_DOMAIN_FINANCE,
    CUSTOMER_DOMAIN_HEALTH,
    CUSTOMER_DOMAIN_LABELS,
    CUSTOMER_DOMAIN_RELATIONSHIP,
)

PUBLISHED_NARRATIVE_BUILDER_ID: Final[str] = "published_narrative_builder_v1"

DECISION_PUBLISH: Final[str] = "PUBLISH"
DECISION_DROP: Final[str] = "DROP"
DECISION_APPENDIX: Final[str] = "APPENDIX"

# Publication limits. Internal narrative may contain more.
SECTION_LIMITS: Final[Mapping[str, int]] = {
    "sec-executive_summary": 6,
    "sec-observation": 8,
    "sec-reasoning": 3,
    "sec-impact": 4,
    "sec-recommendation": 5,
    "sec-warning": 3,
    "sec-conclusion": 1,
}

# Higher customer value wins when space or meaning collides.
SECTION_PRIORITY: Final[tuple[str, ...]] = (
    "sec-executive_summary",
    "sec-reasoning",
    "sec-recommendation",
    "sec-impact",
    "sec-warning",
    "sec-observation",
    "sec-conclusion",
)

IMPACT_SPINE_LABELS: Final[tuple[str, ...]] = (
    CUSTOMER_DOMAIN_LABELS[CUSTOMER_DOMAIN_CAREER],
    CUSTOMER_DOMAIN_LABELS[CUSTOMER_DOMAIN_FINANCE],
    CUSTOMER_DOMAIN_LABELS[CUSTOMER_DOMAIN_RELATIONSHIP],
    CUSTOMER_DOMAIN_LABELS[CUSTOMER_DOMAIN_HEALTH],
)

ENGLISH_DOMAIN_TAGS: Final[tuple[str, ...]] = (
    "Career:",
    "Finance:",
    "Relationship:",
    "Health:",
    "Learning:",
    "Decision:",
    "Environment:",
)

ENGINE_PHRASES: Final[tuple[str, ...]] = (
    "loaded",
    "candidates from engine",
    "from engine",
    "detector",
    "alias",
    "token",
    "emit",
    "engine emit",
    "winner",
    "debug",
    "bundle_id",
    "knowledge_id",
    "engine_output",
    "rule_id",
    "group priority",
    "engine chọn",
    "lý do engine",
    "ứng viên thắng",
    "decision explanation",
    "strength engine",
    "production phải",
    "knowledge không sửa engine",
    "cả hai key",
    "cùng hit",
    "candidate group",
    "matched_rules",
    "reason_codes",
    "select_winner",
    "engine_version",
    "golden dataset",
)

ENGINE_WORD_PATTERNS: Final[tuple[str, ...]] = (
    r"\bpriority\s*[:=]?\s*\d+",
    r"\bpriority\b",
    r"\bscore\s*[:=]?\s*\d",
    r"\bscore\b",
    r"\bengine\b",
    r"\btoken\b",
    r"\balias\b",
    r"\bdetector\b",
    r"\bdebug\b",
    r"\bloaded\b",
    r"\bwinner\b",
    r"\bproduction\b",
)

GLOSSARY_MARKERS: Final[tuple[str, ...]] = (
    "không suy ra",
    "là quan hệ ",
    "không đồng nhất",
    "không phải nghĩa tượng trưng",
    "sao quý nhân đầy đủ tên",
    "hệ thống xác định nhãn",
    "tên gọi khác",
    "không phải thập thần",
    "khắc nghịch",
    "đồng khí đối cực",
    "tiết thuận, đổi sức",
    "khác chính quan",
    "khác thương quan",
    "là nhãn hiện diện",
)

APPENDIX_MARKERS: Final[tuple[str, ...]] = (
    "tên gọi khác",
    "ứng viên",
    "candidate",
    "bản đủ tên",
    "không tách nghề",
    "không cộng dồn",
    "bước nhận diện",
    "giữ hai key",
    "rule commentary",
    "so sánh nội bộ",
)

CHART_FACT_PREFIXES: Final[tuple[str, ...]] = (
    "nhật chủ:",
    "dụng thần được chọn:",
    "hỷ thần:",
    "kỵ thần:",
    "cục:",
    "thân:",
    "đại vận",
    "lệnh tháng",
    "can ngày",
    "trụ ngày",
)

TEN_GOD_LABELS: Final[tuple[str, ...]] = (
    "chính quan",
    "thất sát",
    "chính ấn",
    "thiên ấn",
    "chính tài",
    "thiên tài",
    "thực thần",
    "thương quan",
    "tỷ kiên",
    "kiếp tài",
    "thiên quan",
    "nhật chủ",
)

MEANING_JACCARD_THRESHOLD: Final[float] = 0.72
MULTI_TOPIC_GOD_COUNT: Final[int] = 4
MULTI_TOPIC_GLOSSARY_HITS: Final[int] = 2
DUMP_CHAR_LIMIT: Final[int] = 420
MEANING_TOKEN_MIN: Final[int] = 2
