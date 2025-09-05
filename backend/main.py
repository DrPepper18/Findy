from routes.user_router import *
from routes.event_router import *
from models.database import *
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
        await asyncio.sleep(6 * 60 * 60)  # 6 hours


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(event_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


async def startup():
    await init_db()

if __name__ == "__main__":
    asyncio.run(startup())
    uvicorn.run("main:app", port=8000, reload=True)