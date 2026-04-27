from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import settings


def now_in_tz(tz_name: str | None = None) -> datetime:
    return datetime.now(ZoneInfo(tz_name or settings.session_timezone))


def get_session_type(now: datetime) -> str:
    if settings.day_session_start_hour <= now.hour < settings.day_session_end_hour:
        return 'day'
    return 'night'
