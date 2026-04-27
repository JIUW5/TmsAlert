from fastapi import APIRouter
from prometheus_client import generate_latest
from starlette.responses import Response

router = APIRouter()


@router.get('/healthz')
def healthz() -> dict:
    return {'status': 'ok'}


@router.get('/metrics')
def metrics() -> Response:
    return Response(generate_latest(), media_type='text/plain; version=0.0.4')
