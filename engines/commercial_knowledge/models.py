"""Commercial Knowledge models (Retrieval Contract v1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

CONTRACT_ID = "bte.commercial_knowledge.retrieval.v1"
CONTRACT_VERSION = "1.0.0"

WAVE_1_1_ALLOW_LIST: frozenset[str] = frozenset(
    {
        "KU-ID-001",
        "KU-ST-001",
        "KU-WK-001",
        "KU-UG-001",
        "KU-RC-001",
    }
)

DEFAULT_TARGET_COMPONENTS: tuple[str, ...] = (
    "executive_summary",
    "recommendation",
    "observation",
    "reasoning",
    "warning",
    "conclusion",
)


@dataclass(slots=True)
class RetrievalRequest:
    """Inputs for commercial knowledge retrieval."""

    analysis_signals: dict[str, Any]
    scenario_id: str = "default"
    allow_list_ids: frozenset[str] = WAVE_1_1_ALLOW_LIST
    target_components: tuple[str, ...] = DEFAULT_TARGET_COMPONENTS
    locale: str = "vi"
    run_id: str = ""


@dataclass(slots=True)
class SelectedUnitSummary:
    """Allow-listed unit summary for traces — not a raw Knowledge Unit dump."""

    knowledge_unit_id: str
    version: str
    evidence_kind: str
    priority: int
    confidence: float
    narrative_targets: tuple[str, ...] = ()


@dataclass(slots=True)
class DroppedUnit:
    """Record of a unit that was considered but not selected."""

    knowledge_unit_id: str
    reason: str


@dataclass(slots=True)
class BundleItem:
    """One customer-facing commercial statement with provenance."""

    text: str
    evidence_kind: str
    knowledge_unit_id: str
    version: str
    component_targets: tuple[str, ...]
    signal_refs: tuple[str, ...]
    confidence: float
    role: str = ""


@dataclass(slots=True)
class CommercialKnowledgeBundle:
    """
    Narrative-facing commercial bundle.

    Must not expose raw Knowledge Unit records.
    """

    contract_id: str = CONTRACT_ID
    contract_version: str = CONTRACT_VERSION
    bundle_id: str = ""
    scenario_id: str = "default"
    bundle_status: str = "empty"
    identity: tuple[BundleItem, ...] = ()
    strengths: tuple[BundleItem, ...] = ()
    weaknesses: tuple[BundleItem, ...] = ()
    useful_god: tuple[BundleItem, ...] = ()
    recommendations: tuple[BundleItem, ...] = ()
    warnings: tuple[BundleItem, ...] = ()
    opportunities: tuple[BundleItem, ...] = ()
    confidence: float = 0.0
    selected_units: tuple[SelectedUnitSummary, ...] = ()
    dropped_units: tuple[DroppedUnit, ...] = ()
    traceability: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class NarrativeEvidenceUnit:
    """Narrative-ready evidence unit derived from the bundle."""

    evidence_kind: str
    text: str
    knowledge_unit_id: str
    version: str
    component_targets: tuple[str, ...]
    signal_refs: tuple[str, ...]
    confidence: float


@dataclass(slots=True)
class NarrativeKnowledgePayload:
    """Payload Narrative consumes (via merge helper) — never raw KUs."""

    evidence_units: tuple[NarrativeEvidenceUnit, ...] = ()
    bundle_id: str = ""
    bundle_status: str = "empty"
