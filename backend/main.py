from routes.routes import *
from models.database import *
import asyncio
import uvicorn


async def startup():
    await init_db()  # Initialize the DB before starting FastAPI

if __name__ == "__main__":
    asyncio.run(startup())
    uvicorn.run("main:app", port=8000, reload=True)