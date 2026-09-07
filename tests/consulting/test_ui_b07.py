"""TV1-B07 presentation, layout, isolated host, and B06 factory freeze."""

from __future__ import annotations

import ast
from pathlib import Path

from fastapi.testclient import TestClient

from consulting.marriage.adapters.canonical_runtime import CanonicalOrchestratorAdapter
from consulting.marriage.api.http import create_marriage_api_app
from consulting.marriage.presentation.adapter import (
    SemanticMarriagePresentationAdapter,
    unpublished_optional_domains,
)
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.runtime.api_wiring import wire_marriage_api_runtime
from consulting.marriage.runtime.ui_wiring import wire_marriage_ui_runtime
from consulting.marriage.ui.host import create_marriage_customer_app
from consulting.marriage.ui.layout import (
    CUSTOMER_JOURNEY,
    MarriageCustomerLayoutProfile,
    ROUTE_PATH,
)
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from tests.consulting.api_fixtures import api_client, api_service, valid_body
from tests.consulting.runtime_fixtures import FakeCanonicalRunner

ROOT = Path(__file__).resolve().parents[2]


def test_b06_wiring_keeps_placeholder_ui() -> None:
    """Frozen B06 factory still leaves presentation and UI unimplemented."""
    container = wire_marriage_api_runtime()
    assert isinstance(container.presentation_adapter, PlaceholderMarriagePresentationAdapter)
    assert isinstance(container.ui_layout_profile, PlaceholderMarriageUILayoutProfile)


def test_b07_wiring_binds_layout_and_presentation() -> None:
    """B07 factory binds semantic presentation and customer layout."""
    container = wire_marriage_ui_runtime()
    assert isinstance(container.presentation_adapter, SemanticMarriagePresentationAdapter)
    profile = container.ui_layout_profile
    assert isinstance(profile, MarriageCustomerLayoutProfile)
    descriptor = profile.descriptor()
    assert descriptor.profile_id.startswith("marriage.ui.layout")
    assert profile.route_path() == "/marriage-consulting"
    assert profile.customer_journey()[1] == "compatibility_hero"


def test_customer_journey_order() -> None:
    """Customer journey is identity → hero → summary → details → action."""
    assert CUSTOMER_JOURNEY[:5] == (
        "identity",
        "compatibility_hero",
        "executive_summary",
        "strengths",
        "risks",
    )
    assert "action_plan" in CUSTOMER_JOURNEY
    assert "appendix" == CUSTOMER_JOURNEY[-1]


def test_semantic_adapter_does_not_invent_score() -> None:
    """Presentation mapping keeps score and grade unavailable."""
    client, container = api_client(live=False)
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert created.status_code == 201
    stored = api_service(container).get_stored(created.json()["data"]["consultation_id"])
    view = SemanticMarriagePresentationAdapter().adapt(stored.result)
    assert view.hero.score_display == ""
    assert view.hero.grade_display == ""
    assert all(item.score_display is None for item in view.domains)
    assert all(item.grade_display is None for item in view.domains)
    omitted = {item.value for item in unpublished_optional_domains(stored.result)}
    assert "interaction" in omitted
    assert "family" in omitted
    assert "children" in omitted


def test_isolated_customer_route_loads() -> None:
    """Isolated legal composition serves the customer route and Public API."""
    container = wire_marriage_ui_runtime(
        canonical_adapter=CanonicalOrchestratorAdapter(runner=FakeCanonicalRunner())
    )
    client = TestClient(create_marriage_customer_app(container))
    page = client.get(ROUTE_PATH)
    assert page.status_code == 200
    assert "Tư vấn hôn nhân" in page.text
    assert 'data-testid="marriage-form"' in page.text or "marriage_consulting.js" in page.text
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert created.status_code == 201
    assert created.json()["data"]["score"] is None
    assert created.json()["data"]["grade"] is None


def test_isolated_api_app_unchanged_contract() -> None:
    """API-only host still exposes the B06 envelope."""
    client = TestClient(create_marriage_api_app())
    response = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert response.status_code == 201
    assert response.json()["status"] == "SUCCESS"


def test_applications_still_do_not_import_consulting() -> None:
    """B07 HTTP proxy must not introduce a Python reverse dependency."""
    apps = ROOT / "applications"
    violations: list[str] = []
    for path in apps.rglob("*.py"):
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "consulting.marriage" or alias.name.startswith("consulting.marriage."):
                        violations.append(str(path))
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module == "consulting.marriage" or node.module.startswith("consulting.marriage."):
                    violations.append(str(path))
    assert violations == []
