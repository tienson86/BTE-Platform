"""
Pattern Rule Loader.

Loads all pattern rule files from database/14_pattern/.
File loading order determines priority layering:
  01_main_pattern.csv        — standard cách cục
  02_special_pattern.csv     — chuyên cách (Tòng, Hóa...)
  03_follow_pattern.csv      — override rules (follow-pattern beats main)
  04_combination_pattern.csv — combination patterns
  05_priority_rules.csv      — global priority overrides
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

# Primary rules file (legacy + canonical aliases)
MAIN_FILE_CANDIDATES = (
    "rules.csv",           # legacy alias
    "01_main_pattern.csv", # canonical
)

# Additional rule files loaded in order (skipped when absent)
SUPPLEMENTARY_FILES = (
    "02_special_pattern.csv",
    "03_follow_pattern.csv",
    "04_combination_pattern.csv",
)

# Metadata-only files — loaded on demand but NOT merged into rules
METADATA_FILES = (
    "05_priority_rules.csv",
    "06_pattern_conditions.csv",
    "07_pattern_examples.csv",
)



class PatternLoader:

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self.cache: dict[Path, pd.DataFrame] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def resolve_rules_file(self) -> Optional[Path]:
        """Resolve main pattern rules file (legacy alias → canonical)."""
        for name in MAIN_FILE_CANDIDATES:
            candidate = self.database_path / name
            if candidate.exists():
                return candidate
        return None

    def rules_exist(self) -> bool:
        return self.resolve_rules_file() is not None

    def load_rules(self) -> pd.DataFrame:
        """
        Load and merge all pattern rule files.

        Main file is required. Supplementary files are optional.
        Rules from later files override earlier ones only when they have
        higher priority — the merged frame is returned unsorted;
        PatternCalculator applies priority logic.
        """
        main_path = self.resolve_rules_file()
        if main_path is None:
            raise FileNotFoundError(
                f"Pattern rules not found under {self.database_path}. "
                f"Tried: {', '.join(MAIN_FILE_CANDIDATES)}"
            )

        frames = [self._load_csv(main_path)]
        loaded = [main_path.name]

        for name in SUPPLEMENTARY_FILES:
            path = self.database_path / name
            if path.exists():
                try:
                    frames.append(self._load_csv(path))
                    loaded.append(name)
                except Exception as exc:
                    logger.warning("Pattern loader: skipped %s — %s", name, exc)

        logger.debug("PatternLoader: loaded %s", ", ".join(loaded))

        if len(frames) == 1:
            return frames[0]

        merged = pd.concat(frames, ignore_index=True)
        return merged

    def load_csv(self, filename: str) -> pd.DataFrame:
        """Load an arbitrary CSV by filename under database_path."""
        return self._load_csv(self.database_path / filename)

    def exists(self, filename: str) -> bool:
        return (self.database_path / filename).exists()

    def clear_cache(self) -> None:
        self.cache.clear()

    def cache_size(self) -> int:
        return len(self.cache)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_csv(self, path: Path) -> pd.DataFrame:
        if path in self.cache:
            return self.cache[path]
        data = pd.read_csv(path, encoding="utf-8")
        self.cache[path] = data
        return data
