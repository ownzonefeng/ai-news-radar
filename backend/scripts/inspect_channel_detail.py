import sqlite3

conn = sqlite3.connect("file:/opt/one-api/one-api.db?mode=ro", uri=True)
conn.row_factory = sqlite3.Row
row = conn.execute(
    'SELECT id, type, name, base_url, models, "group", status, model_mapping, config, other FROM channels WHERE id=1'
).fetchone()
print(dict(row))
