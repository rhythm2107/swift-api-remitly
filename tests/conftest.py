import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool
from app.main import create_app
from app.core.database import Base, get_db
from app.core.config import settings
from asgi_lifespan import LifespanManager


# Create a separate engine for testing
# Use NullPool to prevent "Future attached to a different loop" (refer to README)
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
engine_test = create_async_engine(TEST_DATABASE_URL, echo=True, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False)

# Override the dependency database to ensure we hit test_db
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

app = create_app()
app.dependency_overrides[get_db] = override_get_db

# Apply DB schema before any test
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


# HTTPX ASGI Client
@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            yield c


@pytest_asyncio.fixture(autouse=True)
async def clean_swift_table():
    """Run each test inside a fresh table state."""
    yield
    async with engine_test.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE swift_codes RESTART IDENTITY"))