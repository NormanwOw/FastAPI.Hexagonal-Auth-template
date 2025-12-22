from src.config import ID
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class DeleteUser:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: ID):
        async with self.uow:
            await self.uow.users.delete_one(UserModel.id, user_id)
            await self.uow.commit()
