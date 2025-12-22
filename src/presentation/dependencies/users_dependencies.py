from src.application.use_cases.users.delete_user import DeleteUser
from src.application.use_cases.users.get_roles import GetRoles
from src.application.use_cases.users.get_user_roles import GetUserRoles
from src.application.use_cases.users.get_users import GetUsers
from src.application.use_cases.users.set_roles import SetRoles
from src.infrastructure.uow.impl import get_uow


class UsersDependencies:
    @classmethod
    def get_users(cls) -> GetUsers:
        return GetUsers(get_uow())

    @classmethod
    def set_roles(cls) -> SetRoles:
        return SetRoles(get_uow())

    @classmethod
    def delete_user(cls) -> DeleteUser:
        return DeleteUser(get_uow())

    @classmethod
    def get_roles(cls) -> GetRoles:
        return GetRoles(get_uow())

    @classmethod
    def get_user_roles(cls) -> GetUserRoles:
        return GetUserRoles(get_uow())
