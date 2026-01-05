import sys
from pathlib import Path
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, close_all_sessions
from sqlalchemy.orm import sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Импортируем наше приложение и модули базы
from app.main import app
import app.models.database as db_module
from app.models.models import Base
from app.config import TEST_DATABASE_URL

test_engine = create_async_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="function")
async def prepare_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async def override_get_db():
        async with sessionmaker(test_engine, class_=AsyncSession)() as session:
            yield session
            
    app.dependency_overrides[db_module.get_db] = override_get_db
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    """Создает экземпляр event loop для всей тестовой сессии."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def client(prepare_db):
    app.router.lifespan_context = None
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac