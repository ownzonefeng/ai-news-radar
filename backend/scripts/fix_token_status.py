import sqlite3

conn = sqlite3.connect("/opt/one-api/one-api.db")
conn.execute("UPDATE tokens SET status=1, remain_quota=1000000000 WHERE id=1")
conn.commit()
conn.close()
print("token status reset to enabled, quota 1000000000")
