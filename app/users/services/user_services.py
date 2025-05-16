from app.users.repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def get_all_users(self, org_id, order_by: str = "created_at", order: str = "asc"):
        return await self._repo.get_all(org_id=org_id, order_by=order_by, order=order)

    async def get_user_by_id(self, user_id):
        return await self._repo.get_user_by_id(user_id)
