"""Pack 01 Shensha rule loader (read-only CSV).

Loads:
- ``database/05_phan_tich/07_than_sat`` identity / evaluation / explanation
- ``database/15_score_engine/07_shensha`` star score + priority tables
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_THAN_SAT_ROOT = _REPO_ROOT / "database" / "05_phan_tich" / "07_than_sat"
DEFAULT_SCORE_ROOT = _REPO_ROOT / "database" / "15_score_engine" / "07_shensha"


class ShenshaRuleLoader:
    """Read-only loader for Pack 01 Shensha identity / score / explanation rules."""

    def __init__(
        self,
        *,
        than_sat_root: str | Path | None = None,
        score_root: str | Path | None = None,
    ) -> None:
        """Initialize Pack 01 Shensha data paths."""
        self.than_sat_root = (
            Path(than_sat_root) if than_sat_root else DEFAULT_THAN_SAT_ROOT
        )
        self.score_root = Path(score_root) if score_root else DEFAULT_SCORE_ROOT
        self._identity_rules: list[dict[str, Any]] | None = None
        self._evaluation_rules: list[dict[str, Any]] | None = None
        self._explanation_rules: list[dict[str, Any]] | None = None
        self._conflict_rules: list[dict[str, Any]] | None = None
        self._positive_rules: list[dict[str, Any]] | None = None
        self._negative_rules: list[dict[str, Any]] | None = None
        self._domain_score_rules: list[dict[str, Any]] | None = None
        self._priority_rules: list[dict[str, Any]] | None = None

    def load_identity_rules(self) -> list[dict[str, Any]]:
        """Load Than Sat identity catalog."""
        if self._identity_rules is None:
            self._identity_rules = self._load_csv(
                self.than_sat_root / "01_than_sat.csv"
            )
        return self._identity_rules

    def load_evaluation_rules(self) -> list[dict[str, Any]]:
        """Load combination evaluation (danh gia) rules."""
        if self._evaluation_rules is None:
            self._evaluation_rules = self._load_csv(
                self.than_sat_root / "05_danh_gia.csv"
            )
        return self._evaluation_rules

    def load_explanation_rules(self) -> list[dict[str, Any]]:
        """Load explanation templates (giai thich)."""
        if self._explanation_rules is None:
            self._explanation_rules = self._load_csv(
                self.than_sat_root / "06_giai_thich_rule.csv"
            )
        return self._explanation_rules

    def load_conflict_rules(self) -> list[dict[str, Any]]:
        """Load Shensha conflict rules."""
        if self._conflict_rules is None:
            self._conflict_rules = self._load_csv(
                self.than_sat_root / "07_xung_dot_rule.csv"
            )
        return self._conflict_rules

    def load_positive_rules(self) -> list[dict[str, Any]]:
        """Load positive star score rules."""
        if self._positive_rules is None:
            self._positive_rules = self._active(
                self._load_csv(self.score_root / "01_positive_star.csv")
            )
        return self._positive_rules

    def load_negative_rules(self) -> list[dict[str, Any]]:
        """Load negative star score rules."""
        if self._negative_rules is None:
            self._negative_rules = self._active(
                self._load_csv(self.score_root / "02_negative_star.csv")
            )
        return self._negative_rules

    def load_domain_score_rules(self) -> list[dict[str, Any]]:
        """Load marriage/career/health/wealth star score rules."""
        if self._domain_score_rules is None:
            rules: list[dict[str, Any]] = []
            for name, domain in (
                ("03_marriage_star.csv", "marriage"),
                ("04_career_star.csv", "career"),
                ("05_health_star.csv", "health"),
                ("06_wealth_star.csv", "wealth"),
            ):
                for row in self._active(self._load_csv(self.score_root / name)):
                    item = dict(row)
                    item["score_domain"] = domain
                    rules.append(item)
            self._domain_score_rules = rules
        return self._domain_score_rules

    def load_priority_rules(self) -> list[dict[str, Any]]:
        """Load Shensha priority weight table."""
        if self._priority_rules is None:
            self._priority_rules = self._load_csv(
                self.score_root / "07_priority.csv"
            )
        return self._priority_rules

    def identity_by_label(self) -> dict[str, dict[str, Any]]:
        """Map normalized label / code -> identity row."""
        lookup: dict[str, dict[str, Any]] = {}
        for row in self.load_identity_rules():
            for key in ("ten_han_viet", "than_sat", "id"):
                value = str(row.get(key) or "").strip()
                if value:
                    lookup[self._norm(value)] = row
        return lookup

    def explanation_by_label(self) -> dict[str, dict[str, Any]]:
        """Map normalized than_sat label -> explanation row."""
        lookup: dict[str, dict[str, Any]] = {}
        for row in self.load_explanation_rules():
            value = str(row.get("than_sat") or "").strip()
            if value:
                lookup[self._norm(value)] = row
        return lookup

    @staticmethod
    def _active(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            row
            for row in rows
            if str(row.get("status") or "active").lower() in {"active", "true", "1"}
        ]

    @staticmethod
    def _norm(value: str) -> str:
        return value.strip().lower().replace(" ", "_").replace("-", "_")

    @staticmethod
    def _load_csv(path: Path) -> list[dict[str, Any]]:
        """Load a CSV file as list[dict]; missing/empty file -> empty."""
        if not path.exists():
            logger.warning("shensha_rule_csv_missing", extra={"path": str(path)})
            return []
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except pd.errors.EmptyDataError:
            logger.warning("shensha_rule_csv_empty", extra={"path": str(path)})
            return []
        if df.empty:
            return []
        return df.to_dict("records")
