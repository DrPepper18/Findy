from fastapi import APIRouter, Response, Depends
from app.models.database import AsyncSession, get_db
from app.services.user import (
    register_user,
    authenticate_user,
    get_user_info,
    update_user_info,
    delete_user
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
    "path": "/api/auth",
    "httponly": True,
    "samesite": "lax",
    # "secure": True, # prod
    "max_age": TOKEN_LIFESPAN["refresh"]
}


router = APIRouter(prefix='/auth')


@router.post("/register", status_code=201)
async def register(data: RegisterRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await register_user(data=data, session=db)

    tokens = create_both_tokens(user_id=user_id)
    response.set_cookie(value=tokens["refresh"], **COOKIE_SETTINGS)
    return {"token": tokens["access"]}


@router.post("/login")
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await authenticate_user(data=data, session=db)

    tokens = create_both_tokens(user_id=user_id)
    response.set_cookie(value=tokens["refresh"], **COOKIE_SETTINGS)
    return {"token": tokens["access"]}


@router.get("/refresh")
async def refresh(response: Response, payload = Depends(verify_refresh_token)):
    tokens = create_both_tokens(user_id=int(payload["sub"]))
    response.set_cookie(value=tokens["refresh"], **COOKIE_SETTINGS)
    return {"token": tokens["access"]}


@router.get("/")
async def get_user(payload = Depends(verify_access_token),
                   db: AsyncSession = Depends(get_db)):
    user_info = await get_user_info(user_id=int(payload["sub"]), session=db)
    return user_info


@router.patch("/")
async def edit_user(data: EditUserInfoRequest,
                    payload = Depends(verify_access_token),
                    db: AsyncSession = Depends(get_db)):
    await update_user_info(data=data, user_id=int(payload["sub"]), session=db)
    return {"message": "Patch successful"}


@router.delete("/")
async def handle_delete_user(response: Response, payload = Depends(verify_access_token),
                      db: AsyncSession = Depends(get_db)):
    await delete_user(user_id=int(payload["sub"]), session=db)
    response.delete_cookie("refresh")
    return {"message": "Delete successful"}
