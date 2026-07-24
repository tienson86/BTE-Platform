"""
Pattern Rule Loader.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


# Canonical filenames under database/14_pattern (alias order)
RULE_FILE_CANDIDATES = (
    "rules.csv",              # legacy alias
    "01_main_pattern.csv",    # canonical
)


class PatternLoader:

    def __init__(self, database_path):

        self.database_path = Path(database_path)

        self.cache = {}

    def resolve_rules_file(self) -> Path | None:
        """
        Resolve pattern rules file.

        Prefers legacy ``rules.csv`` alias, then ``01_main_pattern.csv``.
        """

        for name in RULE_FILE_CANDIDATES:
            candidate = self.database_path / name
            if candidate.exists():
                return candidate

        return None

    def load_csv(self, filename):

        file = self.database_path / filename

        if file in self.cache:
            return self.cache[file]

        data = pd.read_csv(file, encoding="utf-8")

        self.cache[file] = data

        return data

    def load_rules(self) -> pd.DataFrame:
        """
        Load the active pattern rules CSV via alias resolution.
        """

        path = self.resolve_rules_file()

        if path is None:
            raise FileNotFoundError(
                "Pattern rules not found under "
                f"{self.database_path}. "
                f"Tried: {', '.join(RULE_FILE_CANDIDATES)}"
            )

        if path in self.cache:
            return self.cache[path]

        data = pd.read_csv(path, encoding="utf-8")
        self.cache[path] = data
        return data

    def clear_cache(self):

        self.cache.clear()

    def cache_size(self):

        return len(self.cache)

    def exists(self, filename):

        return (self.database_path / filename).exists()

    def rules_exist(self) -> bool:

        return self.resolve_rules_file() is not None
