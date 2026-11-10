from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy

import pytest

from applications.api.auth.store import JsonUserStore, UserRecord
from applications.api.auth.roles import Role
from applications.api.schemas.membership import MemberRegistration, MembershipReview
from applications.api.services.activity_service import ActivityService, ActivityError, FEATURES
from applications.api.services.member_rewards import referral_code, wallet, redeem
from applications.api.services.membership_service import MembershipService
from applications.api.tests.test_membership import system, open_plan, register, approve


@pytest.mark.parametrize("tier,amount,reward,limit", [
    (1, 551110, 10, 2), (2, 2222222, 50, 13), (3, 10666666, 100, 131),
])
def test_tier_referral_is_frozen_and_only_awarded_after_admin_approval(system, tier, amount, reward, limit):
    client, service, store, headers = system
    open_plan(service)
    referrer = store.get_by_username("existing")
    code = referral_code(referrer)
    activity = ActivityService(store)
    preview = client.get("/api/v1/membership/referral/" + code).json()
    assert preview["discount_percent"] == 20
    result = register(client, tier=tier, referral_code=code).json()
    member = result["membership"]
    assert member["plan"]["amount_vnd"] == amount
    assert member["plan"]["analysis_limit"] == limit
    assert wallet(activity, referrer)["balance"] == 0
    client.post("/api/v1/membership/payment-notice", headers=headers("newmember"), json={})
    assert wallet(activity, referrer)["balance"] == 0
    assert approve(client, headers, result).status_code == 200
    assert wallet(activity, referrer)["balance"] == reward
    assert approve(client, headers, result).status_code == 409
    assert wallet(activity, referrer)["balance"] == reward
    restored = JsonUserStore(store.path)
    assert wallet(ActivityService(restored), restored.get_by_username("existing"))["balance"] == reward
    assert len(wallet(activity, referrer)["entries"]) == 1


def test_invalid_referrer_self_phone_and_client_price_are_rejected(system):
    client, service, store, headers = system
    open_plan(service)
    assert register(client, referral_code="BTE-invalid", tier=1).status_code == 422
    source = store.get_by_username("existing")
    source.phone = "0912345678"
    assert register(client, referral_code=referral_code(source), tier=1).status_code == 422
    assert register(client, tier=1, amount_vnd=1000).status_code == 422
    assert register(client, tier=4).status_code == 422
    assert register(client, tier=True).status_code == 422


def test_approval_failure_creates_no_reward_obligation(system, monkeypatch):
    client, service, store, headers = system
    open_plan(service)
    source = store.get_by_username("existing")
    register(client, tier=2, referral_code=referral_code(source))
    buyer = store.get_by_username("newmember")
    before = deepcopy(buyer.membership)
    monkeypatch.setattr(store, "_after_change", lambda: (_ for _ in ()).throw(OSError("disk")))
    with pytest.raises(OSError):
        service.review(buyer.user_id, MembershipReview(decision="approve", expected_reference=before["reference"]),
                       store.get_by_username("testadmin"))
    assert buyer.membership == before
    assert wallet(ActivityService(store), source)["balance"] == 0


def test_refund_revokes_reward_even_after_spending_and_is_not_repeatable(system):
    client, service, store, headers = system
    open_plan(service)
    source = store.get_by_username("existing")
    result = register(client, tier=1, referral_code=referral_code(source)).json()
    approve(client, headers, result)
    activity = ActivityService(store)
    source.analysis_limit = 0
    redeem(activity, source, "naming", "redeem-first-request")
    redeem(activity, source, "business", "redeem-second-request")
    assert wallet(activity, source)["balance"] == 0
    buyer = store.get_by_username("newmember")
    body = MembershipReview(decision="refund", expected_reference=buyer.membership["reference"])
    service.review(buyer.user_id, body, store.get_by_username("testadmin"))
    assert not buyer.has_member_access()
    assert wallet(activity, source)["balance"] == -10
    with pytest.raises(ActivityError):
        redeem(activity, source, "marriage", "another-request-key")
    with pytest.raises(Exception):
        service.review(buyer.user_id, body, store.get_by_username("testadmin"))


@pytest.mark.parametrize("feature", list(FEATURES))
def test_each_successful_tool_earns_once_and_cancelled_or_redeemed_work_does_not(tmp_path, feature):
    store = JsonUserStore(tmp_path / "users.json")
    user = store.add_user(UserRecord("u1", "tester", "hash", Role.CUSTOMER, analysis_limit=1))
    activity = ActivityService(store)
    failed = activity.reserve(user, feature, "failed", {})
    activity.cancel(user, failed["ticket"])
    assert wallet(activity, user)["balance"] == 0
    held = activity.reserve(user, feature, "success", {}, legacy=feature == "bazi")
    if feature == "bazi":
        store.consume_analysis(user.user_id)
    output = {"analysis_id": "result-1"}
    activity.finish(user, held["ticket"], output)
    activity.finish(user, held["ticket"], output)
    assert wallet(activity, user)["balance"] == 1
    # Seed four extra points for this test to exercise redemption and the normal entry point.
    with activity.connect() as connection:
        connection.execute("INSERT INTO linh_ledger VALUES('seed',?,4,'test','test',NULL,'2026')", (user.user_id,))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: redeem(activity, user, feature, "same-operation-key"), range(2)))
    assert all(item["redeemed"] for item in results)
    assert wallet(activity, user)["balance"] == 0
    assert next(item for item in activity.summary(user) if item["feature"] == feature)["remaining"] == 1
    held = activity.reserve(user, feature, "redeemed-use", {}, legacy=feature == "bazi")
    if feature == "bazi":
        assert store.consume_analysis(user.user_id, reserved=True)
    activity.finish(user, held["ticket"], {"analysis_id": "result-2"})
    assert wallet(activity, user)["balance"] == 0
    with pytest.raises(ActivityError):
        activity.reserve(user, feature, "too-many", {})


def test_redeemed_chart_works_through_normal_analysis_endpoint(system, monkeypatch):
    from types import SimpleNamespace
    from applications.api.routes import v1
    client, service, store, headers = system
    source = store.get_by_username("existing")
    source.analysis_limit = 0
    activity = ActivityService(store)
    with activity.connect() as connection:
        connection.execute("INSERT INTO linh_ledger VALUES('seed',?,5,'test','test',NULL,'2026')", (source.user_id,))
    redeem(activity, source, "bazi", "redeemed-chart-operation")
    client.app.dependency_overrides[v1.get_orchestrator] = lambda: SimpleNamespace(analyze=lambda **kwargs: {})
    monkeypatch.setattr(v1, "attach_presentation_metadata", lambda data, body: {"analysis_id": "redeemed-chart"})
    monkeypatch.setattr(v1, "stamp_customer_result_identity", lambda data, request_id: data)
    monkeypatch.setattr(v1, "build_bazi_analysis_result", lambda *args, **kwargs: {})
    monkeypatch.setattr(v1.KnowledgePipeline, "portal_status", lambda: {})
    monkeypatch.setattr(v1, "save_snapshot", lambda *args: None)
    result = client.post("/api/v1/analyze", headers=headers("existing"), json={
        "year":1987,"month":1,"day":21,"hour":4,"minute":30,"gender":"male","timezone":"Asia/Ho_Chi_Minh",
    })
    assert result.status_code == 200, result.text
    assert source.analyses_used == 1
    assert wallet(activity, source)["balance"] == 0
    assert client.post("/api/v1/analyze", headers=headers("existing"), json={
        "year":1987,"month":1,"day":21,"hour":4,"minute":30,"gender":"male","timezone":"Asia/Ho_Chi_Minh",
    }).status_code == 429
