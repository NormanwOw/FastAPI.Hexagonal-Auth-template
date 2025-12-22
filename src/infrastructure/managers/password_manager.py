import string
from random import choice

from passlib.context import CryptContext

from src.infrastructure.interfaces import IPasswordManager


class PasswordManager(IPasswordManager):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')

    def hash(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_password(self, length: int) -> str:
        return ''.join(
            choice(string.ascii_letters + string.digits) for _ in range(length)
        )
