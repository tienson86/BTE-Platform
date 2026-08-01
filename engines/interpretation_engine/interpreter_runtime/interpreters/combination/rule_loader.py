"""Pack 01 Combination rule loader (read-only CSV).

Loads:
- ``database/02_quan_he`` stem/branch combination tables
- ``database/15_score_engine/02_wuxing/04_combination_score.csv``
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_QUAN_HE_ROOT = _REPO_ROOT / "database" / "02_quan_he"
DEFAULT_SCORE_CSV = (
    _REPO_ROOT
    / "database"
    / "15_score_engine"
    / "02_wuxing"
    / "04_combination_score.csv"
)


class CombinationRuleLoader:
    """Read-only loader for Pack 01 combination relation + score rules."""

    def __init__(
        self,
        *,
        quan_he_root: str | Path | None = None,
        score_csv: str | Path | None = None,
    ) -> None:
        """Initialize Pack 01 combination data paths."""
        self.quan_he_root = Path(quan_he_root) if quan_he_root else DEFAULT_QUAN_HE_ROOT
        self.score_csv = Path(score_csv) if score_csv else DEFAULT_SCORE_CSV
        self._stem_rules: list[dict[str, Any]] | None = None
        self._branch_rules: list[dict[str, Any]] | None = None
        self._score_rules: list[dict[str, Any]] | None = None

    def load_stem_rules(self) -> list[dict[str, Any]]:
        """Load Thiên Can hợp rules."""
        if self._stem_rules is None:
            path = self.quan_he_root / "thien_can" / "du_lieu.csv"
            self._stem_rules = self._load_csv(path)
        return self._stem_rules

    def load_branch_rules(self) -> list[dict[str, Any]]:
        """Load Địa Chi lục hợp / tam hợp / bán hợp / tam hội rules."""
        if self._branch_rules is None:
            files = (
                ("luc_hop", "dia_chi/luc_hop.csv"),
                ("tam_hop", "dia_chi/tam_hop.csv"),
                ("ban_hop", "dia_chi/ban_hop.csv"),
                ("tam_hoi", "dia_chi/tam_hoi.csv"),
            )
            rules: list[dict[str, Any]] = []
            for group, relative in files:
                path = self.quan_he_root / relative
                for row in self._load_csv(path):
                    item = dict(row)
                    item["branch_group"] = group
                    rules.append(item)
            self._branch_rules = rules
        return self._branch_rules

    def load_score_rules(self) -> list[dict[str, Any]]:
        """Load Pack 01 combination score table."""
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
        """Map combination_type → score rule row."""
        return {
            str(row.get("combination_type") or ""): row
            for row in self.load_score_rules()
            if row.get("combination_type")
        }

    @staticmethod
    def _load_csv(path: Path) -> list[dict[str, Any]]:
        """Load a CSV file as list[dict]; missing file → empty."""
        if not path.exists():
            logger.warning("combination_rule_csv_missing", extra={"path": str(path)})
            return []
        df = pd.read_csv(path, encoding="utf-8")
        return df.to_dict("records")
