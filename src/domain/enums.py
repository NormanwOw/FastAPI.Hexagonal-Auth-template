from enum import Enum


class RoleEnum(str, Enum):
    user = 'user'
    admin = 'admin'

    @classmethod
    def get_id_mapper(cls) -> dict:
        return {
            'admin': 'cb9bf05d-d87d-407b-92ca-0bf348add278',
            'user': '81e08695-0e57-4f1c-8c12-e6bb0614df78',
        }

    @classmethod
    def get_role_id(cls, role: str) -> int:
        return cls.get_id_mapper()[role]


class TokenTypes(str, Enum):
    access = 'access'
    refresh = 'refresh'
