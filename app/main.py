import asyncio
import logging

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import router as api_router
from app.config import settings
from app.services.aggregation_service import flush_aggregations_once

logging.basicConfig(level=settings.log_level)
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
app.include_router(api_router)


def main() -> None:
    uvicorn.run('app.main:app', host=settings.app_host, port=settings.app_port, reload=False)


if __name__ == '__main__':
    main()
