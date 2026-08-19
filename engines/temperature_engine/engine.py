"""Temperature Engine V2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .analyzer import TemperatureAnalyzer
from .loader import TemperatureLoader
from .matcher import TemperatureMatcher
from .models import TemperatureResult
from .priority import TemperaturePriorityResolver
from .scorer import TemperatureScorer

_REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATABASE_PATH = str(_REPO_ROOT / "database" / "11_temperature")


class TemperatureEngine:
    """Data-driven temperature analyzer based on BaziChart context."""

    def __init__(self, database_path: str | None = None) -> None:
        self.database_path = database_path or DEFAULT_DATABASE_PATH
        self.loader = TemperatureLoader(self.database_path)
        self.matcher = TemperatureMatcher()
        self.analyzer = TemperatureAnalyzer(self.matcher)
        self.scorer = TemperatureScorer()

    def calculate(self, context: Any) -> TemperatureResult:
        """Run temperature pipeline and return TemperatureResult."""
        grouped_rules = self.loader.load_rule_groups()
        priority_rules = self.loader.load_priority_rules()
        level_rules = self.loader.load_level_rules()
        config = self.loader.load_config()

        primary = self.analyzer.analyze_primary(context, grouped_rules)
        resolver = TemperaturePriorityResolver(priority_rules)
        scored = self.scorer.score(
            context,
            primary,
            grouped_rules,
            self.analyzer,
            config,
            level_rules,
            self.matcher,
            resolver,
        )

        all_matches = scored.get("all_matches") or []
        matched_rules = [str(m.get("rule_id")) for m in all_matches if m.get("rule_id")]

        if not matched_rules:
            return TemperatureResult(
                success=False,
                error="no temperature rule matched",
                metadata={"analysis": self._public_analysis(primary, scored)},
            )

        reasoning = scored.get("reasoning") or self._build_reasoning(primary)
        winner = scored.get("level_rule")

        climate_state = str(scored.get("climate_state") or scored.get("temperature_level") or "warm")
        return TemperatureResult(
            success=True,
            temperature_level=climate_state,
            temperature_score=float(scored.get("temperature_score") or 0.0),
            warm_score=float(scored.get("warm_score") or 0.0),
            cold_score=float(scored.get("cold_score") or 0.0),
            dry_score=float(scored.get("dry_score") or 0.0),
            humid_score=float(scored.get("humid_score") or 0.0),
            confidence=float(scored.get("confidence") or 0.0),
            matched_rules=matched_rules,
            reasoning=reasoning,
            recommendations=list(scored.get("recommendations") or []),
            climate_state=climate_state,
            balancing_need=str(scored.get("balancing_need") or ""),
            climate_state_label=str(scored.get("climate_state_label") or ""),
            balancing_need_label=str(scored.get("balancing_need_label") or ""),
            evidence_compact=str(scored.get("evidence_compact") or ""),
            month_branch=str(scored.get("month_branch") or ""),
            season=str(scored.get("season") or ""),
            score_semantic=str(scored.get("score_semantic") or "imbalance_intensity"),
            climate_source=str(scored.get("climate_source") or ""),
            metadata={
                "trace": {
                    "context": self._context_snapshot(context),
                    "matched_rules": matched_rules,
                    "analysis": self._public_analysis(primary, scored),
                    "temperature_score": float(scored.get("temperature_score") or 0.0),
                    "score_semantic": "imbalance_intensity",
                    "climate_state": climate_state,
                    "balancing_need": scored.get("balancing_need"),
                    "priority": [r for r in priority_rules if str(r.get("score_target")) != "level"],
                    "winner": {
                        "climate_state": climate_state,
                        "climate_source": scored.get("climate_source"),
                        "level_rule": self._public_rule(winner),
                    },
                    "confidence": float(scored.get("confidence") or 0.0),
                    "scoring": {
                        "raw_total": scored.get("raw_total"),
                        "config": config,
                    },
                },
            },
        )

    @staticmethod
    def _context_snapshot(context: Any) -> dict[str, Any]:
        keys = [
            "day_master",
            "day_master_element",
            "month_branch",
            "season",
            "climate_type",
            "dryness_level",
            "humidity_level",
            "fire_count",
            "water_count",
            "temperature_score",
        ]
        return {k: getattr(context, k, None) for k in keys}

    @staticmethod
    def _public_rule(rule: dict[str, Any] | None) -> dict[str, Any] | None:
        if rule is None:
            return None
        return {
            "rule_id": rule.get("rule_id"),
            "temperature_level": rule.get("temperature_level"),
            "priority": int(rule.get("priority") or 0),
            "reason": rule.get("reason") or rule.get("description") or "",
        }

    @staticmethod
    def _public_analysis(primary: dict[str, Any], scored: dict[str, Any]) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for key, matches in primary.items():
            if not key.endswith("_matches"):
                continue
            out[key] = [str(m.get("rule_id")) for m in matches if m.get("rule_id")]
        balance = scored.get("balance_matches") or []
        out["balance_matches"] = [str(m.get("rule_id")) for m in balance if m.get("rule_id")]
        return out

    @staticmethod
    def _build_reasoning(primary: dict[str, Any]) -> str:
        parts: list[str] = []
        for group in ("climate", "season", "dryness", "humidity", "special", "flow"):
            matches = primary.get(f"{group}_matches") or []
            if matches:
                reason = str(matches[0].get("reason") or matches[0].get("description") or "")
                if reason:
                    parts.append(reason)
        return "; ".join(parts)
