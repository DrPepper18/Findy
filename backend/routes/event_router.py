from fastapi import APIRouter, Header
from services.event_services import *
from services.user_services import *
from crypt_module import *

event_router = APIRouter(prefix='/event')

@event_router.post("/")
async def get_events(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(token=authorization.split()[1])

    user_data = await get_user_info(email=payload["sub"])
    eventlist = await get_all_events(user_data=user_data)
    return {"message": "Here will be your events", "events": eventlist}


@event_router.post("/create")
async def new_event(data: EventPostRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(token=authorization.split()[1])

    await add_new_event(data)
    return {"message": "POST request is completed"}


@event_router.post("/join")
async def event_join(data: EventJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(token=authorization.split()[1])
    
    user_info = await get_user_info(payload["sub"])
    event_info = await get_event_info(data.EventID)
    user_age, min_age, max_age = user_info.Age, event_info.MinAge, event_info.MaxAge
    
    if (not min_age or min_age <= user_age) and (not max_age or user_age <= max_age):
        await register_join(data, payload["sub"])
        return {"message": "POST request is completed"}
    else:
        raise HTTPException(status_code=403, detail="Not allowed")
    

@event_router.post("/joincheck")
async def event_join_check(data: CheckJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(token=authorization.split()[1])
    
    result = await join_check(data, payload["sub"])
    return {"joined": result}
