"""
Interpretation Service

API công khai cho BTE Platform.
"""

from __future__ import annotations

from pathlib import Path

from .bootstrap import Bootstrap


class InterpretationService:

    """
    API duy nhất mà các Engine khác sử dụng.
    """

    def __init__(

        self,

        root_directory

    ):

        self.engine = Bootstrap(
            root_directory
        ).build()

        self.engine.startup()

    def interpret(

        self,

        chart

    ):

        return self.engine.interpret(chart)

    def validate(self):

        return self.engine.validate()

    @property
    def version(self):

        return self.engine.VERSION
