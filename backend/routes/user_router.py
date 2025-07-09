from fastapi import HTTPException, APIRouter, Header
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
    
@user_router.post("/api/v1/event/joincheck")
async def event_join(data: CheckJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])

    if payload:
        result = await join_check(data, payload["sub"])
        return {"joined": result}
