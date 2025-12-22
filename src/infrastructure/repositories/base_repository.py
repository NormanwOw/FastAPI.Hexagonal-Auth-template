from typing import Any, Type, TypeVar

from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.infrastructure.models import Base
from src.infrastructure.repositories.interfaces import ISQLAlchemyRepository
from src.presentation.pagination import Pagination

T = TypeVar('T', bound=Base)


class SQLAlchemyRepository(ISQLAlchemyRepository):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def add(self, data: T, flush: bool = False) -> T | None:
        self.session.add(data)
        if flush:
            await self.session.flush()

        return data

    async def bulk_add(self, objects: list[T]):
        if not objects:
            return
        await self.session.run_sync(
            lambda sync_sess: sync_sess.bulk_save_objects(
                objects, return_defaults=False
            )
        )

    async def find_all(
        self,
        filter_field: InstrumentedAttribute = None,
        filter_value: Any = None,
        order_by: InstrumentedAttribute = None,
        pagination: Pagination = None,
    ) -> list[T]:
        if not pagination:
            pagination = Pagination()
        if not order_by:
            order_by = self.model.id
        if not filter_field:
            res = await self.session.scalars(
                select(self.model)
                .order_by(desc(order_by))
                .limit(pagination.limit)
                .offset(pagination.offset)
            )
            return list(res.all())

        res = await self.session.scalars(
            select(self.model)
            .where(filter_field == filter_value)
            .order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        return list(res.all())

    async def find_last_id(self) -> int:
        res = await self.session.scalars(
            select(self.model).order_by(self.model.id.desc()).limit(1)
        )
        res = res.first()
        if not res:
            return 0
        return res.id

    async def find_with_pagination(
        self,
        order_by: InstrumentedAttribute = None,
        pagination: Pagination = None,
        **filters: Any,
    ) -> tuple[int, list[T]]:
        res = await self.session.scalars(
            select(func.count()).select_from(self.model).filter_by(**filters)
        )
        total = res.first()
        items = await self.find(order_by, pagination, **filters)
        return total, items

    async def find(
        self,
        order_by: InstrumentedAttribute = None,
        pagination: Pagination = None,
        **filters: Any,
    ) -> list[T]:
        if not order_by:
            order_by = self.model.id
        if not pagination:
            pagination = Pagination()
        res = await self.session.scalars(
            select(self.model)
            .filter_by(**filters)
            .order_by(order_by)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        return list(res.all())

    async def find_one(
        self,
        filter_field: InstrumentedAttribute = None,
        filter_value: Any = None,
        cache: bool = False,
        data: T = None,
    ) -> T | None:
        if filter_field:
            query = select(self.model).where(filter_field == filter_value)
        else:
            query = select(self.model)
        res = await self.session.execute(query)
        item = res.scalars().first()
        return item

    async def update(
        self,
        filter_field: InstrumentedAttribute = None,
        filter_value: Any = None,
        **values,
    ) -> T:
        if filter_field:
            stmt = (
                update(self.model)
                .values(**values)
                .where(filter_field == filter_value)
                .returning(self.model)
            )
        else:
            stmt = update(self.model).values(**values).returning(self.model)
        res = await self.session.execute(stmt)

        return res.scalars().first()

    async def delete_one(self, filter_field: InstrumentedAttribute, filter_value: Any):
        await self.session.execute(
            delete(self.model).where(filter_field == filter_value)
        )

    async def delete(self, **filters):
        await self.session.execute(delete(self.model).filter_by(**filters))
