from fastapi import APIRouter
from .auth import router

auth_router = APIRouter(prefix='/api')
auth_router.include_router(router=router)
