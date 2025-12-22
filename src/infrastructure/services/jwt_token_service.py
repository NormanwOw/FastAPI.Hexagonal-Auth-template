import datetime
from typing import Optional

import jwt

from src.config import Settings
from src.domain.enums import TokenTypes
from src.infrastructure.interfaces import IJwtTokenService


class JwtTokenService(IJwtTokenService):
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_invite_token(self) -> str:
        delta = datetime.timedelta(minutes=self.settings.INVITE_TOKEN_EXPIRE_MINUTES)
        return self.create_jwt(data={'token_type': 'invite'}, expires_delta=delta)

    def create_access_token(self, data: dict, delta: datetime.timedelta = None) -> str:
        delta = delta or datetime.timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        data['token_type'] = TokenTypes.access
        return self.create_jwt(data=data, expires_delta=delta)

    def create_refresh_token(self, data: dict) -> str:
        delta = datetime.timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)
        data['token_type'] = TokenTypes.refresh
        return self.create_jwt(data=data, expires_delta=delta)

    def create_jwt(self, data: dict, expires_delta: datetime.timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.now(tz=datetime.timezone.utc) + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM
        )
        return encoded_jwt

    def is_expired(self, token: str) -> bool:
        try:
            jwt.decode(
                token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM]
            )
            return False
        except Exception:
            return True

    def get_payload(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(
                token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM]
            )
        except Exception:
            return None
