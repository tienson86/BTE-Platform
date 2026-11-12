"""Member courses use the same SQLite transaction as the Linh Thach wallet."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from uuid import uuid4

from applications.api.auth.roles import Role
from applications.api.services.activity_service import ActivityError, ActivityService
from applications.api.services.member_rewards import balance, sync_referrals

CONTENT_PATH = Path(__file__).with_name("course_content.json")
MEDIA_PATH = Path(__file__).parents[1] / "course_media" / "mai-hoa-thuc-hanh.mp4"


def content():
    return json.loads(CONTENT_PATH.read_text(encoding="utf-8"))


def ensure_course_schema(connection):
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS courses_settings(
            id TEXT PRIMARY KEY,payload TEXT NOT NULL,revision INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE IF NOT EXISTS courses_access(
            id TEXT PRIMARY KEY,owner TEXT NOT NULL,course TEXT NOT NULL,
            price INTEGER NOT NULL,revision INTEGER NOT NULL,started_at TEXT NOT NULL,
            expires_at TEXT,operation_key TEXT NOT NULL,UNIQUE(owner,operation_key));
        CREATE INDEX IF NOT EXISTS courses_access_owner ON courses_access(owner,course,started_at);
        CREATE TABLE IF NOT EXISTS courses_custom(
            id TEXT PRIMARY KEY,subject TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS course_lessons(
            course TEXT NOT NULL,id TEXT NOT NULL,payload TEXT NOT NULL,revision INTEGER NOT NULL,
            PRIMARY KEY(course,id));
        CREATE TABLE IF NOT EXISTS courses_progress(
            owner TEXT NOT NULL,course TEXT NOT NULL,lesson TEXT NOT NULL,completed INTEGER NOT NULL,
            updated_at TEXT NOT NULL,PRIMARY KEY(owner,course,lesson));
    """)
    for course in content():
        initial = {key: course[key] for key in ("title", "summary")}
        initial.update(price=0, access_days=None, status="draft")
        initial.update(course.get("defaults", {}))
        payload = json.dumps(initial, ensure_ascii=False)
        connection.execute("INSERT OR IGNORE INTO courses_settings VALUES(?,?,1)",
                           (course["id"], payload))
        if course["id"] == "kinh-dich-nhap-mon":
            # Upgrade the original placeholder without overwriting admin changes.
            placeholder = {
                "title": "Kinh Dịch nhập môn",
                "summary": "Nền tảng Dịch học, 64 quẻ và ý nghĩa hào. Nội dung đang biên soạn.",
                "price": 0, "access_days": None, "status": "draft",
            }
            connection.execute(
                "UPDATE courses_settings SET payload=?, revision=2 WHERE id=? AND revision=1 AND payload=?",
                (payload, course["id"], json.dumps(placeholder, ensure_ascii=False)),
            )
    connection.commit()  # Schema/seed run before ActivityService starts its write transaction.


def fail(message, status=409):
    raise ActivityError(message, status, "course_error")


class CourseService:
    def __init__(self, store, path=None, clock=None):
        self.activity = ActivityService(store, path)
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def _member(self, user):
        if not user.has_member_access():
            fail("Khóa học dành cho tài khoản thành viên còn hiệu lực.", 403)

    def _admin(self, user):
        if not user.is_active or user.role != Role.ADMIN:
            fail("Chỉ Admin được quản lý khóa học.", 403)

    def _course(self, connection, course_id, built_in=None):
        base = built_in or next((c for c in content() if c["id"] == course_id), None)
        if base is None:
            row = connection.execute("SELECT * FROM courses_custom WHERE id=?", (course_id,)).fetchone()
            if row is None:
                fail("Không tìm thấy khóa học.", 404)
            base = {**dict(row), "lessons": []}
        lessons = {item["id"]: {**item, "revision": 0} for item in base["lessons"]}
        for row in connection.execute(
            "SELECT * FROM course_lessons WHERE course=? ORDER BY rowid", (course_id,)
        ):
            lessons[row["id"]] = {**json.loads(row["payload"]), "revision": row["revision"]}
        return {**base, "lessons": list(lessons.values())}

    def create(self, user, body):
        self._admin(user)
        course_id = uuid4().hex
        settings = dict(title=body.title, summary="", price=0, access_days=None, status="draft")
        with self.activity.connect() as c:
            c.execute("INSERT INTO courses_custom VALUES(?,?)", (course_id, body.subject))
            c.execute("INSERT INTO courses_settings VALUES(?,?,1)", (course_id, json.dumps(settings, ensure_ascii=False)))
        return {"id": course_id}

    def lesson_catalog(self, user, course_id):
        self._admin(user)
        with self.activity.connect() as c:
            return self._course(c, course_id)["lessons"]

    def save_lesson(self, user, course_id, body, lesson_id=None):
        self._admin(user)
        with self.activity.connect() as c:
            course = self._course(c, course_id)
            original = next((item for item in course["lessons"] if item["id"] == lesson_id), None)
            if lesson_id is not None and original is None:
                fail("Không tìm thấy bài học.", 404)
            if body.expected_revision != (original["revision"] if original else 0):
                fail("Bài học đã thay đổi. Vui lòng tải lại trước khi lưu.")
            item = body.model_dump(exclude={"expected_revision"})
            item.update(id=lesson_id or uuid4().hex, video=bool(original and original.get("video")))
            revision = body.expected_revision + 1
            c.execute(
                "INSERT INTO course_lessons VALUES(?,?,?,?) ON CONFLICT(course,id) "
                "DO UPDATE SET payload=excluded.payload,revision=excluded.revision",
                (course_id, item["id"], json.dumps(item, ensure_ascii=False), revision),
            )
            return {**item, "revision": revision}

    def _settings(self, connection, course_id):
        row = connection.execute("SELECT * FROM courses_settings WHERE id=?", (course_id,)).fetchone()
        return {**json.loads(row["payload"]), "revision": row["revision"]}

    def _access(self, connection, user, course_id):
        rows = connection.execute("SELECT * FROM courses_access WHERE owner=? AND course=? ORDER BY started_at DESC,id DESC",
                                  (user.user_id, course_id)).fetchall()
        for row in rows:
            if row["expires_at"] is None or datetime.fromisoformat(row["expires_at"]) > self.clock():
                return {**dict(row), "active": True}
        return {**dict(rows[0]), "active": False} if rows else None

    def _view(self, connection, user, course, management=False):
        settings = self._settings(connection, course["id"])
        access = self._access(connection, user, course["id"])
        return {"id": course["id"], "subject": course["subject"], **settings,
                "lesson_count": len(course["lessons"]), "ready": bool(course["lessons"]),
                "has_trial": any(lesson.get("trial") for lesson in course["lessons"]),
                "access": access, "admin_preview": user.role == Role.ADMIN}

    def catalog(self, user, management=False):
        self._admin(user) if management else self._member(user)
        sync_referrals(self.activity)
        with self.activity.connect() as c:
            courses = [self._course(c, course["id"], course) for course in content()]
            ids = c.execute("SELECT id FROM courses_custom ORDER BY rowid").fetchall()
            courses.extend(self._course(c, row["id"]) for row in ids)
            return {"courses": [self._view(c, user, course, management) for course in courses],
                    "balance": balance(c, user.user_id)}

    def configure(self, user, course_id, body):
        self._admin(user)
        values = body.model_dump(exclude={"expected_revision"})
        values["title"] = values["title"].strip()
        if not values["title"]:
            fail("Vui lòng nhập tên khóa học.", 422)
        with self.activity.connect() as c:
            course = self._course(c, course_id)
            if values["status"] == "published" and not course["lessons"]:
                fail("Khóa học chưa có bài học để mở bán.", 422)
            old = self._settings(c, course_id)
            if old["revision"] != body.expected_revision:
                fail("Cấu hình đã thay đổi. Vui lòng tải lại trước khi lưu.")
            c.execute("UPDATE courses_settings SET payload=?,revision=revision+1 WHERE id=?",
                      (json.dumps(values, ensure_ascii=False), course_id))
            return self._view(c, user, course, True)

    def detail(self, user, course_id):
        self._member(user)
        with self.activity.connect() as c:
            course = self._course(c, course_id)
            view = self._view(c, user, course)
            progress = {r["lesson"]: bool(r["completed"]) for r in c.execute(
                "SELECT * FROM courses_progress WHERE owner=? AND course=?", (user.user_id, course_id))}
            paid = user.role == Role.ADMIN or bool(view["access"] and view["access"]["active"])
            view["lessons"] = [{"id": l["id"], "title": l["title"], "section": l["section"],
                                "trial": l.get("trial", False), "completed": progress.get(l["id"], False),
                                "locked": not (paid or l.get("trial", False))} for l in course["lessons"]]
            return view

    def _lesson(self, connection, user, course_id, lesson_id):
        course = self._course(connection, course_id)
        lesson = next((l for l in course["lessons"] if l["id"] == lesson_id), None)
        if lesson is None:
            fail("Không tìm thấy bài học.", 404)
        access = self._access(connection, user, course_id)
        if user.role != Role.ADMIN and not lesson.get("trial") and not (access and access["active"]):
            fail("Bạn cần mở khóa học hoặc gia hạn quyền truy cập.", 403)
        return lesson

    def lesson(self, user, course_id, lesson_id):
        self._member(user)
        with self.activity.connect() as c:
            return self._lesson(c, user, course_id, lesson_id)

    def progress(self, user, course_id, lesson_id, completed):
        self._member(user)
        with self.activity.connect() as c:
            self._lesson(c, user, course_id, lesson_id)
            c.execute("INSERT INTO courses_progress VALUES(?,?,?,?,?) ON CONFLICT(owner,course,lesson) "
                      "DO UPDATE SET completed=excluded.completed,updated_at=excluded.updated_at",
                      (user.user_id, course_id, lesson_id, int(completed), self.clock().isoformat()))
            return {"completed": completed}

    def redeem(self, user, course_id, body):
        self._member(user)
        sync_referrals(self.activity)
        with self.activity.connect() as c:
            course = self._course(c, course_id)
            previous = c.execute("SELECT * FROM courses_access WHERE owner=? AND operation_key=?",
                                 (user.user_id, body.operation_key)).fetchone()
            if previous:
                if previous["course"] != course_id:
                    fail("Mã giao dịch đã dùng cho khóa học khác.")
                return {"access": dict(previous), "balance": balance(c, user.user_id), "replay": True}
            active = self._access(c, user, course_id)
            if active and active["active"]:
                return {"access": active, "balance": balance(c, user.user_id), "replay": True}
            settings = self._settings(c, course_id)
            if settings["status"] != "published" or not course["lessons"]:
                fail("Khóa học chưa mở đổi hoặc đang tạm ngừng.")
            if settings["revision"] != body.expected_revision:
                fail("Giá hoặc thời hạn đã thay đổi. Vui lòng tải lại và xác nhận mức mới.")
            if balance(c, user.user_id) < settings["price"]:
                fail("Số dư Linh Thạch chưa đủ để mở khóa học.")
            date = self.clock()
            expires = (date + timedelta(days=settings["access_days"])).isoformat() if settings["access_days"] else None
            access_id = str(uuid4())
            c.execute("INSERT INTO courses_access VALUES(?,?,?,?,?,?,?,?)",
                      (access_id, user.user_id, course_id, settings["price"], settings["revision"],
                       date.isoformat(), expires, body.operation_key))
            c.execute("INSERT INTO linh_ledger VALUES(?,?,?,?,?,?,?)",
                      ("course:" + access_id, user.user_id, -settings["price"], "course_purchase",
                       "Mở khóa học: " + settings["title"], None, date.isoformat()))
            return {"access": dict(c.execute("SELECT * FROM courses_access WHERE id=?", (access_id,)).fetchone()),
                    "balance": balance(c, user.user_id), "replay": False}
