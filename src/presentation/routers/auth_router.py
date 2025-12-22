from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.application.use_cases.auth.get_access_token import GetAccessToken
from src.application.use_cases.auth.invalidate_token_use_case import InvalidateToken
from src.application.use_cases.auth.login_use_case import LoginUser
from src.application.use_cases.auth.register_user_use_case import RegisterUser
from src.config import PREFIX_URL
from src.domain.entities import User
from src.infrastructure.forms.register_form import RegisterForm
from src.infrastructure.logger.logger import logger
from src.presentation.dependencies.auth_dependencies import AuthDependencies
from src.presentation.schemas import AccessToken, RefreshToken, TokensResponse

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


@router.post(path='/register', status_code=201, summary='Регистрация')
async def register(
    register_form: RegisterForm,
    register_user: RegisterUser = Depends(AuthDependencies.register_user),
):
    user = await register_user(register_form)
    logger.info(f'Зарегистрирован пользователь: {user.username}')
    return Response(status_code=201)
