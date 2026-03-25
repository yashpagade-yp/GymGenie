from collections.abc import Callable
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_db_session
from app.models.enums import UserRole
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        token_type = payload.get("type")
        if not user_id or token_type != "access":
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc

    user = await session.scalar(select(User).where(User.id == UUID(user_id), User.is_active.is_(True)))
    if user is None:
        raise credentials_error
    return user


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    async def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user

    return dependency


async def get_current_member(current_user: User = Depends(require_roles(UserRole.MEMBER))) -> User:
    return current_user


async def get_current_trainer(current_user: User = Depends(require_roles(UserRole.TRAINER))) -> User:
    return current_user


async def get_current_owner(current_user: User = Depends(require_roles(UserRole.OWNER))) -> User:
    return current_user


async def get_current_gym_id(current_user: User = Depends(get_current_user)) -> UUID:
    if current_user.gym_id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not associated with a gym")
    return current_user.gym_id
