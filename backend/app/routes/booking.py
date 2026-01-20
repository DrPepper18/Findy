from fastapi import APIRouter, Depends
from app.models.database import AsyncSession, get_db
from app.services.booking import (
    get_join_status,
    join_user_to_event,
    cancel_join_to_event
)
from app.crypt_module import get_user_from_jwt


router = APIRouter(prefix='/book')


@router.post("/{event_id}")
async def join_event(event_id: int, 
                     payload = Depends(get_user_from_jwt), 
                     db: AsyncSession = Depends(get_db)):
    await join_user_to_event(event_id=event_id, user_email=payload["sub"], session=db)
    return {"message": "POST request is completed"}


@router.delete("/{event_id}")
async def cancel_join(event_id: int, 
                     payload = Depends(get_user_from_jwt), 
                     db: AsyncSession = Depends(get_db)):
    await cancel_join_to_event(event_id=event_id, user_email=payload["sub"], session=db)
    return {"message": "DELETE request is completed"}
    

@router.get("/{event_id}")
async def check_event_join(event_id: int, 
                           payload = Depends(get_user_from_jwt), 
                           db: AsyncSession = Depends(get_db)):    
    result = await get_join_status(event_id=event_id, user_email=payload["sub"], session=db)
    return {"joined": result}