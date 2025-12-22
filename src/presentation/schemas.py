from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class TokensResponse(RefreshToken, AccessToken):
    pass


class ApiToken(BaseModel):
    token: str


class UserWithTokens(TokensResponse):
    name: str


class Role(BaseModel):
    name: str


class InviteToken(BaseModel):
    invite_token: str


class RegistrationSchema(BaseModel):
    is_open: bool
