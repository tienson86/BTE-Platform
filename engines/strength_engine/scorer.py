"""Strength score aggregation and level classification."""

from __future__ import annotations

from typing import Any


class StrengthScorer:
    """Aggregate matched rule scores and classify strength level."""

    def score(
        self,
        context: Any,
        analysis: dict[str, Any],
        config: dict[str, float],
        level_rules: list[dict[str, Any]],
        matcher: Any,
        priority_resolver: Any,
    ) -> dict[str, Any]:
        """Compute component scores, total score, and level."""
        buckets = {
            "season": 0.0,
            "root": 0.0,
            "support": 0.0,
            "drain": 0.0,
            "control": 0.0,
            "combination": 0.0,
            "special": 0.0,
        }

        matched: list[dict[str, Any]] = list(analysis.get("all_matches") or [])
        for rule in matched:
            target = str(rule.get("score_target") or rule.get("rule_group") or "")
            if target not in buckets:
                continue
            buckets[target] += float(rule.get("score") or 0.0)

        raw_total = sum(buckets.values())
        baseline = float(config.get("baseline") or 50.0)
        scale = float(config.get("scale") or 100.0)
        normalized = (raw_total + baseline) / scale if scale else 0.0
        normalized = max(0.0, min(1.0, normalized))

        context.strength_score = normalized
        context.season_score = buckets["season"] / scale if scale else 0.0
        context.root_score = buckets["root"] / scale if scale else 0.0
        context.support_score = buckets["support"] / scale if scale else 0.0
        context.drain_score = buckets["drain"] / scale if scale else 0.0
        context.control_score = buckets["control"] / scale if scale else 0.0

        level_rule = priority_resolver.resolve_level(context, level_rules, matcher)
        strength_level = "balanced"
        reasoning = ""
        if level_rule is not None:
            strength_level = str(level_rule.get("strength_level") or "balanced")
            reasoning = str(level_rule.get("reason") or level_rule.get("description") or "")

        # Special rules may override level hint
        for rule in analysis.get("special_matches") or []:
            hint = str(rule.get("strength_level") or "").strip()
            if hint and int(rule.get("priority") or 0) >= 105:
                strength_level = hint
                reasoning = str(rule.get("reason") or rule.get("description") or reasoning)

        confidence = min(1.0, len(matched) / 5.0) if matched else 0.0
        if level_rule is not None:
            confidence = min(1.0, confidence + 0.2)

        return {
            "strength_level": strength_level,
            "strength_score": normalized,
            "season_score": context.season_score,
            "root_score": context.root_score,
            "support_score": context.support_score,
            "drain_score": context.drain_score,
            "control_score": context.control_score,
            "confidence": confidence,
            "reasoning": reasoning,
            "raw_total": raw_total,
            "level_rule": level_rule,
        }
