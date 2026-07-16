"""
Pattern Rule Loader.
"""

from pathlib import Path
import pandas as pd


class PatternLoader:

    def __init__(self, database_path):

        self.database_path = Path(database_path)

        self.cache = {}

    def load_csv(self, filename):

        file = self.database_path / filename

        if file in self.cache:
            return self.cache[file]

        data = pd.read_csv(file, encoding="utf-8")

        self.cache[file] = data

        return data

    def clear_cache(self):

        self.cache.clear()

    def cache_size(self):

        return len(self.cache)

    def exists(self, filename):

        return (self.database_path / filename).exists()
