"""Build Pack 03 AnalysisResult from ScoreResult + RuleContext."""

from __future__ import annotations

from typing import Any

from engines.score_engine.result import ScoreResult

from .analysis_result import AnalysisResult
from .nodes import (
    ConfidenceSummary,
    ElementScore,
    Evidence,
    EvidenceCollection,
    FiveElementAnalysis,
    OverallAnalysis,
    PatternAnalysis,
    SeasonAnalysis,
    StrengthAnalysis,
    TemperatureAnalysis,
    TenGodAnalysis,
    TenGodItem,
    UsefulGodAnalysis,
)

_ELEMENT_KEYS = ("wood", "fire", "earth", "metal", "water")

_STRENGTH_LABELS = (
    (80.0, "Follow Strong"),
    (70.0, "Strong"),
    (40.0, "Balanced"),
    (20.0, "Weak"),
    (0.0, "Follow Weak"),
)


class AnalysisResultBuilder:
    """Construct the Pack 03 AnalysisResult aggregate."""

    def build(
        self,
        score_result: ScoreResult,
        rule_context: dict[str, Any] | None = None,
    ) -> AnalysisResult:
        """
        Build AnalysisResult from production ScoreResult.

        Parameters
        ----------
        score_result:
            Output of ``ScoreEngine.calculate``.
        rule_context:
            Optional RuleContext used for season / temperature / element facts.
        """
        context = rule_context or {}
        details = score_result.details or {}
        evidence = self._collect_evidence(details)

        strength_score = float(score_result.strength_score or 0.0)
        season_score = float(score_result.season_score or 0.0)
        temperature_score = float(score_result.temperature_score or 0.0)
        five_elements_score = float(score_result.five_elements_score or 0.0)
        ten_god_score = float(score_result.ten_god_score or 0.0)
        pattern_score = float(score_result.pattern_score or 0.0)
        useful_god_score = float(score_result.useful_god_score or 0.0)
        overall_score = float(score_result.overall_score or 0.0)

        wuxing = context.get("wuxing") or {}
        temperature = context.get("temperature") or {}
        pattern = context.get("pattern") or {}
        useful_god = context.get("useful_god") or {}

        by_dimension = {
            "strength": self._score_confidence(strength_score),
            "season": self._score_confidence(season_score),
            "temperature": self._score_confidence(temperature_score),
            "five_elements": self._score_confidence(five_elements_score),
            "ten_gods": self._score_confidence(ten_god_score),
            "pattern": self._score_confidence(pattern_score),
            "useful_god": self._score_confidence(useful_god_score),
            "overall": self._score_confidence(overall_score),
        }

        return AnalysisResult(
            strength=StrengthAnalysis(
                value=self._strength_value(strength_score),
                score=strength_score,
                confidence=by_dimension["strength"],
                matched_rules=self._matched(details, "strength"),
            ),
            season=SeasonAnalysis(
                season=str(wuxing.get("season") or context.get("birth_season") or ""),
                season_status=str(wuxing.get("season_status") or ""),
                score=season_score,
                confidence=by_dimension["season"],
                matched_rules=self._matched(details, "season"),
            ),
            temperature=TemperatureAnalysis(
                status=str(
                    temperature.get("status") or temperature.get("result") or ""
                ),
                score=temperature_score,
                cold_score=float(temperature.get("cold_score") or 0.0),
                hot_score=float(temperature.get("hot_score") or 0.0),
                confidence=by_dimension["temperature"],
                matched_rules=self._matched(details, "temperature"),
            ),
            five_elements=FiveElementAnalysis(
                score=five_elements_score,
                confidence=by_dimension["five_elements"],
                elements=self._element_scores(wuxing, season_score),
                matched_rules=self._matched(details, "wuxing"),
            ),
            ten_gods=TenGodAnalysis(
                score=ten_god_score,
                confidence=by_dimension["ten_gods"],
                items=self._ten_god_items(score_result, context),
                matched_rules=self._matched(details, "ten_gods"),
            ),
            pattern=PatternAnalysis(
                pattern_name=str(
                    pattern.get("name")
                    or pattern.get("pattern_name")
                    or pattern.get("primary")
                    or ""
                ),
                pattern_category=str(
                    pattern.get("category") or pattern.get("type") or ""
                ),
                score=pattern_score,
                confidence=by_dimension["pattern"],
                matched_rules=self._matched(details, "pattern"),
            ),
            useful_god=UsefulGodAnalysis(
                useful_god=str(
                    useful_god.get("useful_god")
                    or useful_god.get("primary")
                    or useful_god.get("name")
                    or ""
                ),
                favorable_elements=list(
                    useful_god.get("favorable_elements")
                    or useful_god.get("hy_than")
                    or []
                ),
                unfavorable_elements=list(
                    useful_god.get("unfavorable_elements")
                    or useful_god.get("ky_than")
                    or []
                ),
                score=useful_god_score,
                confidence=by_dimension["useful_god"],
                matched_rules=self._matched(details, "useful_god"),
            ),
            overall=OverallAnalysis(
                overall_score=overall_score,
                overall_confidence=str(score_result.confidence or ""),
                grade=str(score_result.grade or ""),
                summary_code=str(score_result.grade or ""),
                recommendation_code=str(score_result.recommendation or ""),
            ),
            evidence=evidence,
            confidence=ConfidenceSummary(
                overall=str(score_result.confidence or ""),
                by_dimension=by_dimension,
            ),
            success=bool(score_result.success),
            metadata={
                "source": "ScoreEngine.calculate",
                "pack": "03",
                "modules": list(score_result.modules),
            },
        )

    @staticmethod
    def _matched(details: dict[str, Any], module: str) -> list[dict[str, Any]]:
        calc = details.get(module)
        if calc is None:
            return []
        rules = getattr(calc, "matched_rules", None)
        if rules is None and isinstance(calc, dict):
            rules = calc.get("matched_rules")
        return list(rules or [])

    def _collect_evidence(self, details: dict[str, Any]) -> EvidenceCollection:
        collection = EvidenceCollection()
        index = 0
        for module_name, calc in details.items():
            rules = self._matched(details, module_name)
            for rule in rules:
                index += 1
                code = str(
                    rule.get("rule_code")
                    or rule.get("id")
                    or rule.get("rule_id")
                    or f"{module_name}_{index}"
                )
                collection.add(
                    Evidence(
                        evidence_id=f"EV-{index:04d}-{code}",
                        source=code,
                        category=module_name,
                        description=str(rule.get("description", "") or ""),
                        weight=float(rule.get("score", 0) or 0),
                        priority=int(float(rule.get("priority", 0) or 0)),
                    )
                )
        return collection

    @staticmethod
    def _strength_value(score: float) -> str:
        for threshold, label in _STRENGTH_LABELS:
            if score >= threshold:
                return label
        return "unknown"

    @staticmethod
    def _score_confidence(score: float) -> float:
        if score >= 80:
            return 0.9
        if score >= 50:
            return 0.7
        if score > 0:
            return 0.5
        return 0.0

    @staticmethod
    def _element_scores(
        wuxing: dict[str, Any],
        season_score: float,
    ) -> list[ElementScore]:
        counts = wuxing.get("counts") or {}
        elements: list[ElementScore] = []
        for key in _ELEMENT_KEYS:
            entry = wuxing.get(key) or {}
            structural = float(
                counts.get(key)
                if counts.get(key) is not None
                else entry.get("count") or 0.0
            )
            elements.append(
                ElementScore(
                    name=key,
                    structural_score=structural,
                    seasonal_score=float(season_score or 0.0),
                    final_score=structural,
                    confidence=0.7 if structural > 0 else 0.0,
                )
            )
        return elements

    @staticmethod
    def _ten_god_items(
        score_result: ScoreResult,
        context: dict[str, Any],
    ) -> list[TenGodItem]:
        series = list(score_result.ten_god_series or [])
        if series:
            return [
                TenGodItem(
                    name=str(item.get("label") or ""),
                    value=float(item.get("value") or 0.0),
                    score=float(item.get("value") or 0.0),
                    confidence=0.7,
                )
                for item in series
                if item.get("label")
            ]

        ten_gods = context.get("ten_gods") or {}
        items = list(ten_gods.get("items") or [])
        counts: dict[str, int] = {}
        for name in items:
            label = str(name or "").strip()
            if not label or label == "Nhật Chủ":
                continue
            counts[label] = counts.get(label, 0) + 1
        return [
            TenGodItem(name=name, value=float(count), score=float(count), confidence=0.7)
            for name, count in counts.items()
        ]
