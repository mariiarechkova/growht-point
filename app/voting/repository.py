from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.voting.models import MainVoteEvent


class VoteEventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_vote_event(self, org_id: int) -> MainVoteEvent:
        result = await self.session.execute(select(MainVoteEvent).where(MainVoteEvent.organisation_id == org_id))
        return result.scalars().first()
