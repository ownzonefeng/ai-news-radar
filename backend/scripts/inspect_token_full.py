import sqlite3

conn = sqlite3.connect("file:/opt/one-api/one-api.db?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
for row in conn.execute("SELECT id, name, status, remain_quota, unlimited_quota, used_quota, expired_time FROM tokens WHERE id=1"):
    print(dict(row))
for row in conn.execute("SELECT id, username, quota, used_quota, status FROM users WHERE id=1"):
    print(dict(row))
