"""
Pattern Service.

Cung cấp API cho các Engine khác.
"""

from .loader import PatternLoader
from .calculator import PatternCalculator


class PatternService:

    def __init__(self,
                 database_path="database/04_pattern"):

        self.loader = PatternLoader(
            database_path
        )

        self.calculator = PatternCalculator(
            self.loader
        )

    def analyze(self, context):

        return self.calculator.calculate(
            context
        )

    def clear_cache(self):

        self.loader.clear_cache()

    def cache_size(self):

        return self.loader.cache_size()
