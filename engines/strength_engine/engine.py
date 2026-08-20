"""Strength Engine V2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .analyzer import StrengthAnalyzer
from .evidence import compact_evidence
from .loader import StrengthLoader
from .matcher import StrengthMatcher
from .models import StrengthResult
from .priority import StrengthPriorityResolver
from .scorer import StrengthScorer

_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = str(_REPO_ROOT / "database" / "12_strength")


class StrengthEngine:
    """Data-driven strength analyzer based on BaziChart context."""

    def __init__(self, database_path: str | None = None) -> None:
        self.database_path = database_path or DEFAULT_DATABASE_PATH
        self.loader = StrengthLoader(self.database_path)
        self.matcher = StrengthMatcher()
        self.analyzer = StrengthAnalyzer(self.matcher)
        self.scorer = StrengthScorer()

    def calculate(self, context: Any) -> StrengthResult:
        """Run strength pipeline and return StrengthResult."""
        grouped_rules = self.loader.load_rule_groups()
        priority_rules = self.loader.load_priority_rules()
        level_rules = self.loader.load_level_rules()
        config = self.loader.load_config()

        analysis = self.analyzer.analyze(context, grouped_rules)
        resolver = StrengthPriorityResolver(priority_rules)
        scored = self.scorer.score(
            context,
            analysis,
            config,
            level_rules,
            self.matcher,
            resolver,
        )

        all_matches = analysis.get("all_matches") or []
        matched_rules = [str(m.get("rule_id")) for m in all_matches if m.get("rule_id")]

        if not matched_rules:
            return StrengthResult(
                success=False,
                strength_level="balanced",
                error="no strength rule matched",
                metadata={"analysis": self._public_analysis(analysis)},
            )

        reasoning = scored.get("reasoning") or self._build_reasoning(analysis)

        return StrengthResult(
            success=True,
            strength_level=str(scored.get("strength_level") or "balanced"),
            strength_score=float(scored.get("strength_score") or 0.0),
            season_score=float(scored.get("season_score") or 0.0),
            root_score=float(scored.get("root_score") or 0.0),
            support_score=float(scored.get("support_score") or 0.0),
            drain_score=float(scored.get("drain_score") or 0.0),
            control_score=float(scored.get("control_score") or 0.0),
            combination_score=float(scored.get("combination_score") or 0.0),
            special_score=float(scored.get("special_score") or 0.0),
            raw_total=float(scored.get("raw_total") or 0.0),
            confidence=float(scored.get("confidence") or 0.0),
            matched_rules=matched_rules,
            evidence_compact=compact_evidence(all_matches),
            reasoning=reasoning,
            metadata={
                "trace": {
                    "context": self._context_snapshot(context),
                    "matched_rules": matched_rules,
                    "analysis": self._public_analysis(analysis),
                    "scoring": {
                        "raw_total": scored.get("raw_total"),
                        "level_rule": scored.get("level_rule"),
                        "config": config,
                    },
                    "confidence": float(scored.get("confidence") or 0.0),
                },
            },
        )

    @staticmethod
    def _context_snapshot(context: Any) -> dict[str, Any]:
        keys = [
            "day_master",
            "day_master_element",
            "month_branch",
            "month_status",
            "root_level",
            "support_type",
            "control_type",
            "drain_type",
            "output_branch_count",
            "drain_count",
            "season",
            "strength_score",
        ]
        return {k: getattr(context, k, None) for k in keys}

    @staticmethod
    def _public_analysis(analysis: dict[str, Any]) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for key, matches in analysis.items():
            if not key.endswith("_matches"):
                continue
            out[key] = [str(m.get("rule_id")) for m in matches if m.get("rule_id")]
        return out

    @staticmethod
    def _build_reasoning(analysis: dict[str, Any]) -> str:
        parts: list[str] = []
        for group in ("season", "root", "support", "control", "drain", "special"):
            matches = analysis.get(f"{group}_matches") or []
            if matches:
                reason = str(matches[0].get("reason") or matches[0].get("description") or "")
                if reason:
                    parts.append(reason)
        return "; ".join(parts)
