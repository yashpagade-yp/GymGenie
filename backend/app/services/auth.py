from uuid import UUID

from fastapi import HTTPException, status
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from app.models.enums import AuthProvider, UserRole
from app.models.gym import Gym
from app.models.user import User
from app.schemas.auth import AuthResponse, GoogleLoginRequest, LoginRequest, RegisterRequest
from app.schemas.user import UserSummary


def _build_auth_response(user: User) -> AuthResponse:
    access_claims = {"role": user.role.value, "gym_id": str(user.gym_id)}
    return AuthResponse(
        access_token=create_access_token(str(user.id), access_claims),
        refresh_token=create_refresh_token(str(user.id)),
        user=UserSummary.model_validate(user),
    )


async def register_member(session: AsyncSession, payload: RegisterRequest) -> AuthResponse:
    existing_user = await session.scalar(select(User).where(User.email == payload.email))
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    gym = None
    if payload.gym_id is not None:
        gym = await session.scalar(select(Gym).where(Gym.id == payload.gym_id))
    elif payload.invite_code:
        gym = await session.scalar(select(Gym).where(Gym.invite_code == payload.invite_code.strip().upper()))

    if gym is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found for the provided invite code")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
        role=UserRole.MEMBER,
        auth_provider=AuthProvider.EMAIL,
        gym_id=gym.id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return _build_auth_response(user)


async def login_with_password(session: AsyncSession, payload: LoginRequest) -> AuthResponse:
    user = await session.scalar(select(User).where(User.email == payload.email, User.is_active.is_(True)))
    if user is None or user.password_hash is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return _build_auth_response(user)


async def refresh_session(session: AsyncSession, refresh_token: str) -> AuthResponse:
    from app.core.security import decode_token

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")
        user_id = payload["sub"]
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    user = await session.scalar(select(User).where(User.id == UUID(user_id), User.is_active.is_(True)))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return _build_auth_response(user)


async def login_with_google(session: AsyncSession, payload: GoogleLoginRequest) -> AuthResponse:
    if not settings.google_client_id:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google OAuth is not configured")

    try:
        token_info = id_token.verify_oauth2_token(payload.id_token, requests.Request(), settings.google_client_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token") from exc

    email = token_info.get("email")
    subject = token_info.get("sub")
    name = token_info.get("name") or email
    if not email or not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google token is missing required claims")

    user = await session.scalar(select(User).where(User.email == email))
    if user is None:
        if not payload.invite_code:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No account exists for this Google email. Use a valid gym invite code to sign up first.",
            )

        gym = await session.scalar(select(Gym).where(Gym.invite_code == payload.invite_code.strip().upper()))
        if gym is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found for the provided invite code")

        user = User(
            email=email,
            full_name=name,
            password_hash=None,
            role=UserRole.MEMBER,
            auth_provider=AuthProvider.GOOGLE,
            google_id=subject,
            gym_id=gym.id,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return _build_auth_response(user)

    user.google_id = subject
    user.auth_provider = AuthProvider.GOOGLE
    if not user.full_name:
        user.full_name = name
    await session.commit()
    await session.refresh(user)
    return _build_auth_response(user)
