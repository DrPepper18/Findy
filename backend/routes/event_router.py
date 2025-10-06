from fastapi import APIRouter, Header
from services.event_services import *
from services.user_services import *
from config import YANDEX_API
from crypt_module import *

event_router = APIRouter(prefix='/event')

@event_router.post("/get_all")
async def get_events(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])
    if payload:
        user_data = await get_user_info(email=payload["sub"])
        eventlist = await get_all_events(user_data=user_data)
        return {"message": "Here will be your events", "events": eventlist}


@event_router.post("/create")
async def new_event(data: EventPostRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    if await verify_jwt_token(authorization.split()[1]):
        await add_new_event(data)
        return {"message": "POST request is completed"}


@event_router.post("/join")
async def event_join(data: EventJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])

    if payload:
        await register_join(data, payload["sub"])
        return {"message": "POST request is completed"}
    

@event_router.post("/joincheck")
async def event_join_check(data: CheckJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])

    if payload:
        result = await join_check(data, payload["sub"])
        return {"joined": result}
