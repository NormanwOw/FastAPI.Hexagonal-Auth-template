from pydantic import BaseModel, Field


class RegisterForm(BaseModel):
    login: str = Field(max_length=16, min_length=3)
    password: str = Field(max_length=32, min_length=8)
    password_confirmation: str = Field(max_length=32)
