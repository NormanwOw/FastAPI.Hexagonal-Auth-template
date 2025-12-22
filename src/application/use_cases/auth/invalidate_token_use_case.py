from src.config import ID
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class InvalidateToken:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: ID):
        async with self.uow:
            user = await self.uow.users.find_one(UserModel.id, user_id)
            await self.uow.users.update(
                UserModel.id, user_id, token_version=user.token_version + 1
            )
            await self.uow.commit()
