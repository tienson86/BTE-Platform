"""UI-01 Customer Portal shell & navigation (N1–N10)."""

from __future__ import annotations

import re

from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app
from applications.customer_portal.pages import CUSTOMER_NAV_ITEMS

_FORBIDDEN_NAV_LABELS = ("Báo cáo", "Lịch sử", "Tài khoản", "Hướng dẫn", "Luận giải", "Kết quả")


def _client() -> TestClient:
    return TestClient(create_app())


def _primary_nav(html: str) -> str:
    match = re.search(
        r'<nav[^>]*data-customer-nav="primary"[^>]*>(.*?)</nav>',
        html,
        flags=re.S,
    )
    assert match is not None, "customer primary navigation is missing"
    return match.group(1)


def _main_html(html: str) -> str:
    match = re.search(r'<main[^>]*id="mainContent"[^>]*>(.*?)</main>', html, flags=re.S)
    return match.group(1) if match else html


def _nav_labels(nav_html: str) -> list[str]:
    return re.findall(r">([^<]+)</a>", nav_html)


def test_n1_customer_navigation_has_three_product_items() -> None:
    html = _client().get("/good-date").text
    labels = _nav_labels(_primary_nav(html))
    assert labels == ["Trang chủ", "Chọn ngày tốt", "Xem lá số"]
    assert len(CUSTOMER_NAV_ITEMS) == 3


def test_n2_reports_not_in_customer_navigation() -> None:
    nav = _primary_nav(_client().get("/good-date").text)
    assert "Báo cáo" not in nav


def test_n3_history_not_in_customer_navigation() -> None:
    nav = _primary_nav(_client().get("/good-date").text)
    assert "Lịch sử" not in nav


def test_n4_default_route_opens_good_date_home() -> None:
    client = _client()
    root = client.get("/", follow_redirects=False)
    assert root.status_code in {302, 307}
    assert root.headers["location"].endswith("/good-date")
    home = client.get("/", follow_redirects=True)
    assert home.status_code == 200
    assert 'data-screen="lookup"' in home.text
    assert "id=\"dsCalendar\"" in home.text
    assert 'id="dashGreeting"' not in _main_html(home.text)


def test_n5_trang_chu_opens_good_date_home() -> None:
    nav = _primary_nav(_client().get("/choose-date").text)
    assert re.search(r'href="/good-date"[^>]*>Trang chủ<', nav)
    home = _client().get("/good-date")
    assert home.status_code == 200
    assert 'data-screen="lookup"' in home.text
    home_nav = _primary_nav(home.text)
    assert 'data-nav-id="home"' in home_nav
    assert 'aria-current="page"' in home_nav


def test_n6_chon_ngay_tot_opens_search_screen() -> None:
    response = _client().get("/choose-date")
    assert response.status_code == 200
    nav = _primary_nav(response.text)
    assert re.search(r'href="/choose-date"[^>]*>Chọn ngày tốt<', nav)
    assert 'data-screen="search"' in response.text
    assert 'data-nav-id="choose-date"' in nav
    assert 'aria-current="page"' in nav


def test_n7_xem_la_so_opens_input_screen() -> None:
    response = _client().get("/analyze")
    assert response.status_code == 200
    nav = _primary_nav(response.text)
    assert re.search(r'href="/analyze"[^>]*>Xem lá số<', nav)
    assert 'id="analyzeForm"' in response.text
    assert 'data-nav-id="analyze"' in nav
    assert "Luận giải" not in nav


def test_n8_result_route_still_works() -> None:
    response = _client().get("/result")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_n9_result_does_not_redirect_to_welcome_dashboard() -> None:
    response = _client().get("/result", follow_redirects=False)
    assert response.status_code == 200
    location = response.headers.get("location", "")
    assert "/dashboard" not in location
    assert 'id="dashGreeting"' not in response.text
    assert 'class="dash-hero"' not in response.text


def test_n10_legacy_welcome_is_not_production_landing() -> None:
    client = _client()
    landing = client.get("/", follow_redirects=True)
    assert landing.status_code == 200
    main = _main_html(landing.text)
    assert 'data-screen="lookup"' in landing.text
    assert 'id="dashGreeting"' not in main
    assert 'class="dash"' not in main
    dashboard = client.get("/dashboard")
    assert dashboard.status_code == 200
    nav = _primary_nav(dashboard.text)
    assert _nav_labels(nav) == ["Trang chủ", "Chọn ngày tốt", "Xem lá số"]
    for label in _FORBIDDEN_NAV_LABELS:
        assert label not in nav
