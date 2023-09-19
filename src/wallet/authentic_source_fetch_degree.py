from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from redis.asyncio.client import Redis


async def authentic_source_fetch_degree(redis_conn: Redis[str], degree_id: str) -> Optional[str]:
    """Get degree"""

    if not degree_id.isalnum():
        raise ValueError("Wrong format")

    return await redis_conn.get(degree_id)
