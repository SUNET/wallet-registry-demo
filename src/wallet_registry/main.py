"""Main module, FastAPI runs from here"""
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request, Response
from redis.asyncio.client import Redis

# if "_" in os.environ and "sphinx-build" in os.environ["_"]:
#     print("Running sphinx build")
# else:
#     loop = asyncio.get_running_loop()
#     startup_task = loop.create_task(startup())

# Create fastapi app
# Disable swagger and docs endpoints for now


if TYPE_CHECKING:
    redis_conn = Redis[str](
        host=os.environ.get("REDIS_URL", "localhost"),
        socket_timeout=5,
        socket_connect_timeout=5,
        socket_keepalive=True,
        encoding="utf-8",
        decode_responses=True,
        health_check_interval=60,
    )
else:
    redis_conn = Redis(
        host=os.environ.get("REDIS_URL", "localhost"),
        socket_timeout=5,
        socket_connect_timeout=5,
        socket_keepalive=True,
        encoding="utf-8",
        decode_responses=True,
        health_check_interval=60,
    )


app = FastAPI(docs_url=None, redoc_url=None)


@app.on_event("startup")
async def test_redis() -> None:
    """Ensure database is online"""

    if not await redis_conn.ping():
        print(f"Problem with redis at {os.environ.get('REDIS_URL', 'localhost')}")
        sys.exit(1)


# @app.get("/healthcheck")
# async def get_healthcheck(request: Request) -> JSONResponse:
#     """/healthcheck, GET method.

#     Do a healthcheck. Sign some data.

#     Parameters:
#     request (fastapi.Request): The entire HTTP request.

#     Returns:
#     fastapi.responses.JSONResponse
#     """

#     _ = await authorized_by(request)
#     return await healthcheck()


@app.post("/verify")
async def post_verify(request: Request) -> Response:
    """verify fixme"""

    reply_media_type = "application/json"

    content_type = request.headers.get("Content-type")
    if content_type is None or content_type != "application/json":
        return Response(status_code=400, content=b"0", media_type=reply_media_type)

    # data = await request.body()

    try:
        # data_content = await timestamp_handle_request(data)
        data_content = "fixme"
        return Response(status_code=200, content=data_content, media_type=reply_media_type)
    except (ValueError, TypeError) as _:
        return Response(status_code=400, content=b"0", media_type=reply_media_type)


@app.get("/dummy01")
async def get_dummy() -> Response:
    """dummy fixme"""

    data = await redis_conn.get("asd")
    return Response(status_code=200, content=data, media_type="application/json")
