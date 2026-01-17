import asyncio
import pytest
import pytest_asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.models.database import Base, get_db
from app.main import app
from app.config import TEST_DATABASE_URL

# 1. Специфика Windows: ПРИНУДИТЕЛЬНО выставляем политику цикла ДО всех тестов
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 2. Переопределяем event_loop, чтобы он был один на всю сессию
@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# 3. Создаем движок, привязанный к сессионному циклу
@pytest_asyncio.fixture(scope="function")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, pool_pre_ping=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()

# 4. Финальный Dependency Injection — подменяем базу в приложении
@pytest_asyncio.fixture(autouse=True)
async def override_db(db_engine):
    # Создаем фабрику сессий на базе нашего тестового движка
    TestingSessionLocal = async_sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession)
    
    async def _get_test_db():
        async with TestingSessionLocal() as session:
            yield session

    # Ключевой момент: подменяем зависимость в FastAPI
    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()

# 5. Клиент
@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac