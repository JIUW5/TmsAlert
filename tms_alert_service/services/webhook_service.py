import logging

import httpx

from tms_alert_service.config import settings
from tms_alert_service.metrics import WEBHOOK_SEND_TOTAL

logger = logging.getLogger('tms-alert-service')


async def send_webhook(token: str, title: str, text: str) -> bool:
    url = settings.webhook_url_template.format(token=token)
    body = {'msgtype': 'markdown', 'markdown': {'title': title, 'text': text}}

    try:
        async with httpx.AsyncClient(timeout=settings.webhook_timeout_seconds) as client:
            response = await client.post(url, json=body)
            response.raise_for_status()
        WEBHOOK_SEND_TOTAL.labels(result='success').inc()
        return True
    except Exception as exc:
        logger.exception('webhook send failed: %s', exc)
        WEBHOOK_SEND_TOTAL.labels(result='failed').inc()
        return False
