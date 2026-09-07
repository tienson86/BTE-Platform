"""DI registration tests. Structural only."""

from __future__ import annotations

import pytest

from consulting.marriage.adapters.contract import CanonicalRuntimeAdapter
from consulting.marriage.api.contract import MarriageApiContract
from consulting.marriage.decision.contract import MarriageDecisionResolver
from consulting.marriage.evidence.contract import MarriageEvidenceBuilder
from consulting.marriage.finding.contract import MarriageFindingBuilder
from consulting.marriage.orchestrator.contract import MarriageOrchestrator
from consulting.marriage.policy.contract import MarriagePolicyProvider
from consulting.marriage.presentation.contract import MarriagePresentationAdapter
from consulting.marriage.recommendation.contract import MarriageRecommendationProvider
from consulting.marriage.report.contract import MarriageReportProfile
from consulting.marriage.repository.contract import MarriageRepository
from consulting.marriage.runtime.wiring import wire_marriage_runtime
from consulting.marriage.ui.contract import MarriageUILayoutProfile
from consulting.marriage.validation.contract import MarriageValidationContract


def test_wire_marriage_runtime_registers_contracts() -> None:
    """Factory must bind every TV-01 contract to a placeholder implementation."""
    container = wire_marriage_runtime()
    assert isinstance(container.orchestrator, MarriageOrchestrator)
    assert isinstance(container.repository, MarriageRepository)
    assert isinstance(container.policy_provider, MarriagePolicyProvider)
    assert isinstance(container.evidence_builder, MarriageEvidenceBuilder)
    assert isinstance(container.finding_builder, MarriageFindingBuilder)
    assert isinstance(container.decision_resolver, MarriageDecisionResolver)
    assert isinstance(container.recommendation_provider, MarriageRecommendationProvider)
    assert isinstance(container.report_profile, MarriageReportProfile)
    assert isinstance(container.presentation_adapter, MarriagePresentationAdapter)
    assert isinstance(container.ui_layout_profile, MarriageUILayoutProfile)
    assert isinstance(container.api_contract, MarriageApiContract)
    assert isinstance(container.validation, MarriageValidationContract)
    assert isinstance(container.canonical_adapter, CanonicalRuntimeAdapter)


def test_placeholders_do_not_execute_business_logic() -> None:
    """Placeholder methods must refuse execution in TV1-B01."""
    container = wire_marriage_runtime()
    with pytest.raises(NotImplementedError):
        container.orchestrator.run(None)  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        container.policy_provider.descriptor()
    with pytest.raises(NotImplementedError):
        container.report_profile.descriptor()
    with pytest.raises(NotImplementedError):
        container.ui_layout_profile.descriptor()
    with pytest.raises(NotImplementedError):
        container.repository.list_history()
    with pytest.raises(NotImplementedError):
        container.api_contract.list_history()
