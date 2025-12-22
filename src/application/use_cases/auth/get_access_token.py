from src.application.use_cases.auth.get_current_user_use_case import GetCurrentUser
from src.infrastructure.interfaces import IJwtTokenService, IPasswordManager
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.schemas import AccessToken, RefreshToken


class GetAccessToken:
    def __init__(
        self,
        uow: IUnitOfWork,
        password_manager: IPasswordManager,
        jwt_service: IJwtTokenService,
        get_current_user: GetCurrentUser,
    ):
        self.uow = uow
        self.password_manager = password_manager
        self.jwt_service = jwt_service
        self.get_current_user = get_current_user

    async def __call__(self, token: RefreshToken) -> AccessToken:
        async with self.uow:
            user = await self.get_current_user(token.refresh_token)
            data = {
                'user_id': user.id,
                'roles': ', '.join(user.roles),
                'token_version': user.token_version,
            }
            token = self.jwt_service.create_access_token(data)
            return AccessToken(access_token=token)
