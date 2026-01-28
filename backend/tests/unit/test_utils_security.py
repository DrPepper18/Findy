from app.utils.security import *


def test_jwt_token_cycle(user_id: int = 1):
    token = create_jwt_token(user_id=user_id)
    payload = verify_access_token(token=token)
    assert payload["sub"] == str(user_id)


def test_tokens_pair_cycle(user_id: int = 1):
    tokens = create_both_tokens(user_id=user_id)
    payload_access = verify_access_token(token=tokens["access"])
    payload_refresh = verify_refresh_token(token=tokens["refresh"])
    assert payload_access["sub"] == payload_refresh["sub"]


def test_password_hash_cycle(password: str = "password123"):
    password_hash = create_password_hash(password=password)
    assert is_password_correct(password=password, password_hash=password_hash)