from src.infrastructure.uow.interfaces import IUnitOfWork


class CheckIsOpenRegistration:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self) -> bool:
        async with self.uow:
            return await self.uow.settings.is_reg_open()
