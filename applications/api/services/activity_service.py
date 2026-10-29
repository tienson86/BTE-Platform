"""Durable per-tool allowances and the shared consultation/contact archive."""
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from pathlib import Path
import secrets
import sqlite3
import time
from threading import RLock
from uuid import uuid4

FEATURES = {"bazi":"Xem lá số", "date_selection":"Chọn ngày tốt", "marriage":"Tư vấn hôn nhân",
            "childbirth":"Tư vấn sinh con", "naming":"Tư vấn đặt tên", "business":"Tư vấn hợp tác", "van_han":"Tính vận hạn"}
ROOT = Path(__file__).resolve().parents[3]
_SCHEMA_LOCK = RLock()

def timestamp():
    return datetime.now(timezone.utc).isoformat()

class ActivityError(Exception):
    def __init__(self, message, status=409, code="activity_error"):
        super().__init__(message)
        self.status, self.code = status, code

def service_key():
    configured = os.getenv("BTE_INTERNAL_SERVICE_SECRET")
    if configured:
        return configured
    path = Path(os.getenv("BTE_DATA_DIR") or ROOT / "applications/data") / "consulting-service.key"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        pass
    else:
        with os.fdopen(handle, "w", encoding="ascii") as output:
            output.write(secrets.token_hex(32))
            output.flush(); os.fsync(output.fileno())
    for _ in range(5):
        key = path.read_text(encoding="ascii").strip()
        if len(key) >= 32:
            return key
        time.sleep(.01)
    raise RuntimeError("Internal service key is not ready")

def result_identity(feature, output, fallback):
    data = output.get("data") or output.get("row") or output
    if not isinstance(data, dict):
        data = {}
    return str(data.get("consultation_id") or data.get("analysis_id") or data.get("id") or fallback)

def customer_label(inputs):
    for key in ("full_name", "name", "current_name", "family_name", "surname"):
        if inputs.get(key):
            return str(inputs[key])[:200]
    names = [str((inputs.get(key) or {}).get("full_name") or "") for key in ("person_a", "person_b", "father", "mother") if isinstance(inputs.get(key), dict)]
    return " / ".join(filter(None, names)) or "Hồ sơ tư vấn"

class ActivityService:
    def __init__(self, store, path=None):
        self.store = store
        directory = Path(getattr(store, "path", ROOT / "applications/data/users.json")).parent
        self.path = Path(path or os.getenv("BTE_USAGE_DB_PATH") or directory / "customer_activity.sqlite3")

    @contextmanager
    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        try:
            with _SCHEMA_LOCK:
                if connection.execute("PRAGMA journal_mode").fetchone()[0] != "wal":
                    connection.execute("PRAGMA journal_mode=WAL")
                connection.execute("PRAGMA synchronous=FULL")
                connection.executescript("""
                CREATE TABLE IF NOT EXISTS feature_baselines(owner TEXT,feature TEXT,used INTEGER,ids TEXT,PRIMARY KEY(owner,feature));
                CREATE TABLE IF NOT EXISTS usage_tickets(id TEXT PRIMARY KEY,owner TEXT,feature TEXT,operation_key TEXT,input_hash TEXT,input_json TEXT,state TEXT,legacy INTEGER,created_at TEXT,output_json TEXT,status_code INTEGER,UNIQUE(owner,feature,operation_key));
                CREATE TABLE IF NOT EXISTS activity_results(owner TEXT,kind TEXT,id TEXT,created_at TEXT,customer_name TEXT,creator_username TEXT,creator_display_name TEXT,phone TEXT,snapshot TEXT,PRIMARY KEY(owner,kind,id));
                CREATE INDEX IF NOT EXISTS usage_owner_feature ON usage_tickets(owner,feature,state);
                """)
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback(); raise
        finally:
            connection.close()

    def _old_ids(self, user, feature):
        identifiers = []
        if feature in ("marriage", "business"):
            path = Path(os.getenv("BTE_MARRIAGE_DATA_PATH") or ROOT / "applications/data/marriage_consultations.json")
            records = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else []
            for record in records:
                client = ((record.get("request") or {}).get("request_meta") or {}).get("client") or ""
                kind = "business" if record.get("business_profile") or client.split(";",1)[0] == "business_consulting" else "marriage"
                if record.get("owner_user_id") == user.user_id and kind == feature:
                    identifiers.append(record["history"]["consultation_id"])
        if feature == "childbirth":
            directory = Path(os.getenv("BTE_CHILDBIRTH_DATA_DIR") or ROOT / "applications/data/childbirth")
            for path in directory.glob("CB-*.json"):
                record = json.loads(path.read_text(encoding="utf-8-sig"))
                if record.get("owner_user_id") == user.user_id:
                    identifiers.append(record["consultation_id"])
        if feature == "van_han":
            from applications.api.services.analysis_archive import _connect
            with _connect() as connection:
                if connection.execute("SELECT name FROM sqlite_master WHERE name='van_han_results'").fetchone():
                    identifiers = [row[0] for row in connection.execute("SELECT id FROM van_han_results WHERE owner=?", ("user:"+user.user_id,))]
        return list(set(identifiers))

    def _usage(self, connection, user, feature):
        baseline = connection.execute("SELECT used,ids FROM feature_baselines WHERE owner=? AND feature=?", (user.user_id,feature)).fetchone()
        if baseline is None:
            ids = self._old_ids(user, feature)
            connection.execute("INSERT INTO feature_baselines VALUES(?,?,?,?)", (user.user_id,feature,len(ids),json.dumps(ids)))
            baseline_used = len(ids)
        else:
            baseline_used = baseline[0]
        # Existing chart usage remains authoritative and is never reset on deployment.
        if feature == "bazi":
            baseline_used = user.analyses_used
        committed, pending = connection.execute("SELECT COALESCE(SUM(state='committed' AND legacy=0),0),COALESCE(SUM(state='held'),0) FROM usage_tickets WHERE owner=? AND feature=?", (user.user_id,feature)).fetchone()
        return int(baseline_used + committed), int(pending)

    def summary(self, user):
        items = []
        with self.connect() as connection:
            for feature, label in FEATURES.items():
                used, pending = self._usage(connection, user, feature)
                limit = user.analysis_limit
                items.append({"feature":feature,"label":label,"limit":limit,"used":used,"pending":pending,
                              "remaining":None if limit is None else max(0,limit-used-pending)})
        return items

    def reserve(self, user, feature, operation_key, inputs, legacy=False):
        if feature not in FEATURES:
            raise ActivityError("Loại tư vấn không hợp lệ.", 422)
        if not user.has_member_access():
            raise ActivityError("Tài khoản chưa có quyền thành viên còn hiệu lực.",403,"membership_required")
        encoded = json.dumps(inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        fingerprint = hashlib.sha256(encoded.encode()).hexdigest()
        with self.connect() as connection:
            previous = connection.execute("SELECT * FROM usage_tickets WHERE owner=? AND feature=? AND operation_key=?",(user.user_id,feature,operation_key)).fetchone()
            if previous:
                if previous["input_hash"] != fingerprint:
                    raise ActivityError("Mã yêu cầu đã được dùng với thông tin khác.")
                if previous["state"] == "committed":
                    return {"ticket":previous["id"],"replay":True,"output":json.loads(previous["output_json"]),"status_code":200}
                if previous["state"] == "held":
                    raise ActivityError("Yêu cầu này đang được xử lý. Vui lòng chờ rồi thử lại.")
            used, pending = self._usage(connection, user, feature)
            if user.analysis_limit is not None and used + pending >= user.analysis_limit:
                raise ActivityError(f"Bạn đã hết lượt {FEATURES[feature].lower()}. Vui lòng liên hệ ADMIN để được cấp thêm hạn mức.",429,"quota_exhausted")
            ticket = previous["id"] if previous else uuid4().hex
            if previous:
                connection.execute("UPDATE usage_tickets SET state='held',created_at=?,legacy=? WHERE id=?", (timestamp(),int(legacy),ticket))
            else:
                connection.execute("INSERT INTO usage_tickets VALUES(?,?,?,?,?,?,'held',?,?,NULL,NULL)", (ticket,user.user_id,feature,operation_key,fingerprint,encoded,int(legacy),timestamp()))
            return {"ticket":ticket,"replay":False}

    def cancel(self, user, ticket):
        with self.connect() as connection:
            connection.execute("UPDATE usage_tickets SET state='cancelled' WHERE id=? AND owner=? AND state='held'",(ticket,user.user_id))

    def finish(self, user, ticket, output, status_code=200):
        with self.connect() as connection:
            record = connection.execute("SELECT * FROM usage_tickets WHERE id=? AND owner=?",(ticket,user.user_id)).fetchone()
            if record is None or record["state"] == "cancelled":
                raise ActivityError("Không tìm thấy lượt xử lý hợp lệ.")
            if record["state"] == "committed":
                return {"saved":True,"id":result_identity(record["feature"],json.loads(record["output_json"]),ticket)}
            feature = record["feature"]
            identifier = result_identity(feature, output, ticket)
            baseline = connection.execute("SELECT ids FROM feature_baselines WHERE owner=? AND feature=?",(user.user_id,feature)).fetchone()
            existed = connection.execute("SELECT 1 FROM activity_results WHERE owner=? AND kind=? AND id=?",("user:"+user.user_id,feature,identifier)).fetchone()
            replay = existed or (baseline and identifier in json.loads(baseline[0]))
            inputs = json.loads(record["input_json"])
            snapshot = {"id":identifier,"kind":feature,"input":inputs,"result":output,"owner_user_id":user.user_id,
                        "creator_username":user.username,"creator_display_name":user.display_name,"created_at":record["created_at"]}
            connection.execute("INSERT OR IGNORE INTO activity_results VALUES(?,?,?,?,?,?,?,?,?)",("user:"+user.user_id,feature,identifier,record["created_at"],customer_label(inputs),user.username,user.display_name,user.phone,json.dumps(snapshot,ensure_ascii=False)))
            connection.execute("UPDATE usage_tickets SET state='committed',legacy=?,output_json=?,status_code=? WHERE id=?",(int(bool(record["legacy"] or replay)),json.dumps(output,ensure_ascii=False),status_code,ticket))
            return {"saved":True,"id":identifier}

    def records(self):
        with self.connect() as connection:
            rows = connection.execute("SELECT owner,kind,id,created_at,customer_name,creator_username,creator_display_name,phone,json_extract(snapshot,'$.status') AS status FROM activity_results ORDER BY created_at DESC").fetchall()
        return [dict(row) for row in rows]

    def get(self, kind, identifier, owner=""):
        with self.connect() as connection:
            row = connection.execute("SELECT snapshot FROM activity_results WHERE kind=? AND id=?"+(" AND owner=?" if owner else ""), (kind,identifier,owner) if owner else (kind,identifier)).fetchone()
        return json.loads(row[0]) if row else None

    def contact(self, body, actor=None):
        identifier = "CT-"+uuid4().hex
        owner = "user:"+actor.user_id if actor else "guest:"+identifier
        snapshot = {"id":identifier,"kind":"contact","created_at":timestamp(),"contact":body.model_dump(),"status":"open","admin_note":""}
        with self.connect() as connection:
            connection.execute("INSERT INTO activity_results VALUES(?,?,?,?,?,?,?,?,?)",(owner,"contact",identifier,snapshot["created_at"],body.full_name,actor.username if actor else "Khách liên hệ",actor.display_name if actor else body.full_name,body.phone,json.dumps(snapshot,ensure_ascii=False)))
        return {"id":identifier,"message":"Đã lưu yêu cầu hỗ trợ để quản trị viên tiếp nhận."}

    def update_contact(self, identifier, status, note):
        with self.connect() as connection:
            row = connection.execute("SELECT snapshot FROM activity_results WHERE kind='contact' AND id=?",(identifier,)).fetchone()
            if not row:
                raise ActivityError("Không tìm thấy liên hệ.",404)
            snapshot = json.loads(row[0]); snapshot.update(status=status,admin_note=note,updated_at=timestamp())
            connection.execute("UPDATE activity_results SET snapshot=? WHERE kind='contact' AND id=?",(json.dumps(snapshot,ensure_ascii=False),identifier))
        return snapshot

    def release_stale(self, user):
        cutoff = (datetime.now(timezone.utc)-timedelta(minutes=30)).isoformat()
        with self.connect() as connection:
            result = connection.execute("UPDATE usage_tickets SET state='cancelled' WHERE owner=? AND state='held' AND created_at<?",(user.user_id,cutoff))
        return result.rowcount

def get_activity_service():
    from applications.api.dependencies import get_auth_service
    return ActivityService(get_auth_service().store)
