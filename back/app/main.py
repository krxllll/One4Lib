from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings

from app.account.models import User
from app.files.models import File
from app.points.models import PointPurchaseTransaction, PointRewardTransaction
from app.comments.models import Comment
from app.ratings.models import Rating
from app.file_purchase.models import FilePurchaseTransaction


from app.account.router import router as account_router
from app.files.router import router as files_router
from app.points.router import router as points_router
from app.comments.router import router as comments_router
from app.ratings.router import router as ratings_router
from app.file_purchase.router import router as file_purchase_router

app = FastAPI(title="Secure Media Exchange")

@app.on_event("startup")
async def on_startup():
    # Initialize MongoDB client and Beanie ODM
    client = AsyncIOMotorClient(settings.mongo_uri)
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

@app.on_event("shutdown")
async def on_shutdown():
    # Optional: close MongoDB connection
    client = AsyncIOMotorClient(settings.mongo_uri)
    client.close()

# API routes
app.include_router(account_router, prefix="/api/auth", tags=["auth"])
app.include_router(files_router, prefix="/api/files", tags=["files"])
app.include_router(file_purchase_router, prefix="/api/file-purchase", tags=["file-purchase"])
app.include_router(points_router, prefix="/api/points", tags=["points"])
app.include_router(comments_router, prefix="/api/comments", tags=["comments"])
app.include_router(ratings_router, prefix="/api/ratings", tags=["ratings"])

