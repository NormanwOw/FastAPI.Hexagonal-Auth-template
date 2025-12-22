from datetime import datetime

from pydantic import BaseModel

from src.config import ID


class User(BaseModel):
    id: ID
    name: str
    disabled: bool
    registered_at: datetime
    roles: list[str]
    token_version: int
