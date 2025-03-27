from fastapi import HTTPException, APIRouter
from services.user_services import *
from crypt_module import *

user_router = APIRouter()

@user_router.post("/api/v1/auth/register")
async def register(data: RegisterRequest):
    jwt_token = await register_user(data)
    return {"message": "Registration successful", "token": jwt_token}


@user_router.post("/api/v1/auth/login")
async def login(data: LoginRequest):
    jwt_token = await login_check(data)
    if jwt_token:
        return {"message": "Registration successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    