from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import ID
from src.infrastructure.models import UserRoleModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IUserRoleRepository


class UserRoleRepository(IUserRoleRepository, SQLAlchemyRepository):
    model = UserRoleModel

    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, self.model)

    async def delete_by_ids(self, user_id: ID, role_id: ID):
        await self.__session.execute(
            delete(UserRoleModel).where(
                UserRoleModel.user_id == user_id, UserRoleModel.role_id == role_id
            )
        )
