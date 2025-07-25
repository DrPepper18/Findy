from fastapi import APIRouter, Header
from services.event_services import *
from config import YANDEX_API
from crypt_module import *

event_router = APIRouter()

@event_router.post("/api/v1/events")
async def get_events(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    if await verify_jwt_token(authorization.split()[1]):
        eventlist = await get_all_events()
        return {"message": "Here will be your events", "events": eventlist}


@event_router.post("/api/v1/event/create")
async def new_event(data: EventPostRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    if await verify_jwt_token(authorization.split()[1]):
        await add_new_event(data)
        return {"message": "POST request is completed"}


@event_router.post("/api/v1/event/join")
async def event_join(data: EventJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])

    if payload:
        await register_join(data, payload["sub"])
        return {"message": "POST request is completed"}


@event_router.get("/api/v1/yandexmap")
async def get_api_key():
    return {"api_key": YANDEX_API}