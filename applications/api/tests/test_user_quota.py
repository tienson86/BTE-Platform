from applications.api.auth.roles import Role
from applications.api.auth.store import InMemoryUserStore, UserRecord
from applications.api.services.user_service import UserService


def test_analysis_quota_is_consumed_and_capped() -> None:
    store = InMemoryUserStore()
    store.add_user(UserRecord("u-abc", "ABC", "hash", Role.CUSTOMER, analysis_limit=2))

    assert store.consume_analysis("u-abc") is True
    assert store.consume_analysis("u-abc") is True
    assert store.consume_analysis("u-abc") is False
    assert store.get_by_username("abc").to_public_dict()["analyses_remaining"] == 0


def test_admin_can_change_limit_and_reset_usage() -> None:
    store = InMemoryUserStore()
    store.add_user(UserRecord("u-abc", "ABC", "hash", Role.CUSTOMER, analysis_limit=50, analyses_used=12))

    updated = UserService(store).update_quota("ABC", analysis_limit=200, analyses_used=0)

    assert updated.analysis_limit == 200
    assert updated.analyses_used == 0
    assert updated.to_public_dict()["analyses_remaining"] == 200
