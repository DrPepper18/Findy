import jwt
import bcrypt
import time
from fastapi import HTTPException, Header
from app.config import SECRET_TOKEN


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=["HS256"])
        if not payload:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_user_from_jwt(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split()[1]
    return verify_jwt_token(token)


def create_jwt_token(email: str) -> str:
    payload = {
        "sub": email,
        "iss": "Findy",
        "iat": int(time.time()),
        "exp": int(time.time()) + 7 * 24 * 60 * 60
    }
    token = jwt.encode(payload, SECRET_TOKEN, algorithm="HS256")
    return token


def create_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_password_correct(password: str, passwordhash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), passwordhash)