from app.db import db


def fetch_owner_mobile(owner_name: str | None) -> str | None:
    if not owner_name:
        return None
    sql = 'SELECT mobile FROM service_owner_contact WHERE owner_name=%s LIMIT 1'
    with db.conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (owner_name,))
            row = cur.fetchone()
            return row['mobile'] if row else None
