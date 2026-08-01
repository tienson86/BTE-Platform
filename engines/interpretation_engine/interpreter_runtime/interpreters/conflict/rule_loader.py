"""Pack 01 Conflict rule loader (read-only CSV).

Loads:
- ``database/02_quan_he/dia_chi`` xung / hinh / hai / pha tables
- ``database/15_score_engine/02_wuxing/05_clash_score.csv``
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_QUAN_HE_ROOT = _REPO_ROOT / "database" / "02_quan_he" / "dia_chi"
DEFAULT_SCORE_CSV = (
    _REPO_ROOT
    / "database"
    / "15_score_engine"
    / "02_wuxing"
    / "05_clash_score.csv"
)


class ConflictRuleLoader:
    """Read-only loader for Pack 01 conflict relation + score rules."""

    def __init__(
        self,
        *,
        quan_he_root: str | Path | None = None,
        score_csv: str | Path | None = None,
    ) -> None:
        """Initialize Pack 01 conflict data paths."""
        self.quan_he_root = Path(quan_he_root) if quan_he_root else DEFAULT_QUAN_HE_ROOT
        self.score_csv = Path(score_csv) if score_csv else DEFAULT_SCORE_CSV
        self._clash_rules: list[dict[str, Any]] | None = None
        self._punishment_rules: list[dict[str, Any]] | None = None
        self._harm_rules: list[dict[str, Any]] | None = None
        self._destruction_rules: list[dict[str, Any]] | None = None
        self._score_rules: list[dict[str, Any]] | None = None

    def load_clash_rules(self) -> list[dict[str, Any]]:
        """Load Luc Xung rules."""
        if self._clash_rules is None:
            self._clash_rules = self._load_csv(self.quan_he_root / "luc_xung.csv")
        return self._clash_rules

    def load_punishment_rules(self) -> list[dict[str, Any]]:
        """Load Tuong Hinh rules."""
        if self._punishment_rules is None:
            self._punishment_rules = self._load_csv(
                self.quan_he_root / "tuong_hinh.csv"
            )
        return self._punishment_rules

    def load_harm_rules(self) -> list[dict[str, Any]]:
        """Load Luc Hai / Tuong Hai rules."""
        if self._harm_rules is None:
            rules: list[dict[str, Any]] = []
            for name in ("luc_hai.csv", "tuong_hai.csv"):
                for row in self._load_csv(self.quan_he_root / name):
                    item = dict(row)
                    item["harm_source"] = name
                    rules.append(item)
            self._harm_rules = rules
        return self._harm_rules

    def load_destruction_rules(self) -> list[dict[str, Any]]:
        """Load Tuong Pha rules."""
        if self._destruction_rules is None:
            self._destruction_rules = self._load_csv(
                self.quan_he_root / "tuong_pha.csv"
            )
        return self._destruction_rules

    def load_score_rules(self) -> list[dict[str, Any]]:
        """Load Pack 01 clash score table."""
        if self._score_rules is None:
            rows = self._load_csv(self.score_csv)
            self._score_rules = [
                row
                for row in rows
                if str(row.get("status") or "active").lower()
                in {"active", "true", "1"}
            ]
        return self._score_rules

    def score_lookup(self) -> dict[str, dict[str, Any]]:
        """Map clash_type to score rule row."""
        return {
            str(row.get("clash_type") or ""): row
            for row in self.load_score_rules()
            if row.get("clash_type")
        }

    @staticmethod
    def _load_csv(path: Path) -> list[dict[str, Any]]:
        """Load a CSV file as list[dict]; missing/empty file -> empty."""
        if not path.exists():
            logger.warning("conflict_rule_csv_missing", extra={"path": str(path)})
            return []
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except pd.errors.EmptyDataError:
            logger.warning("conflict_rule_csv_empty", extra={"path": str(path)})
            return []
        if df.empty:
            return []
        return df.to_dict("records")