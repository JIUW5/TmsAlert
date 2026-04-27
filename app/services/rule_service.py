from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from croniter import croniter

from app.config import settings
from app.db import db


def fetch_rules(hostname: str, service_name: str) -> list[dict[str, Any]]:
    sql = """
    SELECT id, host_name, service_name, action_type, cron_expr, timezone, is_enabled, service_owner
    FROM service_schedule_rule
    WHERE host_name=%s AND service_name=%s AND is_enabled=1
    """
    with db.conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (hostname, service_name))
            return cur.fetchall()


def is_time_in_schedule(rules: list[dict[str, Any]], ref_time: datetime) -> bool:
    starts = [r for r in rules if str(r['action_type']).upper() == 'START']
    stops = [r for r in rules if str(r['action_type']).upper() == 'STOP']
    if not starts:
        return True

    last_start = None
    for row in starts:
        tz = row.get('timezone') or settings.session_timezone
        dt = croniter(row['cron_expr'], ref_time.astimezone(ZoneInfo(tz))).get_prev(datetime)
        last_start = dt if last_start is None or dt > last_start else last_start

    if not stops:
        return True

    last_stop = None
    for row in stops:
        tz = row.get('timezone') or settings.session_timezone
        dt = croniter(row['cron_expr'], ref_time.astimezone(ZoneInfo(tz))).get_prev(datetime)
        last_stop = dt if last_stop is None or dt > last_stop else last_stop

    return bool(last_start and (last_stop is None or last_start > last_stop))
