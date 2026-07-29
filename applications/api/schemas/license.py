"""License API schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LicenseActivateRequest(BaseModel):
    """Activate a license key offline."""

    license_key: str = Field(..., min_length=3, examples=["BTE-STANDARD-ABC123"])


class LicenseValidateRequest(BaseModel):
    """Validate license / feature / usage limits."""

    license_key: str | None = None
    feature: str | None = Field(None, examples=["report"])
    current_users: int | None = Field(None, ge=0)
    current_cases: int | None = Field(None, ge=0)


class LicenseIssueRequest(BaseModel):
    """Optional helper for tests/dev: issue a license (not in WP14 public list)."""

    edition: str = Field("STANDARD", examples=["STANDARD"])
    customer: str = Field(..., examples=["Acme"])
    organization: str = ""
    days_valid: int | None = 365
    max_users: int | None = None
    max_cases: int | None = None
