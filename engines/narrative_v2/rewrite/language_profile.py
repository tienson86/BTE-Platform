"""Customer language profile for Narrative V2 rewrite."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.rewrite.rewrite_strategy import CUSTOMER_ADDRESS


@dataclass(frozen=True, slots=True)
class LanguageProfile:
    """Audience and voice. Not a sentence library."""

    audience: str = "customer"
    address: str = CUSTOMER_ADDRESS
    locale: str = "vi"
    voice: str = "professional"
    style: str = "consultant"

    def is_customer(self) -> bool:
        """True when rewrite targets the default customer audience."""
        return self.audience == "customer"
