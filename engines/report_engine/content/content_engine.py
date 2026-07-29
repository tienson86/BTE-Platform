"""
Content Engine (WP7A) — Analysis Layer.

InterpretationResult → ContentContext

Does not mutate Report Engine / Knowledge / Matcher / RuleContext.
"""

from __future__ import annotations

import importlib
from typing import Any

from .models import ContentContext

_analysis = importlib.import_module(
    "engines.report_engine.content.01_analysis"
)
ContextAnalyzer = _analysis.ContextAnalyzer
ImportanceRanker = _analysis.ImportanceRanker
KeywordExtractor = _analysis.KeywordExtractor
SectionOptimizer = _analysis.SectionOptimizer


class ContentEngine:
    """
    Orchestrate content analysis over InterpretationResult.
    """

    def __init__(
        self,
        *,
        importance_threshold: float = 25.0,
        keyword_top_k: int = 30,
    ) -> None:
        self.context_analyzer = ContextAnalyzer()
        self.importance_ranker = ImportanceRanker(
            importance_threshold=importance_threshold
        )
        self.keyword_extractor = KeywordExtractor(top_k=keyword_top_k)
        self.section_optimizer = SectionOptimizer()

    def analyze(self, interpretation: Any) -> ContentContext:
        """
        Build ContentContext from InterpretationResult (object or dict).
        """
        analysis = self.context_analyzer.analyze(interpretation)
        ranked = self.importance_ranker.rank(analysis)
        lexical = self.keyword_extractor.extract(analysis)
        suggested = self.section_optimizer.optimize(
            section_scores=ranked["section_scores"],
            important_sections=ranked["important_sections"],
            grouped_rules=analysis.get("grouped_rules") or {},
        )
        return ContentContext(
            section_scores=ranked["section_scores"],
            important_sections=ranked["important_sections"],
            keywords=lexical["keywords"],
            grouped_rules=analysis.get("grouped_rules") or {},
            repeated_topics=lexical["repeated_topics"],
            suggested_order=suggested,
            metadata={
                "rule_count": analysis.get("rule_count", 0),
                "confidence": analysis.get("confidence", 0.0),
                "matched_rule_count": analysis.get("matched_rule_count", 0),
                "resolved_rule_count": analysis.get("resolved_rule_count", 0),
                "summary_present": bool(str(analysis.get("summary") or "").strip()),
            },
        )

    def analyze_to_dict(self, interpretation: Any) -> dict[str, Any]:
        """Convenience: analyze and return a plain dict."""
        return self.analyze(interpretation).to_dict()
