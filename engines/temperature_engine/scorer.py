"""Temperature score aggregation and level classification."""

from __future__ import annotations

from typing import Any

from .climate import (
    climate_aligned_recommendations,
    compact_evidence,
    resolve_climate_state,
    winning_climate_rule_id,
)

_WARM_LEVELS = frozenset({"warm", "hot"})
_COLD_LEVELS = frozenset({"cold", "cool"})


class TemperatureScorer:
    """Aggregate matched rule scores and classify temperature level."""

    def score(
        self,
        context: Any,
        primary_analysis: dict[str, Any],
        grouped_rules: dict[str, list[dict[str, Any]]],
        analyzer: Any,
        config: dict[str, float],
        level_rules: list[dict[str, Any]],
        matcher: Any,
        priority_resolver: Any,
    ) -> dict[str, Any]:
        """Compute component scores, total score, level, and recommendations."""
        scale = float(config.get("scale") or 100.0)
        baseline = float(config.get("baseline") or 50.0)
        divisor = float(config.get("divisor") or 1.0)
        if divisor <= 0:
            divisor = 1.0

        primary_matches: list[dict[str, Any]] = []
        for key in (
            "season_matches",
            "climate_matches",
            "dryness_matches",
            "humidity_matches",
            "special_matches",
            "flow_matches",
        ):
            primary_matches.extend(primary_analysis.get(key) or [])

        warm_raw = 0.0
        cold_raw = 0.0
        dry_raw = 0.0
        humid_raw = 0.0

        for rule in primary_matches:
            score = float(rule.get("score") or 0.0)
            target = str(rule.get("score_target") or rule.get("rule_group") or "")
            level = str(rule.get("temperature_level") or "")
            if target == "dryness":
                dry_raw += score
            elif target == "humidity":
                humid_raw += score
            elif level in _WARM_LEVELS:
                warm_raw += score
            elif level in _COLD_LEVELS:
                cold_raw += score
            elif score >= 0:
                warm_raw += score
            else:
                cold_raw += abs(score)

        context.warm_score = warm_raw / scale if scale else 0.0
        context.cold_score = abs(cold_raw) / scale if scale else 0.0
        context.dry_score = dry_raw / scale if scale else 0.0
        context.humid_score = humid_raw / scale if scale else 0.0

        balance_matches = analyzer.analyze_balance(context, grouped_rules)
        all_matches = primary_matches + balance_matches

        raw_total = sum(float(r.get("score") or 0.0) for r in all_matches) / divisor
        normalized = (raw_total + baseline) / scale if scale else 0.0
        normalized = max(0.0, min(1.0, normalized))
        context.temperature_score = normalized

        # Score is imbalance/intensity, not a cold→hot axis. Do not classify from it.
        climate = resolve_climate_state(context, primary_analysis)
        climate_state = str(climate.get("climate_state") or "")
        climate_rule_id = winning_climate_rule_id(primary_analysis)
        reasoning = str(climate.get("climate_state_label") or climate_state)
        climate_matches = list(primary_analysis.get("climate_matches") or [])
        if climate_matches:
            climate_matches.sort(key=lambda item: int(item.get("priority") or 0), reverse=True)
            reasoning = str(
                climate_matches[0].get("reason")
                or climate_matches[0].get("description")
                or reasoning
            )

        recommendations = climate_aligned_recommendations(primary_analysis, climate_state)
        confidence = min(1.0, len(all_matches) / 4.0) if all_matches else 0.0
        if climate_state:
            confidence = min(1.0, confidence + 0.2)

        return {
            "temperature_level": climate_state or "warm",
            "climate_state": climate_state,
            "balancing_need": str(climate.get("balancing_need") or ""),
            "climate_state_label": str(climate.get("climate_state_label") or ""),
            "balancing_need_label": str(climate.get("balancing_need_label") or ""),
            "evidence_compact": compact_evidence(
                climate, winning_climate_rule_id=climate_rule_id
            ),
            "month_branch": str(climate.get("month_branch") or ""),
            "season": str(climate.get("season") or ""),
            "score_semantic": "imbalance_intensity",
            "climate_source": str(climate.get("climate_source") or ""),
            "temperature_score": normalized,
            "warm_score": context.warm_score,
            "cold_score": context.cold_score,
            "dry_score": context.dry_score,
            "humid_score": context.humid_score,
            "confidence": confidence,
            "reasoning": reasoning,
            "recommendations": recommendations,
            "raw_total": raw_total,
            "level_rule": None,
            "all_matches": all_matches,
            "balance_matches": balance_matches,
        }

    @staticmethod
    def _collect_recommendations(
        matches: list[dict[str, Any]],
        level_rule: dict[str, Any] | None,
    ) -> list[str]:
        recs: list[str] = []
        seen: set[str] = set()
        if level_rule is not None:
            rec = str(level_rule.get("recommendation") or "").strip()
            if rec and rec not in seen:
                recs.append(rec)
                seen.add(rec)
        for rule in sorted(matches, key=lambda r: int(r.get("priority") or 0), reverse=True):
            rec = str(rule.get("recommendation") or "").strip()
            if rec and rec not in seen:
                recs.append(rec)
                seen.add(rec)
            if len(recs) >= 5:
                break
        return recs
