from fastapi import APIRouter, Depends

from app.users.dependencies import require_admin_user
from app.users.models import User
from app.voting import schemas
from app.voting.dependencies import get_vote_event_repository
from app.voting.repository import VoteEventRepository


router = APIRouter(prefix="/api/main_vote_event", tags=["Main event"])


@router.get("/", response_model=schemas.VoteEventRead)
async def get_main_vote_event(
    current_user: User = Depends(require_admin_user), repo: VoteEventRepository = Depends(get_vote_event_repository)
):
    return await repo.get_vote_event(current_user.organisation_id)
