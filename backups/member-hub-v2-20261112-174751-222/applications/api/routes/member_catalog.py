"""Member listings and manually handled registrations/orders."""
from datetime import date, datetime, timezone
import json
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator

from applications.api.auth.dependencies import CurrentUser
from applications.api.auth.roles import Role
from applications.api.dependencies import get_auth_service
from applications.api.services.activity_service import ActivityService

router = APIRouter(tags=["Member catalog"])
Kind = Literal["offline", "shop", "notices"]
RequestKind = Literal["offline", "shop"]


class Listing(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=60000)
    category: str = Field(default="", max_length=120)
    price: int = Field(default=0, ge=0, le=10**10, strict=True)
    offer: int | None = Field(default=None, ge=0, le=10**10, strict=True)
    event_url: HttpUrl | None = None
    published: bool = False
    expected_revision: int = Field(default=0, ge=0, strict=True)

    @model_validator(mode="after")
    def validate_offer(self):
        if self.event_url is not None and (
            self.event_url.scheme != "https" or self.event_url.username or self.event_url.password
        ):
            raise ValueError("Đường dẫn sự kiện phải dùng HTTPS.")
        if self.offer is not None and self.offer > self.price:
            raise ValueError("Giá ưu đãi phải nhỏ hơn hoặc bằng giá niêm yết.")
        return self


class Submission(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    full_name: str = Field(min_length=2, max_length=160)
    phone: str = Field(pattern=r"^\+?[0-9][0-9 .-]{6,22}$")
    birth_date: date
    address: str = Field(min_length=3, max_length=500)
    note: str = Field(default="", max_length=2000)
    quantity: int = Field(default=1, ge=1, le=100, strict=True)
    expected_revision: int = Field(ge=1, strict=True)
    request_key: str = Field(pattern=r"^[a-zA-Z0-9_-]{8,100}$")

    @field_validator("birth_date")
    @classmethod
    def check_date(cls, value):
        if not date(1900, 1, 1) <= value <= date.today():
            raise ValueError("Ngày sinh không hợp lệ.")
        return value


class SubmissionStatus(BaseModel):
    status: Literal["pending", "confirmed", "cancelled"]


def _authorize(user, admin=False):
    if admin:
        if user.role != Role.ADMIN or not user.is_active:
            raise HTTPException(403, "Chỉ Admin được quản lý nội dung và yêu cầu.")
    elif not user.has_member_access():
        raise HTTPException(403, "Tính năng dành cho tài khoản thành viên còn hiệu lực.")


def _db():
    return ActivityService(get_auth_service().store).connect()


def _tables(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS member_listings (
        id TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL, revision INTEGER NOT NULL)""")
    connection.execute("""CREATE TABLE IF NOT EXISTS member_submissions (
        id TEXT PRIMARY KEY, owner TEXT NOT NULL, kind TEXT NOT NULL, listing TEXT NOT NULL,
        request_key TEXT NOT NULL, payload TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL,
        UNIQUE(owner, request_key))""")
    connection.execute("CREATE INDEX IF NOT EXISTS member_submissions_kind_date ON member_submissions(kind,created_at)")


def _listing(row):
    return {"id": row["id"], "revision": row["revision"], **json.loads(row["payload"])}


@router.get("/member-catalog/{kind}")
def listings(kind: Kind, user: CurrentUser):
    _authorize(user)
    with _db() as c:
        _tables(c)
        rows = c.execute("SELECT * FROM member_listings WHERE kind=? AND json_extract(payload,'$.published')=1 ORDER BY rowid DESC", (kind,))
        return {"items": [_listing(row) for row in rows]}


@router.get("/admin/member-catalog/{kind}")
def admin_listings(kind: Kind, user: CurrentUser):
    _authorize(user, admin=True)
    with _db() as c:
        _tables(c)
        rows = c.execute("SELECT * FROM member_listings WHERE kind=? ORDER BY rowid DESC", (kind,))
        return {"items": [_listing(row) for row in rows]}


@router.post("/admin/member-catalog/{kind}", status_code=201)
def create_listing(kind: Kind, body: Listing, user: CurrentUser):
    return _save(kind, body, user)


@router.put("/admin/member-catalog/{kind}/{identifier}")
def edit_listing(kind: Kind, identifier: str, body: Listing, user: CurrentUser):
    return _save(kind, body, user, identifier)


def _save(kind: Kind, body: Listing, user, identifier=None):
    _authorize(user, admin=True)
    payload = body.model_dump(mode="json", exclude={"expected_revision"})
    if kind == "notices":
        payload.update(price=0, offer=None, category="")
    else:
        payload["event_url"] = None
    with _db() as c:
        _tables(c)
        if identifier is None:
            identifier = uuid4().hex
            revision = 1
            c.execute("INSERT INTO member_listings VALUES(?,?,?,?)",
                      (identifier, kind, json.dumps(payload, ensure_ascii=False), revision))
        else:
            revision = body.expected_revision + 1
            changed = c.execute("UPDATE member_listings SET payload=?, revision=? WHERE id=? AND kind=? AND revision=?",
                                (json.dumps(payload, ensure_ascii=False), revision, identifier, kind, body.expected_revision))
            if not changed.rowcount:
                raise HTTPException(409, "Nội dung đã thay đổi hoặc không tồn tại. Vui lòng tải lại.")
        return {"id": identifier, "revision": revision, **payload}


@router.post("/member-catalog/{kind}/{identifier}/requests", status_code=201)
def submit(kind: RequestKind, identifier: str, body: Submission, user: CurrentUser):
    _authorize(user)
    with _db() as c:
        _tables(c)
        previous = c.execute("SELECT id,kind,listing,status FROM member_submissions WHERE owner=? AND request_key=?",
                             (user.user_id, body.request_key)).fetchone()
        if previous:
            if previous["kind"] != kind or previous["listing"] != identifier:
                raise HTTPException(409, "Mã gửi đã được dùng cho yêu cầu khác.")
            return {"id": previous["id"], "status": previous["status"]}
        row = c.execute("SELECT * FROM member_listings WHERE id=? AND kind=?", (identifier, kind)).fetchone()
        if not row or not _listing(row)["published"]:
            raise HTTPException(404, "Mục này đã ngừng nhận yêu cầu.")
        item = _listing(row)
        if body.expected_revision != item["revision"]:
            raise HTTPException(409, "Nội dung hoặc giá đã thay đổi. Vui lòng tải lại để kiểm tra.")
        if kind == "offline" and c.execute(
            "SELECT 1 FROM member_submissions WHERE owner=? AND kind=? AND listing=? AND status!='cancelled'",
            (user.user_id, kind, identifier),
        ).fetchone():
            raise HTTPException(409, "Anh/chị đã đăng ký khóa học này.")
        payload = body.model_dump(mode="json", exclude={"request_key", "expected_revision"})
        quantity = body.quantity if kind == "shop" else 1
        unit_price = item["offer"] if item["offer"] is not None else item["price"]
        payload.update(title=item["title"], quantity=quantity, unit_price=unit_price, total=unit_price * quantity)
        request_id = uuid4().hex
        c.execute("INSERT INTO member_submissions VALUES(?,?,?,?,?,?,?,?)",
                  (request_id, user.user_id, kind, identifier, body.request_key,
                   json.dumps(payload, ensure_ascii=False), "pending", datetime.now(timezone.utc).isoformat()))
        return {"id": request_id, "status": "pending"}


@router.get("/admin/member-catalog/{kind}/requests")
def submissions(kind: RequestKind, user: CurrentUser, page: int = 1):
    _authorize(user, admin=True)
    if not 1 <= page <= 100000:
        raise HTTPException(422, "Số trang không hợp lệ.")
    with _db() as c:
        _tables(c)
        rows = c.execute(
            "SELECT id,payload,status,created_at FROM member_submissions WHERE kind=? "
            "ORDER BY created_at DESC,id DESC LIMIT 51 OFFSET ?", (kind, (page - 1) * 50)
        ).fetchall()
        return {"items": [{**json.loads(r["payload"]), "id": r["id"], "status": r["status"],
                           "created_at": r["created_at"]} for r in rows[:50]], "has_next": len(rows) > 50}


@router.patch("/admin/member-catalog/{kind}/requests/{identifier}")
def update_submission(kind: RequestKind, identifier: str, body: SubmissionStatus, user: CurrentUser):
    _authorize(user, admin=True)
    with _db() as c:
        _tables(c)
        if kind == "offline" and body.status != "cancelled":
            duplicate = c.execute(
                """SELECT 1 FROM member_submissions AS target
                   JOIN member_submissions AS other
                   ON target.owner=other.owner AND target.listing=other.listing AND target.kind=other.kind
                   WHERE target.id=? AND target.kind=? AND other.id!=target.id AND other.status!='cancelled'""",
                (identifier, kind),
            ).fetchone()
            if duplicate:
                raise HTTPException(409, "Thành viên đã có đăng ký còn hiệu lực cho khóa này.")
        result = c.execute("UPDATE member_submissions SET status=? WHERE id=? AND kind=?",
                           (body.status, identifier, kind))
        if not result.rowcount:
            raise HTTPException(404, "Không tìm thấy yêu cầu.")
        return {"status": body.status}
