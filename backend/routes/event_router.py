from fastapi import HTTPException, APIRouter
from services.event_services import *
from config import YANDEX_API
from crypt_module import *

event_router = APIRouter()

@event_router.get("/api/v1/events")
async def get_events():
    eventlist = await get_all_events()
    return {"message": "Here will be your events", "events": eventlist}

@event_router.post("/api/v1/events")
async def new_event(data: EventPostRequest):
    await add_new_event(data)
    return {"message": "POST request is completed"}

@event_router.get("/api/v1/yandexmap")
async def get_api_key():
    return {"api_key": YANDEX_API}