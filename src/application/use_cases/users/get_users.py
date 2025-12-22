from src.domain.entities import User
from src.infrastructure.uow.interfaces import IUnitOfWork


class GetUsers:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self) -> list[User]:
        async with self.uow:
            users = await self.uow.users.find_all()
            return [
                User(
                    **user.to_dict(),
                    name=user.username,
                    roles=[role.name for role in user.roles],
                )
                for user in users
            ]
