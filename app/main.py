from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import swift_codes

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(swift_codes.router, prefix="/v1/swift-codes", tags=["swift-codes"])