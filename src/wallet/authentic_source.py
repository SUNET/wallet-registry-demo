"""Main module, FastAPI runs from here"""
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from redis.asyncio.client import Redis

from .authentic_source_fetch_degree import authentic_source_fetch_degree
from .authentic_source_login import AuthenticSourceLoginInput, authentic_source_login

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


@app.post("/login")
async def post_login(authentic_source_login_input: AuthenticSourceLoginInput) -> Response:
    """login fixme"""

    try:
        db_url = await authentic_source_login(redis_conn, authentic_source_login_input)
        return JSONResponse(content={"status": "ok", "degree_url": f"/degree/{db_url}"})

    except (ValueError, TypeError) as _:
        return JSONResponse(status_code=400, content={"error": "Invalid format"})


@app.get("/degree/{degree_id}")
async def get_degree(degree_id: str) -> Response:
    """add fixme"""

    try:
        degree = await authentic_source_fetch_degree(redis_conn, degree_id)

        if degree is None:
            return JSONResponse(content={"status": "no such degree"})

        return JSONResponse(content={"status": "ok", "degree": degree})

    except (ValueError, TypeError) as _:
        return JSONResponse(status_code=400, content={"error": "Invalid format"})
