from src.application.use_cases.users.delete_user import DeleteUser
from src.application.use_cases.users.get_roles import GetRoles
from src.application.use_cases.users.get_user_roles import GetUserRoles
from src.application.use_cases.users.get_users import GetUsers
from src.application.use_cases.users.set_roles import SetRoles
from src.infrastructure.uow.impl import get_uow


class UsersDependencies:
    @classmethod
    async def get_users(cls):
        return GetUsers(get_uow())

    @classmethod
    async def set_roles(cls):
        return SetRoles(get_uow())

    @classmethod
    async def delete_user(cls):
        return DeleteUser(get_uow())

    @classmethod
    async def get_roles(cls):
        return GetRoles(get_uow())

    @classmethod
    async def get_user_roles(cls):
        return GetUserRoles(get_uow())
