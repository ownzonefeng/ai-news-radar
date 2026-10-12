import json
import sqlite3
import urllib.error
import urllib.request

conn = sqlite3.connect("file:/opt/one-api/one-api.db?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
channel = conn.execute("SELECT base_url, key FROM channels WHERE id=1").fetchone()
base_url = channel["base_url"].rstrip("/")
headers = {"Authorization": f"Bearer {channel['key']}", "Content-Type": "application/json"}
models = [
    "deepseek-v4.1-flash",
    "deepseek-v4-flash",
    "deepseek-v3.2",
    "glm-5.3-flash",
    "qwen3.8-flash",
    "claude-sonnet-4.6",
]

for model in models:
    payload = {"model": model, "messages": [{"role": "user", "content": "只回复OK"}]}
    req = urllib.request.Request(
        base_url + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status, body = resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        status, body = exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:
        status, body = None, repr(exc)
    print(model, status, body[:300])
