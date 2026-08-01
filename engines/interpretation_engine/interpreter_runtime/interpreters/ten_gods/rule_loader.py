"""Pack 01 Ten Gods rule loader (read-only CSV).

Loads:
- ``database/01_du_lieu_goc/thap_than/du_lieu.csv``
- ``database/05_phan_tich/03_than_vuong_than_nhuoc/diem_thap_than.csv``
- ``database/15_score_engine/04_ten_gods/*.csv``
- ``database/interpretation_rules/ten_gods_rules.csv``
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_IDENTITY_CSV = (
    _REPO_ROOT / "database" / "01_du_lieu_goc" / "thap_than" / "du_lieu.csv"
)
DEFAULT_STRENGTH_CSV = (
    _REPO_ROOT
    / "database"
    / "05_phan_tich"
    / "03_than_vuong_than_nhuoc"
    / "diem_thap_than.csv"
)
DEFAULT_SCORE_ROOT = _REPO_ROOT / "database" / "15_score_engine" / "04_ten_gods"
DEFAULT_INTERPRETATION_CSV = (
    _REPO_ROOT / "database" / "interpretation_rules" / "ten_gods_rules.csv"
)


class TenGodsRuleLoader:
    """Read-only loader for Pack 01 Ten Gods identity / strength / score rules."""

    def __init__(
        self,
        *,
        identity_csv: str | Path | None = None,
        strength_csv: str | Path | None = None,
        score_root: str | Path | None = None,
        interpretation_csv: str | Path | None = None,
    ) -> None:
        """Initialize Pack 01 Ten Gods data paths."""
        self.identity_csv = Path(identity_csv) if identity_csv else DEFAULT_IDENTITY_CSV
        self.strength_csv = Path(strength_csv) if strength_csv else DEFAULT_STRENGTH_CSV
        self.score_root = Path(score_root) if score_root else DEFAULT_SCORE_ROOT
        self.interpretation_csv = (
            Path(interpretation_csv) if interpretation_csv else DEFAULT_INTERPRETATION_CSV
        )
        self._identity_rules: list[dict[str, Any]] | None = None
        self._strength_rules: list[dict[str, Any]] | None = None
        self._positive_rules: list[dict[str, Any]] | None = None
        self._negative_rules: list[dict[str, Any]] | None = None
        self._combination_rules: list[dict[str, Any]] | None = None
        self._structure_rules: list[dict[str, Any]] | None = None
        self._priority_rules: list[dict[str, Any]] | None = None
        self._interpretation_rules: list[dict[str, Any]] | None = None

    def load_identity_rules(self) -> list[dict[str, Any]]:
        """Load Ten Gods identity catalog."""
        if self._identity_rules is None:
            self._identity_rules = self._load_csv(self.identity_csv)
        return self._identity_rules

    def load_strength_rules(self) -> list[dict[str, Any]]:
        """Load Than Vuong / Nhuoc Ten God strength points."""
        if self._strength_rules is None:
            self._strength_rules = self._load_csv(self.strength_csv)
        return self._strength_rules

    def load_positive_rules(self) -> list[dict[str, Any]]:
        """Load positive Ten God score rules."""
        if self._positive_rules is None:
            self._positive_rules = self._active(
                self._load_csv(self.score_root / "01_positive_score.csv")
            )
        return self._positive_rules

    def load_negative_rules(self) -> list[dict[str, Any]]:
        """Load negative Ten God score rules."""
        if self._negative_rules is None:
            self._negative_rules = self._active(
                self._load_csv(self.score_root / "02_negative_score.csv")
            )
        return self._negative_rules

    def load_combination_rules(self) -> list[dict[str, Any]]:
        """Load Ten God combination / interaction score rules."""
        if self._combination_rules is None:
            self._combination_rules = self._active(
                self._load_csv(self.score_root / "03_combination_score.csv")
            )
        return self._combination_rules

    def load_structure_rules(self) -> list[dict[str, Any]]:
        """Load Ten God structure score rules."""
        if self._structure_rules is None:
            self._structure_rules = self._active(
                self._load_csv(self.score_root / "04_structure_score.csv")
            )
        return self._structure_rules

    def load_priority_rules(self) -> list[dict[str, Any]]:
        """Load Ten God priority weights."""
        if self._priority_rules is None:
            self._priority_rules = self._load_csv(self.score_root / "06_priority.csv")
        return self._priority_rules

    def load_interpretation_rules(self) -> list[dict[str, Any]]:
        """Load narrative Ten Gods interpretation rules."""
        if self._interpretation_rules is None:
            self._interpretation_rules = self._load_csv(self.interpretation_csv)
        return self._interpretation_rules

    def identity_by_label(self) -> dict[str, dict[str, Any]]:
        """Map normalized label / code -> identity row."""
        lookup: dict[str, dict[str, Any]] = {}
        for row in self.load_identity_rules():
            for key in ("ten", "ma_thap_than", "ten_han"):
                value = str(row.get(key) or "").strip()
                if value:
                    lookup[self._norm(value)] = row
        return lookup

    def strength_by_label(self) -> dict[str, dict[str, Any]]:
        """Map Vietnamese Ten God label -> strength point row."""
        return {
            self._norm(str(row.get("thap_than") or "")): row
            for row in self.load_strength_rules()
            if row.get("thap_than")
        }

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
            logger.warning("ten_gods_rule_csv_missing", extra={"path": str(path)})
            return []
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except pd.errors.EmptyDataError:
            logger.warning("ten_gods_rule_csv_empty", extra={"path": str(path)})
            return []
        if df.empty:
            return []
        return df.to_dict("records")
