"""Marriage Report Profile contract. Profile only. Not a Report Engine."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarriageReportProfileDescriptor:
    """Identity of the Marriage Report Profile. Contains no renderer logic."""

    profile_id: str
    version: str


class MarriageReportProfile(ABC):
    """Declares report story flow and section configuration. Does not render."""

    @abstractmethod
    def descriptor(self) -> MarriageReportProfileDescriptor:
        """Return report profile identity."""
