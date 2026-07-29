"""
interpretation_service.py
=========================

Interpretation Service

Facade của Interpretation Engine.

Pipeline:

InterpretationContext
        │
        ▼
RuleLoader
        │
        ▼
RuleEngine
        │
        ▼
RuleResult
        │
        ▼
InterpretationBuilder
        │
        ▼
InterpretationReport

.. deprecated:: WP0B
    Alternate pipeline. Active entry: ``engine.InterpretationEngine.run()``.
    Giữ lại để tương thích; unify ở WP1.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from ..builders.interpretation_builder import InterpretationBuilder
from ..models.context import InterpretationContext
from ..models.report import InterpretationReport
from ..models.rule import Rule
from ..models.rule_result import RuleResult
from ..rule_engine.engine import RuleEngine
from ..rule_loader import RuleLoader


class InterpretationService:
    """
    Dịch vụ điều phối toàn bộ Interpretation Engine.
    """

    def __init__(
        self,
        rule_loader: RuleLoader | None = None,
        rule_engine: RuleEngine | None = None,
        builder: InterpretationBuilder | None = None,
    ) -> None:

        self.rule_loader = rule_loader or RuleLoader()

        self.rule_engine = rule_engine or RuleEngine()

        self.builder = builder or InterpretationBuilder()

    # =====================================================
    # Rule
    # =====================================================

    def load_rules(
        self,
        path: str | Path,
    ) -> list[Rule]:
        """
        Đọc Rule Database.
        """

        return self.rule_loader.load(path)

    # =====================================================
    # Evaluate
    # =====================================================

    def evaluate(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> list[RuleResult]:
        """
        Chạy Rule Engine.
        """

        return self.rule_engine.run_matched(
            context=context,
            rules=rules,
        )

    # =====================================================
    # Build Report
    # =====================================================

    def build_report(
        self,
        context: InterpretationContext,
        results: Iterable[RuleResult],
    ) -> InterpretationReport:

        return self.builder.build(
            context=context,
            results=results,
        )

    # =====================================================
    # Run
    # =====================================================

    def run(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> InterpretationReport:
        """
        Chạy toàn bộ Pipeline.
        """

        results = self.evaluate(
            context=context,
            rules=rules,
        )

        return self.build_report(
            context=context,
            results=results,
        )

    # =====================================================
    # Run From Folder
    # =====================================================

    def run_from_database(
        self,
        context: InterpretationContext,
        database_path: str | Path,
    ) -> InterpretationReport:
        """
        Chạy trực tiếp từ Rule Database.
        """

        rules = self.load_rules(database_path)

        return self.run(
            context=context,
            rules=rules,
        )

    # =====================================================
    # Markdown
    # =====================================================

    def build_markdown(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> str:

        report = self.run(
            context=context,
            rules=rules,
        )

        return self.builder.formatter.to_markdown(
            report
        )

    # =====================================================
    # HTML
    # =====================================================

    def build_html(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> str:

        report = self.run(
            context=context,
            rules=rules,
        )

        return self.builder.formatter.to_html(
            report
        )

    # =====================================================
    # Text
    # =====================================================

    def build_text(
        self,
        context: InterpretationContext,
        rules: Iterable[Rule],
    ) -> str:

        report = self.run(
            context=context,
            rules=rules,
        )

        return self.builder.formatter.to_text(
            report
        )
