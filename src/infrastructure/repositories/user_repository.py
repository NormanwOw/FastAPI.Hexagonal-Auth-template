from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import UserModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import IUserRepository


class UserRepository(IUserRepository, SQLAlchemyRepository):
    model = UserModel

    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, self.model)
