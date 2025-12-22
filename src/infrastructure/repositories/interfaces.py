from abc import ABC, abstractmethod
from typing import Any, TypeVar

from sqlalchemy.orm import InstrumentedAttribute

from src.config import ID
from src.infrastructure.models import Base
from src.presentation.pagination import Pagination

T = TypeVar('T', bound=Base)


class ISQLAlchemyRepository(ABC):
    @abstractmethod
    async def add(self, data: T, flush: bool = False) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def bulk_add(self, objects: list[T]):
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        filter_field: InstrumentedAttribute = None,
        filter_value: Any = None,
        order_by: InstrumentedAttribute = None,
        pagination: Pagination = None,
    ) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def find(
        self,
        order_by: InstrumentedAttribute = None,
        pagination: Pagination = None,
        **filters: Any,
    ) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    async def find_with_pagination(
        self,
        order_by: InstrumentedAttribute = None,
        pagination: Pagination = None,
        **filters: Any,
    ) -> tuple[int, list[T]]:
        raise NotImplementedError

    @abstractmethod
    async def find_one(
        self,
        filter_field: InstrumentedAttribute = None,
        filter_value: Any = None,
        cache: bool = False,
        data: T = None,
    ) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        filter_field: InstrumentedAttribute = None,
        filter_value: Any = None,
        **values,
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, filter_field: InstrumentedAttribute, filter_value: Any):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **filters):
        raise NotImplementedError


class IUserRepository(ISQLAlchemyRepository, ABC): ...


class IRoleRepository(ISQLAlchemyRepository, ABC): ...


class ISettingsRepository(ISQLAlchemyRepository, ABC):
    @abstractmethod
    async def is_reg_open(self) -> bool:
        raise NotImplementedError


class IUserRoleRepository(ISQLAlchemyRepository, ABC):
    @abstractmethod
    async def delete_by_ids(self, user_id: ID, role_id: ID):
        raise NotImplementedError
