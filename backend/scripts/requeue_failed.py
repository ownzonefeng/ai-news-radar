from app import db

with db.get_conn() as conn:
    row = conn.execute(
        "UPDATE articles SET status=0, attempts=0 WHERE status=2"
    )
    print("requeued", row.rowcount if hasattr(row, "rowcount") else "done")
