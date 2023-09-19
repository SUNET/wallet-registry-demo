from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from redis.asyncio.client import Redis


class VerifyCredentialInput(BaseModel):
    credential_hash: str


async def verify_credential(redis_conn: Redis[str], verify_credential_input: VerifyCredentialInput) -> Optional[str]:
    """Check credential"""

    if not verify_credential_input.credential_hash.isalnum():
        raise ValueError("Wrong format")
    return await redis_conn.get(verify_credential_input.credential_hash)
