"""TV1-B07A live Customer Portal navigation mount."""

from __future__ import annotations

import re

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.pages import CUSTOMER_NAV_ITEMS, MARRIAGE_CONSULTING_PATH

_ORIGINAL_THREE = (
    ("home", "/good-date", "Trang chủ"),
    ("choose-date", "/choose-date", "Chọn ngày tốt"),
    ("analyze", "/analyze", "Xem lá số"),
)


def _client() -> TestClient:
    return TestClient(create_app())


def _primary_nav(html: str) -> str:
    match = re.search(
        r'<nav[^>]*data-customer-nav="primary"[^>]*>(.*?)</nav>',
        html,
        flags=re.S,
    )
    assert match is not None, "live primary navigation is missing"
    return match.group(1)


def _nav_labels(nav_html: str) -> list[str]:
    return re.findall(r">([^<]+)</a>", nav_html)


def test_fourth_primary_item_exists_on_live_shell_routes() -> None:
    """Tư vấn hôn nhân is visible in the live portal primary nav on all product routes."""
    client = _client()
    for path in ("/good-date", "/choose-date", "/analyze", MARRIAGE_CONSULTING_PATH):
        nav = _primary_nav(client.get(path).text)
        labels = _nav_labels(nav)
        assert labels == ["Trang chủ", "Chọn ngày tốt", "Xem lá số", "Tư vấn hôn nhân"]
        assert re.search(r'href="/marriage-consulting"[^>]*>Tư vấn hôn nhân<', nav)


def test_existing_three_destinations_unchanged() -> None:
    """TV1-B07A does not change the original three primary items."""
    assert len(CUSTOMER_NAV_ITEMS) == 4
    for index, (key, path, _label) in enumerate(_ORIGINAL_THREE):
        assert CUSTOMER_NAV_ITEMS[index].key == key
        assert CUSTOMER_NAV_ITEMS[index].path == path
    assert CUSTOMER_NAV_ITEMS[3].key == "marriage-consulting"
    assert CUSTOMER_NAV_ITEMS[3].path == MARRIAGE_CONSULTING_PATH


def test_marriage_route_renders_and_is_active() -> None:
    """Click target /marriage-consulting renders the B07 page with active nav."""
    response = _client().get(MARRIAGE_CONSULTING_PATH)
    assert response.status_code == 200
    assert 'id="marriage-consulting-root"' in response.text
    nav = _primary_nav(response.text)
    assert 'data-nav-id="marriage-consulting"' in nav
    assert 'class="nav-link active"' in nav
    assert 'aria-current="page"' in nav
    home_nav = _primary_nav(_client().get("/good-date").text)
    assert 'data-nav-id="home"' in home_nav
    assert 'aria-current="page"' in home_nav


def test_header_actions_are_not_a_hidden_nav_region() -> None:
    """Marriage is not parked in .app-header-actions."""
    html = _client().get("/good-date").text
    actions = re.search(r'<div class="app-header-actions">(.*?)</div>', html, flags=re.S)
    assert actions is not None
    assert "Tư vấn hôn nhân" not in actions.group(1)
    assert "marriage-consulting" not in actions.group(1)
