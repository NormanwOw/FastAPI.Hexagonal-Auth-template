import datetime
from abc import ABC, abstractmethod
from typing import Optional


class IJwtTokenService(ABC):
    @abstractmethod
    def create_invite_token(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(self, data: dict, delta: datetime.timedelta = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, data: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_jwt(self, data: dict, expires_delta: datetime.timedelta) -> str:
        raise NotImplementedError

    @abstractmethod
    def is_expired(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_payload(self, token: str) -> Optional[dict]:
        raise NotImplementedError


class IPasswordManager(ABC):
    @abstractmethod
    def hash(self, plain_password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_password(self, length: int) -> str:
        raise NotImplementedError
