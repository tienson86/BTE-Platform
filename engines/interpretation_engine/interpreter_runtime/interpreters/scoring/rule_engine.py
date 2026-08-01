"""Scoring Interpretation Rule Engine.

Enriches Pack 02 score facts with Pack 01 final-score grade/rating/confidence rules.
Does not call ScoreEngine.calculate.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.extractor import (
    ScoringDimensionFact,
    ScoringFacts,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.models import (
    ScoringItemResult,
)
from engines.interpretation_engine.interpreter_runtime.interpreters.scoring.rule_loader import (
    ScoringRuleLoader,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class ScoringRuleEngineResult:
    """Rule-engine output for Scoring Interpreter."""

    overall: tuple[ScoringItemResult, ...]
    dimensions: tuple[ScoringItemResult, ...]
    confidence: tuple[ScoringItemResult, ...]
    quality: tuple[ScoringItemResult, ...]
    overall_score: float
    confidence_value: float
    grade: str
    matched_rule_ids: tuple[str, ...]
    reasoning: str


class ScoringInterpretationRuleEngine:
    """Rule Engine for Scoring Interpreter."""

    def __init__(
        self,
        *,
        loader: ScoringRuleLoader | None = None,
    ) -> None:
        """Initialize with Pack 01 scoring rule loader."""
        self.loader = loader or ScoringRuleLoader()

    def evaluate(self, facts: ScoringFacts) -> ScoringRuleEngineResult:
        """Interpret Overall Score / Dimension Scores / Confidence / Quality."""
        weight_lookup = self.loader.dimension_weight_lookup()
        overall_score = self._resolve_overall(facts, weight_lookup)
        dimensions = tuple(
            self._enrich_dimension(item, weight_lookup=weight_lookup)
            for item in facts.dimensions
        )
        overall = self._build_overall(overall_score, facts.grade)
        confidence_value = (
            float(facts.confidence_value)
            if facts.confidence_value is not None
            else 0.0
        )
        confidence = self._build_confidence(
            confidence_value, facts.confidence_level
        )
        quality = self._build_quality(
            overall_score=overall_score,
            grade_hint=facts.grade or facts.quality_label,
            dimensions=dimensions,
        )
        grade = ""
        if overall:
            grade = overall[0].level or str(overall[0].attributes.get("grade") or "")

        matched_ids = list(facts.matched_rules)
        for item in (*overall, *dimensions, *confidence, *quality):
            for key in (
                "pack01_rule_id",
                "grade_rule_id",
                "rating_rule_id",
                "confidence_rule_id",
                "recommendation_rule_id",
                "weight_rule_id",
            ):
                rule_id = str(item.attributes.get(key) or "")
                if rule_id:
                    matched_ids.append(rule_id)

        seen: set[str] = set()
        ordered_ids: list[str] = []
        for rule_id in matched_ids:
            if rule_id and rule_id not in seen:
                seen.add(rule_id)
                ordered_ids.append(rule_id)

        reasoning = facts.reasoning
        if not reasoning:
            parts = [
                f"overall={overall_score}",
                f"dimensions={len(dimensions)}",
                f"confidence={confidence_value}",
                f"grade={grade or '-'}",
            ]
            reasoning = "Scoring interpretation: " + ", ".join(parts)

        logger.info(
            "scoring_rule_engine_evaluated",
            extra={
                "overall_score": overall_score,
                "dimension_count": len(dimensions),
                "confidence_value": confidence_value,
                "grade": grade,
            },
        )

        return ScoringRuleEngineResult(
            overall=overall,
            dimensions=dimensions,
            confidence=confidence,
            quality=quality,
            overall_score=overall_score,
            confidence_value=confidence_value,
            grade=grade,
            matched_rule_ids=tuple(ordered_ids),
            reasoning=reasoning,
        )

    def _resolve_overall(
        self,
        facts: ScoringFacts,
        weight_lookup: dict[str, dict[str, Any]],
    ) -> float:
        """Use Pack 02 overall when present; else weighted dimension aggregate."""
        if facts.overall_score is not None:
            return float(facts.overall_score)
        if not facts.dimensions:
            return 0.0

        weighted_sum = 0.0
        weight_total = 0.0
        for item in facts.dimensions:
            row = weight_lookup.get(item.dimension.upper())
            weight = float((row or {}).get("weight") or 0.0)
            if weight <= 0.0:
                continue
            weighted_sum += float(item.value) * weight
            weight_total += weight
        if weight_total > 0.0:
            return weighted_sum / weight_total
        return sum(float(item.value) for item in facts.dimensions) / len(facts.dimensions)

    def _build_overall(
        self,
        overall_score: float,
        grade_hint: str,
    ) -> tuple[ScoringItemResult, ...]:
        """Build overall score item with Pack 01 grade + recommendation."""
        grade_row = self._match_grade(overall_score, grade_hint)
        reco_row = self._match_recommendation(overall_score)
        grade = str((grade_row or {}).get("grade") or grade_hint or "")
        level = str((grade_row or {}).get("level") or grade)
        return (
            ScoringItemResult(
                item_id="overall",
                item_type="overall",
                label="Overall Score",
                value=overall_score,
                level=grade or level,
                rating=level,
                score=overall_score,
                priority=int(float((grade_row or {}).get("min_score") or 0)),
                description=str((grade_row or {}).get("description") or ""),
                recommendation=str((reco_row or {}).get("recommendation") or ""),
                attributes={
                    "grade": grade,
                    "grade_rule_id": str((grade_row or {}).get("id") or ""),
                    "recommendation_rule_id": str((reco_row or {}).get("id") or ""),
                    "recommendation_level": str(
                        (reco_row or {}).get("recommendation_level") or ""
                    ),
                },
            ),
        )

    def _enrich_dimension(
        self,
        fact: ScoringDimensionFact,
        *,
        weight_lookup: dict[str, dict[str, Any]],
    ) -> ScoringItemResult:
        """Enrich one dimension score with Pack 01 rating + weight."""
        dimension = fact.dimension.upper()
        rating_row = self._match_rating(dimension, fact.value)
        weight_row = weight_lookup.get(dimension)
        weight = float((weight_row or {}).get("weight") or 0.0)
        priority = int(float((weight_row or {}).get("priority") or 0))
        return ScoringItemResult(
            item_id=dimension,
            item_type="dimension",
            label=dimension,
            value=float(fact.value),
            level=str((rating_row or {}).get("rating") or ""),
            rating=str((rating_row or {}).get("rating") or ""),
            score=float(fact.value) * weight if weight else float(fact.value),
            priority=priority,
            description=str((rating_row or {}).get("description") or ""),
            attributes={
                "rating_rule_id": str((rating_row or {}).get("id") or ""),
                "weight_rule_id": str((weight_row or {}).get("id") or ""),
                "weight": weight,
                "unit": fact.unit,
                "raw_value": float(fact.value),
            },
        )

    def _build_confidence(
        self,
        confidence_value: float,
        confidence_level_hint: str,
    ) -> tuple[ScoringItemResult, ...]:
        """Build confidence item from Pack 01 confidence bands."""
        row = self._match_confidence(confidence_value, confidence_level_hint)
        level = str(
            (row or {}).get("confidence_level") or confidence_level_hint or ""
        )
        return (
            ScoringItemResult(
                item_id="confidence",
                item_type="confidence",
                label="Confidence",
                value=confidence_value,
                level=level,
                rating=level,
                score=confidence_value,
                priority=int(float((row or {}).get("min_value") or 0)),
                description=str((row or {}).get("description") or ""),
                attributes={
                    "confidence_rule_id": str((row or {}).get("id") or ""),
                    "confidence_level": level,
                },
            ),
        )

    def _build_quality(
        self,
        *,
        overall_score: float,
        grade_hint: str,
        dimensions: tuple[ScoringItemResult, ...],
    ) -> tuple[ScoringItemResult, ...]:
        """Build quality view from grade + recommendation + dimension ratings."""
        grade_row = self._match_grade(overall_score, grade_hint)
        reco_row = self._match_recommendation(overall_score)
        grade = str((grade_row or {}).get("grade") or grade_hint or "")
        level = str((grade_row or {}).get("level") or "")
        items: list[ScoringItemResult] = [
            ScoringItemResult(
                item_id="quality_grade",
                item_type="quality",
                label="Grade Quality",
                value=overall_score,
                level=grade,
                rating=level,
                score=overall_score,
                priority=100,
                description=str((grade_row or {}).get("description") or ""),
                recommendation=str((reco_row or {}).get("recommendation") or ""),
                attributes={
                    "grade_rule_id": str((grade_row or {}).get("id") or ""),
                    "recommendation_rule_id": str((reco_row or {}).get("id") or ""),
                    "recommendation_level": str(
                        (reco_row or {}).get("recommendation_level") or ""
                    ),
                },
            )
        ]
        for dim in dimensions:
            if not dim.rating:
                continue
            items.append(
                ScoringItemResult(
                    item_id=f"quality_{dim.item_id}",
                    item_type="quality_dimension",
                    label=dim.label,
                    value=dim.value,
                    level=dim.level,
                    rating=dim.rating,
                    score=dim.score,
                    priority=dim.priority,
                    description=dim.description,
                    attributes={
                        "rating_rule_id": dim.attributes.get("rating_rule_id", ""),
                        "dimension": dim.item_id,
                    },
                )
            )
        return tuple(items)

    def _match_grade(
        self,
        score: float,
        grade_hint: str,
    ) -> dict[str, Any] | None:
        """Match Pack 01 grade band by score range or explicit grade hint."""
        hint = (grade_hint or "").strip().upper()
        for row in self.loader.load_grade_rules():
            if hint and str(row.get("grade") or "").upper() == hint:
                return row
        for row in self.loader.load_grade_rules():
            low = float(row.get("min_score") or 0.0)
            high = float(row.get("max_score") or 100.0)
            if low <= score <= high:
                return row
        return None

    def _match_recommendation(self, score: float) -> dict[str, Any] | None:
        """Match Pack 01 recommendation band by overall score."""
        for row in self.loader.load_recommendation_rules():
            low = float(row.get("min_score") or 0.0)
            high = float(row.get("max_score") or 100.0)
            if low <= score <= high:
                return row
        return None

    def _match_rating(
        self,
        dimension: str,
        score: float,
    ) -> dict[str, Any] | None:
        """Match Pack 01 dimension rating; fallback to STRENGTH bands."""
        rows = [
            row
            for row in self.loader.load_rating_rules()
            if str(row.get("dimension") or "").upper() == dimension.upper()
        ]
        matched = self._match_score_band(rows, score, min_key="min_score", max_key="max_score")
        if matched is not None:
            return matched
        # Pack 01 only fully populates STRENGTH bands; reuse as generic scale.
        fallback = [
            row
            for row in self.loader.load_rating_rules()
            if str(row.get("dimension") or "").upper() == "STRENGTH"
        ]
        return self._match_score_band(
            fallback, score, min_key="min_score", max_key="max_score"
        )

    def _match_confidence(
        self,
        value: float,
        level_hint: str,
    ) -> dict[str, Any] | None:
        """Match Pack 01 confidence level by value or hint."""
        hint = (level_hint or "").strip().upper()
        for row in self.loader.load_confidence_rules():
            if hint and str(row.get("confidence_level") or "").upper() == hint:
                return row
        return self._match_score_band(
            self.loader.load_confidence_rules(),
            value,
            min_key="min_value",
            max_key="max_value",
        )

    @staticmethod
    def _match_score_band(
        rows: list[dict[str, Any]],
        score: float,
        *,
        min_key: str,
        max_key: str,
    ) -> dict[str, Any] | None:
        """Find first band containing score."""
        for row in rows:
            low = float(row.get(min_key) or 0.0)
            high = float(row.get(max_key) or 100.0)
            if low <= score <= high:
                return row
        return None
