"""TV1-B07 customer journey layout profile. Information architecture only."""

from __future__ import annotations

from consulting.marriage.ui.contract import (
    MarriageUILayoutProfile,
    MarriageUILayoutProfileDescriptor,
)

LAYOUT_PROFILE_ID = "marriage.ui.layout.customer.v1"
LAYOUT_PROFILE_VERSION = "1.0.0"

CUSTOMER_JOURNEY = (
    "identity",
    "compatibility_hero",
    "executive_summary",
    "strengths",
    "risks",
    "domain_analysis",
    "timing",
    "action_plan",
    "confidence_limitations",
    "conclusion",
    "appendix",
)

DEFAULT_CUSTOMER_SECTIONS = (
    "identity",
    "compatibility_hero",
    "executive_summary",
    "strengths",
    "risks",
    "domain_analysis",
    "action_plan",
    "confidence_limitations",
    "conclusion",
)

EXPANDED_SECTIONS = ("domain_analysis",)
EXPERT_SECTIONS = ("appendix",)
ROUTE_PATH = "/marriage-consulting"
PRODUCT_LABEL = "Tư vấn hôn nhân"
FAMILY_LABEL = "Tư vấn"


class MarriageCustomerLayoutProfile(MarriageUILayoutProfile):
    """Declares TV-01 customer journey. Does not render HTML or CSS."""

    def descriptor(self) -> MarriageUILayoutProfileDescriptor:
        """Return the bound customer layout identity."""
        return MarriageUILayoutProfileDescriptor(
            profile_id=LAYOUT_PROFILE_ID,
            version=LAYOUT_PROFILE_VERSION,
        )

    def customer_journey(self) -> tuple[str, ...]:
        """Return the customer reading order. Hero precedes details."""
        return CUSTOMER_JOURNEY

    def default_sections(self) -> tuple[str, ...]:
        """Sections visible before progressive disclosure."""
        return DEFAULT_CUSTOMER_SECTIONS

    def route_path(self) -> str:
        """Return the customer route for this layout."""
        return ROUTE_PATH
