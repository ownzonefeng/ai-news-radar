import sqlite3

conn = sqlite3.connect("file:/opt/one-api/one-api.db?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
for row in conn.execute("SELECT id, name, type, status, models, key FROM channels"):
    print(dict(row))
