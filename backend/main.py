from modules.cors import *
from modules.models import *
from modules.database import *
import asyncio
import uvicorn


async def startup():
    await init_db()  # Initialize the DB before starting Flask

if __name__ == "__main__":
    asyncio.run(startup())
    uvicorn.run("main:app", port=8000, reload=True)