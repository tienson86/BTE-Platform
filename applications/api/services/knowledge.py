"""Ordered member library. Draft content is accessible only through Admin APIs."""
from contextlib import contextmanager
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
from threading import RLock
import unicodedata
from uuid import uuid4
from applications.api.auth.roles import Role
from applications.api.services.activity_service import ActivityError, ActivityService

_SCHEMA_LOCK = RLock()
INITIAL_CATEGORIES = (
    ("co-ban", "Phong thủy cơ bản", "Kiến thức nhập môn và các khái niệm nền tảng về phong thủy."),
    ("bat-tu-co-ban", "Luận Bát tự cơ bản", "Tìm hiểu kiến thức nền và cách tiếp cận việc luận Bát tự."),
    ("tho-cung", "Các Nghi thức thờ cúng", "Tìm hiểu từng chủ đề về nghi thức và thực hành thờ cúng."),
    ("ngay-gio", "Phương pháp tính ngày giờ", "Tìm hiểu từ kiến thức nền đến phương pháp tính và ví dụ thực hành."),
    ("nang-luong-so", "Phương pháp luận dãy số", "Tìm hiểu phương pháp đọc, cách luận dãy số và các bài thực hành."),
    ("nha-o", "Phong thủy nhà ở", "Kiến thức về bố trí không gian sống và các tình huống áp dụng."),
    ("phan-mo", "Phong thủy phần mộ", "Các chủ đề về phong thủy phần mộ được tổ chức thành từng nhóm bài."),
    ("vat-pham", "Các vật phẩm phong thủy", "Tìm hiểu các nhóm vật phẩm phong thủy và từng chủ đề liên quan."),
    ("nghi-le", "Các Nghi lễ phong thủy", "Tìm hiểu các nghi lễ phong thủy theo từng nhóm kiến thức."),
)
INITIAL_GROUPS = ("Kiến thức nhập môn", "Phương pháp và ứng dụng", "Ví dụ thực hành", "Câu hỏi thường gặp")


def now():
    return datetime.now(timezone.utc).isoformat()


def fold(text):
    text = unicodedata.normalize("NFD", text.casefold().replace("đ", "d"))
    return " ".join("".join(char for char in text if not unicodedata.combining(char)).split())


def fail(message="Không tìm thấy nội dung.", status=404, code="knowledge_error"):
    raise ActivityError(message, status, code)


def require_member(user):
    if not user.has_member_access():
        fail("Kiến thức phong thủy dành cho thành viên còn quyền sử dụng.", 403, "membership_required")


def require_admin(user):
    if user.role != Role.ADMIN:
        fail("Chỉ Admin được quản lý thư viện kiến thức.", 403)


def check_revision(row, expected):
    if row["revision"] != expected:
        fail("Nội dung đã thay đổi. Vui lòng tải lại trước khi lưu.", 409, "revision_conflict")


class KnowledgeService:
    def __init__(self, store, path=None):
        self.path = Path(path or os.getenv("BTE_KNOWLEDGE_DB_PATH") or ActivityService(store).path.with_name("knowledge_library.sqlite3"))

    @contextmanager
    def connect(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            with _SCHEMA_LOCK:
                if connection.execute("PRAGMA journal_mode").fetchone()[0] != "wal":
                    connection.execute("PRAGMA journal_mode=WAL")
                connection.execute("PRAGMA synchronous=FULL")
                connection.executescript("""
                    CREATE TABLE IF NOT EXISTS library_meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
                    CREATE TABLE IF NOT EXISTS library_categories(
                        id TEXT PRIMARY KEY,title TEXT NOT NULL,description TEXT NOT NULL,position INTEGER NOT NULL,
                        revision INTEGER NOT NULL DEFAULT 1,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
                    CREATE TABLE IF NOT EXISTS library_groups(
                        id TEXT PRIMARY KEY,category_id TEXT NOT NULL REFERENCES library_categories(id),
                        title TEXT NOT NULL,description TEXT NOT NULL,position INTEGER NOT NULL,
                        revision INTEGER NOT NULL DEFAULT 1,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
                    CREATE INDEX IF NOT EXISTS library_groups_category ON library_groups(category_id,position);
                    CREATE TABLE IF NOT EXISTS library_articles(
                        id TEXT PRIMARY KEY,group_id TEXT NOT NULL REFERENCES library_groups(id),
                        title TEXT NOT NULL,summary TEXT NOT NULL,body TEXT NOT NULL,search_text TEXT NOT NULL,
                        status TEXT NOT NULL CHECK(status IN ('draft','published')),position INTEGER NOT NULL,
                        revision INTEGER NOT NULL DEFAULT 1,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,
                        published_at TEXT,author_id TEXT NOT NULL,author_name TEXT NOT NULL,client_key TEXT NOT NULL,
                        UNIQUE(author_id,client_key));
                    CREATE INDEX IF NOT EXISTS library_articles_group ON library_articles(group_id,status,position);
                    CREATE INDEX IF NOT EXISTS library_articles_recent ON library_articles(status,updated_at);
                """)
            connection.execute("BEGIN IMMEDIATE")
            if not connection.execute("SELECT 1 FROM library_meta WHERE key='initialized'").fetchone():
                date = now()
                for index, (identifier, title, description) in enumerate(INITIAL_CATEGORIES, 1):
                    self._insert_category(connection,identifier,title,description,index*10,date)
                connection.execute("INSERT INTO library_meta VALUES('initialized','1')")
            # Apply this requested reorganization once. Later Admin edits remain authoritative.
            if not connection.execute("SELECT 1 FROM library_meta WHERE key='categories_v2'").fetchone():
                date = now()
                for index, (identifier, title, description) in enumerate(INITIAL_CATEGORIES, 1):
                    existing = connection.execute("SELECT * FROM library_categories WHERE id=?",(identifier,)).fetchone()
                    if existing is None:
                        self._insert_category(connection,identifier,title,description,index*10,date)
                    elif existing["title"] != title or existing["position"] != index*10:
                        connection.execute("UPDATE library_categories SET title=?,position=?,revision=revision+1,updated_at=? WHERE id=?",(title,index*10,date,identifier))
                connection.execute("INSERT INTO library_meta VALUES('categories_v2','1')")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _insert_category(self, connection, identifier, title, description, position, date):
        connection.execute("INSERT INTO library_categories VALUES(?,?,?,?,1,?,?)",(identifier,title,description,position,date,date))
        for index, group_title in enumerate(INITIAL_GROUPS,1):
            connection.execute("INSERT INTO library_groups VALUES(?,?,?,?,?,1,?,?)",(identifier+"-"+str(index),identifier,group_title,"",index*10,date,date))

    def _row(self, connection, table, identifier):
        # Table names are internal constants; all external values are bound parameters.
        row = connection.execute(f"SELECT * FROM {table} WHERE id=?", (identifier,)).fetchone()
        if row is None:
            fail()
        return row

    def _article_query(self):
        return """SELECT a.*,g.category_id,g.title AS group_title,c.title AS category_title
            FROM library_articles a JOIN library_groups g ON g.id=a.group_id
            JOIN library_categories c ON c.id=g.category_id"""

    def _article_view(self, row, detail=False, management=False):
        keys = ["id","group_id","category_id","group_title","category_title","title","summary","position","updated_at","published_at","author_name"]
        if detail:
            keys.append("body")
        if management:
            keys += ["status","revision","created_at"]
        return {key: row[key] for key in keys}

    def _catalog(self, connection, management=False):
        visibility = "" if management else " AND a.status='published'"
        categories = [dict(row) for row in connection.execute("""SELECT c.*,
            (SELECT COUNT(*) FROM library_articles a JOIN library_groups g ON g.id=a.group_id
             WHERE g.category_id=c.id"""+visibility+""") AS article_count
            FROM library_categories c ORDER BY c.position,c.created_at,c.id""")]
        groups = [dict(row) for row in connection.execute("""SELECT g.*,
            (SELECT COUNT(*) FROM library_articles a WHERE a.group_id=g.id"""+visibility+""") AS article_count
            FROM library_groups g ORDER BY g.position,g.created_at,g.id""")]
        for category in categories:
            category["groups"] = [group for group in groups if group["category_id"] == category["id"]]
        return categories

    def catalog(self, user, management=False):
        require_admin(user) if management else require_member(user)
        with self.connect() as connection:
            result = {"categories":self._catalog(connection,management)}
            if not management:
                rows = connection.execute(self._article_query()+" WHERE a.status='published' ORDER BY a.updated_at DESC,a.id DESC LIMIT 6").fetchall()
                result["latest"] = [self._article_view(row) for row in rows]
            return result

    def category(self, user, identifier):
        require_member(user)
        with self.connect() as connection:
            category = next((row for row in self._catalog(connection) if row["id"]==identifier),None)
            if category is None:
                fail()
            rows = connection.execute(self._article_query()+" WHERE g.category_id=? AND a.status='published' ORDER BY g.position,g.created_at,g.id,a.position,a.created_at,a.id", (identifier,)).fetchall()
            for group in category["groups"]:
                group["articles"] = [self._article_view(row) for row in rows if row["group_id"]==group["id"]]
            return {"category":category}

    def article(self, user, identifier, management=False):
        require_admin(user) if management else require_member(user)
        with self.connect() as connection:
            row = connection.execute(self._article_query()+" WHERE a.id=?"+("" if management else " AND a.status='published'"),(identifier,)).fetchone()
            if row is None:
                fail()
            result = {"article":self._article_view(row,True,management)}
            if not management:
                ordered = connection.execute(self._article_query()+" WHERE g.category_id=? AND a.status='published' ORDER BY g.position,g.created_at,g.id,a.position,a.created_at,a.id",(row["category_id"],)).fetchall()
                index = next(i for i,item in enumerate(ordered) if item["id"]==identifier)
                result["previous"] = self._article_view(ordered[index-1]) if index else None
                result["next"] = self._article_view(ordered[index+1]) if index+1<len(ordered) else None
            return result

    def search(self, user, query, page=1, limit=20, management=False, category_id=None, group_id=None, status=None):
        require_admin(user) if management else require_member(user)
        conditions,args = [],[]
        if not management:
            conditions.append("a.status='published'")
        elif status:
            conditions.append("a.status=?");args.append(status)
        if category_id:
            conditions.append("g.category_id=?");args.append(category_id)
        if group_id:
            conditions.append("a.group_id=?");args.append(group_id)
        if query.strip():
            term = fold(query).replace("\\","\\\\").replace("%","\\%").replace("_","\\_")
            conditions.append("a.search_text LIKE ? ESCAPE '\\'");args.append("%"+term+"%")
        where = " WHERE "+" AND ".join(conditions) if conditions else ""
        with self.connect() as connection:
            base = self._article_query()+where
            total = connection.execute("SELECT COUNT(*) FROM ("+base+")",args).fetchone()[0]
            rows = connection.execute(base+" ORDER BY a.updated_at DESC,a.id DESC LIMIT ? OFFSET ?",args+[limit,(page-1)*limit]).fetchall()
            return {"items":[self._article_view(row,management=management) for row in rows],"total":total,"page":page,"limit":limit}

    def save_category(self, user, body, identifier=None):
        require_admin(user)
        with self.connect() as connection:
            date = now()
            if identifier:
                check_revision(self._row(connection,"library_categories",identifier),body.expected_revision)
                connection.execute("UPDATE library_categories SET title=?,description=?,position=?,revision=revision+1,updated_at=? WHERE id=?",(body.title,body.description,body.position,date,identifier))
            else:
                identifier = uuid4().hex
                connection.execute("INSERT INTO library_categories VALUES(?,?,?,?,1,?,?)",(identifier,body.title,body.description,body.position,date,date))
            return dict(self._row(connection,"library_categories",identifier))

    def save_group(self, user, body, identifier=None):
        require_admin(user)
        with self.connect() as connection:
            self._row(connection,"library_categories",body.category_id)
            date = now()
            if identifier:
                check_revision(self._row(connection,"library_groups",identifier),body.expected_revision)
                connection.execute("UPDATE library_groups SET category_id=?,title=?,description=?,position=?,revision=revision+1,updated_at=? WHERE id=?",(body.category_id,body.title,body.description,body.position,date,identifier))
            else:
                identifier = uuid4().hex
                connection.execute("INSERT INTO library_groups VALUES(?,?,?,?,?,1,?,?)",(identifier,body.category_id,body.title,body.description,body.position,date,date))
            return dict(self._row(connection,"library_groups",identifier))

    def save_article(self, user, body, identifier=None):
        require_admin(user)
        with self.connect() as connection:
            self._row(connection,"library_groups",body.group_id)
            date = now()
            if identifier:
                row = self._row(connection,"library_articles",identifier)
                check_revision(row,body.expected_revision)
                published_at = (row["published_at"] or date) if body.status=="published" else None
                connection.execute("""UPDATE library_articles SET group_id=?,title=?,summary=?,body=?,search_text=?,status=?,position=?,
                    revision=revision+1,updated_at=?,published_at=? WHERE id=?""",
                    (body.group_id,body.title,body.summary,body.body,fold(body.title+" "+body.summary+" "+body.body),body.status,body.position,date,published_at,identifier))
            else:
                previous = connection.execute("SELECT * FROM library_articles WHERE author_id=? AND client_key=?",(user.user_id,body.client_key)).fetchone()
                if previous:
                    if any(previous[key]!=getattr(body,key) for key in ("group_id","title","summary","body","status","position")):
                        fail("Mã lưu bài đã được dùng cho nội dung khác.",409)
                    identifier = previous["id"]
                else:
                    identifier = uuid4().hex
                    connection.execute("""INSERT INTO library_articles(id,group_id,title,summary,body,search_text,status,position,
                        created_at,updated_at,published_at,author_id,author_name,client_key) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                        (identifier,body.group_id,body.title,body.summary,body.body,fold(body.title+" "+body.summary+" "+body.body),body.status,body.position,date,date,date if body.status=="published" else None,user.user_id,user.display_name or user.username,body.client_key))
            row = connection.execute(self._article_query()+" WHERE a.id=?",(identifier,)).fetchone()
            return self._article_view(row,True,True)


def get_knowledge_service():
    from applications.api.dependencies import get_auth_service
    return KnowledgeService(get_auth_service().store)
