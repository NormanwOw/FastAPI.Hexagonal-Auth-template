from src.domain.exceptions import NoTokenProvidedException, RoleMismatch
from src.infrastructure.interfaces import IJwtTokenService


class CheckRoles:
    def __init__(self, jwt_service: IJwtTokenService):
        self.jwt_service = jwt_service

    async def __call__(self, token: str, roles_list: list[str]):
        if not roles_list:
            return
        payload = self.jwt_service.get_payload(token=token)
        if not payload:
            raise NoTokenProvidedException
        roles = payload.get('roles', '').split(', ')

        for role in roles:
            if role in roles_list:
                return

        raise RoleMismatch
