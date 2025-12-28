from fastapi import APIRouter, Header, HTTPException
from app.services.event import (
    add_new_event,
    get_all_events,
    get_event_info,
    get_event_signups,
    register_join
)
from app.services.user import get_user_info, join_check
from app.crypt_module import verify_jwt_token
from app.schemas import EventJoinRequest, EventPostRequest, CheckJoinRequest

router = APIRouter(prefix='/event')

@router.post("/")
async def get_events(authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = verify_jwt_token(token=authorization.split()[1])

    user_data = await get_user_info(email=payload["sub"])
    eventlist = await get_all_events(user_data=user_data)
    return {"message": "Here will be your events", "events": eventlist}


@router.post("/create")
async def new_event(data: EventPostRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = verify_jwt_token(token=authorization.split()[1])

    await add_new_event(data)
    return {"message": "POST request is completed"}


@router.post("/join")
async def event_join(data: EventJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = verify_jwt_token(authorization.split()[1])

    if payload:
        user = await get_user_info(payload["sub"])
        event = await get_event_info(data.EventID)
        event_load = await get_event_signups(data.EventID)
        
        if not((not event.MinAge or event.MinAge <= user.Age) and (not event.MaxAge or user.Age <= event.MaxAge)):
            raise HTTPException(status_code=403, detail="Вы не подходите по возрасту")
        
        if not (event.Capacity > event_load):
            raise HTTPException(status_code=403, detail="Уже набрано нужное количество человек")
        
        await register_join(data, payload["sub"])
        return {"message": "POST request is completed"}
    

@router.post("/joincheck")
async def event_join_check(data: CheckJoinRequest, authorization: str = Header(...)):

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    payload = verify_jwt_token(token=authorization.split()[1])
    
    result = await join_check(data, payload["sub"])
    return {"joined": result}
