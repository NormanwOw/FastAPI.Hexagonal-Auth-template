from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import SettingsModel
from src.infrastructure.repositories.base_repository import SQLAlchemyRepository
from src.infrastructure.repositories.interfaces import ISettingsRepository


class SettingsRepository(ISettingsRepository, SQLAlchemyRepository):
    model = SettingsModel

    def __init__(self, session: AsyncSession):
        self.__session = session
        super().__init__(session, self.model)

    async def is_reg_open(self) -> bool:
        res = await self.__session.scalars(
            select(self.model).where(self.model.key == 'is_reg_open')
        )
        return res.first().value.lower() == 'true'
