"""Admin account lifecycle and explicit manual tier grants, without payment rewards."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4
from applications.api.auth.roles import Role
from applications.api.exceptions import ApplicationsAPIError
from applications.api.services.membership_service import MembershipService


def fail(message, status=409):
    raise ApplicationsAPIError(message, status_code=status, code="account_admin_error")


class AccountAdminService:
    def __init__(self, store):
        self.store = store
        self.memberships = MembershipService(store, Path(getattr(store, "path", "applications/data/users.json")).parent / "membership_settings.json")

    def _target(self, admin, username, revision):
        if admin.role != Role.ADMIN or not admin.is_active or admin.deleted_at:
            fail("Chỉ Admin được thực hiện thao tác này.", 403)
        user = self.store.get_by_username(username)
        if not user:
            fail("Không tìm thấy tài khoản.", 404)
        if user.account_revision != revision:
            fail("Tài khoản đã thay đổi. Vui lòng tải lại trước khi thao tác.")
        return user

    def _save(self, user, changes, admin, action, note):
        event = {"action": action, "actor": admin.user_id, "at": datetime.now(timezone.utc).isoformat(),
                 "note": note, "previous_membership": deepcopy(user.membership), "previous_active": user.is_active,
                 "previous_limit": user.analysis_limit}
        updates = {**changes, "account_revision": user.account_revision + 1, "admin_events": [*user.admin_events, event]}
        before = {key: getattr(user, key) for key in updates}
        try:
            for key, value in updates.items():
                setattr(user, key, value)
            self.store._after_change()
        except Exception:
            for key, value in before.items():
                setattr(user, key, value)
            raise
        return user.to_public_dict()

    def grant(self, admin, username, body):
        with self.store._lock:
            user = self._target(admin, username, body.expected_revision)
            if user.deleted_at:
                fail("Khôi phục tài khoản trước khi cấp thành viên.")
            plan = self.memberships.plan()
            tier = next(t for t in plan.configured_tiers() if t.tier == body.tier)
            selected = plan.model_dump(exclude={"tiers"})
            selected.update(tier.model_dump(include={"title", "amount_vnd", "analysis_limit", "feature_limits", "enabled_features"}))
            selected["validity_days"] = body.validity_days
            date = datetime.now(timezone.utc)
            membership = {"status": "active", "source": "manual", "tier": body.tier,
                          "plan": selected, "reference": "MANUAL-" + uuid4().hex,
                          "registered_at": date.isoformat(), "reviewed_at": date.isoformat(),
                          "reviewed_by": admin.user_id, "review_note": body.note,
                          "expires_at": (date + timedelta(days=body.validity_days)).isoformat(),
                          "payment_method": "manual_grant", "paid_amount_vnd": 0,
                          "referral_reward": 0, "referrer_user_id": None,
                          "referral_events": deepcopy((user.membership or {}).get("referral_events", []))}
            # Keep accumulated usage, credits, courses and the account's locked/unlocked state.
            return self._save(user, {"membership": membership, "analysis_limit": tier.analysis_limit},
                              admin, "grant_tier_" + str(body.tier), body.note)

    def action(self, admin, username, action, body):
        with self.store._lock:
            user = self._target(admin, username, body.expected_revision)
            if action in ("lock", "delete"):
                if user.user_id == admin.user_id:
                    fail("Không thể tự khóa hoặc xóa tài khoản đang quản trị.")
                active_admins = [u for u in self.store.users_by_id.values()
                                 if u.role == Role.ADMIN and u.is_active and not u.deleted_at]
                if user.role == Role.ADMIN and user.is_active and len(active_admins) <= 1:
                    fail("Không thể khóa hoặc xóa Admin cuối cùng.")
            if action == "restore":
                if not user.deleted_at:
                    fail("Tài khoản chưa bị xóa.")
                updates = {"deleted_at": None, "is_active": False}
            elif user.deleted_at:
                fail("Tài khoản đã xóa. Vui lòng khôi phục trước.")
            elif action == "delete":
                updates = {"deleted_at": datetime.now(timezone.utc).isoformat(), "is_active": False}
            elif action in ("lock", "unlock"):
                updates = {"is_active": action == "unlock"}
            else:
                fail("Thao tác không hợp lệ.", 422)
            return self._save(user, updates, admin, action, body.note)
