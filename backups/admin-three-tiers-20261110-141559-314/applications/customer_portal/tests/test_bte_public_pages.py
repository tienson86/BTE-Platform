import re

import pytest
from fastapi.testclient import TestClient

from applications.customer_portal.app import create_app


@pytest.mark.parametrize("path,key", [
    ("/gioi-thieu-bte", "about-bte"),
    ("/thanh-vien-bte", "member-plans"),
])
def test_public_pages_have_active_navigation_and_resolvable_assets(path, key):
    client = TestClient(create_app())
    response = client.get(path)
    assert response.status_code == 200
    assert re.search(rf'data-nav-id="{key}" aria-current="page"', response.text)
    assert "{{" not in response.text
    for asset in re.findall(r'(?:src|href)="(/static/(?:images/membership|css/bte_public_pages)[^"]+)"', response.text):
        assert client.get(asset).status_code == 200


def test_member_page_has_exact_seven_earn_and_redeem_rates():
    html = TestClient(create_app()).get("/thanh-vien-bte").text
    table = re.search(r"<tbody>(.*?)</tbody>", html, re.S).group(1)
    assert table.count("<tr>") == 7
    assert table.count("<td>+1 Linh Thạch</td>") == 7
    assert table.count("<td>5 Linh Thạch</td>") == 7
    for value in ("688.888", "2.777.777", "13.333.333"):
        assert value in html
    for tier in ("1", "2", "3"):
        assert f'href="/membership?tier={tier}"' in html


def test_referral_link_is_below_member_status_and_logout_is_available():
    client = TestClient(create_app())
    html = client.get("/membership").text
    assert html.index('href="/membership">Trạng thái thành viên') < html.index('href="/chia-se-gioi-thieu"')
    assert 'id="memberLogout"' in html
    assert 'name="tier"' in html and 'name="referral_code"' in html
    share = client.get("/chia-se-gioi-thieu")
    assert share.status_code == 200 and 'id="referralRewards"' in share.text


def test_public_member_page_omits_referral_promotion():
    html = TestClient(create_app()).get("/thanh-vien-bte").text
    assert "Giới thiệu bạn đồng hành — Cùng nhận ưu đãi" not in html
    assert "người giới thiệu nhận" not in html
    assert "551.110" not in html
    assert "Cùng học hỏi và mở rộng góc nhìn" in html
    assert "Các nội dung học thêm" in html
