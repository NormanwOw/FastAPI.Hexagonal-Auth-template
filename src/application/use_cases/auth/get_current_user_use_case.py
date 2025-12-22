from src.domain.entities import User
from src.domain.enums import TokenTypes
from src.domain.exceptions import (
    NotAuthenticatedException,
    NoTokenProvidedException,
    TokenInvalidatedException,
    TokenTypeMismatchException,
    UserDisabledException,
    UserNotFoundException,
)
from src.infrastructure.interfaces import IJwtTokenService
from src.infrastructure.models import UserModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class GetCurrentUser:
    def __init__(self, uow: IUnitOfWork, jwt_service: IJwtTokenService):
        self.uow = uow
        self.jwt_service = jwt_service

    async def __call__(self, token: str) -> User:
        async with self.uow:
            if self.jwt_service.is_expired(token):
                raise NotAuthenticatedException

            payload = self.jwt_service.get_payload(token)
            if not payload:
                raise NoTokenProvidedException

            if payload.get('token_type') not in [TokenTypes.access, TokenTypes.refresh]:
                raise TokenTypeMismatchException

            user_id = payload.get('user_id')
            token_version = payload.get('token_version')
            user: UserModel = await self.uow.users.find_one(UserModel.id, user_id)
            if not user:
                raise UserNotFoundException

            if token_version != user.token_version:
                raise TokenInvalidatedException

            if user.disabled:
                raise UserDisabledException

            return User(
                **user.to_dict(),
                name=user.username,
                roles=[role.name for role in user.roles],
            )
