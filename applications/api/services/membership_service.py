"""Manual bank-transfer membership; approval is only a server-side admin action."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
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
from applications.api.schemas.membership import MemberRegistration, MembershipPlan, MembershipReview


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
        plan = self.plan()
        return {**plan.model_dump(), "ready": plan.ready, "currency": "VND", "payment_method": "bank_transfer_manual"}

    def configure(self, plan: MembershipPlan):
        with self.lock:
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
            reference = "BTE" + uuid4().hex[:16].upper()
            record = UserRecord(
                user_id="u-" + uuid4().hex, username=body.username,
                display_name=body.display_name, password_hash=password_hash, role=Role.CUSTOMER,
                analysis_limit=0, membership={
                    "status": "pending", "reference": reference,
                    "registered_at": now().isoformat(), "plan": plan.model_dump(),
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
        memo = None
        instructions_updated = False
        if membership:
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
                "transfer_content": memo, "transfer_instructions_updated": instructions_updated}

    def _save(self, user, membership, analysis_limit):
        previous, previous_limit = user.membership, user.analysis_limit
        try:
            user.membership, user.analysis_limit = membership, analysis_limit
            self.store._after_change()
        except Exception:
            user.membership, user.analysis_limit = previous, previous_limit
            raise

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
            if membership.get("reference") != body.expected_reference:
                fail("Hồ sơ đã thay đổi. Vui lòng tải lại trước khi duyệt.")
            if membership.get("status") != "pending":
                fail("Hồ sơ đã được xử lý. Không cấp lại thời hạn hoặc lượt sử dụng.")
            plan = MembershipPlan.model_validate(membership["plan"])
            freeze_transfer_content(user, membership)
            approved = body.decision == "approve"
            membership.update({
                "status": "active" if approved else "rejected",
                "reviewed_by": admin.user_id, "reviewed_at": now().isoformat(),
                "review_note": body.note,
                "expires_at": (now() + timedelta(days=plan.validity_days)).isoformat() if approved else None,
            })
            self._save(user, membership, plan.analysis_limit if approved else 0)
            return self.details(user, internal=True)

    def applications(self):
        with self.store._lock:
            return sorted([self.details(user, internal=True) for user in self.store.users_by_id.values() if user.membership],
                          key=lambda item: item["membership"]["registered_at"], reverse=True)
