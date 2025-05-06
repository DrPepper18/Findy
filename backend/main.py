from routes.user_router import *
from routes.event_router import *
from models.database import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(event_router)

async def startup():
    await init_db()

if __name__ == "__main__":
    asyncio.run(startup())
    uvicorn.run("main:app", port=8000, reload=True)