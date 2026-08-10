"""Log retention, rotation, and ownership. Policy only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from applications.logging.logging_contract import LogStreamKind


@dataclass(slots=True, frozen=True)
class RetentionRule:
    """Retention rule for one log kind."""

    kind: LogStreamKind
    rotate: str
    retain_days: int
    owner: str
    compress: bool = True


RETENTION_RULES: Final[tuple[RetentionRule, ...]] = (
    RetentionRule("application", "daily or 50 MB", 14, "api-owner"),
    RetentionRule("access", "daily", 30, "edge-owner"),
    RetentionRule("error", "daily", 30, "api-owner"),
    RetentionRule("audit", "daily", 90, "security-owner"),
    RetentionRule("security", "daily", 90, "security-owner"),
    RetentionRule("operational", "daily", 30, "platform-ops"),
)

FORBIDDEN_LOG_CONTENT: Final[tuple[str, ...]] = (
    "passwords",
    "jwt_tokens",
    "api_keys",
    "stack_traces_to_clients",
    "filesystem_secrets",
)


def rule_for(kind: LogStreamKind) -> RetentionRule:
    """Return the retention rule for a log kind."""
    for item in RETENTION_RULES:
        if item.kind == kind:
            return item
    raise KeyError(kind)
