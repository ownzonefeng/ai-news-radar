import pymysql
import os

conn = pymysql.connect(
    host=os.environ["MYSQL_HOST"],
    port=int(os.environ.get("MYSQL_PORT", "3306")),
    user=os.environ["MYSQL_USER"],
    password=os.environ["MYSQL_PASSWORD"],
    database=os.environ["MYSQL_DB"],
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True,
)
cur = conn.cursor()
cur.execute(
    "UPDATE articles SET title_zh=NULL, summary=NULL, topic=NULL, tags=NULL, "
    "status=0, attempts=0 WHERE summary LIKE '%%?%%' OR title_zh LIKE '%%?%%'"
)
print("reset rows:", cur.rowcount)
conn.close()
