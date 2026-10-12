import sqlite3

conn = sqlite3.connect("file:/opt/one-api/one-api.db?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
cols = [r[1] for r in conn.execute("PRAGMA table_info(tokens)")]
print("token_columns", cols)
for row in conn.execute("SELECT id, name, status, remain_quota, unlimited_quota, used_quota FROM tokens"):
    print(dict(row))
