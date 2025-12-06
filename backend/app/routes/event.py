from fastapi import APIRouter, Header
from app.services.event import *
from app.services.user import *
from app.crypt_module import *

router = APIRouter(prefix='/event')

@router.post("/get_all")
async def get_events(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])
    if payload:
        user_data = await get_user_info(email=payload["sub"])
        eventlist = await get_all_events(user_data=user_data)
        return {"message": "Here will be your events", "events": eventlist}


@router.post("/create")
async def new_event(data: EventPostRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    if await verify_jwt_token(authorization.split()[1]):
        await add_new_event(data)
        return {"message": "POST request is completed"}


@router.post("/join")
async def event_join(data: EventJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])

    if payload:
        user_info = await get_user_info(payload["sub"])
        event_info = await get_event_info(data.EventID)
        user_age, min_age, max_age = user_info.Age, event_info.MinAge, event_info.MaxAge
        
        if (not min_age or min_age <= user_age) and (not max_age or user_age <= max_age):
            await register_join(data, payload["sub"])
            return {"message": "POST request is completed"}
        else:
            raise HTTPException(status_code=403, detail="Not allowed")
    

@router.post("/joincheck")
async def event_join_check(data: CheckJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = await verify_jwt_token(authorization.split()[1])

    if payload:
        result = await join_check(data, payload["sub"])
        return {"joined": result}
