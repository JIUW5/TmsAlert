import asyncio
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_client import generate_latest
from starlette.responses import Response

from tms_alert_service.metrics import EVENT_LATENCY
from tms_alert_service.models import N9eEvent
from tms_alert_service.services.aggregation_service import flush_aggregations_once
from tms_alert_service.services.event_processor import process_event
from tms_alert_service.config import settings

logging.basicConfig(level='INFO')
logger = logging.getLogger('tms-alert-service')


async def flush_loop(stop_event: asyncio.Event) -> None:
    while not stop_event.is_set():
        try:
            await flush_aggregations_once()
        except Exception as exc:
            logger.exception('flush loop failed: %s', exc)
        await asyncio.sleep(settings.aggregation_flush_interval_seconds)


flush_stop_event = asyncio.Event()
flush_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global flush_task
    flush_task = asyncio.create_task(flush_loop(flush_stop_event))
    yield
    flush_stop_event.set()
    if flush_task:
        await flush_task


app = FastAPI(title='TMS Alert Service', lifespan=lifespan)


@app.get('/healthz')
def healthz() -> dict:
    return {'status': 'ok'}


@app.get('/metrics')
def metrics() -> Response:
    return Response(generate_latest(), media_type='text/plain; version=0.0.4')


@app.post('/events/n9e')
async def receive_event(event: N9eEvent) -> dict:
    with EVENT_LATENCY.time():
        return await process_event(event)


@app.post('/admin/flush')
async def force_flush() -> dict:
    await flush_aggregations_once()
    return {'ok': True}
