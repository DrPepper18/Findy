from app.utils.security import (
    create_jwt_token,
    verify_jwt_token,
    is_password_correct,
    create_password_hash,
)


def test_jwt_token_cycle(email="test@gmail.com"):
    token = create_jwt_token(email=email)
    payload = verify_jwt_token(token=token)
    assert payload["sub"] == email


def test_password_hash_cycle(password="password123"):
    password_hash = create_password_hash(password=password)
    assert is_password_correct(password=password, passwordhash=password_hash)