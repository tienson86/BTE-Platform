"""
Pipeline Validator.
"""

from __future__ import annotations

from .context import IntegrationContext


class IntegrationValidator:

    REQUIRED_FIELDS = [

        "birth_info",

    ]

    def validate(

        self,

        context: IntegrationContext,

    ) -> bool:

        for field in self.REQUIRED_FIELDS:

            if getattr(context, field) is None:

                raise ValueError(

                    f"Missing field: {field}"

                )

        return True
