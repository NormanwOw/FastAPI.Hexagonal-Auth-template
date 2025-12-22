from pydantic import BaseModel


class Pagination(BaseModel):
    limit: int | None = None
    offset: int | None = None
