import json
import os
import sqlite3

from openai import OpenAI

conn = sqlite3.connect("/data/ai_news.db")
conn.row_factory = sqlite3.Row
art = conn.execute(
    "SELECT id, source, title, coalesce(raw_summary, '') AS s FROM articles "
    "WHERE status = 0 AND attempts < 3 ORDER BY id LIMIT 1"
).fetchone()
if not art:
    print("NO PENDING ARTICLE")
    raise SystemExit

client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])
resp = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],
    messages=[
        {"role": "system", "content": "输出JSON"},
        {"role": "user", "content": json.dumps(
            {"title": art["title"], "summary": (art["s"] or "")[:1500],
             "source": art["source"]}, ensure_ascii=False)},
    ],
    temperature=0.2,
    max_tokens=600,
)
msg = resp.choices[0].message
print("ID", art["id"])
print("CONTENT", repr((msg.content or "")[:800]))
reasoning = getattr(msg, "reasoning_content", None)
if reasoning:
    print("REASONING", repr(reasoning[:500]))
