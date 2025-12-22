from src.infrastructure.repositories.interfaces import (
    IRoleRepository,
    IUserRepository,
    IUserRoleRepository,
)
from src.infrastructure.repositories.role_repository import RoleRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_role_repository import UserRoleRepository
from src.infrastructure.session import async_session
from src.infrastructure.uow.interfaces import IUnitOfWork


class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory):
        self.__session_factory = session_factory

    async def __aenter__(self):
        self.__session = self.__session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            await self.rollback()
        await self.__session.close()

    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()

    @property
    def users(self) -> IUserRepository:
        return UserRepository(self.__session)

    @property
    def roles(self) -> IRoleRepository:
        return RoleRepository(self.__session)

    @property
    def user_role(self) -> IUserRoleRepository:
        return UserRoleRepository(self.__session)


def get_uow() -> IUnitOfWork:
    return UnitOfWork(session_factory=async_session)
