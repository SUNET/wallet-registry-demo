"""Main module, FastAPI runs from here"""
from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from redis.asyncio.client import Redis

from .add_credential import AddCredentialInput, add_credential
from .revoke_credential import RevokeCredentialInput, revoke_credential
from .verify_credential import VerifyCredentialInput, verify_credential

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


@app.post("/verify_credential")
async def post_verify(verify_credential_input: VerifyCredentialInput) -> Response:
    """verify fixme"""

    try:
        db_status = await verify_credential(redis_conn, verify_credential_input)
        if db_status is None:
            return JSONResponse(content={"status": "no such credential"})
        if db_status == "0":
            return JSONResponse(content={"status": "valid credential"})
        return JSONResponse(content={"status": "revoked credential"})

    except (ValueError, TypeError) as _:
        return JSONResponse(status_code=400, content={"error": "Invalid format"})


@app.post("/add_credential")
async def post_add(add_credential_input: AddCredentialInput) -> Response:
    """add fixme"""

    try:
        await add_credential(redis_conn, add_credential_input)
        return JSONResponse(content={"status": "added credential"})

    except (ValueError, TypeError) as _:
        return JSONResponse(status_code=400, content={"error": "Invalid format"})


@app.post("/revoke_credential")
async def post_revoke(revoke_credential_input: RevokeCredentialInput) -> Response:
    """revoke fixme"""

    try:
        await revoke_credential(redis_conn, revoke_credential_input)
        return JSONResponse(content={"status": "revoked credential"})

    except (ValueError, TypeError) as _:
        return JSONResponse(status_code=400, content={"error": "Invalid format"})
