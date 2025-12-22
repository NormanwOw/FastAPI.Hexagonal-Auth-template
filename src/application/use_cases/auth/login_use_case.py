from src.domain.exceptions import InvalidPasswordException, UnauthorizedException
from src.infrastructure.interfaces import IJwtTokenService
from src.infrastructure.managers.password_manager import PasswordManager
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork
from src.presentation.schemas import UserWithTokens


class LoginUser:
    def __init__(
        self,
        uow: IUnitOfWork,
        password_manager: PasswordManager,
        jwt_service: IJwtTokenService,
    ):
        self.uow = uow
        self.password_manager = password_manager
        self.jwt_service = jwt_service

    async def __call__(self, username: str, password: str) -> UserWithTokens:
        async with self.uow:
            if not (
                user := await self.uow.users.find_one(UserModel.username, username)
            ):
                raise UnauthorizedException

            if not self.password_manager.verify_password(password, user.password):
                raise InvalidPasswordException

            data = {
                'user_id': str(user.id),
                'roles': ', '.join(role.name for role in user.roles),
                'token_version': user.token_version,
            }
            access_token = self.jwt_service.create_access_token(data=data)
            refresh_token = self.jwt_service.create_refresh_token(data=data)

            return UserWithTokens(
                access_token=access_token,
                refresh_token=refresh_token,
                name=user.username,
            )
