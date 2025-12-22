from src.domain.exceptions import InvalidTokenException
from src.infrastructure.interfaces import IJwtTokenService


class ValidateInviteToken:
    def __init__(self, token_service: IJwtTokenService):
        self.token_service = token_service

    async def __call__(self, token: str):
        if self.token_service.is_expired(token):
            raise InvalidTokenException

        payload = self.token_service.get_payload(token)
        if payload is None or payload.get('token_type', '') != 'invite':
            raise InvalidTokenException
