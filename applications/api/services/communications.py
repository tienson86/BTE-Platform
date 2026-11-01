"""Private member/Admin conversations and a separately moderated member forum."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
from threading import RLock
from uuid import uuid4

from applications.api.auth.roles import Role
from applications.api.services.activity_service import ActivityError, ActivityService

_SCHEMA_LOCK = RLock()

def now():
    return datetime.now(timezone.utc).isoformat()

def admin(user):
    return user.role == Role.ADMIN

def deny(message="Không tìm thấy nội dung trong quyền truy cập của bạn.", status=404, code="communication_error"):
    raise ActivityError(message, status, code)

def require_forum(user):
    if not user.has_member_access():
        deny("Trao đổi kiến thức dành cho thành viên còn quyền sử dụng. Vui lòng xem trạng thái thành viên.",403,"forum_membership_required")

def require_revision(row, revision):
    if row["revision"] != revision:
        deny("Nội dung đã thay đổi. Vui lòng tải lại trước khi thao tác.",409,"revision_conflict")

class CommunicationsService:
    def __init__(self, store, path=None):
        self.store = store
        self.activity = ActivityService(store)
        self.path = Path(path or os.getenv("BTE_COMMUNICATIONS_DB_PATH") or self.activity.path.with_name("communications.sqlite3"))

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
                    CREATE TABLE IF NOT EXISTS support_threads(
                        id TEXT PRIMARY KEY,owner_id TEXT NOT NULL,subject TEXT NOT NULL,
                        created_by TEXT NOT NULL,client_key TEXT NOT NULL,created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,contact_id TEXT UNIQUE,
                        UNIQUE(created_by,client_key));
                    CREATE TABLE IF NOT EXISTS support_messages(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,thread_id TEXT NOT NULL,
                        sender_id TEXT NOT NULL,sender_name TEXT NOT NULL,sender_username TEXT NOT NULL,
                        sender_is_admin INTEGER NOT NULL,body TEXT NOT NULL,client_key TEXT NOT NULL,
                        created_at TEXT NOT NULL,UNIQUE(thread_id,sender_id,client_key));
                    CREATE INDEX IF NOT EXISTS support_messages_thread ON support_messages(thread_id,id);
                    CREATE INDEX IF NOT EXISTS support_threads_owner ON support_threads(owner_id,updated_at);
                    CREATE TABLE IF NOT EXISTS support_reads(
                        thread_id TEXT,user_id TEXT,last_id INTEGER NOT NULL DEFAULT 0,
                        updated_at TEXT NOT NULL,PRIMARY KEY(thread_id,user_id));
                    CREATE TABLE IF NOT EXISTS knowledge_topics(
                        id TEXT PRIMARY KEY,author_id TEXT NOT NULL,author_name TEXT NOT NULL,
                        author_username TEXT NOT NULL,author_is_admin INTEGER NOT NULL,title TEXT NOT NULL,
                        body TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'pending',revision INTEGER NOT NULL DEFAULT 1,
                        client_key TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
                        approved_at TEXT,approved_by TEXT,moderation_note TEXT NOT NULL DEFAULT '',deleted_by TEXT,
                        UNIQUE(author_id,client_key));
                    CREATE INDEX IF NOT EXISTS knowledge_topics_status ON knowledge_topics(status,approved_at);
                    CREATE TABLE IF NOT EXISTS knowledge_comments(
                        id TEXT PRIMARY KEY,topic_id TEXT NOT NULL,author_id TEXT NOT NULL,
                        author_name TEXT NOT NULL,author_username TEXT NOT NULL,author_is_admin INTEGER NOT NULL,
                        body TEXT NOT NULL,revision INTEGER NOT NULL DEFAULT 1,client_key TEXT NOT NULL,
                        created_at TEXT NOT NULL,updated_at TEXT NOT NULL,deleted_at TEXT,deleted_by TEXT,
                        UNIQUE(topic_id,author_id,client_key));
                    CREATE INDEX IF NOT EXISTS knowledge_comments_topic ON knowledge_comments(topic_id,created_at,id);
                    CREATE TABLE IF NOT EXISTS community_audit(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,actor_id TEXT NOT NULL,action TEXT NOT NULL,
                        target_id TEXT NOT NULL,note TEXT NOT NULL DEFAULT '',created_at TEXT NOT NULL);
                """)
            connection.execute("BEGIN IMMEDIATE")
            if "category_id" not in {row["name"] for row in connection.execute("PRAGMA table_info(knowledge_topics)")}:
                connection.execute("ALTER TABLE knowledge_topics ADD COLUMN category_id TEXT")
            connection.execute("CREATE INDEX IF NOT EXISTS knowledge_topics_category ON knowledge_topics(category_id,status,created_at)")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def sync_contacts(self, viewer):
        # Only server-verified account ownership links a contact to an inbox.
        # Never infer ownership from phone/name or publish old internal admin_note.
        with self.activity.connect() as source:
            query="SELECT * FROM activity_results WHERE kind='contact' AND owner LIKE 'user:%'"
            rows=source.execute(query if admin(viewer) else query+" AND owner=?",
                                () if admin(viewer) else ("user:"+viewer.user_id,)).fetchall()
        if not rows:
            return
        with self.connect() as connection:
            for record in rows:
                owner_id=record["owner"].removeprefix("user:")
                owner=self.store.get_by_id(owner_id)
                if owner is None or admin(owner):
                    continue
                try:
                    contact=json.loads(record["snapshot"])["contact"]
                    body=str(contact["message"])
                except (ValueError,KeyError,TypeError):
                    continue
                existing=connection.execute("SELECT id FROM support_threads WHERE contact_id=?",(record["id"],)).fetchone()
                if existing:
                    continue
                identifier=uuid4().hex
                date=record["created_at"]
                connection.execute("INSERT INTO support_threads VALUES(?,?,?,?,?,?,?,?)",
                    (identifier,owner_id,str(contact.get("subject") or "Yêu cầu hỗ trợ")[:180],owner_id,"contact:"+record["id"],date,date,record["id"]))
                connection.execute("INSERT INTO support_messages(thread_id,sender_id,sender_name,sender_username,sender_is_admin,body,client_key,created_at) VALUES(?,?,?,?,?,?,?,?)",
                    (identifier,owner_id,record["creator_display_name"] or owner.display_name,record["creator_username"] or owner.username,0,body,"contact:"+record["id"],date))

    def _thread(self, connection, user, identifier):
        row=connection.execute("SELECT * FROM support_threads WHERE id=?",(identifier,)).fetchone()
        if row is None or (not admin(user) and row["owner_id"] != user.user_id):
            deny()
        return row

    def _thread_view(self, connection, row, user):
        owner=self.store.get_by_id(row["owner_id"])
        direction=0 if admin(user) else 1
        unread=connection.execute("""SELECT COUNT(*) FROM support_messages WHERE thread_id=?
            AND sender_is_admin=? AND id>COALESCE((SELECT last_id FROM support_reads WHERE thread_id=? AND user_id=?),0)""",
            (row["id"],direction,row["id"],user.user_id)).fetchone()[0]
        return {"id":row["id"],"subject":row["subject"],"created_at":row["created_at"],
                "updated_at":row["updated_at"],"contact_id":row["contact_id"],"unread":unread,
                "owner":{"id":row["owner_id"],"username":owner.username if owner else "Tài khoản cũ",
                         "display_name":(owner.display_name or owner.username) if owner else "Tài khoản cũ"}}

    def list_threads(self, user, page=1, limit=30):
        self.sync_contacts(user)
        with self.connect() as connection:
            where="" if admin(user) else " WHERE owner_id=?"
            args=() if admin(user) else (user.user_id,)
            total=connection.execute("SELECT COUNT(*) FROM support_threads"+where,args).fetchone()[0]
            rows=connection.execute("SELECT * FROM support_threads"+where+" ORDER BY updated_at DESC,id DESC LIMIT ? OFFSET ?",args+(limit,(page-1)*limit)).fetchall()
            return {"items":[self._thread_view(connection,row,user) for row in rows],"total":total,"page":page,"limit":limit}

    def recipients(self, user):
        if not admin(user):
            deny("Chỉ Admin được chọn tài khoản nhận tin.",403)
        return [{"id":other.user_id,"username":other.username,"display_name":other.display_name or other.username}
                for other in sorted(self.store.users_by_id.values(),key=lambda person:person.username.casefold())
                if not admin(other) and other.is_active]

    def create_thread(self, user, body):
        if admin(user):
            owner=self.store.get_by_id(body.recipient_user_id or "")
            if owner is None or admin(owner):
                deny("Vui lòng chọn tài khoản thành viên nhận tin.",422)
        else:
            if body.recipient_user_id is not None:
                deny("Thành viên chỉ gửi tin riêng cho Admin.",403)
            owner=user
        with self.connect() as connection:
            existing=connection.execute("SELECT * FROM support_threads WHERE created_by=? AND client_key=?",(user.user_id,body.client_key)).fetchone()
            if existing:
                first=connection.execute("SELECT body FROM support_messages WHERE thread_id=? ORDER BY id LIMIT 1",(existing["id"],)).fetchone()
                if existing["owner_id"] != owner.user_id or existing["subject"] != body.subject or not first or first[0] != body.message:
                    deny("Mã gửi tin đã được dùng cho nội dung khác.",409)
                return self._thread_view(connection,existing,user)
            identifier=uuid4().hex; date=now()
            connection.execute("INSERT INTO support_threads VALUES(?,?,?,?,?,?,?,NULL)",(identifier,owner.user_id,body.subject,user.user_id,body.client_key,date,date))
            self._insert_message(connection,identifier,user,body.message,body.client_key,date)
            return self._thread_view(connection,self._thread(connection,user,identifier),user)

    def _insert_message(self, connection, thread_id, user, message, client_key, date):
        existing=connection.execute("SELECT * FROM support_messages WHERE thread_id=? AND sender_id=? AND client_key=?",(thread_id,user.user_id,client_key)).fetchone()
        if existing:
            if existing["body"] != message:
                deny("Mã gửi tin đã được dùng cho nội dung khác.",409)
            return dict(existing)
        cursor=connection.execute("INSERT INTO support_messages(thread_id,sender_id,sender_name,sender_username,sender_is_admin,body,client_key,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (thread_id,user.user_id,user.display_name or user.username,user.username,int(admin(user)),message,client_key,date))
        connection.execute("UPDATE support_threads SET updated_at=? WHERE id=?",(date,thread_id))
        return dict(connection.execute("SELECT * FROM support_messages WHERE id=?",(cursor.lastrowid,)).fetchone())

    def send_message(self, user, identifier, body):
        with self.connect() as connection:
            self._thread(connection,user,identifier)
            return self._insert_message(connection,identifier,user,body.message,body.client_key,now())

    def thread_messages(self, user, identifier, before=None, limit=50):
        with self.connect() as connection:
            thread=self._thread(connection,user,identifier)
            query="SELECT * FROM support_messages WHERE thread_id=?"
            args=(identifier,)
            if before is not None:
                query+=" AND id<?";args+=(before,)
            rows=connection.execute(query+" ORDER BY id DESC LIMIT ?",args+(limit+1,)).fetchall()
            more=len(rows)>limit;rows=rows[:limit]
            return {"thread":self._thread_view(connection,thread,user),"messages":[dict(row) for row in reversed(rows)],
                    "has_more":more,"before":rows[-1]["id"] if rows else None}

    def mark_read(self, user, identifier, last_id):
        with self.connect() as connection:
            self._thread(connection,user,identifier)
            maximum=connection.execute("SELECT COALESCE(MAX(id),0) FROM support_messages WHERE thread_id=?",(identifier,)).fetchone()[0]
            value=min(maximum,last_id)
            connection.execute("INSERT INTO support_reads VALUES(?,?,?,?) ON CONFLICT(thread_id,user_id) DO UPDATE SET last_id=MAX(support_reads.last_id,excluded.last_id),updated_at=excluded.updated_at",
                (identifier,user.user_id,value,now()))
        return {"read":True}

    def contact_thread(self, user, identifier):
        if not admin(user):
            deny("Chỉ Admin được mở trao đổi từ hồ sơ liên hệ.",403)
        self.sync_contacts(user)
        with self.connect() as connection:
            row=connection.execute("SELECT * FROM support_threads WHERE contact_id=?",(identifier,)).fetchone()
            if not row:
                deny("Liên hệ này chưa gắn với tài khoản thành viên đã xác thực.",404)
            return self._thread_view(connection,row,user)

    def summary(self, user):
        self.sync_contacts(user)
        with self.connect() as connection:
            query="""SELECT COUNT(*) FROM support_messages m JOIN support_threads t ON t.id=m.thread_id
                LEFT JOIN support_reads r ON r.thread_id=t.id AND r.user_id=?
                WHERE m.id>COALESCE(r.last_id,0) AND m.sender_is_admin=?"""
            args=(user.user_id,0 if admin(user) else 1)
            if not admin(user):
                query+=" AND t.owner_id=?";args+=(user.user_id,)
            unread=connection.execute(query,args).fetchone()[0]
            pending=connection.execute("SELECT COUNT(*) FROM knowledge_topics WHERE status='pending'"+("" if admin(user) else " AND author_id=?"),() if admin(user) else (user.user_id,)).fetchone()[0]
        return {"unread_messages":unread,"can_community":user.has_member_access(),"pending_topics":pending}

    def _audit(self, connection, user, action, target, note=""):
        connection.execute("INSERT INTO community_audit(actor_id,action,target_id,note,created_at) VALUES(?,?,?,?,?)",(user.user_id,action,target,note,now()))

    def _topic(self, connection, user, identifier):
        row=connection.execute("SELECT * FROM knowledge_topics WHERE id=?",(identifier,)).fetchone()
        if not row or (row["status"] != "approved" and not admin(user) and row["author_id"] != user.user_id):
            deny()
        return row

    def category_labels(self, user):
        require_forum(user)
        from applications.api.services.knowledge import KnowledgeService
        with KnowledgeService(self.store).connect() as library:
            return {row["id"]:row["title"] for row in library.execute("SELECT id,title FROM library_categories ORDER BY position,created_at,id")}

    def _topic_view(self, connection, row, user, detail=False, category_labels=None):
        deleted=row["status"] == "deleted"
        result={key:row[key] for key in ("id","author_id","author_name","author_username","author_is_admin","status","revision","created_at","updated_at","approved_at")}
        result.update(title="Chủ đề đã được gỡ" if deleted else row["title"],
                      can_edit=not deleted and row["author_id"]==user.user_id,
                      can_moderate=not deleted and admin(user),can_delete=not deleted and admin(user))
        result["category_id"]=row["category_id"]
        result["category_title"]=(category_labels if category_labels is not None else self.category_labels(user)).get(row["category_id"],"Chuyên mục cũ") if row["category_id"] else ""
        result["comment_count"]=connection.execute("SELECT COUNT(*) FROM knowledge_comments WHERE topic_id=? AND deleted_at IS NULL",(row["id"],)).fetchone()[0]
        if detail:
            result["body"]="" if deleted else row["body"]
        if admin(user) or row["author_id"]==user.user_id:
            result["moderation_note"]=row["moderation_note"]
        return result

    def list_topics(self, user, scope="feed", page=1, limit=30, category_id=None):
        require_forum(user)
        if scope in ("pending","all") and not admin(user):
            deny("Chỉ Admin được xem hàng đợi duyệt.",403)
        where,args=("status='approved'",())
        if scope=="mine":where,args="author_id=?",(user.user_id,)
        elif scope=="pending":where="status='pending'"
        elif scope=="all":where="1=1"
        labels=self.category_labels(user) if category_id is not None else None
        if category_id is not None:
            if category_id not in labels:deny("Không tìm thấy chuyên mục kiến thức.")
            where="("+where+") AND category_id=?";args+=(category_id,)
        with self.connect() as connection:
            total=connection.execute("SELECT COUNT(*) FROM knowledge_topics WHERE "+where,args).fetchone()[0]
            rows=connection.execute("SELECT * FROM knowledge_topics WHERE "+where+" ORDER BY COALESCE(approved_at,created_at) DESC,id DESC LIMIT ? OFFSET ?",args+(limit,(page-1)*limit)).fetchall()
            if labels is None and any(row["category_id"] for row in rows):labels=self.category_labels(user)
            return {"items":[self._topic_view(connection,row,user,category_labels=labels) for row in rows],"total":total,"page":page,"limit":limit}

    def create_topic(self, user, body):
        require_forum(user)
        category_id=body.category_id
        labels=self.category_labels(user) if category_id is not None else {}
        if category_id is not None and category_id not in labels:deny("Không tìm thấy chuyên mục kiến thức.")
        with self.connect() as connection:
            previous=connection.execute("SELECT * FROM knowledge_topics WHERE author_id=? AND client_key=?",(user.user_id,body.client_key)).fetchone()
            if previous:
                if previous["title"]!=body.title or previous["body"]!=body.body or previous["category_id"]!=category_id:
                    deny("Mã gửi chủ đề đã được dùng cho nội dung khác.",409)
                return self._topic_view(connection,previous,user,True)
            identifier=uuid4().hex;date=now()
            connection.execute("INSERT INTO knowledge_topics(id,author_id,author_name,author_username,author_is_admin,title,body,client_key,created_at,updated_at,category_id) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (identifier,user.user_id,user.display_name or user.username,user.username,int(admin(user)),body.title,body.body,body.client_key,date,date,category_id))
            self._audit(connection,user,"topic_created",identifier)
            return self._topic_view(connection,self._topic(connection,user,identifier),user,True)

    def topic_detail(self, user, identifier):
        require_forum(user)
        with self.connect() as connection:
            return self._topic_view(connection,self._topic(connection,user,identifier),user,True)

    def edit_topic(self, user, identifier, body):
        require_forum(user)
        with self.connect() as connection:
            row=self._topic(connection,user,identifier)
            if row["author_id"]!=user.user_id:
                deny("Bạn chỉ được sửa chủ đề của mình.",403)
            if row["status"]=="deleted":deny()
            require_revision(row,body.expected_revision)
            connection.execute("UPDATE knowledge_topics SET title=?,body=?,status='pending',revision=revision+1,updated_at=?,approved_at=NULL,approved_by=NULL,moderation_note='' WHERE id=?",(body.title,body.body,now(),identifier))
            self._audit(connection,user,"topic_edited_pending",identifier)
            return self._topic_view(connection,self._topic(connection,user,identifier),user,True)

    def moderate(self, user, identifier, body):
        if not admin(user):deny("Chỉ Admin được duyệt chủ đề.",403)
        with self.connect() as connection:
            row=self._topic(connection,user,identifier)
            if row["status"]=="deleted":deny()
            require_revision(row,body.expected_revision)
            status="approved" if body.decision=="approve" else "rejected"
            date=now()
            connection.execute("UPDATE knowledge_topics SET status=?,revision=revision+1,updated_at=?,approved_at=?,approved_by=?,moderation_note=? WHERE id=?",
                (status,date,date if status=="approved" else None,user.user_id,body.note,identifier))
            self._audit(connection,user,"topic_"+status,identifier,body.note)
            return self._topic_view(connection,self._topic(connection,user,identifier),user,True)

    def delete_topic(self, user, identifier, revision):
        if not admin(user):deny("Chỉ Admin được gỡ chủ đề.",403)
        with self.connect() as connection:
            row=self._topic(connection,user,identifier)
            require_revision(row,revision)
            connection.execute("UPDATE knowledge_topics SET status='deleted',deleted_by=?,revision=revision+1,updated_at=? WHERE id=?",(user.user_id,now(),identifier))
            self._audit(connection,user,"topic_deleted",identifier)
        return {"deleted":True}

    def _comment_view(self, row, user):
        deleted=row["deleted_at"] is not None
        return {"id":row["id"],"topic_id":row["topic_id"],"author_id":row["author_id"] if not deleted else None,
                "author_name":row["author_name"] if not deleted else "", "author_username":row["author_username"] if not deleted else "",
                "author_is_admin":bool(row["author_is_admin"]) if not deleted else False,"body":"" if deleted else row["body"],
                "revision":row["revision"],"created_at":row["created_at"],"updated_at":row["updated_at"],"deleted":deleted,
                "can_edit":not deleted and row["author_id"]==user.user_id,
                "can_delete":not deleted and (admin(user) or row["author_id"]==user.user_id)}

    def comments(self, user, identifier, page=1, limit=50):
        require_forum(user)
        with self.connect() as connection:
            topic=self._topic(connection,user,identifier)
            if topic["status"]=="deleted":return {"items":[],"total":0,"page":page,"limit":limit}
            total=connection.execute("SELECT COUNT(*) FROM knowledge_comments WHERE topic_id=?",(identifier,)).fetchone()[0]
            rows=connection.execute("SELECT * FROM knowledge_comments WHERE topic_id=? ORDER BY created_at,id LIMIT ? OFFSET ?",(identifier,limit,(page-1)*limit)).fetchall()
            return {"items":[self._comment_view(row,user) for row in rows],"total":total,"page":page,"limit":limit}

    def create_comment(self, user, identifier, body):
        require_forum(user)
        with self.connect() as connection:
            topic=self._topic(connection,user,identifier)
            if topic["status"]!="approved":deny("Chủ đề cần được Admin duyệt trước khi trao đổi.",409)
            previous=connection.execute("SELECT * FROM knowledge_comments WHERE topic_id=? AND author_id=? AND client_key=?",(identifier,user.user_id,body.client_key)).fetchone()
            if previous:
                if previous["body"]!=body.body:deny("Mã bình luận đã được dùng cho nội dung khác.",409)
                return self._comment_view(previous,user)
            comment_id=uuid4().hex;date=now()
            connection.execute("INSERT INTO knowledge_comments(id,topic_id,author_id,author_name,author_username,author_is_admin,body,client_key,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (comment_id,identifier,user.user_id,user.display_name or user.username,user.username,int(admin(user)),body.body,body.client_key,date,date))
            self._audit(connection,user,"comment_created",comment_id)
            return self._comment_view(connection.execute("SELECT * FROM knowledge_comments WHERE id=?",(comment_id,)).fetchone(),user)

    def change_comment(self, user, identifier, revision, body=None):
        require_forum(user)
        with self.connect() as connection:
            row=connection.execute("SELECT * FROM knowledge_comments WHERE id=?",(identifier,)).fetchone()
            if not row or row["deleted_at"]:deny()
            self._topic(connection,user,row["topic_id"])
            if row["author_id"]!=user.user_id and (body is not None or not admin(user)):
                deny("Bạn chỉ được sửa, xóa bình luận của mình.",403)
            require_revision(row,revision)
            if body is None:
                connection.execute("UPDATE knowledge_comments SET deleted_at=?,deleted_by=?,updated_at=?,revision=revision+1 WHERE id=?",(now(),user.user_id,now(),identifier))
                self._audit(connection,user,"comment_deleted",identifier)
            else:
                connection.execute("UPDATE knowledge_comments SET body=?,updated_at=?,revision=revision+1 WHERE id=?",(body,now(),identifier))
                self._audit(connection,user,"comment_edited",identifier)
            return self._comment_view(connection.execute("SELECT * FROM knowledge_comments WHERE id=?",(identifier,)).fetchone(),user)

def get_communications_service():
    from applications.api.dependencies import get_auth_service
    return CommunicationsService(get_auth_service().store)
