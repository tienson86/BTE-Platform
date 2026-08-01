"""Pack 01 Luck rule loader (read-only CSV).

Loads:
- ``database/05_phan_tich/11_dai_van`` catalog
- ``database/15_score_engine/08_luck`` support/attack/combination/clash/priority
- ``database/interpretation_rules/luck_rules.csv``
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_DAI_VAN_ROOT = _REPO_ROOT / "database" / "05_phan_tich" / "11_dai_van"
DEFAULT_SCORE_ROOT = _REPO_ROOT / "database" / "15_score_engine" / "08_luck"
DEFAULT_INTERPRETATION_CSV = (
    _REPO_ROOT / "database" / "interpretation_rules" / "luck_rules.csv"
)


class LuckRuleLoader:
    """Read-only loader for Pack 01 Luck catalog / score / interpretation rules."""

    def __init__(
        self,
        *,
        dai_van_root: str | Path | None = None,
        score_root: str | Path | None = None,
        interpretation_csv: str | Path | None = None,
    ) -> None:
        """Initialize Pack 01 Luck data paths."""
        self.dai_van_root = Path(dai_van_root) if dai_van_root else DEFAULT_DAI_VAN_ROOT
        self.score_root = Path(score_root) if score_root else DEFAULT_SCORE_ROOT
        self.interpretation_csv = (
            Path(interpretation_csv) if interpretation_csv else DEFAULT_INTERPRETATION_CSV
        )
        self._catalog_rules: list[dict[str, Any]] | None = None
        self._support_rules: list[dict[str, Any]] | None = None
        self._attack_rules: list[dict[str, Any]] | None = None
        self._combination_rules: list[dict[str, Any]] | None = None
        self._clash_rules: list[dict[str, Any]] | None = None
        self._priority_rules: list[dict[str, Any]] | None = None
        self._interpretation_rules: list[dict[str, Any]] | None = None

    def load_catalog_rules(self) -> list[dict[str, Any]]:
        """Load Dai Van analysis catalog groups."""
        if self._catalog_rules is None:
            self._catalog_rules = self._load_csv(
                self.dai_van_root / "01_danh_muc.csv"
            )
        return self._catalog_rules

    def load_support_rules(self) -> list[dict[str, Any]]:
        """Load luck support score rules."""
        if self._support_rules is None:
            self._support_rules = self._active(
                self._load_csv(self.score_root / "01_luck_support.csv")
            )
        return self._support_rules

    def load_attack_rules(self) -> list[dict[str, Any]]:
        """Load luck attack score rules."""
        if self._attack_rules is None:
            self._attack_rules = self._active(
                self._load_csv(self.score_root / "02_luck_attack.csv")
            )
        return self._attack_rules

    def load_combination_rules(self) -> list[dict[str, Any]]:
        """Load luck combination interaction score rules."""
        if self._combination_rules is None:
            self._combination_rules = self._active(
                self._load_csv(self.score_root / "03_luck_combination.csv")
            )
        return self._combination_rules

    def load_clash_rules(self) -> list[dict[str, Any]]:
        """Load luck clash interaction score rules."""
        if self._clash_rules is None:
            self._clash_rules = self._active(
                self._load_csv(self.score_root / "04_luck_clash.csv")
            )
        return self._clash_rules

    def load_priority_rules(self) -> list[dict[str, Any]]:
        """Load luck priority weights."""
        if self._priority_rules is None:
            self._priority_rules = self._load_csv(
                self.score_root / "05_luck_priority.csv"
            )
        return self._priority_rules

    def load_interpretation_rules(self) -> list[dict[str, Any]]:
        """Load narrative luck interpretation rules."""
        if self._interpretation_rules is None:
            self._interpretation_rules = self._load_csv(self.interpretation_csv)
        return self._interpretation_rules

    def catalog_by_code(self) -> dict[str, dict[str, Any]]:
        """Map ma_nhom -> catalog row."""
        return {
            str(row.get("ma_nhom") or ""): row
            for row in self.load_catalog_rules()
            if row.get("ma_nhom")
        }

    @staticmethod
    def _active(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            row
            for row in rows
            if str(row.get("status") or "active").lower() in {"active", "true", "1"}
        ]

    @staticmethod
    def _load_csv(path: Path) -> list[dict[str, Any]]:
        """Load a CSV file as list[dict]; missing/empty file -> empty."""
        if not path.exists():
            logger.warning("luck_rule_csv_missing", extra={"path": str(path)})
            return []
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except pd.errors.EmptyDataError:
            logger.warning("luck_rule_csv_empty", extra={"path": str(path)})
            return []
        if df.empty:
            return []
        return df.to_dict("records")
