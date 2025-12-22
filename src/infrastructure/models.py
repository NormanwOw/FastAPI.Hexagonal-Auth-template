import uuid
from datetime import datetime
from typing import List

from sqlalchemy import UUID, ForeignKey, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.config import ID


def generate_id() -> ID:
    return ID(str(uuid.uuid4()))


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[ID] = mapped_column(
        UUID, nullable=False, primary_key=True, unique=True, default=uuid.uuid4
    )

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class RoleModel(Base):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    users: Mapped[List['UserModel']] = relationship(
        back_populates='roles', secondary='users_roles', lazy='select'
    )


class UserModel(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
    token_version: Mapped[int] = mapped_column(default=1)
    roles: Mapped[List['RoleModel']] = relationship(
        back_populates='users', secondary='users_roles', lazy='selectin'
    )

    async def get_roles(self) -> list[str]:
        return [role.name for role in self.roles]


class UserRoleModel(Base):
    __tablename__ = 'users_roles'

    user_id: Mapped[ID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, index=True
    )
    role_id: Mapped[ID] = mapped_column(
        ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True, index=True
    )


class Settings(Base):
    __tablename__ = 'settings'

    key: Mapped[str] = mapped_column(nullable=False, unique=True)
    value: Mapped[str] = mapped_column(nullable=False)
