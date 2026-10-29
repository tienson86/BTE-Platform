from datetime import datetime, timedelta, timezone
from copy import deepcopy
from unicodedata import normalize
from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from fastapi.testclient import TestClient

from applications.api import dependencies
from applications.api.app import create_app
from applications.api.auth.membership import requires_membership
from applications.api.auth.password_hasher import hash_password, verify_password
from applications.api.auth.roles import Role
from applications.api.auth.store import JsonUserStore, UserRecord
from applications.api.routes.membership import get_membership_service
from applications.api.schemas.membership import MemberRegistration, MembershipPlan, MembershipReview
from applications.api.services.auth_service import AuthService
from applications.api.services.membership_service import MembershipService


@pytest.fixture
def system(tmp_path, monkeypatch):
    store = JsonUserStore(tmp_path / "users.json")
    for role, name in ((Role.ADMIN, "testadmin"), (Role.CUSTOMER, "existing")):
        store.add_user(UserRecord("u-" + name, name, hash_password("test-password-123"), role))
    auth = AuthService(store)
    monkeypatch.setattr(dependencies, "get_auth_service", lambda: auth)
    service = MembershipService(store, tmp_path / "membership_settings.json")
    app = create_app()
    app.dependency_overrides[get_membership_service] = lambda: service
    client = TestClient(app)
    def headers(name):
        token = auth.login(name, "test-password-123")[1].access_token
        return {"Authorization": "Bearer " + token}
    return client, service, store, headers


def open_plan(service):
    return service.configure(MembershipPlan(amount_vnd=100000, validity_days=365, registration_enabled=True))


def register(client, username="newmember", **extra):
    return client.post("/api/v1/membership/register", json={
        "username": username, "display_name": "Khách thử nghiệm", "phone":"0912345678", "password": "test-password-123", **extra,
    })


def approve(client, headers, data):
    applications = client.get("/api/v1/membership/admin/applications", headers=headers("testadmin")).json()["items"]
    application = next(item for item in applications if item["user"]["user_id"] == data["user"]["user_id"])
    return client.post("/api/v1/membership/admin/applications/" + data["user"]["user_id"] + "/review",
                       headers=headers("testadmin"), json={"decision": "approve", "expected_reference": application["membership"]["reference"]})


def test_initial_plan_has_owner_bank_details_and_no_invented_fee(system):
    client, service, store, headers = system
    plan = client.get("/api/v1/membership/plan").json()
    assert (plan["bank_name"], plan["bank_account"], plan["bank_holder"]) == ("SHB", "28676875", "Nguyễn Tiến Sơn")
    assert plan["amount_vnd"] is None and plan["validity_days"] is None
    assert plan["ready"] is False
    assert register(client).status_code == 503
    assert store.get_by_username("newmember") is None


def test_admin_settings_are_persistent_and_validate_complete_payment_details(system):
    client, service, store, headers = system
    body = MembershipPlan(amount_vnd=100000, validity_days=365, registration_enabled=True,
                          public_notice="Thông báo thử", description="Giới thiệu thử").model_dump()
    assert client.put("/api/v1/membership/admin/settings", json=body).status_code == 401
    assert client.put("/api/v1/membership/admin/settings", json=body, headers=headers("existing")).status_code == 403
    response = client.put("/api/v1/membership/admin/settings", json=body, headers=headers("testadmin"))
    assert response.status_code == 200
    assert MembershipService(store, service.path).public_plan()["public_notice"] == "Thông báo thử"
    assert client.get("/api/v1/membership/plan").json()["description"] == "Giới thiệu thử"
    assert client.put("/api/v1/membership/admin/settings", headers=headers("testadmin"),
                      json={**body, "bank_account": ""}).status_code == 422


def test_register_is_pending_hashed_and_cannot_self_activate(system):
    client, service, store, headers = system
    open_plan(service)
    response = register(client)
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["role"] == "CUSTOMER"
    assert data["user"]["member_access"] is False
    assert data["membership"]["status"] == "pending"
    assert data["transfer_content"] == "Khách thử nghiệm newmember"
    assert "reference" not in data["membership"]
    assert "password" not in response.text
    user = store.get_by_username("newmember")
    assert user.membership["reference"].startswith("BTE")
    assert user.membership["reference"] not in response.text
    assert verify_password("test-password-123", user.password_hash)
    assert "test-password-123" not in store.path.read_text(encoding="utf-8")
    duplicate = register(client, "NEWMEMBER")
    assert duplicate.status_code == 409
    assert duplicate.json()["code"] == "username_taken"
    assert duplicate.json()["details"] == {"field": "username"}
    assert "chọn tên đăng nhập khác" in duplicate.json()["message"]
    member_headers = headers("newmember")
    notice = client.post("/api/v1/membership/payment-notice", headers=member_headers, json={"note": "Giao dịch thử"})
    assert notice.status_code == 200
    assert notice.json()["user"]["member_access"] is False
    assert notice.json()["membership"]["payment_reported_at"]
    assert client.get("/api/v1/membership/admin/applications", headers=member_headers).status_code == 403
    assert client.post("/api/v1/membership/admin/applications/" + user.user_id + "/review", headers=member_headers,
                       json={"decision": "approve", "expected_reference": user.membership["reference"]}).status_code == 403


@pytest.mark.parametrize("extra", [{"role": "ADMIN"}, {"member_access": True}, {"membership": {"status": "active"}},
                                 {"analysis_limit": None}, {"username": "bad name"}, {"password": "short"}])
def test_registration_rejects_privilege_fields_and_invalid_credentials(system, extra):
    client, service, store, headers = system
    open_plan(service)
    assert register(client, **extra).status_code == 422
    assert len(store.users_by_id) == 2


def test_admin_approval_opens_access_once_and_survives_restart(system):
    client, service, store, headers = system
    open_plan(service)
    data = register(client).json()
    member_headers = headers("newmember")
    before = datetime.now(timezone.utc)
    approved = approve(client, headers, data)
    assert approved.status_code == 200
    assert approved.json()["user"]["member_access"] is True
    expires = datetime.fromisoformat(approved.json()["membership"]["expires_at"])
    assert before + timedelta(days=364) < expires < before + timedelta(days=366)
    assert approve(client, headers, data).status_code == 409
    reloaded = JsonUserStore(store.path).get_by_username("newmember")
    assert reloaded.has_member_access() is True
    assert reloaded.analysis_limit is None
    assert client.get("/api/v1/auth/me", headers=member_headers).json()["member_access"] is True
    assert client.post("/api/v1/analyze", headers=member_headers, json={}).status_code == 422


@pytest.mark.parametrize("path,method", [
    ("/analysis", "post"), ("/api/v1/analyze", "post"), ("/api/v1/bazi", "post"),
    ("/api/v1/report", "post"), ("/api/v1/date-selection/search", "post"),
    ("/api/v1/export/pdf", "post"), ("/api/v1/export/docx", "post"),
    ("/api/v1/date-selection/report/pdf", "post"), ("/api/v1/van-han/history", "get"),
    ("/api/v1/analysis-archive", "get"),
])
def test_paid_views_and_downloads_are_blocked_before_processing(system, path, method):
    client, service, store, headers = system
    open_plan(service); register(client)
    assert getattr(client, method)(path).status_code == 401
    assert getattr(client, method)(path, headers=headers("newmember")).status_code == 403


def test_free_tools_remain_available_without_login_even_for_pending_member(system):
    client, service, store, headers = system
    open_plan(service); register(client)
    for options in ({}, {"headers": headers("newmember")}):
        result = client.post("/api/v1/date-selection/month", json={"year": 2026, "month": 10}, **options)
        assert result.status_code == 200
        result = client.post("/api/v1/number-energy/analyze", json={"number": "0912345678", "purpose_context": "phone_number"}, **options)
        assert result.status_code == 200
    for path in ("/api/v1/calendar", "/api/v1/date-selection/day", "/api/v1/number-energy/analyze"):
        assert requires_membership(path) is False


def test_expiry_and_existing_accounts_use_current_server_record(system):
    client, service, store, headers = system
    open_plan(service)
    data = register(client).json(); approve(client, headers, data)
    user = store.get_by_username("newmember")
    user.membership["expires_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    assert client.get("/api/v1/auth/me", headers=headers("newmember")).json()["member_access"] is False
    assert client.post("/api/v1/export/pdf", headers=headers("newmember"), json={}).status_code == 403
    assert client.post("/api/v1/analyze", headers=headers("existing"), json={}).status_code == 422
    assert client.get("/api/v1/auth/me", headers=headers("existing")).json()["membership_status"] == "existing"


def test_bank_and_price_changes_do_not_rewrite_an_existing_order(system):
    client, service, store, headers = system
    open_plan(service)
    register(client)
    service.configure(MembershipPlan(amount_vnd=200000, validity_days=30, bank_name="Other", bank_account="123456", registration_enabled=True))
    own = client.get("/api/v1/membership/me", headers=headers("newmember")).json()
    assert own["membership"]["plan"]["amount_vnd"] == 100000
    assert own["membership"]["plan"]["bank_account"] == "28676875"
    assert own["membership"]["plan"]["validity_days"] == 365


def test_approval_rolls_back_if_durable_save_fails(system, monkeypatch):
    client, service, store, headers = system
    open_plan(service)
    data = register(client).json()
    user = store.get_by_username("newmember")
    def disk_error():
        raise OSError("disk test")
    monkeypatch.setattr(store, "_after_change", disk_error)
    with pytest.raises(OSError):
        service.review(user.user_id, MembershipReview(decision="approve", expected_reference=user.membership["reference"]), store.get_by_username("testadmin"))
    assert user.membership["status"] == "pending" and user.analysis_limit == 0


def test_transfer_memo_normalizes_name_and_preserves_username_and_snapshot(system):
    client, service, store, headers = system
    open_plan(service)
    name = normalize("NFD", "  Nguyễn   Văn\tAn  ")
    data = register(client, "An.Test_29", display_name=name).json()
    expected = "Nguyễn Văn An An.Test_29"
    assert data["transfer_content"] == expected
    user = store.get_by_username("An.Test_29")
    reference = user.membership["reference"]
    user.display_name = "Tên đã thay đổi"
    store._after_change()
    own = client.get("/api/v1/membership/me", headers=headers("An.Test_29"))
    assert own.json()["transfer_content"] == expected
    assert reference not in own.text
    assert JsonUserStore(store.path).get_by_username("An.Test_29").membership["transfer_content"] == expected
    application = client.get("/api/v1/membership/admin/applications", headers=headers("testadmin")).json()["items"][0]
    assert application["membership"]["reference"] == reference
    assert application["transfer_content"] == expected
    assert "legacy_transfer_content" not in application["membership"]


@pytest.mark.parametrize("already_reported", [False, True])
def test_old_pending_order_keeps_previous_memo_for_admin_only(system, already_reported):
    client, service, store, headers = system
    open_plan(service)
    register(client)
    user = store.get_by_username("newmember")
    user.membership.pop("transfer_content")
    if already_reported:
        user.membership["payment_reported_at"] = "2026-10-28T01:00:00+00:00"
    store._after_change()
    reference = user.membership["reference"]
    original = deepcopy(user.membership)
    disk_before = store.path.read_bytes()
    own = client.get("/api/v1/membership/me", headers=headers("newmember"))
    assert own.json()["transfer_content"] == "Khách thử nghiệm newmember"
    assert own.json()["transfer_instructions_updated"] is True
    assert reference not in own.text
    application = client.get("/api/v1/membership/admin/applications", headers=headers("testadmin")).json()["items"][0]
    assert application["membership"]["reference"] == reference
    assert application["membership"]["legacy_transfer_content"] == reference
    assert user.membership == original and store.path.read_bytes() == disk_before
    notice = client.post("/api/v1/membership/payment-notice", headers=headers("newmember"), json={"note": "Đã chuyển theo hướng dẫn cũ"})
    assert notice.status_code == 200 and reference not in notice.text
    reloaded = JsonUserStore(store.path).get_by_username("newmember")
    assert reloaded.membership["legacy_transfer_content"] == reference
    assert reloaded.membership["transfer_content"] == "Khách thử nghiệm newmember"
    result = approve(client, headers, own.json())
    assert result.status_code == 200 and result.json()["user"]["member_access"] is True
    assert result.json()["membership"]["reference"] == reference
    assert result.json()["membership"]["legacy_transfer_content"] == reference
    assert approve(client, headers, own.json()).status_code == 409


def test_approved_member_download_still_enforces_ownership(system, monkeypatch, tmp_path):
    client, service, store, headers = system
    open_plan(service); data = register(client).json(); approve(client, headers, data)
    owner = "user:" + data["user"]["user_id"]
    from applications.api.routes import export
    monkeypatch.setattr(export, "get_snapshot", lambda actual_owner, identifier: {"data": {"test": True}, "input": {}} if actual_owner == owner and identifier == "owned" else None)
    file = tmp_path / "sample.pdf"; file.write_bytes(b"%PDF-1.4 test")
    monkeypatch.setattr(export, "prepare_customer_report_input", lambda **kwargs: kwargs)
    monkeypatch.setattr(export, "export_customer_file", lambda **kwargs: (file, "sample.pdf", None))
    response = client.post("/api/v1/export/pdf", headers=headers("newmember"), json={"analysis_id": "owned"})
    assert response.status_code == 200 and response.content.startswith(b"%PDF")
    assert "attachment" in response.headers["content-disposition"]
    assert client.post("/api/v1/export/pdf", headers=headers("existing"), json={"analysis_id": "owned"}).status_code == 404


def test_consulting_api_checks_membership_from_verified_main_profile(monkeypatch, tmp_path):
    monkeypatch.setenv("BTE_MARRIAGE_DATA_PATH", str(tmp_path / "marriage.json"))
    monkeypatch.setenv("BTE_CHILDBIRTH_DATA_DIR", str(tmp_path / "childbirth"))
    from consulting.marriage.api.http import create_marriage_api_app
    client = TestClient(create_marriage_api_app())
    response = httpx.Response(200, json={"user_id": "pending", "member_access": False})
    requester = AsyncMock(return_value=response)
    factory = Mock(return_value=AsyncMock()); factory.return_value.__aenter__.return_value.get = requester
    monkeypatch.setattr("consulting.archive_access.httpx.AsyncClient", factory)
    for route in ("naming/analyze", "marriage", "childbirth/analyze", "marriage/example/export/pdf"):
        result = client.post("/api/v1/consulting/" + route, headers={"Authorization": "Bearer test"}, json={})
        assert result.status_code == 403
