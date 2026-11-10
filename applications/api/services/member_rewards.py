"""Shared tier definitions and durable, idempotent Linh Thach ledger."""
import hashlib

TIERS = {
    1: {"tier": 1, "title": "Phong thủy sư cấp 1", "amount_vnd": 688888, "analysis_limit": 2, "referral_reward": 10},
    2: {"tier": 2, "title": "Phong thủy sư cấp 2", "amount_vnd": 2777777, "analysis_limit": 13, "referral_reward": 50},
    3: {"tier": 3, "title": "Phong thủy sư cấp 3", "amount_vnd": 13333333, "analysis_limit": 131, "referral_reward": 100},
}


def feature_entitlement(user, feature):
    plan = (user.membership or {}).get("plan") or {}
    limits = plan.get("feature_limits")
    enabled = plan.get("enabled_features")
    if isinstance(limits, dict) and feature in limits:
        return limits[feature], enabled is None or feature in enabled
    return user.analysis_limit, True


def referral_code(user):
    return "BTE-" + hashlib.sha256(user.user_id.encode()).hexdigest()[:20].upper()


def find_referrer(store, code):
    return next((user for user in store.users_by_id.values() if referral_code(user) == code.upper()), None)


def discounted_price(amount):
    return (amount * 80 + 50) // 100


def ensure_ledger(connection):
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS linh_ledger(
            event TEXT PRIMARY KEY,owner TEXT NOT NULL,delta INTEGER NOT NULL,
            kind TEXT NOT NULL,description TEXT NOT NULL,feature TEXT,created_at TEXT NOT NULL);
        CREATE INDEX IF NOT EXISTS linh_owner ON linh_ledger(owner,created_at);
        CREATE TABLE IF NOT EXISTS linh_ticket_sources(ticket TEXT PRIMARY KEY,redeemed INTEGER NOT NULL);
    """)


def balance(connection, owner):
    return connection.execute("SELECT COALESCE(SUM(delta),0) FROM linh_ledger WHERE owner=?", (owner,)).fetchone()[0]


def extra_credits(connection, owner, feature):
    return connection.execute(
        "SELECT COUNT(*) FROM linh_ledger WHERE owner=? AND kind='redeem' AND feature=?", (owner, feature)
    ).fetchone()[0]


def sync_referrals(service):
    """Replay approval/refund obligations after a crash, once per immutable event."""
    from applications.api.services.activity_service import timestamp
    with service.store._lock:
        events = [
            event for user in service.store.users_by_id.values()
            for event in (user.membership or {}).get("referral_events", [])
        ]
    with service.connect() as connection:
        for event in events:
            connection.execute(
                "INSERT OR IGNORE INTO linh_ledger VALUES(?,?,?,?,?,?,?)",
                (event["event"], event["owner"], event["delta"], event["kind"],
                 event["description"], None, event.get("created_at") or timestamp()),
            )


def wallet(service, user):
    sync_referrals(service)
    with service.connect() as connection:
        entries = connection.execute(
            "SELECT event,delta,kind,description,feature,created_at FROM linh_ledger WHERE owner=? "
            "ORDER BY created_at DESC,event DESC LIMIT 100", (user.user_id,)
        ).fetchall()
        return {"balance": balance(connection, user.user_id), "entries": [dict(row) for row in entries]}


def redeem(service, user, feature, operation_key):
    from applications.api.services.activity_service import ActivityError, FEATURES, timestamp
    if feature not in FEATURES:
        raise ActivityError("Mục đổi không hợp lệ.", 422)
    if not user.has_member_access():
        raise ActivityError("Cần tài khoản thành viên còn hiệu lực.", 403)
    sync_referrals(service)
    event = "redeem:" + user.user_id + ":" + operation_key
    with service.connect() as connection:
        previous = connection.execute("SELECT feature FROM linh_ledger WHERE event=?", (event,)).fetchone()
        if previous:
            if previous["feature"] != feature:
                raise ActivityError("Mã đổi đã được dùng cho mục khác.")
            return {"redeemed": True, "balance": balance(connection, user.user_id)}
        used, pending = service._usage(connection, user, feature)
        limit, enabled = feature_entitlement(user, feature)
        if not enabled:
            raise ActivityError("Chức năng này chưa được mở trong gói của bạn.", 403)
        if limit is None or used + pending < limit + extra_credits(connection, user.user_id, feature):
            raise ActivityError("Bạn vẫn còn lượt ở mục này. Hãy dùng hết trước khi đổi thêm.")
        if balance(connection, user.user_id) < 5:
            raise ActivityError("Cần đủ 5 Linh Thạch để đổi 1 lượt.")
        connection.execute(
            "INSERT INTO linh_ledger VALUES(?,?, -5,'redeem',?,?,?)",
            (event, user.user_id, "Đổi 1 lượt " + FEATURES[feature], feature, timestamp()),
        )
        return {"redeemed": True, "balance": balance(connection, user.user_id)}
