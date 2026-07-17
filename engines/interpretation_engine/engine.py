"""
Interpretation Engine

Engine trung tâm.
"""

from __future__ import annotations


class InterpretationEngine:

    VERSION = "1.0.0"

    def __init__(

        self,

        pipeline

    ):

        self.pipeline = pipeline

    def startup(self):

        """
        Khởi động Engine.
        """

        self.pipeline.initialize()

    def validate(self):

        """
        Kiểm tra Database.
        """

        return self.pipeline.validate()

    def interpret(

        self,

        chart

    ):

        """
        Diễn giải một lá số.
        """

        return self.pipeline.execute(chart)
