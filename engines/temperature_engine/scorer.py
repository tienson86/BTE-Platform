"""Temperature score aggregation and level classification."""

from __future__ import annotations

from typing import Any

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

        level_rule = priority_resolver.resolve_level(context, level_rules, matcher)
        temperature_level = "warm"
        reasoning = ""
        if level_rule is not None:
            temperature_level = str(level_rule.get("temperature_level") or "warm")
            reasoning = str(level_rule.get("reason") or level_rule.get("description") or "")

        for rule in primary_analysis.get("special_matches") or []:
            hint = str(rule.get("temperature_level") or "").strip()
            if hint and int(rule.get("priority") or 0) >= 105:
                temperature_level = hint
                reasoning = str(rule.get("reason") or rule.get("description") or reasoning)

        recommendations = self._collect_recommendations(all_matches, level_rule)
        confidence = min(1.0, len(all_matches) / 4.0) if all_matches else 0.0
        if level_rule is not None:
            confidence = min(1.0, confidence + 0.2)

        return {
            "temperature_level": temperature_level,
            "temperature_score": normalized,
            "warm_score": context.warm_score,
            "cold_score": context.cold_score,
            "dry_score": context.dry_score,
            "humid_score": context.humid_score,
            "confidence": confidence,
            "reasoning": reasoning,
            "recommendations": recommendations,
            "raw_total": raw_total,
            "level_rule": level_rule,
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
