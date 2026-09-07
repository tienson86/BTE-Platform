"""UI layout placeholder. No UI implementation in TV1-B01."""

from __future__ import annotations

from consulting.marriage.ui.contract import (
    MarriageUILayoutProfile,
    MarriageUILayoutProfileDescriptor,
)


class PlaceholderMarriageUILayoutProfile(MarriageUILayoutProfile):
    """Skeleton placeholder. Does not implement layout or components."""

    def descriptor(self) -> MarriageUILayoutProfileDescriptor:
        """Refuse UI layout profile resolution."""
        raise NotImplementedError("TV1-B01: UI layout profile is not implemented")
