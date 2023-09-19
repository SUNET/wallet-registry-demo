from __future__ import annotations

from pydantic import BaseModel
from redis.asyncio.client import Redis


class RevokeCredentialInput(BaseModel):
    credential_hash: str


async def revoke_credential(redis_conn: Redis[str], revoke_credential_input: RevokeCredentialInput) -> None:
    """Check credential"""

    if not revoke_credential_input.credential_hash.isalnum():
        raise ValueError("Wrong format")
    await redis_conn.set(revoke_credential_input.credential_hash, "1")
