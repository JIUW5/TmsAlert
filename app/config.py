from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Settings:
    app_host: str
    app_port: int
    log_level: str

    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    calendar_base_url: str
    calendar_timeout_seconds: int

    webhook_url_template: str
    webhook_timeout_seconds: int

    session_timezone: str
    day_session_start_hour: int
    day_session_end_hour: int

    aggregation_window_seconds: int
    aggregation_flush_interval_seconds: int



def load_settings(config_file: str = 'config.yaml') -> Settings:
    path = Path(config_file)
    if not path.exists():
        raise FileNotFoundError(f'config file not found: {config_file}')

    data = yaml.safe_load(path.read_text(encoding='utf-8'))

    app = data['app']
    db = data['mariadb']
    calendar = data['calendar']
    webhook = data['webhook']
    session = data['session']
    aggregation = data['aggregation']

    return Settings(
        app_host=app['host'],
        app_port=int(app['port']),
        log_level=app.get('log_level', 'INFO'),
        db_host=db['host'],
        db_port=int(db['port']),
        db_user=db['user'],
        db_password=str(db.get('password', '')),
        db_name=db['database'],
        calendar_base_url=calendar['base_url'],
        calendar_timeout_seconds=int(calendar['timeout_seconds']),
        webhook_url_template=webhook['url_template'],
        webhook_timeout_seconds=int(webhook['timeout_seconds']),
        session_timezone=session['timezone'],
        day_session_start_hour=int(session['day_session_start_hour']),
        day_session_end_hour=int(session['day_session_end_hour']),
        aggregation_window_seconds=int(aggregation['window_seconds']),
        aggregation_flush_interval_seconds=int(aggregation['flush_interval_seconds']),
    )


settings = load_settings()
