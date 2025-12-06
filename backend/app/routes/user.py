from fastapi import HTTPException, APIRouter, Header
from app.services.user import *
from app.crypt_module import *

router = APIRouter(prefix='/auth')

@router.post("/register")
async def register(data: RegisterRequest):
    jwt_token = await register_user(data)
    return {"message": "Registration successful", "token": jwt_token}


@router.post("/login")
async def login(data: LoginRequest):
    jwt_token = await login_check(data)
    if jwt_token:
        return {"message": "Registration successful", "token": jwt_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
