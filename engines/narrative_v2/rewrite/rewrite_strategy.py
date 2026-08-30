"""Rewrite status, strategies, and language constants."""

from __future__ import annotations

STATUS_REWRITTEN = "rewritten"
STATUS_PASSTHROUGH = "passthrough"
STATUS_UNRESOLVED = "unresolved"
STATUS_REJECTED = "rejected"

STRATEGY_SIMPLIFICATION = "simplification"
STRATEGY_CLARIFICATION = "clarification"
STRATEGY_CONTEXTUALIZATION = "contextualization"
STRATEGY_PROFESSIONALIZATION = "professionalization"
STRATEGY_ACTION_ORIENTATION = "action_orientation"

ALLOWED_STRATEGIES: frozenset[str] = frozenset(
    {
        STRATEGY_SIMPLIFICATION,
        STRATEGY_CLARIFICATION,
        STRATEGY_CONTEXTUALIZATION,
        STRATEGY_PROFESSIONALIZATION,
        STRATEGY_ACTION_ORIENTATION,
    }
)

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_REWRITTEN,
        STATUS_PASSTHROUGH,
        STATUS_UNRESOLVED,
        STATUS_REJECTED,
    }
)

CUSTOMER_ADDRESS = "Bạn"

FORBIDDEN_ADDRESS: tuple[str, ...] = (
    "đương số",
    "Đương số",
    "mệnh chủ",
    "Mệnh chủ",
    "Quý khách",
)

FORTUNE_ABSOLUTES: tuple[str, ...] = (
    "chắc chắn",
    "nhất định",
    "tất nhiên",
    "không thể tránh",
    "đại cát",
    "đại hung",
)

FEAR_LANGUAGE: tuple[str, ...] = (
    "tai họa",
    "ly hôn",
    "phá sản",
    "bệnh nặng",
    "số khổ",
    "rất nguy hiểm",
)

ENGINE_LEAK: tuple[str, ...] = (
    "Engine",
    "CanonicalAnalysis",
    "Dụng thần",
    "Hỷ thần",
    "Kỵ thần",
    "nhật chủ",
    "Nhật chủ",
    "lệnh tháng",
    "NR-REL",
    "str_",
    "pat_",
    "{{",
    "}}",
)

ESCALATION_ADDED: tuple[str, ...] = (
    "chắc chắn",
    "nhất định",
    "luôn gặp may",
    "sẽ giúp",
    "sẽ ly hôn",
    "quyết định",
    "tình duyên chắc chắn",
    "màu đỏ",
    "hướng Nam",
)

REWRITE_VERSION = "nimp05.1.0"

REASON_NO_CUSTOMER_MEANING = "no_approved_customer_meaning"
REASON_NO_REWRITE_CONTRACT = "no_deterministic_rewrite_contract"
REASON_KNOWLEDGE_UNRESOLVED = "knowledge_unresolved"
REASON_UNSAFE_SOURCE = "source_not_customer_safe"
