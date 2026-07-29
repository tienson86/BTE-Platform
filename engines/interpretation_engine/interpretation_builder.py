"""
Interpretation Builder
======================

Builder chịu trách nhiệm chuyển danh sách MatchedRule
thành InterpretationResult (public contract).

Pipeline:

MatchedRule
    ↓
InterpretationBuilder
    ↓
InterpretationResult
    ↓
SentenceGenerator

Internal SemanticBlock path is preserved as ``build_blocks`` for
engines that still need intermediate blocks — public ``build`` never
returns a list.

.. note::
    Production pipeline uses ``legacy_builder.InterpretationBuilder``
    via ``InterpretationEngine``. This module's public ``build``
    delegates to the same result contract for API compatibility.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .legacy_builder import InterpretationBuilder as _LegacyInterpretationBuilder
from .legacy_builder import InterpretationResult
from .models.semantic_block import SemanticBlock


class InterpretationBuilder:
    """
    Public builder — always returns InterpretationResult.

    SemanticBlock construction remains available via ``build_blocks``.
    """

    def __init__(self) -> None:
        self._legacy = _LegacyInterpretationBuilder()

    def build(
        self,
        matched_rules: list[dict[str, Any]],
        context: Any | None = None,
    ) -> InterpretationResult:
        """
        Build InterpretationResult from matched rules.

        Parameters
        ----------
        matched_rules
            Danh sách rule đã match.

        context
            Interpretation context (optional).

        Returns
        -------
        InterpretationResult
        """
        return self._legacy.build(matched_rules or [], context)

    # =====================================================
    # SemanticBlock path (internal / legacy callers)
    # =====================================================

    def build_blocks(
        self,
        matched_rules: list[dict[str, Any]],
        context: Any | None = None,
    ) -> list[SemanticBlock]:
        """Build SemanticBlocks without changing the public ``build`` contract."""
        del context  # reserved for future enrichment

        normalized = [
            self.normalize_rule(rule)
            for rule in matched_rules
        ]

        grouped = self.group_by_topic(normalized)

        blocks = []

        for topic, rules in grouped.items():
            blocks.append(
                self.build_block(
                    topic,
                    rules,
                )
            )

        blocks.sort(
            key=lambda x: x.priority
        )

        return blocks

    # =====================================================
    # Normalize
    # =====================================================

    def normalize_rule(
        self,
        rule: dict[str, Any],
    ) -> dict[str, Any]:

        data = {
            "rule_id": "",
            "topic": "tong_quan",
            "title": "",
            "priority": 100,
            "severity": "info",
            "facts": [],
            "metadata": {},
        }

        data.update(rule)

        return data

    # =====================================================
    # Group
    # =====================================================

    def group_by_topic(
        self,
        rules: list[dict[str, Any]],
    ) -> dict[str, list[dict[str, Any]]]:

        grouped = defaultdict(list)

        for rule in rules:
            grouped[
                rule["topic"]
            ].append(rule)

        return grouped

    # =====================================================
    # Build Block
    # =====================================================

    def build_block(
        self,
        topic: str,
        rules: list[dict[str, Any]],
    ) -> SemanticBlock:

        block = SemanticBlock(
            topic=topic,
            title=rules[0].get("title", topic),
            priority=min(
                r.get("priority", 100)
                for r in rules
            ),
            severity=self.resolve_severity(rules),
        )

        for rule in rules:

            block.add_rule(
                rule["rule_id"]
            )

            for fact in rule.get(
                "facts",
                [],
            ):
                block.add_fact(fact)

            block.metadata.update(
                rule.get(
                    "metadata",
                    {},
                )
            )

        return block

    # =====================================================
    # Severity
    # =====================================================

    def resolve_severity(
        self,
        rules: list[dict[str, Any]],
    ) -> str:

        order = [
            "critical",
            "bad",
            "warning",
            "good",
            "info",
        ]

        severities = {
            r.get(
                "severity",
                "info",
            )
            for r in rules
        }

        for level in order:
            if level in severities:
                return level

        return "info"


def build_interpretation(
    matched_rules: list[dict[str, Any]],
    context: Any | None = None,
) -> InterpretationResult:
    """
    Helper function — always returns InterpretationResult.
    """

    return InterpretationBuilder().build(
        matched_rules,
        context,
    )
