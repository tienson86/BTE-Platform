"""Useful God Engine V2."""

from __future__ import annotations

from pathlib import Path

from .analyzer import UsefulGodAnalyzer
from .loader import UsefulGodLoader
from .matcher import UsefulGodMatcher
from .models import UsefulGodResult
from .priority import PriorityResolver
from .roles import enrich_useful_god_result

_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = str(_REPO_ROOT / "database" / "13_useful_god")


class UsefulGodEngine:
    """Data-driven useful-god selector based on PatternContext V2."""

    def __init__(self, database_path: str | None = None) -> None:
        self.database_path = database_path or DEFAULT_DATABASE_PATH
        self.loader = UsefulGodLoader(self.database_path)
        self.matcher = UsefulGodMatcher()
        self.analyzer = UsefulGodAnalyzer(self.matcher)

    def calculate(self, context) -> UsefulGodResult:
        grouped_rules = self.loader.load_rule_groups()
        priority_rules = self.loader.load_priority_rules()

        analysis = self.analyzer.analyze(context, grouped_rules)
        candidates = analysis["candidate_list"]

        resolver = PriorityResolver(priority_rules)
        winner = resolver.resolve(candidates)

        if winner is None:
            return UsefulGodResult(
                success=False,
                useful_god=None,
                error="no useful god rule matched",
                metadata={"analysis": analysis},
            )

        favorable = self._parse_json_list(winner.get("favorable_gods"))
        unfavorable = self._parse_json_list(winner.get("unfavorable_gods"))

        confidence = float(winner.get("score") or 0.0)
        matched_rules = [str(c.get("rule_id")) for c in candidates if c.get("rule_id")]

        result = UsefulGodResult(
            success=True,
            useful_god=str(winner.get("useful_god") or "").strip() or None,
            favorable_gods=favorable,
            unfavorable_gods=unfavorable,
            candidate_list=[self._public_candidate(c) for c in candidates],
            confidence=confidence,
            matched_rules=matched_rules,
            reasoning=str(winner.get("reason") or winner.get("description") or ""),
            temperature_reason=self._first_reason(analysis["temperature_candidates"]),
            season_reason=self._first_reason(analysis["season_candidates"]),
            strength_reason=self._first_reason(analysis["strength_candidates"]),
            balance_reason=str(analysis["balance_summary"].get("status") or ""),
            recommendations=self._build_recommendations(favorable, unfavorable),
            winning_rule_id=str(winner.get("rule_id") or ""),
            winning_rule_group=str(winner.get("rule_group") or ""),
            metadata={
                "trace": {
                    "context": self._context_snapshot(context),
                    "matched_rules": matched_rules,
                    "candidate_list": [self._public_candidate(c) for c in candidates],
                    "priority": [r for r in priority_rules],
                    "winner": self._public_candidate(winner),
                    "confidence": confidence,
                },
            },
        )
        return enrich_useful_god_result(
            result, str(getattr(context, "day_master", "") or "")
        )

    @staticmethod
    def _parse_json_list(value) -> list[str]:
        import json

        if value is None:
            return []
        if isinstance(value, list):
            return [str(v) for v in value]
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return []
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return [text]
            if isinstance(parsed, list):
                return [str(v) for v in parsed]
            return [str(parsed)]
        return [str(value)]

    @staticmethod
    def _public_candidate(candidate: dict) -> dict:
        return {
            "rule_id": candidate.get("rule_id"),
            "rule_group": candidate.get("rule_group"),
            "useful_god": candidate.get("useful_god"),
            "priority": int(candidate.get("priority") or 0),
            "score": float(candidate.get("score") or 0.0),
            "reason": candidate.get("reason") or candidate.get("description") or "",
        }

    @staticmethod
    def _first_reason(candidates: list[dict]) -> str | None:
        if not candidates:
            return None
        c = candidates[0]
        text = str(c.get("reason") or c.get("description") or "").strip()
        return text or None

    @staticmethod
    def _build_recommendations(favorable: list[str], unfavorable: list[str]) -> list[str]:
        out: list[str] = []
        if favorable:
            out.append("Ưu tiên yếu tố: " + ", ".join(favorable))
        if unfavorable:
            out.append("Hạn chế yếu tố: " + ", ".join(unfavorable))
        return out

    @staticmethod
    def _context_snapshot(context) -> dict:
        keys = [
            "day_master",
            "day_master_element",
            "month_branch",
            "month_branch_ten_god",
            "season",
            "season_phase",
            "temperature_type",
            "strength_level",
            "follow_pattern",
            "special_pattern",
            "main_pattern",
        ]
        snap = {k: getattr(context, k, None) for k in keys}
        return snap
