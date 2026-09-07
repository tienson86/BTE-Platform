"""Policy context. Canonical information required by Marriage Policy only."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.enums import MarriageDomain
from consulting.marriage.models.options import ResolvedMarriageOptions
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot
from consulting.marriage.models.versioning import MarriageVersionBundle


@dataclass(frozen=True, slots=True)
class MarriagePolicyContext:
    """Read-only policy input. Does not expose mutable runtime state."""

    consultation_id: str
    snapshot_a: MarriageCanonicalSnapshot
    snapshot_b: MarriageCanonicalSnapshot
    options: ResolvedMarriageOptions
    versions: MarriageVersionBundle
    available_domains: tuple[MarriageDomain, ...]
    limitations: tuple[str, ...]
    source_analysis_id_a: str
    source_analysis_id_b: str
