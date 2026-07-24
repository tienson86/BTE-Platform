"""
BTE Rule Contract V1

Shared Adapter + Matcher for Pattern / Score / Priority / Interpretation.

See: docs/rule_contract_v1.md
"""

from .adapter import RuleAdapter
from .context_builder import (
    EXPECTED_SIGNALS,
    REQUIRED_SECTIONS,
    RuleContextBuilder,
    build_rule_context,
)
from .matcher import RuleConditionMatcher
from .models import (
    ConditionPredicate,
    RuleContract,
    RuleContext,
    normalize_context,
)

__all__ = [
    "ConditionPredicate",
    "EXPECTED_SIGNALS",
    "REQUIRED_SECTIONS",
    "RuleAdapter",
    "RuleConditionMatcher",
    "RuleContext",
    "RuleContextBuilder",
    "RuleContract",
    "build_rule_context",
    "normalize_context",
]

__version__ = "1.0.0"
