import sqlite3

conn = sqlite3.connect("/data/ai_news.db")
conn.row_factory = sqlite3.Row
rows = conn.execute(
    "SELECT id, title_zh, summary FROM articles WHERE summary IS NOT NULL ORDER BY id DESC LIMIT 20"
).fetchall()

suspicious = []
for r in rows:
    s = r["summary"] or ""
    # 句末标点：中文句号/感叹号/问号
    ends_clean = s.rstrip().endswith(("。", "！", "？", ".", "!", "?", "）", ")", "」", "\""))
    flag = "OK " if ends_clean else "TRUNC"
    if not ends_clean:
        suspicious.append(r["id"])
    print(f"{flag} id={r['id']} len={len(s)} tail=...{s[-30:]}")

print()
print("suspicious_ids:", suspicious)
