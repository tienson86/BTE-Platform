"""
Interpretation Builder
======================

Builder chịu trách nhiệm chuyển danh sách MatchedRule
thành các SemanticBlock.

Pipeline:

MatchedRule
    ↓
InterpretationBuilder
    ↓
SemanticBlock
    ↓
SentenceGenerator

Builder KHÔNG sinh câu.
Builder KHÔNG tạo report.
Builder KHÔNG quyết định cách diễn đạt.

.. deprecated:: WP0B
    Không dùng cho InterpretationEngine.run().
    Active builder: ``legacy_builder.InterpretationBuilder`` → InterpretationResult.
    SemanticBlock path giữ lại; bridge sang SentenceGenerator ở WP1.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models.semantic_block import SemanticBlock


class InterpretationBuilder:
    """
    Xây dựng SemanticBlock từ kết quả Rule Engine.
    """

    def build(
        self,
        matched_rules: list[dict[str, Any]],
        context: Any | None = None,
    ) -> list[SemanticBlock]:
        """
        Build Semantic Blocks.

        Parameters
        ----------
        matched_rules
            Danh sách rule đã match.

        context
            Interpretation context (dự phòng cho các phiên bản sau).

        Returns
        -------
        list[SemanticBlock]
        """

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
) -> list[SemanticBlock]:
    """
    Helper function.
    """

    return InterpretationBuilder().build(
        matched_rules,
        context,
    )