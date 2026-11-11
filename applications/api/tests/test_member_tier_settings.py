from copy import deepcopy

import pytest

from applications.api.schemas.membership import MembershipPlan, MembershipReview
from applications.api.services.activity_service import ActivityService, ActivityError
from applications.api.services.member_rewards import referral_code, wallet, redeem, feature_entitlement
from applications.api.services.membership_service import MembershipService
from applications.api.services.user_service import UserService
from applications.api.tests.test_membership import system, open_plan, register, approve


def editable(client, headers):
    data = client.get("/api/v1/membership/admin/settings", headers=headers("testadmin")).json()
    revision = data.pop("revision")
    data.pop("features")
    return data, revision


def save(client, headers, data, revision):
    return client.put("/api/v1/membership/admin/settings",
                      headers={**headers("testadmin"), "If-Match": revision}, json=data)


def test_admin_can_edit_three_tiers_and_order_freezes_price_permissions_and_reward(system):
    client, service, store, headers = system
    open_plan(service)
    assert client.get("/api/v1/membership/admin/settings").status_code == 401
    assert client.get("/api/v1/membership/admin/settings", headers=headers("existing")).status_code == 403
    data, revision = editable(client, headers)
    tier = data["tiers"][0]
    tier.update(amount_vnd=900000, validity_days=90, referral_reward=17)
    tier["feature_limits"].update(bazi=4, naming=2)
    tier["enabled_features"].remove("marriage")
    assert save(client, headers, data, revision).status_code == 200
    public = client.get("/api/v1/membership/plan").json()["tiers"][0]
    assert public["amount_vnd"] == 900000 and public["validity_days"] == 90
    assert "referral_reward" not in public
    assert MembershipService(store, service.path).plan().configured_tiers()[0].referral_reward == 17
    source = store.get_by_username("existing")
    result = register(client, tier=1, referral_code=referral_code(source)).json()
    order = result["membership"]["plan"]
    assert order["amount_vnd"] == 720000 and order["validity_days"] == 90
    changed, revision = editable(client, headers)
    changed["tiers"][0].update(amount_vnd=1000000, validity_days=120, referral_reward=99)
    assert save(client, headers, changed, revision).status_code == 200
    assert approve(client, headers, result).status_code == 200
    buyer = store.get_by_username("newmember")
    assert buyer.analysis_limit == 4
    assert buyer.membership["plan"] == order
    assert feature_entitlement(buyer, "naming") == (2, True)
    assert feature_entitlement(buyer, "marriage") == (2, False)
    activity = ActivityService(store)
    assert wallet(activity, source)["balance"] == 17
    for index in range(2):
        ticket = activity.reserve(buyer, "naming", "op-" + str(index), {})
        activity.finish(buyer, ticket["ticket"], {"analysis_id": str(index)})
    with pytest.raises(ActivityError):
        activity.reserve(buyer, "naming", "over-limit", {})
    with pytest.raises(ActivityError) as error:
        activity.reserve(buyer, "marriage", "blocked", {})
    assert error.value.status == 403
    with pytest.raises(ActivityError) as error:
        redeem(activity, buyer, "marriage", "blocked-redemption")
    assert error.value.status == 403


def test_stale_admin_edit_is_rejected_and_disabled_tier_cannot_be_registered(system):
    client, service, store, headers = system
    open_plan(service)
    data, revision = editable(client, headers)
    original = deepcopy(data)
    data["tiers"][1]["enabled"] = False
    assert save(client, headers, data, revision).status_code == 200
    assert save(client, headers, original, revision).status_code == 412
    assert register(client, tier=2).status_code == 409
    assert store.get_by_username("newmember") is None
    assert client.get("/api/v1/membership/plan").json()["tiers"][1]["enabled"] is False


@pytest.mark.parametrize("change", ["duplicate", "negative", "missing-feature", "unknown-feature"])
def test_invalid_tier_configuration_does_not_overwrite_settings(system, change):
    client, service, store, headers = system
    open_plan(service)
    data, revision = editable(client, headers)
    if change == "duplicate":
        data["tiers"][1]["tier"] = 1
    elif change == "negative":
        data["tiers"][0]["feature_limits"]["bazi"] = -1
    elif change == "missing-feature":
        data["tiers"][0]["feature_limits"].pop("naming")
    else:
        data["tiers"][0]["enabled_features"].append("unknown")
    before = service.path.read_bytes()
    assert save(client, headers, data, revision).status_code == 422
    assert service.path.read_bytes() == before


def test_legacy_account_quota_adjustment_still_updates_all_enabled_quotas_and_rolls_back(system, monkeypatch):
    client, service, store, headers = system
    open_plan(service)
    result = register(client).json()
    approve(client, headers, result)
    user = store.get_by_username("newmember")
    UserService(store).update_user(user.username, analysis_limit=9)
    assert feature_entitlement(user, "bazi") == (9, True)
    assert feature_entitlement(user, "naming") == (9, True)
    old = deepcopy(user.membership)
    monkeypatch.setattr(store, "_after_change", lambda: (_ for _ in ()).throw(OSError("disk")))
    with pytest.raises(OSError):
        UserService(store).update_user(user.username, analysis_limit=12)
    assert user.analysis_limit == 9 and user.membership == old


def test_config_write_failure_keeps_previous_file(system, monkeypatch):
    client, service, store, headers = system
    open_plan(service)
    data, revision = editable(client, headers)
    data["tiers"][0]["amount_vnd"] = 800000
    before = service.path.read_bytes()
    monkeypatch.setattr("applications.api.services.membership_service.os.replace",
                        lambda *args: (_ for _ in ()).throw(OSError("disk")))
    with pytest.raises(OSError):
        service.configure(MembershipPlan.model_validate(data), expected_revision=revision)
    assert service.path.read_bytes() == before


@pytest.mark.parametrize("disabled", [False, True])
def test_zero_or_disabled_chart_allowance_can_be_approved_without_blocking_other_tools(system, disabled):
    client, service, store, headers = system
    open_plan(service)
    data, revision = editable(client, headers)
    data["tiers"][0]["feature_limits"]["bazi"] = 0
    if disabled:
        data["tiers"][0]["enabled_features"].remove("bazi")
    assert save(client, headers, data, revision).status_code == 200
    result = register(client, tier=1).json()
    assert approve(client, headers, result).status_code == 200
    buyer = store.get_by_username("newmember")
    assert buyer.analysis_limit == 0
    assert feature_entitlement(buyer, "naming") == (2, True)
    activity = ActivityService(store)
    with pytest.raises(ActivityError) as error:
        activity.reserve(buyer, "bazi", "chart-blocked", {})
    assert error.value.status == (403 if disabled else 429)
    assert activity.reserve(buyer, "naming", "still-allowed", {})["replay"] is False


def test_good_years_inherits_old_settings_then_uses_its_own_quota(system):
    client, service, store, headers = system
    open_plan(service)
    data, revision = editable(client, headers)
    for tier in data["tiers"]:
        tier["feature_limits"].pop("good_years")
        tier["enabled_features"].remove("good_years")
    data["tiers"][0]["feature_limits"]["van_han"] = 3
    assert save(client, headers, data, revision).status_code == 200
    data, revision = editable(client, headers)
    assert data["tiers"][0]["feature_limits"]["good_years"] == 3
    data["tiers"][0]["feature_limits"]["good_years"] = 1
    assert save(client, headers, data, revision).status_code == 200
    order = register(client, tier=1).json()
    assert approve(client, headers, order).status_code == 200
    user = store.get_by_username("newmember")
    activity = ActivityService(store)
    ticket = activity.reserve(user, "good_years", "first-good-year", {})
    activity.finish(user, ticket["ticket"], {"id": "GY-test"})
    result = client.post("/api/v1/van-han/good-years/analyze", headers=headers("newmember"), json={})
    assert result.status_code == 429
    assert result.json()["code"] == "quota_exhausted"
    summary = {item["feature"]: item["remaining"] for item in activity.summary(user)}
    assert summary["good_years"] == 0
    assert summary["van_han"] == 3
