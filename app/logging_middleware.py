import logging
from datetime import datetime

from fastapi import Request

from app.models import RequestLogs
from app.services.sessionmaking import get_session

from __main__ import app


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path}")

    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    client_ip = request.headers.get('X-Forwarded-For')
    proxy_ip = request.client.host

    if client_ip is None:
        client_ip = proxy_ip

    logging.info(
        f"Response: {response.status_code} for {request.method} {request.url.path} (Duration: {process_time}s)"
    )

    async for session in get_session():
        log_entry = RequestLogs(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
            client_ip=client_ip,
            proxy_ip=proxy_ip,
        )
        session.add(log_entry)
        await session.commit()

    return response
