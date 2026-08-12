"""Hidden stem weights loader — reads ``database/09_hidden_stems/hidden_stems.csv``."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from engines.ten_gods_engine.constants import HIDDEN_POSITION_NAMES, HIDDEN_STEMS_CSV
from engines.ten_gods_engine.exceptions import TenGodsLoaderError

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_DB_ROOT = _REPO_ROOT / "database"


@dataclass(frozen=True, slots=True)
class HiddenStemSlot:
    """One hidden stem slot with canonical weight."""

    branch: str
    hidden_stem: str
    hidden_position: int
    position_name: str
    weight: float


class HiddenStemWeightLoader:
    """Load hidden stem weights from the canonical CSV database."""

    def __init__(self, database_root: Path | None = None) -> None:
        self._database_root = database_root or _DEFAULT_DB_ROOT

    def load_branch_slots(self, branch: str) -> tuple[HiddenStemSlot, ...]:
        """Return ordered hidden stem slots for a branch."""
        rules = self._load_rules()
        row = rules.get(branch)
        if row is None:
            raise TenGodsLoaderError(f"No hidden stem rule for branch '{branch}'")

        slots: list[HiddenStemSlot] = []
        for index, position_name in enumerate(HIDDEN_POSITION_NAMES):
            stem_key = position_name
            weight_key = f"{position_name}_weight"
            stem = str(row.get(stem_key) or "").strip()
            if not stem:
                continue
            weight_raw = row.get(weight_key)
            if weight_raw is None or str(weight_raw).strip() == "":
                raise TenGodsLoaderError(
                    f"Missing weight '{weight_key}' for branch '{branch}'",
                )
            weight = float(weight_raw)
            slots.append(
                HiddenStemSlot(
                    branch=branch,
                    hidden_stem=stem,
                    hidden_position=index,
                    position_name=position_name,
                    weight=weight,
                )
            )
        if not slots:
            raise TenGodsLoaderError(f"No hidden stems defined for branch '{branch}'")
        return tuple(slots)

    @lru_cache(maxsize=1)
    def _load_rules(self) -> dict[str, dict[str, str]]:
        path = self._database_root / HIDDEN_STEMS_CSV
        if not path.exists():
            raise TenGodsLoaderError(
                f"Hidden stem database missing: {path}",
            )
        rules: dict[str, dict[str, str]] = {}
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                branch = str(row.get("branch") or "").strip()
                if branch:
                    rules[branch] = dict(row)
        if len(rules) != 12:
            raise TenGodsLoaderError(
                f"Expected 12 branch hidden stem rules, found {len(rules)}",
            )
        return rules
