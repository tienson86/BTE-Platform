import re
import pytest
from fastapi.testclient import TestClient
from applications.customer_portal.app import create_app

PUBLIC = ["/good-date", "/name-analysis", "/number-energy"]
MEMBER = ["/analyze", "/choose-date", "/marriage-consulting", "/childbirth-consulting", "/naming-consulting", "/business-consulting", "/tinh-van-han"]


@pytest.mark.parametrize("path", ["/good-date", "/name-analysis", "/number-energy", "/membership", "/analyze", "/result", "/marriage-consulting"])
def test_three_public_and_seven_member_tools_have_separate_navigation(path):
    html = TestClient(create_app()).get(path).text
    public = re.search(r'<nav[^>]*data-customer-nav="primary"[^>]*>(.*?)</nav>', html, re.S).group(1)
    member = re.search(r'<nav[^>]*data-customer-nav="member"[^>]*>(.*?)</nav>', html, re.S).group(1)
    assert re.findall(r'href="([^"]+)"', public) == PUBLIC
    assert re.findall(r'href="([^"]+)"', member) == MEMBER
    assert "Xem Năng lượng số" in public
    assert "Tư vấn năng lượng số" not in public
    assert re.search(r'<aside[^>]*id="memberSidebar"[^>]*\bhidden', html)
    assert html.index('class="app-brand"') < html.index('id="memberSidebar"')
    assert 'member_layout.css?v=member-01' in html


def test_membership_pages_and_registration_entries_exist_without_prefilled_credentials():
    client = TestClient(create_app())
    assert client.get("/membership").status_code == 200
    admin = client.get("/admin-membership").text
    assert 'id="memberAdminContent" hidden' in admin
    assert 'name="bank_account"' in admin and 'name="public_notice"' in admin
    redirect = client.get("/admin-membership", follow_redirects=False)
    assert redirect.status_code == 307 and redirect.headers["location"] == "/admin/memberships"
    login = client.get("/login").text
    assert 'href="/membership"' in login
    assert 'value="customer123"' not in login and 'value="customer"' not in login
    for file in ("member_layout.css", "membership.css"):
        assert client.get("/static/css/" + file).status_code == 200
    for file in ("membership.js", "admin_membership.js"):
        assert client.get("/static/js/" + file).status_code == 200


@pytest.mark.parametrize("path", ["/admin", "/admin/accounts", "/admin/memberships", "/admin/website-settings", "/admin/settings"])
def test_unified_admin_uses_one_sidebar_session_and_correct_assets(path):
    client = TestClient(create_app())
    response = client.get(path)
    assert response.status_code == 200
    html = response.text
    assert 'data-admin-session="portal"' in html
    assert 'id="adminWorkspace" hidden' in html
    for section in ("accounts", "memberships", "website-settings", "settings"):
        assert f'href="/admin/{section}"' in html
    assert html.index('src="/admin/static/js/api.js') < html.index('id="adminWorkspace"')
    assert 'href="/accounts"' not in html and 'src="/static/js/accounts.js"' not in html
    assert client.get("/admin/static/js/api.js?v=admin-03").status_code == 200
    assert client.get("/admin/portal-static/js/admin_membership.js?v=admin-03").status_code == 200
    assert 'href="/admin" data-admin-only hidden>Quản trị hệ thống' in client.get("/membership").text


def test_unknown_admin_section_does_not_read_arbitrary_templates():
    assert TestClient(create_app()).get("/admin/not-a-page").status_code == 404
