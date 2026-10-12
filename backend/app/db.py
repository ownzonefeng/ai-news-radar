import json
import os
import pymysql
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "ainews")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "ainews_pass")
MYSQL_DB = os.getenv("MYSQL_DB", "ai_news")

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_hash VARCHAR(64) NOT NULL UNIQUE,
    url VARCHAR(2048) NOT NULL,
    source VARCHAR(128) NOT NULL,
    source_type VARCHAR(32) NOT NULL,
    title VARCHAR(1024) NOT NULL,
    raw_summary TEXT,
    published_at DATETIME,
    collected_at DATETIME NOT NULL,
    title_zh VARCHAR(512),
    summary TEXT,
    topic VARCHAR(64),
    tags TEXT,
    is_ai TINYINT NOT NULL DEFAULT 1,
    stars INT,
    language VARCHAR(64),
    status TINYINT NOT NULL DEFAULT 0,
    attempts INT NOT NULL DEFAULT 0,
    INDEX idx_articles_status (status, attempts),
    INDEX idx_articles_topic (topic),
    INDEX idx_articles_time (published_at, collected_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""


class _Conn:
    """薄封装：把 execute/fetchall/fetchone 转发给 cursor，
    让原来的 sqlite3 风格调用点无需改动。"""

    def __init__(self, conn):
        self._conn = conn
        self._cur = conn.cursor()

    def execute(self, sql, params=None):
        self._cur.execute(sql, params or ())
        return self._cur

    def fetchall(self):
        return self._cur.fetchall()

    def fetchone(self):
        return self._cur.fetchone()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._cur.close()
        self._conn.close()


@contextmanager
def get_conn():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset="utf8mb4",
        init_command="SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
    wrapped = _Conn(conn)
    try:
        yield wrapped
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        wrapped.close()


def init_db():
    with get_conn() as conn:
        for stmt in [s.strip() for s in SCHEMA.split(";") if s.strip()]:
            conn.execute(stmt)
        cols = conn.execute(
            "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA=%s AND TABLE_NAME='articles' AND COLUMN_NAME='is_ai'",
            (MYSQL_DB,),
        ).fetchall()
        if not cols:
            conn.execute(
                "ALTER TABLE articles ADD COLUMN is_ai TINYINT NOT NULL DEFAULT 1"
            )


def _now_utc():
    return datetime.now(timezone.utc)


def insert_article(item: dict, url_hash: str) -> bool:
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT IGNORE INTO articles
               (url_hash, url, source, source_type, title, raw_summary,
                published_at, collected_at, stars, language)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                url_hash,
                item["url"],
                item["source"],
                item.get("source_type", "rss"),
                item["title"],
                item.get("raw_summary"),
                item.get("published_at"),
                _now_utc().strftime("%Y-%m-%d %H:%M:%S"),
                item.get("stars"),
                item.get("language"),
            ),
        )
        return cur.rowcount > 0


def recent_titles(days: int = 3, limit: int = 1000):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT title FROM articles WHERE collected_at >= %s ORDER BY id DESC LIMIT %s",
            (cutoff, limit),
        ).fetchall()
    return [r["title"] for r in rows]


def pending_articles(limit: int, max_attempts: int):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM articles WHERE status = 0 AND attempts < %s ORDER BY id LIMIT %s",
            (max_attempts, limit),
        ).fetchall()


def update_result(article_id: int, title_zh, summary, topic, tags, is_ai=1):
    if not summary or not summary.strip():
        raise ValueError("summary is empty, refuse to mark as done")
    with get_conn() as conn:
        conn.execute(
            """UPDATE articles
               SET title_zh = %s, summary = %s, topic = %s, tags = %s, is_ai = %s, status = 1
               WHERE id = %s""",
            (title_zh, summary, topic, json.dumps(tags, ensure_ascii=False), is_ai, article_id),
        )


def mark_failed(article_id: int, max_attempts: int):
    with get_conn() as conn:
        row = conn.execute("SELECT attempts FROM articles WHERE id = %s", (article_id,)).fetchone()
        if row is None:
            return
        attempts = row["attempts"] + 1
        status = 2 if attempts >= max_attempts else 0
        conn.execute(
            "UPDATE articles SET attempts = %s, status = %s WHERE id = %s",
            (attempts, status, article_id),
        )


def query_news(topic=None, days=None, source=None, page=1, page_size=60):
    where = ["is_ai = 1"]
    params = []
    if topic:
        where.append("topic = %s")
        params.append(topic)
    if source:
        where.append("source = %s")
        params.append(source)
    if days:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        where.append("COALESCE(published_at, collected_at) >= %s")
        params.append(cutoff)
    cond = " AND ".join(where)
    with get_conn() as conn:
        total = conn.execute(
            f"SELECT COUNT(*) AS c FROM articles WHERE {cond}", params
        ).fetchone()["c"]
        rows = conn.execute(
            f"""SELECT * FROM articles WHERE {cond}
                ORDER BY COALESCE(published_at, collected_at) DESC, id DESC
                LIMIT %s OFFSET %s""",
            [*params, page_size, (page - 1) * page_size],
        ).fetchall()
    items = []
    for r in rows:
        item = dict(r)
        item.pop("url_hash", None)
        try:
            item["tags"] = json.loads(item.get("tags") or "[]")
        except json.JSONDecodeError:
            item["tags"] = []
        items.append(item)
    return items, total


def topic_counts(days=None):
    where = ["is_ai = 1"]
    params = []
    if days:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        where.append("COALESCE(published_at, collected_at) >= %s")
        params.append(cutoff)
    cond = " AND ".join(where)
    with get_conn() as conn:
        total = conn.execute(
            f"SELECT COUNT(*) AS c FROM articles WHERE {cond}", params
        ).fetchone()["c"]
        rows = conn.execute(
            f"""SELECT topic, COUNT(*) AS c FROM articles
                WHERE {cond} AND topic IS NOT NULL
                GROUP BY topic""",
            params,
        ).fetchall()
    return {"total": total, "topics": {r["topic"]: r["c"] for r in rows}}


def meta():
    with get_conn() as conn:
        row = conn.execute(
            "SELECT MAX(collected_at) AS last_collect FROM articles"
        ).fetchone()
    return {"last_updated": row["last_collect"] if row else None}


VISITOR_SCHEMA = """
CREATE TABLE IF NOT EXISTS visitors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""


def init_visitors():
    with get_conn() as conn:
        for stmt in [s.strip() for s in VISITOR_SCHEMA.split(";") if s.strip()]:
            conn.execute(stmt)


def increment_visitors():
    init_visitors()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO visitors (created_at) VALUES (%s)",
            (_now_utc().strftime("%Y-%m-%d %H:%M:%S"),),
        )
        row = conn.execute("SELECT COUNT(id) AS c FROM visitors").fetchone()
    return row["c"]


def sources():
    with get_conn() as conn:
        rows = conn.execute("SELECT DISTINCT source FROM articles ORDER BY source").fetchall()
    return [r["source"] for r in rows]

