from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings

from app.models.account import User
from app.models.files import File
from app.models.points import PointPurchaseTransaction, PointRewardTransaction
from app.models.comments import Comment
from app.models.ratings import Rating
from app.models.file_purchase import FilePurchaseTransaction

from app.api.v1.endpoints.account import router as account_router
from app.api.v1.endpoints.files import router as files_router
from app.api.v1.endpoints.points import router as points_router
from app.api.v1.endpoints.comments import router as comments_router
from app.api.v1.endpoints.ratings import router as ratings_router
from app.api.v1.endpoints.file_purchase import router as file_purchase_router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(application: FastAPI):
    client = AsyncIOMotorClient(settings.mongo_uri)
    application.state.mongo_client = client # type: ignore[attr-defined]

    db = client.get_default_database()
    await init_beanie(
        database=db,
        document_models=[
            User,
            File,
            PointPurchaseTransaction,
            PointRewardTransaction,
            Comment,
            Rating,
            FilePurchaseTransaction,
        ],
    )

    yield

    client.close()

app = FastAPI(lifespan=lifespan,
docs_url = "/api/",
redoc_url = None,
openapi_url = "/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://one4lib.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(account_router, prefix="/api/auth", tags=["auth"])
app.include_router(files_router, prefix="/api/files", tags=["files"])
app.include_router(file_purchase_router, prefix="/api/file-purchase", tags=["file-purchase"])
app.include_router(points_router, prefix="/api/points", tags=["points"])
app.include_router(comments_router, prefix="/api/comments", tags=["comments"])
app.include_router(ratings_router, prefix="/api/ratings", tags=["ratings"])

