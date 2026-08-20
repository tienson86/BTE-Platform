"""Useful God Engine V2."""

from __future__ import annotations

from pathlib import Path

from .analyzer import UsefulGodAnalyzer
from .layers import OVERALL_INCOMPLETE_MESSAGE, candidate_layer
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
        candidates = [
            self._with_layer(item) for item in analysis["candidate_list"]
        ]
        overall_candidates = [
            item for item in candidates if item.get("layer") == "overall"
        ]
        climate_candidates = [
            item for item in candidates if item.get("layer") == "climate"
        ]

        resolver = PriorityResolver(priority_rules)
        overall = resolver.resolve(overall_candidates)
        climate = resolver.resolve(climate_candidates)

        public_all = [self._public_candidate(item) for item in candidates]
        public_overall = [self._public_candidate(item) for item in overall_candidates]
        public_climate = [self._public_candidate(item) for item in climate_candidates]
        matched_rules = [str(item.get("rule_id")) for item in candidates if item.get("rule_id")]

        climate_fields = self._climate_fields(climate)
        trace = {
            "context": self._context_snapshot(context),
            "matched_rules": matched_rules,
            "candidate_list": public_all,
            "overall_candidate_list": public_overall,
            "climate_candidate_list": public_climate,
            "priority": [row for row in priority_rules],
            "winner": self._public_candidate(overall) if overall else None,
            "climate_winner": self._public_candidate(climate) if climate else None,
        }

        if overall is None:
            result = UsefulGodResult(
                success=False,
                useful_god=None,
                error=OVERALL_INCOMPLETE_MESSAGE,
                overall_incomplete=True,
                useful_display=OVERALL_INCOMPLETE_MESSAGE,
                candidate_list=public_all,
                overall_candidate_list=public_overall,
                climate_candidate_list=public_climate,
                matched_rules=matched_rules,
                temperature_reason=self._first_reason(analysis["temperature_candidates"]),
                season_reason=self._first_reason(analysis["season_candidates"]),
                strength_reason=self._first_reason(analysis["strength_candidates"]),
                balance_reason=str(analysis["balance_summary"].get("status") or ""),
                metadata={"trace": trace, "analysis": analysis},
                **climate_fields,
            )
            return enrich_useful_god_result(
                result, str(getattr(context, "day_master", "") or "")
            )

        favorable = self._parse_json_list(overall.get("favorable_gods"))
        unfavorable = self._parse_json_list(overall.get("unfavorable_gods"))
        confidence = float(overall.get("score") or 0.0)
        result = UsefulGodResult(
            success=True,
            useful_god=str(overall.get("useful_god") or "").strip() or None,
            favorable_gods=favorable,
            unfavorable_gods=unfavorable,
            candidate_list=public_all,
            overall_candidate_list=public_overall,
            climate_candidate_list=public_climate,
            confidence=confidence,
            matched_rules=matched_rules,
            reasoning=str(overall.get("reason") or overall.get("description") or ""),
            temperature_reason=self._first_reason(analysis["temperature_candidates"]),
            season_reason=self._first_reason(analysis["season_candidates"]),
            strength_reason=self._first_reason(analysis["strength_candidates"]),
            balance_reason=str(analysis["balance_summary"].get("status") or ""),
            recommendations=self._build_recommendations(favorable, unfavorable),
            winning_rule_id=str(overall.get("rule_id") or ""),
            winning_rule_group=str(overall.get("rule_group") or ""),
            metadata={"trace": {**trace, "confidence": confidence}},
            **climate_fields,
        )
        return enrich_useful_god_result(
            result, str(getattr(context, "day_master", "") or "")
        )

    @staticmethod
    def _with_layer(candidate: dict) -> dict:
        item = dict(candidate)
        item["layer"] = candidate_layer(str(item.get("rule_group") or ""))
        return item

    @classmethod
    def _climate_fields(cls, climate: dict | None) -> dict:
        if not climate:
            return {}
        token = str(climate.get("useful_god") or "").strip()
        return {
            "climate_candidate": token,
            "climate_rule_id": str(climate.get("rule_id") or ""),
            "climate_rule_group": str(climate.get("rule_group") or ""),
            "climate_reason": str(
                climate.get("reason") or climate.get("description") or ""
            ),
        }

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
    def _public_candidate(candidate: dict | None) -> dict:
        if not candidate:
            return {}
        return {
            "rule_id": candidate.get("rule_id"),
            "rule_group": candidate.get("rule_group"),
            "layer": candidate.get("layer") or candidate_layer(
                str(candidate.get("rule_group") or "")
            ),
            "useful_god": candidate.get("useful_god"),
            "priority": int(candidate.get("priority") or 0),
            "score": float(candidate.get("score") or 0.0),
            "reason": candidate.get("reason") or candidate.get("description") or "",
        }

    @staticmethod
    def _first_reason(candidates: list[dict]) -> str | None:
        if not candidates:
            return None
        item = candidates[0]
        text = str(item.get("reason") or item.get("description") or "").strip()
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
            "officer_elements",
        ]
        snapshot = {key: getattr(context, key, None) for key in keys}
        snapshot["officer_provenance"] = list(
            getattr(context, "officer_provenance", []) or []
        )
        metadata = getattr(context, "metadata", None)
        if isinstance(metadata, dict):
            snapshot["chinh_quan_visibility"] = metadata.get("chinh_quan_visibility")
        return snapshot
