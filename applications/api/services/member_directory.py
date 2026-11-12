"""Admin read model joining member data by immutable account identifier."""
import json

from fastapi import HTTPException

from applications.api.services.activity_service import FEATURES
from applications.api.services.member_rewards import balance


def membership_source(record):
    if record.get("source") == "manual":
        return "Cấp thủ công"
    if record.get("status") == "refunded":
        return "Đã hoàn tiền"
    if record.get("reference") and record.get("status") == "active":
        return "Đã xác nhận thanh toán"
    return "Đăng ký thanh toán" if record.get("reference") else "—"


def _membership_history(user):
    seen = set()
    items = []

    def visit(record):
        if not record or not record.get("reference") or record["reference"] in seen:
            return
        seen.add(record["reference"])
        plan = record.get("plan") or {}
        status = record.get("status")
        amount = record.get("paid_amount_vnd")
        if amount is None:
            amount = plan.get("amount_vnd")
        items.append({
            "reference": record["reference"], "title": plan.get("title"), "tier": record.get("tier"),
            "source": membership_source(record), "status": status,
            "confirmed_amount": amount if status in ("active", "refunded") and record.get("source") != "manual" else None,
            "at": record.get("reviewed_at") or record.get("registered_at"),
            "expires_at": record.get("expires_at"), "refunded_at": record.get("refunded_at"),
            "note": record.get("review_note"),
        })
        visit(record.get("upgrade_order"))
        visit(record.get("previous_membership"))

    visit(user.membership)
    for event in reversed(user.admin_events):
        visit(event.get("previous_membership"))
    return sorted(items, key=lambda row: row["at"] or "", reverse=True)


def setup_member_catalog(connection):
    from applications.api.routes.member_catalog import _tables
    _tables(connection)
    connection.execute("CREATE INDEX IF NOT EXISTS member_submissions_owner_date ON member_submissions(owner,created_at)")


def member_list_activity(connection, owner):
    row = connection.execute("""
        SELECT MAX(at) FROM (
            SELECT MAX(created_at) AS at FROM activity_results WHERE owner=?
            UNION ALL SELECT MAX(created_at) FROM member_submissions WHERE owner=?
            UNION ALL SELECT MAX(created_at) FROM linh_ledger WHERE owner=?
            UNION ALL SELECT MAX(updated_at) FROM courses_progress WHERE owner=?
            UNION ALL SELECT MAX(started_at) FROM courses_access WHERE owner=?
        )""", ("user:" + owner, owner, owner, owner, owner)).fetchone()
    return {"last_activity": row[0]}


def member_history(service, user, section, page):
    limit = 20
    offset = (page - 1) * limit
    owner = user.user_id
    result = {"page": page, "section": section}
    if section == "membership":
        items = _membership_history(user)
        return {**result, "items": items[offset:offset + limit], "has_next": len(items) > offset + limit}
    if section not in ("usage", "orders", "learning", "wallet"):
        raise HTTPException(422, "Mục hồ sơ không hợp lệ.")
    if section == "usage":
        result["usage"] = service.summary(user)
    with service.connect() as connection:
        if section == "usage":
            rows = connection.execute(
                "SELECT kind,id,created_at FROM activity_results WHERE owner=? ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?",
                ("user:" + owner, limit + 1, offset),
            ).fetchall()
            items = [{**dict(row), "label": FEATURES.get(row["kind"], row["kind"])} for row in rows]
        elif section == "orders":
            setup_member_catalog(connection)
            rows = connection.execute(
                "SELECT id,kind,payload,status,created_at FROM member_submissions WHERE owner=? ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?",
                (owner, limit + 1, offset),
            ).fetchall()
            items = []
            for row in rows:
                payload = json.loads(row["payload"])
                item = {key: row[key] for key in ("id", "kind", "status", "created_at")}
                item.update({key: payload.get(key) for key in ("title", "quantity", "total", "reward")})
                granted = connection.execute("SELECT delta FROM linh_ledger WHERE owner=? AND event=?",
                                             (owner, "catalog:" + row["id"])).fetchone()
                item["reward_granted"] = granted[0] if granted else 0
                items.append(item)
        elif section == "learning":
            from applications.api.services.courses import CourseService
            courses = CourseService(service.store)
            rows = connection.execute("""
                SELECT course,price,started_at,expires_at FROM (
                    SELECT course,price,started_at,expires_at,started_at AS sort_at,id
                    FROM courses_access WHERE owner=?
                    UNION ALL
                    SELECT p.course,NULL,NULL,NULL,MAX(p.updated_at),p.course
                    FROM courses_progress AS p WHERE p.owner=? AND p.completed=1
                    AND NOT EXISTS (SELECT 1 FROM courses_access AS a WHERE a.owner=p.owner AND a.course=p.course)
                    GROUP BY p.course
                ) ORDER BY sort_at DESC,id DESC LIMIT ? OFFSET ?
            """, (owner, owner, limit + 1, offset)).fetchall()
            items = []
            for row in rows:
                course_id = row["course"]
                lessons = courses._course(connection, course_id)["lessons"]
                lesson_ids = {lesson["id"] for lesson in lessons}
                marked = connection.execute(
                    "SELECT lesson FROM courses_progress WHERE owner=? AND course=? AND completed=1",
                    (owner, course_id),
                )
                items.append({**dict(row), "title": courses._settings(connection, course_id)["title"],
                              "completed": sum(mark[0] in lesson_ids for mark in marked), "lesson_count": len(lessons)})
        else:
            result["balance"] = balance(connection, owner)
            items = [dict(row) for row in connection.execute("""
                SELECT delta,description,created_at FROM linh_ledger
                WHERE owner=? ORDER BY created_at DESC,event DESC LIMIT ? OFFSET ?
            """, (owner, limit + 1, offset))]
    return {**result, "items": items[:limit], "has_next": len(items) > limit}
