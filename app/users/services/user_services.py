from app.users.repository import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def get_all_users(self, org_id):
        return await self._repo.get_all(org_id=org_id)

    async def get_user_by_id(self, user_id):
        return await self._repo.get_user_by_id(user_id)
