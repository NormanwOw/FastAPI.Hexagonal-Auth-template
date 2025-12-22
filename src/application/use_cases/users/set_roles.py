from src.config import ID
from src.domain.enums import RoleEnum
from src.domain.exceptions import (
    RoleNotFoundException,
    RoleRequiredException,
    UserNotFoundException,
)
from src.infrastructure.models import RoleModel, UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class SetRoles:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: ID, roles: list[RoleEnum]):
        if not roles:
            raise RoleRequiredException

        async with self.uow:
            user: UserModel = await self.uow.users.find_one(UserModel.id, user_id)
            if not user:
                raise UserNotFoundException

            user_roles = set([role.name for role in user.roles])
            roles = set([role.name for role in roles])

            for role in roles:
                if role not in user_roles:
                    role_from_db: RoleModel = await self.uow.roles.find_one(
                        RoleModel.name, role
                    )
                    if not role_from_db:
                        raise RoleNotFoundException
                    user.roles.append(role_from_db)

            for role in user.roles:
                if role.name not in roles:
                    await self.uow.user_role.delete_by_ids(user.id, role.id)

            await self.uow.commit()
