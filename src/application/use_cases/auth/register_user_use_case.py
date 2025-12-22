import string

from src.domain.enums import RoleEnum
from src.domain.exceptions import (
    InvalidUsernameException,
    PasswordConfirmationMissmatchException,
    UsernameAlreadyExistsException,
)
from src.infrastructure.forms.register_form import RegisterForm
from src.infrastructure.interfaces import IPasswordManager
from src.infrastructure.models import RoleModel, UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class RegisterUser:
    def __init__(self, uow: IUnitOfWork, password_manager: IPasswordManager):
        self.uow = uow
        self.password_manager = password_manager

    async def __call__(self, register_form: RegisterForm) -> UserModel:
        async with self.uow:
            if register_form.password != register_form.password_confirmation:
                raise PasswordConfirmationMissmatchException

            if not all(
                [
                    c in string.ascii_letters + string.digits or c == '_'
                    for c in register_form.login
                ]
            ):
                raise InvalidUsernameException

            if await self.uow.users.find_one(UserModel.username, register_form.login):
                raise UsernameAlreadyExistsException

            hashed_password = self.password_manager.hash(register_form.password)
            user_role: RoleModel = await self.uow.roles.find_one(
                RoleModel.name, RoleEnum.user
            )
            new_user_model = UserModel(
                username=register_form.login, password=hashed_password
            )
            new_user_model.roles.append(user_role)
            await self.uow.users.add(new_user_model)
            await self.uow.commit()

        return new_user_model
