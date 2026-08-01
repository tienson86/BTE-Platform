"""Pack 01 Scoring rule loader (read-only CSV).

Loads:
- ``database/15_score_engine/09_final_score/*.csv``
- ``database/15_score_engine/01_weight/module_weight.csv``
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_FINAL_SCORE_ROOT = (
    _REPO_ROOT / "database" / "15_score_engine" / "09_final_score"
)
DEFAULT_MODULE_WEIGHT_CSV = (
    _REPO_ROOT / "database" / "15_score_engine" / "01_weight" / "module_weight.csv"
)


class ScoringRuleLoader:
    """Read-only loader for Pack 01 final-score / quality / confidence rules."""

    def __init__(
        self,
        *,
        final_score_root: str | Path | None = None,
        module_weight_csv: str | Path | None = None,
    ) -> None:
        """Initialize Pack 01 scoring data paths."""
        self.final_score_root = (
            Path(final_score_root) if final_score_root else DEFAULT_FINAL_SCORE_ROOT
        )
        self.module_weight_csv = (
            Path(module_weight_csv) if module_weight_csv else DEFAULT_MODULE_WEIGHT_CSV
        )
        self._grade_rules: list[dict[str, Any]] | None = None
        self._rating_rules: list[dict[str, Any]] | None = None
        self._confidence_rules: list[dict[str, Any]] | None = None
        self._dimension_weights: list[dict[str, Any]] | None = None
        self._recommendation_rules: list[dict[str, Any]] | None = None
        self._output_mapping: list[dict[str, Any]] | None = None
        self._module_weights: list[dict[str, Any]] | None = None

    def load_grade_rules(self) -> list[dict[str, Any]]:
        """Load overall grade bands."""
        if self._grade_rules is None:
            # Descriptions may contain unquoted commas — use flexible CSV parse.
            self._grade_rules = self._load_csv_flexible(
                self.final_score_root / "01_grade.csv"
            )
        return self._grade_rules

    def load_rating_rules(self) -> list[dict[str, Any]]:
        """Load dimension star-rating bands."""
        if self._rating_rules is None:
            self._rating_rules = self._load_csv_flexible(
                self.final_score_root / "02_rating.csv"
            )
        return self._rating_rules

    def load_confidence_rules(self) -> list[dict[str, Any]]:
        """Load confidence level bands."""
        if self._confidence_rules is None:
            self._confidence_rules = self._load_csv_flexible(
                self.final_score_root / "03_confidence.csv"
            )
        return self._confidence_rules

    def load_dimension_weights(self) -> list[dict[str, Any]]:
        """Load final-score dimension weights."""
        if self._dimension_weights is None:
            self._dimension_weights = self._load_csv_flexible(
                self.final_score_root / "04_dimension_weight.csv"
            )
        return self._dimension_weights

    def load_recommendation_rules(self) -> list[dict[str, Any]]:
        """Load recommendation bands by overall score."""
        if self._recommendation_rules is None:
            self._recommendation_rules = self._load_csv_flexible(
                self.final_score_root / "05_recommendation.csv"
            )
        return self._recommendation_rules

    def load_output_mapping(self) -> list[dict[str, Any]]:
        """Load score output field mapping."""
        if self._output_mapping is None:
            self._output_mapping = self._load_csv_flexible(
                self.final_score_root / "06_output_mapping.csv"
            )
        return self._output_mapping

    def load_module_weights(self) -> list[dict[str, Any]]:
        """Load module weight table."""
        if self._module_weights is None:
            rows = self._load_csv_flexible(self.module_weight_csv)
            self._module_weights = [
                row
                for row in rows
                if str(row.get("status") or "active").lower()
                in {"active", "true", "1"}
            ]
        return self._module_weights

    def dimension_weight_lookup(self) -> dict[str, dict[str, Any]]:
        """Map module code -> dimension weight row."""
        lookup: dict[str, dict[str, Any]] = {}
        for row in self.load_dimension_weights():
            module = str(row.get("module") or "").upper()
            if module:
                lookup[module] = row
        return lookup

    @staticmethod
    def _load_csv_flexible(path: Path) -> list[dict[str, Any]]:
        """Load CSV; merge overflow fields into the last header column.

        Pack 01 final-score descriptions sometimes contain unquoted commas.
        """
        import csv

        if not path.exists():
            logger.warning("scoring_rule_csv_missing", extra={"path": str(path)})
            return []
        try:
            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.reader(handle)
                try:
                    headers = next(reader)
                except StopIteration:
                    return []
                headers = [str(item).strip() for item in headers if str(item).strip()]
                if not headers:
                    return []
                rows: list[dict[str, Any]] = []
                for parts in reader:
                    if not parts or all(not str(part).strip() for part in parts):
                        continue
                    values = [str(part).strip() for part in parts]
                    if len(values) > len(headers):
                        head = values[: len(headers) - 1]
                        tail = ",".join(values[len(headers) - 1 :])
                        values = head + [tail]
                    elif len(values) < len(headers):
                        values = values + [""] * (len(headers) - len(values))
                    rows.append(dict(zip(headers, values, strict=False)))
                return rows
        except OSError as exc:
            logger.warning(
                "scoring_rule_csv_read_failed",
                extra={"path": str(path), "error": str(exc)},
            )
            return []

    @staticmethod
    def _load_csv(path: Path) -> list[dict[str, Any]]:
        """Load a CSV file as list[dict]; missing/empty file -> empty."""
        if not path.exists():
            logger.warning("scoring_rule_csv_missing", extra={"path": str(path)})
            return []
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except pd.errors.EmptyDataError:
            logger.warning("scoring_rule_csv_empty", extra={"path": str(path)})
            return []
        if df.empty:
            return []
        return df.to_dict("records")
