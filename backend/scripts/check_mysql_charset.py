import os
import pymysql

conn = pymysql.connect(
    host=os.environ["MYSQL_HOST"],
    port=int(os.environ.get("MYSQL_PORT", "3306")),
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    database=os.environ["MYSQL_DB"],
    charset="utf8mb4",
)
cur = conn.cursor()
cur.execute("SHOW VARIABLES LIKE 'character_set%'")
for r in cur.fetchall():
    print(r)
cur.execute("SHOW CREATE TABLE articles")
row = cur.fetchone()
print(row[1] if row else "NO TABLE")
conn.close()
