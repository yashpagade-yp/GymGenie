from fastapi import APIRouter

from app.api.routers import auth, health, members, owners, trainers

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(trainers.router, prefix="/trainers", tags=["trainers"])
api_router.include_router(owners.router, prefix="/owners", tags=["owners"])
