from fastapi import APIRouter, Depends
from app.models.database import AsyncSession, get_db
from app.services.event import add_new_event, get_all_events
from app.services.user import get_user_info 
from app.utils.security import get_user_from_jwt
from app.schemas import EventPostRequest


router = APIRouter(prefix='/event')


@router.get("/")
async def get_events(payload = Depends(get_user_from_jwt), 
                     db: AsyncSession = Depends(get_db)):
    user_data = await get_user_info(email=payload["sub"], session=db)
    eventlist = await get_all_events(user_data=user_data, session=db)
    return eventlist


@router.post("/", status_code=201)
async def create_event(data: EventPostRequest, 
                       payload = Depends(get_user_from_jwt), 
                       db: AsyncSession = Depends(get_db)):
    event_id = await add_new_event(data, session=db)
    return {"event_id": event_id}
