from fastapi import APIRouter, HTTPException, Header, Depends
from app.services.event import (
    add_new_event,
    get_all_events,
    get_event_info,
    get_event_signups,
    join_user_to_event
)
from app.services.user import get_user_info, join_check
from app.crypt_module import get_user_from_jwt
from app.schemas import EventJoinRequest, EventPostRequest, CheckJoinRequest

router = APIRouter(prefix='/event')

@router.post("/")
async def get_events(payload = Depends(get_user_from_jwt)):
    user_data = await get_user_info(email=payload["sub"])
    eventlist = await get_all_events(user_data=user_data)
    return {"message": "Here will be your events", "events": eventlist}


@router.post("/create")
async def new_event(data: EventPostRequest, payload = Depends(get_user_from_jwt)):
    await add_new_event(data)
    return {"message": "POST request is completed"}


@router.post("/join")
async def event_join(data: EventJoinRequest, payload = Depends(get_user_from_jwt)):
    await join_user_to_event(event_id=data.EventID, user_email=payload["sub"])
    return {"message": "POST request is completed"}
    

@router.post("/joincheck")
async def event_join_check(data: CheckJoinRequest, payload = Depends(get_user_from_jwt)):    
    result = await join_check(data, payload["sub"])
    return {"joined": result}
