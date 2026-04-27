from fastapi import APIRouter

from app.metrics import EVENT_LATENCY
from app.schemas.event import N9eEvent
from app.services.aggregation_service import flush_aggregations_once
from app.services.event_service import process_event

router = APIRouter()


@router.post('/events/n9e')
async def receive_event(event: N9eEvent) -> dict:
    with EVENT_LATENCY.time():
        return await process_event(event)


@router.post('/admin/flush')
async def force_flush() -> dict:
    await flush_aggregations_once()
    return {'ok': True}
