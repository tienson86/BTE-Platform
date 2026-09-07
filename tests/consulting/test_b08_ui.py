"""TV1-B08 presentation/UI contract. No new product features."""

from __future__ import annotations

import json
import re

from fastapi.testclient import TestClient

from consulting.marriage.presentation.adapter import SemanticMarriagePresentationAdapter
from consulting.marriage.ui.host import create_marriage_customer_app
from consulting.marriage.ui.layout import CUSTOMER_JOURNEY
from tests.consulting.api_fixtures import api_client, api_service, valid_body

_ID_LEAK = re.compile(r"\b(?:EV|F|RC)-\d{4}\b")


def test_isolated_host_serves_form_and_static_assets() -> None:
    """Isolated legal host exposes the customer form without a fake score widget."""
    client = TestClient(create_marriage_customer_app())
    page = client.get("/marriage-consulting")
    assert page.status_code == 200
    html = page.text
    assert 'data-testid="marriage-form"' in html or "marriage-consulting-root" in html
    css = client.get("/tv01-static/marriage_consulting.css")
    js = client.get("/tv01-static/marriage_consulting.js")
    assert css.status_code == 200
    assert js.status_code == 200
    assert "/100" not in js.text
    assert "Grade A" not in js.text
    assert "data-testid=\"compatibility-hero\"" in js.text
    assert "data-testid=\"action-plan\"" in js.text
    assert "data-testid=\"expert-mode\"" in js.text


def test_presentation_journey_hides_unavailable_and_ids() -> None:
    """Adapter journey matches layout, omits empty domains, and hides internal ids."""
    client, container = api_client()
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    stored = api_service(container).get_stored(created.json()["data"]["consultation_id"])
    view = SemanticMarriagePresentationAdapter().adapt(stored.result)
    assert view.hero.score_display == ""
    assert view.hero.grade_display == ""
    published = [item.domain for item in view.domains]
    assert "interaction" not in published
    assert "family" not in published
    assert "children" not in published
    blob = json.dumps(
        {
            "headline": view.hero.title,
            "domains": published,
            "actions": [item.title for item in view.recommendations],
        },
        ensure_ascii=False,
    )
    assert _ID_LEAK.search(blob) is None
    assert "identity" in CUSTOMER_JOURNEY
    assert CUSTOMER_JOURNEY.index("compatibility_hero") < CUSTOMER_JOURNEY.index("action_plan")
