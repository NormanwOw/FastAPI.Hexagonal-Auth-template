from fastapi import Depends

from src.application.use_cases.auth.check_roles_use_case import CheckRoles
from src.application.use_cases.auth.get_current_user_use_case import GetCurrentUser
from src.config import settings
from src.domain.enums import RoleEnum
from src.infrastructure.services.jwt_token_service import JwtTokenService
from src.infrastructure.uow.impl import get_uow
from src.presentation.dependencies.auth_dependencies import access_token_getter


def roles(required_roles: list[RoleEnum] = None):
    async def role_checker(access_token: str = Depends(access_token_getter)):
        jwt_service = JwtTokenService(settings)
        await CheckRoles(jwt_service)(access_token, required_roles)
        return await GetCurrentUser(get_uow(), jwt_service)(access_token)

    return role_checker if not settings.DEBUG else lambda: None
