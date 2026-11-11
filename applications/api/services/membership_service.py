"""Manual bank-transfer membership; approval is only a server-side admin action."""
from copy import deepcopy
from applications.api.services.member_rewards import discounted_price, referral_code, find_referrer
from datetime import datetime, timedelta, timezone
import json
import hashlib
import os
from pathlib import Path
import tempfile
from threading import RLock
from unicodedata import normalize
from uuid import uuid4

from applications.api.auth.password_hasher import hash_password
from applications.api.auth.roles import Role
from applications.api.auth.store import InMemoryUserStore, UserRecord
from applications.api.exceptions import ApplicationsAPIError
from applications.api.schemas.membership import MemberRegistration, MembershipPlan, MembershipReview, MembershipOrderPlan


def fail(message, status=409):
    raise ApplicationsAPIError(message, status_code=status, code="membership_error")


def now():
    return datetime.now(timezone.utc)


def transfer_content(user: UserRecord):
    """Keep Vietnamese names and the account's exact username in bank instructions."""
    return " ".join(" ".join(normalize("NFC", part).split())
                    for part in (user.display_name or "", user.username) if part.strip())


def freeze_transfer_content(user, membership):
    if not membership.get("transfer_content"):
        # Preserve instructions already issued to old pending orders for reconciliation.
        if membership.get("reference"):
            membership["legacy_transfer_content"] = membership["reference"]
        membership["transfer_content"] = transfer_content(user)


class MembershipService:
    def __init__(self, store: InMemoryUserStore, settings_path: Path):
        self.store = store
        self.path = settings_path
        self.lock = RLock()

    def plan(self) -> MembershipPlan:
        with self.lock:
            if self.path.exists():
                return MembershipPlan.model_validate_json(self.path.read_text(encoding="utf-8"))
            return MembershipPlan()

    def public_plan(self):
        from applications.api.services.activity_service import FEATURES
        plan = self.plan()
        return {**plan.model_dump(), "ready": plan.ready, "currency": "VND", "payment_method": "bank_transfer_manual", "features": FEATURES,
                "tiers": [tier.model_dump(exclude={"referral_reward"}) for tier in plan.configured_tiers()]}

    def revision(self):
        return hashlib.sha256(self.path.read_bytes() if self.path.exists() else b"").hexdigest()

    def admin_settings(self):
        from applications.api.services.activity_service import FEATURES
        with self.lock:
            plan = self.plan()
            return {**plan.model_dump(), "tiers": [tier.model_dump() for tier in plan.configured_tiers()],
                    "features": FEATURES, "revision": self.revision()}

    def configure(self, plan: MembershipPlan, *, expected_revision=None):
        with self.lock:
            if expected_revision is not None and expected_revision != self.revision():
                fail("Cấu hình đã được quản trị viên khác sửa. Vui lòng tải lại trước khi lưu.", 412)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.path.parent,
                                                 prefix="membership-", suffix=".tmp", delete=False) as handle:
                    temporary = Path(handle.name)
                    handle.write(plan.model_dump_json(indent=2))
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, self.path)
                temporary = None
            finally:
                if temporary is not None:
                    temporary.unlink(missing_ok=True)
            return self.public_plan()

    def register(self, body: MemberRegistration):
        plan = self.plan()
        if not plan.ready:
            fail("Đang cập nhật biểu phí. Vui lòng quay lại sau.", 503)
        # Hash before taking the store lock; passwords never enter the order or response.
        password_hash = hash_password(body.password.get_secret_value())
        with self.store._lock:
            if self.store.get_by_username(body.username):
                raise ApplicationsAPIError(
                    "Tên đăng nhập đã có người dùng rồi. Bạn hãy chọn tên đăng nhập khác.",
                    status_code=409, code="username_taken", details={"field": "username"},
                )
            referrer = None
            if body.referral_code:
                referrer = find_referrer(self.store, body.referral_code)
                if not referrer or not referrer.has_member_access():
                    fail("Mã giới thiệu không hợp lệ hoặc người giới thiệu chưa có quyền thành viên.", 422)
                if referrer.phone and referrer.phone == body.phone:
                    fail("Không thể dùng mã giới thiệu của chính mình.", 422)
            tier = next(item for item in plan.configured_tiers() if item.tier == body.tier)
            if not tier.enabled:
                fail("Cấp thành viên này đang tạm ngừng đăng ký.", 409)
            selected = plan.model_dump(exclude={"tiers"})
            selected.update(tier.model_dump(include={"title", "amount_vnd", "validity_days", "analysis_limit",
                                                     "feature_limits", "enabled_features"}))
            original_amount = selected["amount_vnd"]
            if referrer:
                selected["amount_vnd"] = discounted_price(original_amount)
            reference = "BTE" + uuid4().hex[:16].upper()
            record = UserRecord(
                user_id="u-" + uuid4().hex, username=body.username,
                display_name=body.display_name, password_hash=password_hash, role=Role.CUSTOMER,
                phone=body.phone,
                analysis_limit=0, membership={
                    "status": "pending", "reference": reference,
                    "registered_at": now().isoformat(), "plan": selected,
                    "tier": body.tier, "original_amount_vnd": original_amount,
                    "discount_percent": 20 if referrer else 0,
                    "referrer_user_id": referrer.user_id if referrer else None,
                    "referral_code": referral_code(referrer) if referrer else "",
                    "referral_reward": tier.referral_reward if referrer else 0,
                    "payment_reported_at": None, "payment_note": "", "expires_at": None,
                },
            )
            record.membership["transfer_content"] = transfer_content(record)
            try:
                self.store.add_user(record)
            except Exception:
                self.store.users_by_id.pop(record.user_id, None)
                self.store.users_by_username.pop(record.username.lower(), None)
                raise
            return self.details(record)

    def details(self, user: UserRecord, *, internal=False):
        membership = deepcopy(user.membership)
        upgrade = None
        memo = None
        instructions_updated = False
        if membership:
            upgrade = membership.pop("upgrade_order", None)
            membership.pop("previous_membership", None)
            plan = membership.get("plan") or {}
            limits = plan.get("feature_limits")
            enabled = plan.get("enabled_features")
            if isinstance(limits, dict) and "van_han" in limits and "good_years" not in limits:
                limits["good_years"] = limits["van_han"]
                if isinstance(enabled, list) and "van_han" in enabled and "good_years" not in enabled:
                    enabled.append("good_years")
            memo = membership.get("transfer_content") or transfer_content(user)
            legacy_memo = membership.get("legacy_transfer_content")
            if not membership.get("transfer_content"):
                legacy_memo = legacy_memo or membership.get("reference")
            instructions_updated = bool(legacy_memo) and membership.get("status") == "pending"
            membership["transfer_content"] = memo
            if internal and legacy_memo:
                membership["legacy_transfer_content"] = legacy_memo
            if not internal:
                membership.pop("reference", None)
                membership.pop("legacy_transfer_content", None)
        return {"user": user.to_public_dict(), "membership": membership,
                "transfer_content": memo, "transfer_instructions_updated": instructions_updated, "upgrade": upgrade}

    def _save(self, user, membership, analysis_limit):
        previous, previous_limit, revision = user.membership, user.analysis_limit, user.account_revision
        try:
            user.membership, user.analysis_limit = membership, analysis_limit
            user.account_revision += 1
            self.store._after_change()
        except Exception:
            user.membership, user.analysis_limit = previous, previous_limit
            user.account_revision = revision
            raise

    def request_upgrade(self, user, tier_number):
        with self.store._lock:
            current = deepcopy(user.membership) or {}
            if (user.role != Role.CUSTOMER or not user.has_member_access()
                    or current.get("tier") not in (1, 2) or tier_number <= current["tier"]):
                fail("Chỉ thành viên cấp 1 hoặc cấp 2 còn hiệu lực được nâng lên cấp cao hơn.", 403)
            pending = current.get("upgrade_order") or {}
            if pending.get("status") == "pending":
                if pending["tier"] == tier_number:
                    return self.details(user)
                fail("Bạn đã có một yêu cầu nâng cấp đang chờ xử lý.")
            plan = self.plan()
            if not plan.ready:
                fail("Đang cập nhật biểu phí. Vui lòng quay lại sau.", 503)
            tier = next(item for item in plan.configured_tiers() if item.tier == tier_number)
            if not tier.enabled:
                fail("Cấp này đang tạm ngừng đăng ký.")
            selected = plan.model_dump(exclude={"tiers"})
            selected.update(tier.model_dump(include={"title", "amount_vnd", "validity_days", "analysis_limit",
                                                     "feature_limits", "enabled_features"}))
            reference = "NC" + uuid4().hex[:12].upper()
            current["upgrade_order"] = {
                "reference": reference, "source": "upgrade", "status": "pending",
                "tier": tier_number, "from_tier": current["tier"], "plan": selected,
                "registered_at": now().isoformat(), "payment_reported_at": None, "payment_note": "",
                "transfer_content": f"{transfer_content(user)} {reference}",
            }
            self._save(user, current, user.analysis_limit)
            return self.details(user)

    def report_upgrade_payment(self, user, reference, note):
        with self.store._lock:
            current = deepcopy(user.membership) or {}
            order = current.get("upgrade_order") or {}
            if order.get("status") != "pending" or order.get("reference") != reference:
                fail("Yêu cầu nâng cấp này đã thay đổi hoặc đã được xử lý.")
            order.update(payment_reported_at=now().isoformat(), payment_note=note)
            self._save(user, current, user.analysis_limit)
            return self.details(user)

    def _review_upgrade(self, user, current, order, body, admin):
        if order["status"] != "pending" or body.decision == "refund":
            fail("Yêu cầu nâng cấp đã được xử lý hoặc không thể hoàn tiền ở trạng thái này.")
        if body.decision == "approve" and not order.get("payment_reported_at"):
            fail("Thành viên chưa gửi xác nhận chuyển khoản.")
        if not user.is_active or user.deleted_at or current.get("tier") != order["from_tier"]:
            fail("Tài khoản hoặc cấp hiện tại đã thay đổi. Kiểm tra lại trước khi duyệt.")
        order.update(reviewed_by=admin.user_id, reviewed_at=now().isoformat(), review_note=body.note)
        if body.decision == "reject":
            order["status"] = "rejected"
            self._save(user, current, user.analysis_limit)
        else:
            plan = MembershipOrderPlan.model_validate(order["plan"])
            expires = now() + timedelta(days=plan.validity_days)
            if current.get("expires_at"):
                expires = max(expires, datetime.fromisoformat(current["expires_at"]))
            current.pop("upgrade_order")
            order.update(status="active", expires_at=expires.isoformat(), previous_membership=current,
                         referral_events=current.get("referral_events", []))
            self._save(user, order, plan.analysis_limit)
        return self.details(user, internal=True)

    def report_payment(self, user: UserRecord, note: str):
        with self.store._lock:
            if not user.membership or user.membership.get("status") != "pending":
                fail("Hồ sơ này không ở trạng thái chờ xác nhận thanh toán.")
            membership = deepcopy(user.membership)
            freeze_transfer_content(user, membership)
            membership["payment_reported_at"] = now().isoformat()
            membership["payment_note"] = note
            self._save(user, membership, user.analysis_limit)
            return self.details(user)

    def review(self, user_id: str, body: MembershipReview, admin: UserRecord):
        if admin.role != Role.ADMIN:
            fail("Chỉ quản trị viên được xác nhận thanh toán.", 403)
        with self.store._lock:
            user = self.store.get_by_id(user_id)
            if not user or not user.membership:
                fail("Không tìm thấy đăng ký thành viên.", 404)
            membership = deepcopy(user.membership)
            upgrade = membership.get("upgrade_order") or {}
            if upgrade.get("reference") == body.expected_reference:
                return self._review_upgrade(user, membership, upgrade, body, admin)
            if user.deleted_at or membership.get("source") == "manual":
                fail("Quyền cấp thủ công hoặc tài khoản đã xóa không phải đơn thanh toán để duyệt.")
            if membership.get("reference") != body.expected_reference:
                fail("Hồ sơ đã thay đổi. Vui lòng tải lại trước khi duyệt.")
            if body.decision == "refund":
                if membership.get("status") != "active":
                    fail("Chỉ ghi nhận hoàn tiền cho đăng ký đã được kích hoạt.")
                if upgrade.get("status") == "pending":
                    fail("Xử lý yêu cầu nâng cấp đang chờ trước khi ghi nhận hoàn tiền.")
                if membership.get("source") == "upgrade":
                    previous = membership.pop("previous_membership")
                    membership.update(status="refunded", reviewed_by=admin.user_id, review_note=body.note,
                                      refunded_at=now().isoformat())
                    previous["upgrade_order"] = membership
                    previous_plan = MembershipOrderPlan.model_validate(previous["plan"])
                    self._save(user, previous, previous_plan.analysis_limit)
                    return self.details(user, internal=True)
                membership.update(status="refunded", reviewed_by=admin.user_id,
                                  review_note=body.note, refunded_at=now().isoformat(), expires_at=now().isoformat())
                self._referral_event(membership, refund=True)
                self._save(user, membership, 0)
                return self.details(user, internal=True)
            if membership.get("status") != "pending":
                fail("Hồ sơ đã được xử lý. Không cấp lại thời hạn hoặc lượt sử dụng.")
            plan = MembershipOrderPlan.model_validate(membership["plan"])
            freeze_transfer_content(user, membership)
            approved = body.decision == "approve"
            membership.update({
                "status": "active" if approved else "rejected",
                "reviewed_by": admin.user_id, "reviewed_at": now().isoformat(),
                "review_note": body.note,
                "expires_at": (now() + timedelta(days=plan.validity_days)).isoformat() if approved else None,
            })
            if approved:
                self._referral_event(membership)
            self._save(user, membership, plan.analysis_limit if approved else 0)
            return self.details(user, internal=True)

    def _referral_event(self, membership, *, refund=False):
        owner = membership.get("referrer_user_id")
        reward = membership.get("referral_reward", 0)
        if not owner or not reward:
            return
        kind = "referral_refund" if refund else "referral"
        membership.setdefault("referral_events", []).append({
            "event": kind + ":" + membership["reference"], "owner": owner,
            "delta": -reward if refund else reward, "kind": kind,
            "created_at": now().isoformat(),
            "description": ("Thu hồi thưởng do hoàn tiền" if refund else "Thưởng giới thiệu") +
                           " gói cấp " + str(membership["tier"]),
        })

    def applications(self):
        with self.store._lock:
            rows = []
            for user in self.store.users_by_id.values():
                if not user.membership or user.deleted_at:
                    continue
                item = self.details(user, internal=True)
                if user.membership.get("source") != "manual":
                    rows.append(item)
                if item["upgrade"]:
                    order = item["upgrade"]
                    rows.append({**item, "membership": order, "transfer_content": order["transfer_content"]})
            return sorted(rows, key=lambda item: item["membership"].get("registered_at", ""), reverse=True)
