"""
Lớp cơ sở cho tất cả Interpreter.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from ..context import InterpretationResult


class BaseInterpreter(ABC):

    name = "BaseInterpreter"

    @abstractmethod
    def run(
        self,
        analysis: dict,
    ) -> InterpretationResult:
        ...
