"""Version bundle for a single consultation execution."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.person import CanonicalVersionReference


@dataclass(slots=True)
class MarriageVersionBundle:
    """Atomic version set used for one consultation. Must not change mid-run."""

    module_version: str
    decision_profile_version: str
    score_model_version: str
    rule_catalog_version: str
    canonical_versions: CanonicalVersionReference
    narrative_version: str | None = None
