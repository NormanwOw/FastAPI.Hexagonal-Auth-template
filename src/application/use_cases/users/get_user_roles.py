from src.config import ID
from src.domain.exceptions import UserNotFoundException
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.schemas import Role


class GetUserRoles:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: ID) -> list[Role]:
        async with self.uow:
            user: UserModel = await self.uow.users.find_one(UserModel.id, user_id)
            if not user:
                raise UserNotFoundException

        return [Role(name=role.name) for role in user.roles]
