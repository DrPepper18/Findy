from app.routes import user, event
from app.services.event import delete_expired_events
from app.models.database import *
from app.config import YANDEX_API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    await init_db()
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield
    
    cleanup_task.cancel()

async def periodic_cleanup():
    while True:
        await delete_expired_events()
        await asyncio.sleep(6 * 60 * 60)


app = FastAPI(root_path='/api/v1', lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router)
app.include_router(event.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/yandexmap")
async def get_api_key():
    return {"api_key": YANDEX_API}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)