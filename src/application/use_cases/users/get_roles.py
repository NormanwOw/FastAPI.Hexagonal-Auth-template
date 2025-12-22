from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.schemas import Role


class GetRoles:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self) -> list[Role]:
        async with self.uow:
            roles = await self.uow.roles.find_all()
            return [Role(name=role.name) for role in roles]
