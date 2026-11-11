from fastapi.testclient import TestClient
from applications.customer_portal.app import create_app


def test_header_wallet_replaces_theme_button_across_shared_pages():
    client=TestClient(create_app())
    for path in ('/membership','/khoa-hoc','/good-date','/result'):
        html=client.get(path).text
        assert 'id="btnThemeToggle"' not in html
        assert 'id="headerLinhThach"' in html
        assert 'href="/linh-thach"' in html
        assert 'title="Xem số dư và đổi Linh Thạch" hidden' in html
        assert '/static/images/membership/linh-thach.png' in html
        assert 'auth_gate.js?v=linh-thach-01' in html


def test_wallet_has_its_own_route_and_membership_has_no_wallet():
    client = TestClient(create_app())
    assert 'id="memberRewards"' not in client.get("/membership").text
    wallet = client.get("/linh-thach")
    assert wallet.status_code == 200
    assert 'id="memberRewards"' in wallet.text
    assert "5 Linh Thạch" in wallet.text
    assert 'href="/chia-se-gioi-thieu"' in wallet.text
