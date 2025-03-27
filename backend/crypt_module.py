from config import SECRET_TOKEN
import jwt
import bcrypt


async def create_jwt_token(email: str) -> str:
    payload = {
        "email": email,
    }
    token = jwt.encode(payload, SECRET_TOKEN, algorithm="HS256")
    return token


async def create_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


async def is_password_correct(password: str, passwordhash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), passwordhash)