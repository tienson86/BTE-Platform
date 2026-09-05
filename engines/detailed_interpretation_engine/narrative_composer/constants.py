"""DI-19 Narrative Composer constants. No ranking weights."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import NARRATIVE_COMPOSER_RULESET_VERSION
from engines.detailed_interpretation_engine.domain_interpretation.constants import MAIN_DOMAIN_IDS

MAIN_NARRATIVE_DOMAINS: tuple[str, ...] = MAIN_DOMAIN_IDS

STORY_ORDER: tuple[str, ...] = (
    "executive_summary",
    "strength",
    "risk",
    "opportunity",
    "domain_section",
    "temporal",
    "optimization_section",
    "closing_summary",
)

EDGE_TYPES: frozenset[str] = frozenset(
    {"supports", "explains", "qualifies", "contrasts", "expands", "summarizes"}
)

P0_P1: frozenset[str] = frozenset({"P0", "P1"})

MAX_EXECUTIVE_SENTENCES: int = 10
MIN_EXECUTIVE_SENTENCES: int = 6
MAX_LIST_ITEMS: int = 4

HIGH_CONFIDENCE: float = 0.7

FORBIDDEN_CUSTOMER_TOKENS: tuple[str, ...] = (
    "mặc đỏ",
    "wear red",
    "sống gần nước",
    "mua cây",
    "chẩn đoán",
    "điều trị",
    "uống thuốc",
    "mua cổ phiếu",
    "đòn bẩy",
    "chắc chắn giàu",
    "chắc chắn thăng",
    "năm nay kết hôn",
    "sẽ làm quan lớn",
    "thiên mệnh đã định",
    "bệnh gan",
)

__all__ = (
    "NARRATIVE_COMPOSER_RULESET_VERSION",
    "MAIN_NARRATIVE_DOMAINS",
    "STORY_ORDER",
    "EDGE_TYPES",
    "P0_P1",
    "MAX_EXECUTIVE_SENTENCES",
    "MIN_EXECUTIVE_SENTENCES",
    "MAX_LIST_ITEMS",
    "HIGH_CONFIDENCE",
    "FORBIDDEN_CUSTOMER_TOKENS",
)
