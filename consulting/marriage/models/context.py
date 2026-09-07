"""Relationship context. Aggregates snapshots. Does not conclude."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import MarriageDomain
from consulting.marriage.models.options import ResolvedMarriageOptions
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot


@dataclass(slots=True)
class RuntimeMeta:
    """Runtime metadata for one consultation. Not a decision."""

    module_id: str
    build_phase: str
    pipeline_id: str | None = None


@dataclass(slots=True)
class MarriageRelationshipContext:
    """Paired snapshots and options. No evidence or findings."""

    person_a: MarriageCanonicalSnapshot
    person_b: MarriageCanonicalSnapshot
    options: ResolvedMarriageOptions
    available_domains: list[MarriageDomain]
    limitations: list[str] = field(default_factory=list)
    runtime_meta: RuntimeMeta | None = None
