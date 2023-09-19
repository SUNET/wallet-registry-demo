from __future__ import annotations

from pydantic import BaseModel
from redis.asyncio.client import Redis


class AddCredentialInput(BaseModel):
    credential_hash: str


async def add_credential(redis_conn: Redis[str], add_credential_input: AddCredentialInput) -> None:
    """Check credential"""

    if not add_credential_input.credential_hash.isalnum():
        raise ValueError("Wrong format")
    await redis_conn.set(add_credential_input.credential_hash, "0")
