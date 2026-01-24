from fastapi import APIRouter, Depends
from app.models.database import AsyncSession, get_db
from app.services.user import (
    register_user,
    authenticate_user,
    get_user_info,
    update_user_info
)
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    EditUserInfoRequest
)
from app.utils.security import get_user_from_jwt


router = APIRouter(prefix='/auth')


@router.post("/register", status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    jwt_token = await register_user(data=data, session=db)
    return {"token": jwt_token}


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    jwt_token = await authenticate_user(data=data, session=db)
    return {"token": jwt_token}


@router.get("/")
async def get_info(payload = Depends(get_user_from_jwt),
                   db: AsyncSession = Depends(get_db)):
    user_info = await get_user_info(email=payload["sub"], session=db)
    return user_info


@router.patch("/")
async def edit_info(data: EditUserInfoRequest,
                         payload = Depends(get_user_from_jwt),
                         db: AsyncSession = Depends(get_db)):
    await update_user_info(data=data, email=payload["sub"], session=db)
    return {"message": "Patch successful"}
