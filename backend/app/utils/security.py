import jwt
import bcrypt
import time
from fastapi import HTTPException, Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from app.config import SECRET_TOKEN


TOKEN_LIFESPAN = {
    "refresh": 30 * 24 * 60 * 60, # 30 days
    "access": 10 * 60 # 10 minutes
}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_TOKEN, algorithms=["HS256"])
        if not payload:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def verify_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    payload = validate_token(token)

    if payload["type"] != 'access':
        raise HTTPException(status_code=401, detail="Access token required")
    
    return payload


def verify_refresh_token(token: str = Cookie(None, alias="refresh")) -> dict:
    payload = validate_token(token)

    if payload["type"] != 'refresh':
        raise HTTPException(status_code=401, detail="Access token required")
    
    return validate_token(token)


# I should probably do enum for token_type
def create_jwt_token(user_id: int, token_type: str = "access") -> str:
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_LIFESPAN[token_type]
    }
    token = jwt.encode(payload, SECRET_TOKEN, algorithm="HS256")
    return token


def create_both_tokens(user_id: int) -> dict:
    return {
        "refresh": create_jwt_token(user_id=user_id, token_type="refresh"),
        "access": create_jwt_token(user_id=user_id, token_type="access")
    }


def create_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_password_correct(password: str, password_hash: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash)