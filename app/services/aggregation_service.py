import json
from datetime import timedelta

from app.config import settings
from app.db import db
from app.metrics import PENDING_AGGREGATION
from app.schemas.event import N9eEvent
from app.services.time_service import now_in_tz
from app.services.webhook_service import send_webhook


def upsert_aggregation(event: N9eEvent, session: str, owner: str | None, mobile: str | None) -> None:
    window = settings.aggregation_window_seconds
    now = now_in_tz()
    bucket = now - timedelta(seconds=now.second % window, microseconds=now.microsecond)

    sql = """
    INSERT INTO alert_aggregation(bucket_start, hostname, service_name, status, robot_token, session, service_owner, mobile, count, latest_event_json, flushed, created_at, updated_at)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,%s,0,NOW(),NOW())
    ON DUPLICATE KEY UPDATE
      count=count+1,
      latest_event_json=VALUES(latest_event_json),
      updated_at=NOW(),
      flushed=0,
      service_owner=VALUES(service_owner),
      mobile=VALUES(mobile)
    """

    payload = json.dumps(event.model_dump(by_alias=True), ensure_ascii=False)
    with db.conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    bucket.strftime('%Y-%m-%d %H:%M:%S'),
                    event.labels.hostname,
                    event.labels.name,
                    event.status,
                    event.robot_token,
                    session,
                    owner,
                    mobile,
                    payload,
                ),
            )


async def flush_aggregations_once() -> None:
    cutoff = now_in_tz() - timedelta(seconds=settings.aggregation_window_seconds)
    fetch_sql = """
    SELECT id, hostname, service_name, status, robot_token, session, service_owner, mobile, count
    FROM alert_aggregation
    WHERE flushed=0 AND bucket_start<=%s
    ORDER BY bucket_start ASC
    LIMIT 100
    FOR UPDATE SKIP LOCKED
    """
    mark_sql = 'UPDATE alert_aggregation SET flushed=1, flushed_at=NOW(), updated_at=NOW() WHERE id=%s'
    count_sql = 'SELECT COUNT(1) AS cnt FROM alert_aggregation WHERE flushed=0'

    with db.conn() as conn:
        with conn.cursor() as cur:
            cur.execute(count_sql)
            PENDING_AGGREGATION.set(cur.fetchone()['cnt'])

            cur.execute('START TRANSACTION')
            cur.execute(fetch_sql, (cutoff.strftime('%Y-%m-%d %H:%M:%S'),))
            rows = cur.fetchall()
            cur.execute('COMMIT')

    for row in rows:
        is_alarm = row['status'].lower() == 'active'
        title = f"{'🔴' if is_alarm else '🟢'} {row['service_name']} {'告警' if is_alarm else '恢复'}"
        text = (
            f"### {title}\n"
            f"- 主机: **{row['hostname']}**\n"
            f"- 服务: **{row['service_name']}**\n"
            f"- 状态: **{row['status']}**\n"
            f"- 聚合条数(1分钟): **{row['count']}**\n"
            f"- 交易时段: **{row['session']}**\n"
            f"- 负责人: **{row['service_owner'] or '未知负责人'}**\n"
            f"- 手机号: **{row['mobile'] or '未配置手机号'}**"
        )
        if await send_webhook(row['robot_token'], title, text):
            with db.conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(mark_sql, (row['id'],))
