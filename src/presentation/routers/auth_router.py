from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.application.use_cases.auth.get_access_token import GetAccessToken
from src.application.use_cases.auth.invalidate_token_use_case import InvalidateToken
from src.application.use_cases.auth.login_use_case import LoginUser
from src.application.use_cases.auth.open_close_register_use_case import (
    OpenCloseRegistration,
)
from src.application.use_cases.auth.register_user_use_case import RegisterUser
from src.application.use_cases.auth.validate_invite_token_use_case import (
    ValidateInviteToken,
)
from src.config import PREFIX_URL, settings
from src.domain.entities import User
from src.domain.enums import RoleEnum
from src.infrastructure.forms.register_form import RegisterForm
from src.infrastructure.logger.logger import logger
from src.infrastructure.managers.role_manager import roles
from src.infrastructure.services.jwt_token_service import JwtTokenService
from src.presentation.dependencies.auth_dependencies import AuthDependencies
from src.presentation.schemas import (
    AccessToken,
    InviteToken,
    RefreshToken,
    RegistrationSchema,
    TokensResponse,
)

router = APIRouter(
    prefix=PREFIX_URL + '/auth',
    tags=['Auth'],
)


@router.post('/token')
async def token(
    request: Request,
    get_token: GetAccessToken = Depends(AuthDependencies.get_access_token),
) -> AccessToken:
    token = request.cookies.get('refresh_token')
    refresh_token = RefreshToken(refresh_token=token)
    return await get_token(refresh_token)


if settings.IS_OPEN_CLOSE_REG_ENABLED:

    @router.get('/invite_token')
    async def invite_token(
        token: str = Depends(JwtTokenService(settings).create_invite_token),
        admin: User = Depends(roles([RoleEnum.admin])),
    ) -> InviteToken:
        token = InviteToken(invite_token=token)
        logger.info(f'[{admin.name}] | сгенерирован invite токен')
        return token


@router.post(path='/login', status_code=200, summary='Login')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    login_user: LoginUser = Depends(AuthDependencies.login_user),
) -> TokensResponse:
    user = await login_user(form_data.username, form_data.password)

    logger.info(f'[{user.name}] | Выполнен Login')
    return TokensResponse(
        access_token=user.access_token, refresh_token=user.refresh_token
    )


@router.post(path='/logout', summary='Logout')
async def logout_from_profile(
    user: User = Depends(AuthDependencies.get_current_user),
    invalidate_token: InvalidateToken = Depends(AuthDependencies.invalidate_token),
):
    await invalidate_token(user.id)
    logger.info(f'[{user.name}] | Выполнен Logout')


if settings.IS_OPEN_CLOSE_REG_ENABLED:

    @router.post(path='/register', status_code=201, summary='Регистрация')
    async def register(
        register_form: RegisterForm,
        validate_token: ValidateInviteToken = Depends(
            AuthDependencies.validate_invite_token
        ),
        invite: Optional[str] = None,
        is_open_reg: bool = Depends(AuthDependencies.is_open_reg),
        register_user: RegisterUser = Depends(AuthDependencies.register_user),
    ) -> User:
        if invite:
            await validate_token(invite)
        else:
            if not is_open_reg:
                raise HTTPException(status_code=403)
        user = await register_user(register_form)
        logger.info(f'Зарегистрирован пользователь: {user.name}')
        return user

    @router.get(path='/registration', summary='Получение состояния регистрации')
    async def get_registration_state(
        is_open_reg: bool = Depends(AuthDependencies.is_open_reg),
    ) -> RegistrationSchema:
        return RegistrationSchema(is_open=is_open_reg)

    @router.put(
        path='/registration', status_code=200, summary='Открытие/закрытие регистрации'
    )
    async def open_close_registration(
        reg_schema: RegistrationSchema,
        open_close_reg: OpenCloseRegistration = Depends(
            AuthDependencies.open_close_reg
        ),
        admin: User = Depends(roles([RoleEnum.admin])),
    ):
        await open_close_reg(reg_schema)
        logger.info(
            f'[{admin.name}] | Регистрация '
            f'{"открыта" if reg_schema.is_open else "закрыта"}'
        )
        return Response(status_code=200)
else:

    @router.post(path='/register', status_code=201, summary='Регистрация')
    async def register(
        register_form: RegisterForm,
        register_user: RegisterUser = Depends(AuthDependencies.register_user),
    ) -> User:
        user = await register_user(register_form)
        logger.info(f'Зарегистрирован пользователь: {user.name}')
        return user
