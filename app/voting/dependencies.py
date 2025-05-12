from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session

from .repository import VoteEventRepository


def get_vote_event_repository(
    session: AsyncSession = Depends(get_session),
) -> VoteEventRepository:
    return VoteEventRepository(session)
