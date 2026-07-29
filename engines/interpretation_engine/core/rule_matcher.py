"""
Rule Matcher

So khớp Rule Database với BaziResult.
"""

from __future__ import annotations

from typing import Any

from ..models import InterpretationContext
from ..loader import InterpretationLoader


class RuleMatcher:

    def __init__(
        self,
        loader: InterpretationLoader,
    ) -> None:

        self.loader = loader

    def match(
        self,
        context: InterpretationContext,
    ) -> list[dict[str, Any]]:
        """
        Trả về danh sách Rule phù hợp.
        """

        rules = self.loader.load_rules()

        matched = []

        for rule in rules:

            if self._match_rule(
                rule,
                context,
            ):

                matched.append(rule)

        matched.sort(
            key=lambda x: x.get(
                "priority",
                0,
            ),
            reverse=True,
        )

        return matched

    def _match_rule(
        self,
        rule: dict[str, Any],
        context: InterpretationContext,
    ) -> bool:
        """
        TODO:
            Rule Engine sẽ triển khai tại đây.

        Hiện tại mặc định trả True để
        pipeline hoạt động.
        """

        return True
