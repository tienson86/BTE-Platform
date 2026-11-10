from fastapi.testclient import TestClient
from applications.customer_portal.app import create_app


def test_header_wallet_replaces_theme_button_across_shared_pages():
    client=TestClient(create_app())
    for path in ('/membership','/khoa-hoc','/good-date','/result'):
        html=client.get(path).text
        assert 'id="btnThemeToggle"' not in html
        assert 'id="headerLinhThach"' in html
        assert 'href="/membership#memberRewards"' in html
        assert 'title="Xem số dư và đổi Linh Thạch" hidden' in html
        assert '/static/images/membership/linh-thach.png' in html
        assert 'auth_gate.js?v=wallet-header-01' in html
