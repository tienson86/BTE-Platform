"""
Base Validator.
"""

from __future__ import annotations

from abc import ABC

import pandas as pd


class BaseValidator(ABC):

    REQUIRED_COLUMNS: list[str] = []

    def validate_dataframe(
        self,
        dataframe: pd.DataFrame
    ) -> bool:

        if dataframe is None:

            raise ValueError(
                "DataFrame is None"
            )

        if dataframe.empty:

            raise ValueError(
                "DataFrame is empty"
            )

        missing = [

            col

            for col in self.REQUIRED_COLUMNS

            if col not in dataframe.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns: {missing}"

            )

        return True

    def validate_rule(
        self,
        rule: dict
    ) -> bool:

        for col in self.REQUIRED_COLUMNS:

            if col not in rule:

                raise ValueError(

                    f"Missing key: {col}"

                )

        return True
