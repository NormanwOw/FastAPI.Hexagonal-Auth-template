from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.application.use_cases.auth.check_is_open_reg_use_case import (
    CheckIsOpenRegistration,
)
from src.application.use_cases.auth.get_access_token import GetAccessToken
from src.application.use_cases.auth.get_current_user_use_case import GetCurrentUser
from src.application.use_cases.auth.invalidate_token_use_case import InvalidateToken
from src.application.use_cases.auth.login_use_case import LoginUser
from src.application.use_cases.auth.open_close_register_use_case import (
    OpenCloseRegistration,
)
from src.application.use_cases.auth.register_user_use_case import RegisterUser
from src.application.use_cases.auth.validate_invite_token_use_case import (
    ValidateInviteToken,
)
from src.config import settings
from src.infrastructure.managers.password_manager import PasswordManager
from src.infrastructure.services.jwt_token_service import JwtTokenService
from src.infrastructure.uow.impl import get_uow

access_token_getter = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


class AuthDependencies:
    password_manager = PasswordManager()
    jwt_service = JwtTokenService(settings)

    @classmethod
    async def open_close_reg(cls):
        return OpenCloseRegistration(get_uow())

    @classmethod
    async def is_open_reg(cls):
        return await CheckIsOpenRegistration(get_uow())()

    @classmethod
    async def get_current_user(cls, access_token: str = Depends(access_token_getter)):
        return await GetCurrentUser(get_uow(), cls.jwt_service)(access_token)

    @classmethod
    async def register_user(cls):
        return RegisterUser(get_uow(), cls.password_manager)

    @classmethod
    async def login_user(cls):
        return LoginUser(get_uow(), cls.password_manager, cls.jwt_service)

    @classmethod
    async def get_access_token(cls):
        get_current_user = GetCurrentUser(get_uow(), cls.jwt_service)
        return GetAccessToken(
            get_uow(), cls.password_manager, cls.jwt_service, get_current_user
        )

    @classmethod
    async def invalidate_token(cls):
        return InvalidateToken(get_uow())

    @classmethod
    async def validate_invite_token(cls):
        return ValidateInviteToken(cls.jwt_service)
