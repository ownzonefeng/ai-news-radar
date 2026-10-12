import sqlite3

conn = sqlite3.connect("/data/ai_news.db")
cur = conn.execute(
    """UPDATE articles
       SET summary = NULL, title_zh = NULL, topic = NULL, tags = NULL,
           status = 0, attempts = 0
       WHERE summary IS NOT NULL AND length(summary) = 300"""
)
conn.commit()
print(f"reset {cur.rowcount} truncated articles for reprocessing")
