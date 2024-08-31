from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.models import Base, db_helper
from src.config import settings
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get('/')
async def hello():
    return {"message": "Hello World!"}
