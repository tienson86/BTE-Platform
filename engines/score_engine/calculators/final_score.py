"""
Final Score Calculator

WP2C:
    Aggregate weighted module scores using:
    - database/15_score_engine/01_weight/module_weight.csv
    - database/15_score_engine/09_final_score/04_dimension_weight.csv

    Grade lookup from 01_grade.csv.
"""

from __future__ import annotations

from typing import Any

from ..base.generic_score_calculator import GenericScoreCalculator


# Map calculator module_name → weight codes in CSV
MODULE_CODE_MAP: dict[str, str] = {
    "wuxing": "WUXING",
    "strength": "STRENGTH",
    "ten_gods": "TEN_GODS",
    "pattern": "PATTERN",
    "useful_god": "USEFUL_GOD",
    "shensha": "SHENSHA",
    "luck": "LUCK",
}


class FinalScoreCalculator(GenericScoreCalculator):
    """Tổng hợp và xếp hạng toàn bộ Score Engine."""

    MODULE_NAME = "final_score"

    RULE_FOLDER = "09_final_score"

    DIMENSION_NAME = "Điểm tổng"

    DESCRIPTION = (
        "Tổng hợp và xếp hạng toàn bộ Score Engine."
    )

    def calculate(self, context):
        """
        Weighted aggregation — does not rely on grade CSV matching alone.
        """
        result = self.create_result()
        rule_context = self.resolve_rule_context(context)

        module_scores = self._extract_module_scores(rule_context)
        weights, weight_source = self._load_weights()

        weighted_parts: dict[str, float] = {}
        total = 0.0

        for module_name, raw_score in module_scores.items():
            code = MODULE_CODE_MAP.get(module_name, module_name.upper())
            weight = float(weights.get(code, 0.0) or 0.0)
            part = float(raw_score or 0.0) * weight
            weighted_parts[module_name] = round(part, 4)
            total += part

        total = self.normalize_score(total)
        grade_info = self._lookup_grade(total)

        result.score = total
        result.weighted_score = total
        result.weight = 1.0
        result.matched_rules = []
        result.details = {
            "grade": grade_info.get("grade", ""),
            "level": grade_info.get("level", ""),
            "confidence": self._confidence_from_score(total),
            "recommendation": grade_info.get("description", ""),
            "module_scores": module_scores,
            "weights": weights,
            "weight_source": weight_source,
            "weighted_parts": weighted_parts,
        }
        result.success = True
        return result

    def post_process(self, result, context):
        return result

    # ==================================================

    def _extract_module_scores(self, context: dict[str, Any]) -> dict[str, float]:
        score_section = context.get("score") or {}
        module_scores = score_section.get("module_scores")
        if isinstance(module_scores, dict) and module_scores:
            return {
                key: float(value or 0.0)
                for key, value in module_scores.items()
            }

        # Fallback flat fields
        mapping = {
            "wuxing": "wuxing_score",
            "strength": "strength_score",
            "ten_gods": "ten_god_score",
            "pattern": "pattern_score",
            "useful_god": "useful_god_score",
            "shensha": "shensha_score",
            "luck": "luck_score",
        }
        return {
            module: float(score_section.get(field, 0.0) or 0.0)
            for module, field in mapping.items()
        }

    def _load_weights(self) -> tuple[dict[str, float], str]:
        """
        Prefer dimension_weight (fractions). Fallback to module_weight / 100.
        """
        dimension = self._safe_load_csv("09_final_score/04_dimension_weight.csv")
        if dimension is not None and not dimension.empty:
            weights: dict[str, float] = {}
            for _, row in dimension.iterrows():
                code = str(row.get("module", "")).strip().upper()
                if not code:
                    continue
                weights[code] = float(row.get("weight", 0) or 0)
            if weights:
                return weights, "09_final_score/04_dimension_weight.csv"

        module_weight = self._safe_load_csv("01_weight/module_weight.csv")
        if module_weight is not None and not module_weight.empty:
            weights = {}
            for _, row in module_weight.iterrows():
                code = str(row.get("module_code", "")).strip().upper()
                if not code:
                    continue
                # Percent weights → fraction
                weights[code] = float(row.get("weight", 0) or 0) / 100.0
            if weights:
                return weights, "01_weight/module_weight.csv"

        # Equal weights fallback
        equal = {code: 1.0 / len(MODULE_CODE_MAP) for code in MODULE_CODE_MAP.values()}
        return equal, "equal_fallback"

    def _lookup_grade(self, total_score: float) -> dict[str, Any]:
        grade_df = self._safe_load_csv("09_final_score/01_grade.csv")
        if grade_df is None or grade_df.empty:
            return {"grade": "", "level": "", "description": ""}

        # Some description cells contain unquoted commas; pandas may promote
        # the rule id to the index and shift columns. Normalize each row.
        for index, row in grade_df.iterrows():
            parsed = self._parse_grade_row(index, row)
            if parsed is None:
                continue
            if parsed["min_score"] <= total_score <= parsed["max_score"]:
                return {
                    "grade": parsed["grade"],
                    "level": parsed["level"],
                    "description": parsed["description"],
                }

        return {"grade": "", "level": "", "description": ""}

    @staticmethod
    def _parse_grade_row(index: Any, row: Any) -> dict[str, Any] | None:
        """
        Parse one grade row, tolerating CSV column shift from unquoted commas.
        """
        def _clean_cell(value: Any) -> str:
            if value is None:
                return ""
            text = str(value).strip()
            if text.lower() in {"", "nan", "none"}:
                return ""
            return text

        # Normal layout: id, grade, min_score, max_score, level, description
        try:
            low = float(row.get("min_score"))
            high = float(row.get("max_score"))
            return {
                "grade": _clean_cell(row.get("grade")),
                "level": _clean_cell(row.get("level")),
                "description": _clean_cell(row.get("description")),
                "min_score": low,
                "max_score": high,
            }
        except (TypeError, ValueError):
            pass

        # Shifted layout after unquoted comma in description:
        # index=id, id=grade, grade=min, min_score=max, max_score=level, ...
        try:
            low = float(row.get("grade"))
            high = float(row.get("min_score"))
            level = _clean_cell(row.get("max_score"))
            desc_left = _clean_cell(row.get("level"))
            desc_right = _clean_cell(row.get("description"))
            description = (
                f"{desc_left},{desc_right}".strip(" ,")
                if desc_right
                else desc_left
            )
            return {
                "grade": _clean_cell(row.get("id")),
                "level": level,
                "description": description,
                "min_score": low,
                "max_score": high,
            }
        except (TypeError, ValueError):
            return None

    def _safe_load_csv(self, relative_path: str):
        try:
            return self.loader.load_csv(relative_path)
        except Exception:
            return None

    @staticmethod
    def _confidence_from_score(total_score: float) -> str:
        if total_score >= 80:
            return "high"
        if total_score >= 50:
            return "medium"
        return "low"
