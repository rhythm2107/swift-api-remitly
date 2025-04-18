from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import swift_codes
from app.ingestion.seed_data import seed_data
from app.core.config import settings

def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if settings.DEV_MODE.lower() == "false":
            print("Seeding data...")
            # This is only for local usage, docker uses seed_data in entrypoint.sh
            # await seed_data()

        if settings.DEV_MODE.lower() == "true":
            print("Skipping seed_data() for test environment")

        yield

    app = FastAPI(lifespan=lifespan)
    app.include_router(swift_codes.router, prefix="/v1/swift-codes", tags=["swift-codes"])
    return app

# For Uvicorn
app = create_app()