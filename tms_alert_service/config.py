import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    db_host: str = os.getenv('DB_HOST', '127.0.0.1')
    db_port: int = int(os.getenv('DB_PORT', '3306'))
    db_user: str = os.getenv('DB_USER', 'root')
    db_password: str = os.getenv('DB_PASSWORD', '')
    db_name: str = os.getenv('DB_NAME', 'tms_alert')

    calendar_base_url: str = os.getenv('CALENDAR_BASE_URL', 'http://calendar.saturn-res.ipa.zs')
    calendar_timeout_seconds: int = int(os.getenv('CALENDAR_TIMEOUT_SECONDS', '3'))

    webhook_url_template: str = os.getenv('WEBHOOK_URL_TEMPLATE', 'http://172.17.228.97:5008/robot/send?access_token={token}')
    webhook_timeout_seconds: int = int(os.getenv('WEBHOOK_TIMEOUT_SECONDS', '3'))

    session_timezone: str = os.getenv('SESSION_TIMEZONE', 'Asia/Shanghai')
    day_session_start_hour: int = int(os.getenv('DAY_SESSION_START_HOUR', '8'))
    day_session_end_hour: int = int(os.getenv('DAY_SESSION_END_HOUR', '20'))

    aggregation_window_seconds: int = int(os.getenv('AGGREGATION_WINDOW_SECONDS', '60'))
    aggregation_flush_interval_seconds: int = int(os.getenv('AGGREGATION_FLUSH_INTERVAL_SECONDS', '5'))


settings = Settings()
