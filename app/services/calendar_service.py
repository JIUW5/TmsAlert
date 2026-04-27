import logging
from datetime import datetime

import httpx

from app.config import settings
from app.metrics import EVENT_FILTERED_TOTAL

logger = logging.getLogger('tms-alert-service')


async def pass_trading_day_check(ex: str | None, session: str, now: datetime) -> bool:
    if not ex or ex.upper() in {'NOT_SCHEDULED', 'NONE', 'NULL'}:
        return True

    date_str = now.strftime('%Y%m%d')
    url = f"{settings.calendar_base_url.rstrip('/')}/tradingDays"
    params = {'exchange': ex.lower(), 'session': session, 'eq': date_str}

    try:
        async with httpx.AsyncClient(timeout=settings.calendar_timeout_seconds) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        logger.exception('calendar check failed: %s', exc)
        EVENT_FILTERED_TOTAL.labels(reason='calendar_error').inc()
        return False

    if isinstance(data, list):
        return date_str in [str(item) for item in data]
    if isinstance(data, dict):
        items = data.get('data') or data.get('tradingDays') or data.get('items') or []
        return date_str in [str(item) for item in items]
    return False
