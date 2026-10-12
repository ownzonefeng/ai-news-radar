import sqlite3

conn = sqlite3.connect("/data/ai_news.db")
conn.row_factory = sqlite3.Row
total = conn.execute("SELECT COUNT(*) AS c FROM articles").fetchone()["c"]
done = conn.execute(
    "SELECT COUNT(*) AS c FROM articles WHERE summary IS NOT NULL"
).fetchone()["c"]
print(f"total={total} summarized={done}")

row = conn.execute(
    "SELECT title, title_zh, summary, topic, tags FROM articles "
    "WHERE summary IS NOT NULL ORDER BY id DESC LIMIT 1"
).fetchone()
if row:
    print("title_zh:", row["title_zh"])
    print("topic:", row["topic"])
    print("tags:", row["tags"])
    print("summary_len:", len(row["summary"] or ""))
    print("summary:", (row["summary"] or "")[:500])
