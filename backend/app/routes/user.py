from fastapi import APIRouter, Response, Depends
from app.models.database import AsyncSession, get_db
from app.services.user import (
    register_user,
    authenticate_user,
    get_user_info,
    update_user_info
)
from app.schemas import RegisterRequest, LoginRequest, EditUserInfoRequest
from app.utils.security import (
    verify_access_token, 
    verify_refresh_token, 
    create_both_tokens, 
    TOKEN_LIFESPAN
)


COOKIE_SETTINGS = {
    "key": "refresh",
    "path": "/api/v1/auth",
    "httponly": True,
    "samesite": "lax",
    # "secure": True, # prod
    "max_age": TOKEN_LIFESPAN["refresh"]
}


router = APIRouter(prefix='/auth')


@router.post("/register", status_code=201)
async def register(data: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)):
    await register_user(data=data, session=db)

    tokens = create_both_tokens(email=data.email)
    response.set_cookie(value=tokens["refresh"], **COOKIE_SETTINGS)
    return {"token": tokens["access"]}


@router.post("/login")
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    await authenticate_user(data=data, session=db)

    tokens = create_both_tokens(email=data.email)
    response.set_cookie(value=tokens["refresh"], **COOKIE_SETTINGS)
    return {"token": tokens["access"]}


@router.get("/refresh")
async def refresh(response: Response, payload = Depends(verify_refresh_token)):
    tokens = create_both_tokens(email=payload["sub"])
    response.set_cookie(value=tokens["refresh"], **COOKIE_SETTINGS)
    return {"token": tokens["access"]}


@router.get("/")
async def get_info(payload = Depends(verify_access_token),
                   db: AsyncSession = Depends(get_db)):
    user_info = await get_user_info(email=payload["sub"], session=db)
    return user_info


@router.patch("/")
async def edit_info(data: EditUserInfoRequest,
                         payload = Depends(verify_access_token),
                         db: AsyncSession = Depends(get_db)):
    await update_user_info(data=data, email=payload["sub"], session=db)
    return {"message": "Patch successful"}
