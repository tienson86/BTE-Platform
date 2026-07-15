from pathlib import Path

import pandas as pd


class ScoreLoader:
    """
    Đọc toàn bộ dữ liệu Score Database.
    """

    def __init__(self, database_path):

        self.database_path = Path(database_path)

        self.cache = {}

    def load_csv(self, relative_path):

        path = self.database_path / relative_path

        if relative_path in self.cache:
            return self.cache[relative_path]

        df = pd.read_csv(path)

        self.cache[relative_path] = df

        return df

    def clear_cache(self):

        self.cache.clear()
