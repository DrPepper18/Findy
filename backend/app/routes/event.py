from fastapi import APIRouter, Depends
from app.services.event import (
    add_new_event,
    get_all_events,
    join_user_to_event
)
from app.services.user import get_user_info, get_join_status
from app.crypt_module import get_user_from_jwt
from app.schemas import EventJoinRequest, EventPostRequest

router = APIRouter(prefix='/event')

@router.get("/")
async def get_events(payload = Depends(get_user_from_jwt)):
    user_data = await get_user_info(email=payload["sub"])
    eventlist = await get_all_events(user_data=user_data)
    return {"message": "Here will be your events", "events": eventlist}


@router.post("/")
async def create_event(data: EventPostRequest, payload = Depends(get_user_from_jwt)):
    await add_new_event(data)
    return {"message": "POST request is completed"}


@router.post("/{event_id}/join")
async def join_event(event_id: int, payload = Depends(get_user_from_jwt)):
    await join_user_to_event(event_id=event_id, user_email=payload["sub"])
    return {"message": "POST request is completed"}
    

@router.get("/{event_id}/join")
async def check_event_join(event_id: int, payload = Depends(get_user_from_jwt)):    
    result = await get_join_status(event_id, payload["sub"])
    return {"joined": result}

