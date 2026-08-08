"""Language Rule Engine — Sprint C wording gates at runtime."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

_FORBIDDEN_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"kích hoạt khi", re.IGNORECASE),
    re.compile(r"áp dụng bảng", re.IGNORECASE),
    re.compile(r"ưu tiên xác định", re.IGNORECASE),
    re.compile(r"matched[_ ]?rules?", re.IGNORECASE),
    re.compile(r"\bpack[_\s]?\d+", re.IGNORECASE),
    re.compile(r"presentation layer", re.IGNORECASE),
    re.compile(r"viewmodel", re.IGNORECASE),
    re.compile(r"\(mock\)", re.IGNORECASE),
    re.compile(r"placeholder", re.IGNORECASE),
    re.compile(r"\btodo\b", re.IGNORECASE),
    re.compile(r"chắc chắn sẽ", re.IGNORECASE),
    re.compile(r"định mệnh không thể đổi", re.IGNORECASE),
    re.compile(r"thảm họa chắc chắn", re.IGNORECASE),
    re.compile(r"mệnh xấu tuyệt đối", re.IGNORECASE),
)


class LanguageRuleEngine:
    """
    Apply Sprint C wording rules.

    Rejects forbidden wording. Does not invent replacement prose.
    """

    def is_allowed(self, text: str) -> bool:
        """Return True when text passes forbidden-pattern gates."""
        value = (text or "").strip()
        if not value:
            return False
        for pattern in _FORBIDDEN_PATTERNS:
            if pattern.search(value):
                logger.debug("language_rules.reject pattern=%s", pattern.pattern)
                return False
        return True

    def sanitize_or_none(self, text: str) -> str | None:
        """Return trimmed text if allowed, otherwise None."""
        value = (text or "").strip()
        if not self.is_allowed(value):
            return None
        return value

    def first_sentence(self, text: str, *, max_len: int = 220) -> str:
        """
        Take the first sentence-like unit from source text.

        Does not rewrite meaning — only truncates for paragraph discipline.
        """
        value = (text or "").strip()
        if not value:
            return ""
        parts = re.split(r"(?<=[。.!?])\s+|\n+", value)
        lead = (parts[0] if parts else value).strip()
        if len(lead) <= max_len:
            return lead
        return f"{lead[: max_len - 1].rstrip()}…"
