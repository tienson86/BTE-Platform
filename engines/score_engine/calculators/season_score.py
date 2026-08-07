"""
Season Score Calculator

Đánh giá đắc lệnh / khí mùa từ rule ``02_wuxing/02_season_score.csv``.

Five Elements (wuxing) vẫn giữ season rules để backward compatible;
module này xuất ``season_score`` riêng theo Pack 03 scope.

Season CSV uses codes XUAN/HA/THU/DONG while RuleContext uses
spring/summer/autumn/winter — matching is done in this calculator.
"""

from __future__ import annotations

from typing import Any

from ..base.generic_score_calculator import GenericScoreCalculator

# RuleContext season labels → CSV season codes
_SEASON_CODE_MAP: dict[str, str] = {
    "spring": "XUAN",
    "xuan": "XUAN",
    "summer": "HA",
    "ha": "HA",
    "autumn": "THU",
    "fall": "THU",
    "thu": "THU",
    "winter": "DONG",
    "dong": "DONG",
}


class SeasonScoreCalculator(GenericScoreCalculator):
    """Calculator chấm điểm khí mùa (đắc lệnh)."""

    MODULE_NAME = "season"

    RULE_FOLDER = "02_wuxing"

    DIMENSION_NAME = "Khí mùa"

    DESCRIPTION = "Đánh giá mức độ đắc lệnh theo mùa sinh."

    SEASON_RULE_STEM = "02_season_score"

    def load_rules(self) -> dict[str, Any]:
        """Load only the dedicated season score CSV."""
        dataframe = self.loader.load_csv(
            f"{self.RULE_FOLDER}/{self.SEASON_RULE_STEM}.csv"
        )
        return {self.SEASON_RULE_STEM: dataframe}

    def match_rules(self, dataframe, context):
        """
        Match season rules by CSV season code + element condition.

        Shared RuleAdapter maps element+ENUM to ``wuxing.<element>.status``,
        which never equals ``IN_SEASON``. This calculator applies the intended
        season semantics without changing the shared adapter.
        """
        rule_context = self.resolve_rule_context(context)
        wuxing = rule_context.get("wuxing") or {}
        season_label = str(wuxing.get("season") or "").strip().lower()
        season_code = _SEASON_CODE_MAP.get(season_label, season_label.upper())
        season_status = str(wuxing.get("season_status") or "").strip().upper()

        matched: list[dict[str, Any]] = []
        if not season_code:
            return matched

        rows = dataframe.to_dict(orient="records") if hasattr(dataframe, "to_dict") else list(dataframe)
        for row in rows:
            row_season = str(row.get("season") or "").strip().upper()
            if row_season != season_code:
                continue
            condition = str(row.get("condition") or "").strip().upper()
            element = str(row.get("element") or "").strip().lower()
            if condition == "IN_SEASON":
                if season_status == "IN_SEASON":
                    matched.append(row)
                continue
            if not element:
                continue
            element_status = str(
                (wuxing.get(element) or {}).get("status") or ""
            ).strip().upper()
            if element_status and element_status == condition:
                matched.append(row)
        return matched

    def post_process(self, result, context):
        return result
