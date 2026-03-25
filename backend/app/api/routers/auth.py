from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db_session
from app.core.config import settings
from app.schemas.auth import (
    AuthResponse,
    GoogleAuthConfigResponse,
    GoogleLoginRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
)
from app.schemas.user import UserSummary
from app.services.auth import login_with_google, login_with_password, refresh_session, register_member

router = APIRouter()


@router.post("/register", response_model=AuthResponse, summary="Register a new gym member")
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_db_session)) -> AuthResponse:
    return await register_member(session, payload)


@router.post("/login", response_model=AuthResponse, summary="Login with email and password")
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_db_session)) -> AuthResponse:
    return await login_with_password(session, payload)


@router.post("/google", response_model=AuthResponse, summary="Login with Google")
async def google_login(payload: GoogleLoginRequest, session: AsyncSession = Depends(get_db_session)) -> AuthResponse:
    return await login_with_google(session, payload)


@router.get("/google/config", response_model=GoogleAuthConfigResponse, summary="Get Google auth configuration")
async def google_config() -> GoogleAuthConfigResponse:
    return GoogleAuthConfigResponse(enabled=bool(settings.google_client_id), client_id=settings.google_client_id)


@router.post("/refresh", response_model=AuthResponse, summary="Refresh an access token")
async def refresh(payload: RefreshTokenRequest, session: AsyncSession = Depends(get_db_session)) -> AuthResponse:
    return await refresh_session(session, payload.refresh_token)


@router.get("/me", response_model=UserSummary, summary="Get the authenticated user")
async def me(current_user=Depends(get_current_user)) -> UserSummary:
    return UserSummary.model_validate(current_user)
