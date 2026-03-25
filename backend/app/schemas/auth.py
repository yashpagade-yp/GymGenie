from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.schemas.user import UserSummary


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    gym_id: UUID | None = None
    invite_code: str | None = Field(default=None, min_length=4, max_length=32)

    @model_validator(mode="after")
    def validate_gym_reference(self) -> "RegisterRequest":
        if self.gym_id is None and not self.invite_code:
            raise ValueError("Either gym_id or invite_code is required")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class GoogleLoginRequest(BaseModel):
    id_token: str = Field(min_length=10)
    invite_code: str | None = Field(default=None, min_length=4, max_length=32)


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthResponse(TokenPair):
    user: UserSummary


class GoogleAuthConfigResponse(BaseModel):
    enabled: bool
    client_id: str | None = None
