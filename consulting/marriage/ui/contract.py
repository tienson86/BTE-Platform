"""UI Layout Profile contract. Information architecture only. No HTML/CSS."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarriageUILayoutProfileDescriptor:
    """Identity of the Marriage UI Layout Profile. Contains no widgets."""

    profile_id: str
    version: str


class MarriageUILayoutProfile(ABC):
    """Declares customer journey and layout hierarchy. Does not render UI."""

    @abstractmethod
    def descriptor(self) -> MarriageUILayoutProfileDescriptor:
        """Return UI layout profile identity."""
