from fastapi import HTTPException, APIRouter, Depends
from app.models.database import AsyncSession, get_db
from app.services.user import register_user, authenticate_user
from app.schemas import RegisterRequest, LoginRequest


router = APIRouter(prefix='/auth')


@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    jwt_token = await register_user(data=data, session=db)
    return {"message": "Registration successful", "token": jwt_token}


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    jwt_token = await authenticate_user(data=data, session=db)

    if not jwt_token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "token": jwt_token}
