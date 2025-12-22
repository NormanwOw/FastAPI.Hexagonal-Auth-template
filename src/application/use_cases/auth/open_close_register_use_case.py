from src.infrastructure.models import SettingsModel
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.schemas import RegistrationSchema


class OpenCloseRegistration:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, reg_schema: RegistrationSchema):
        async with self.uow:
            await self.uow.settings.update(
                SettingsModel.key, 'is_reg_open', value=str(reg_schema.is_open).lower()
            )
            await self.uow.commit()
            return reg_schema
