"""Interface contract tests. Structural only. No business assertions."""

from __future__ import annotations

import inspect

from consulting.marriage.adapters.contract import CanonicalRuntimeAdapter
from consulting.marriage.api.contract import MarriageApiContract
from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.contract import MarriageDecisionResolver
from consulting.marriage.evidence.contract import MarriageEvidenceBuilder
from consulting.marriage.finding.contract import MarriageFindingBuilder
from consulting.marriage.orchestrator.contract import MarriageOrchestrator
from consulting.marriage.policy.contract import MarriagePolicyProvider
from consulting.marriage.presentation.contract import MarriagePresentationAdapter
from consulting.marriage.recommendation.contract import MarriageRecommendationProvider
from consulting.marriage.report.contract import MarriageReportProfile
from consulting.marriage.repository.contract import MarriageRepository
from consulting.marriage.runtime.context import MarriageRuntimeContext
from consulting.marriage.ui.contract import MarriageUILayoutProfile
from consulting.marriage.validation.contract import MarriageValidationContract

ABSTRACT_CONTRACTS = (
    MarriageOrchestrator,
    MarriageRepository,
    MarriagePolicyProvider,
    MarriageRecommendationProvider,
    MarriageReportProfile,
    MarriageUILayoutProfile,
    MarriageApiContract,
    MarriageValidationContract,
    CanonicalRuntimeAdapter,
    MarriageEvidenceBuilder,
    MarriageFindingBuilder,
    MarriageDecisionResolver,
    MarriagePresentationAdapter,
)


def test_expected_contracts_are_abstract() -> None:
    """Expected TV-01 contracts must be abstract interfaces."""
    for contract in ABSTRACT_CONTRACTS:
        assert inspect.isabstract(contract)
        assert inspect.isclass(contract)


def test_runtime_and_decision_contexts_are_dataclasses() -> None:
    """Runtime and decision contexts are structural objects, not engines."""
    assert dataclasses_slots(MarriageRuntimeContext)
    assert dataclasses_slots(MarriageDecisionContext)
    fields = {item.name for item in inspect_fields(MarriageRuntimeContext)}
    assert "consultation_id" in fields
    assert "request" in fields
    assert "versions" in fields
    decision_fields = {item.name for item in inspect_fields(MarriageDecisionContext)}
    assert "consultation_id" in decision_fields
    assert "relationship" in decision_fields
    assert "versions" in decision_fields


def dataclasses_slots(cls: type) -> bool:
    """Return True when the class is a slotted dataclass."""
    return hasattr(cls, "__dataclass_fields__") and hasattr(cls, "__slots__")


def inspect_fields(cls: type) -> tuple[inspect.Parameter, ...]:
    """Return dataclass field names via constructor signature."""
    signature = inspect.signature(cls)
    return tuple(signature.parameters.values())
